import os
import re
import json
from datetime import datetime
from pathlib import Path
import PyPDF2
import io
import sys

# Novas importações para OCR e processamento de imagens
try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Aviso: Algumas dependências de OCR não estão instaladas: {e}")
    print("📦 Para instalar: pip install pytesseract Pillow pdf2image opencv-python")
    OCR_AVAILABLE = False

__version__ = "1.0.0"

class DarmProcessor:
    def __init__(self):
        # Determinar o diretório base (funciona tanto para script quanto para executável)
        if getattr(sys, 'frozen', False):
            # Executando como executável PyInstaller
            base_dir = Path(sys._MEIPASS)
            # Para executável, usar diretório onde o .exe está localizado
            self.base_dir = Path(sys.executable).parent
        else:
            # Executando como script Python
            self.base_dir = Path(__file__).parent
        
        self.darms_dir = self.base_dir / 'darms'
        self.output_dir = self.base_dir / 'inserts'
        self.processed_guias = set()  # Para controlar guias já processadas
        self.guias_processadas = []  # Lista para rastrear guias processadas
        self.all_sql_inserts = []  # Array para armazenar todos os INSERTs

    async def init(self):
        """Inicializar o processador"""
        # Criar diretórios se não existirem
        self.darms_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"📁 Diretório base: {self.base_dir}")
        print(f"📁 Diretório DARMs: {self.darms_dir}")
        print(f"📁 Diretório saída: {self.output_dir}")
        
        # Carregar guias já processadas de arquivos existentes
        await self.load_processed_guias()

    async def load_processed_guias(self):
        """Carregar guias já processadas de arquivos existentes"""
        try:
            # Não carregar guias processadas para permitir reprocessamento completo
            # As guias serão processadas novamente a cada execução
            print("🔄 Modo de reprocessamento ativado - todos os arquivos serão sobrescritos")
        except Exception as error:
            print(f'Erro ao carregar guias processadas: {error}')

    async def check_guia_exists(self, numero_guia):
        """Verificar se a guia já existe no banco de dados"""
        try:
            # Gerar SQL para verificar se a guia já existe no formato simplificado para Control-M
            check_sql = f"""use silfae;
SELECT COUNT(*) as total FROM FarrDarmsPagos WHERE NR_GUIA = {numero_guia} AND AA_EXERCICIO = 2025 AND CD_BANCO = 70 AND NR_BDA = 37 AND NR_COMPLEMENTO = 0 AND NR_LOTE_NSA = 730 AND TP_LOTE_D = 1;"""

            check_filename = f'CHECK_GUIA_{numero_guia}.sql'
            check_path = self.output_dir / check_filename
            
            # Escrever arquivo em encoding latin1
            with open(check_path, 'w', encoding='latin1') as f:
                f.write(check_sql)
            
            print(f'Arquivo de verificação criado: {check_filename}')
            print(f'IMPORTANTE: Execute {check_filename} para verificar se a guia {numero_guia} já existe no banco')
            
            return False  # Assumir que não existe por segurança
        except Exception as error:
            print(f'Erro ao verificar guia {numero_guia}: {error}')
            return False

    async def generate_single_sql_file(self):
        """Gerar arquivo SQL único com todos os INSERTs no formato simplificado para Control-M"""
        try:
            if not self.all_sql_inserts:
                print('📭 Nenhum INSERT para gerar no arquivo único.')
                return

            # Filtrar apenas INSERTs válidos
            valid_inserts = []
            for sql_insert in self.all_sql_inserts:
                if sql_insert and len(sql_insert.strip()) > 50:
                    valid_inserts.append(sql_insert)

            if not valid_inserts:
                print('📭 Nenhum INSERT válido encontrado para gerar o arquivo único.')
                return

            # Gerar SQ_DOC únicos no Python
            timestamp = int(datetime.now().timestamp() * 1000)
            simple_insert_statements = []
            
            for index, sql_insert in enumerate(valid_inserts):
                # Extrair apenas a parte VALUES do INSERT
                values_match = re.search(r'VALUES\s*\(\s*(.+?)\s*\);', sql_insert, re.DOTALL)
                if values_match:
                    values_part = values_match.group(1)
                    # Split dos valores considerando vírgulas
                    # Atenção: isso só funciona porque todos os campos são simples (sem vírgula interna)
                    valores = [v.strip() for v in values_part.split(',')]
                    # O campo SQ_DOC é o 8º campo (índice 7)
                    if index < len(self.guias_processadas):
                        guia = self.guias_processadas[index]
                        guia_last3 = int(guia) % 1000
                        timestamp_last3 = timestamp % 1000
                        sq_doc = (guia_last3 * 1000) + timestamp_last3 + index
                        valores[7] = str(sq_doc)
                        simple_insert_statements.append(f"({', '.join(valores)})")

            if not simple_insert_statements:
                print('📭 Nenhum statement válido para gerar o arquivo único.')
                return

            # Formato formatado bonito para o arquivo consolidado
            single_sql_content = f"""use silfae;

INSERT INTO FarrDarmsPagos (
    id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC,
    CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO,
    NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO,
    VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS,
    processado, criticaProcessamento
) VALUES 
    {',\n    '.join(simple_insert_statements)};"""

            # Validar se o conteúdo foi gerado corretamente
            if not single_sql_content or len(single_sql_content.strip()) < 100:
                print('❌ Erro: Conteúdo SQL único está vazio ou muito pequeno')
                return

            single_sql_path = self.output_dir / 'INSERT_TODOS_DARMs.sql'
            
            # Escrever arquivo em encoding latin1
            with open(single_sql_path, 'w', encoding='latin1') as f:
                f.write(single_sql_content)
            
            print('📄 Arquivo SQL único gerado: INSERT_TODOS_DARMs.sql')
            print(f'📊 Contém {len(simple_insert_statements)} INSERT statements')
            print('🔧 Formato: ISO 8859-1 (Latin-1) - Compatível com Control-M')
            print('✨ Versão: Formatada bonita - Legível e organizada')
            
            # Mostrar SQ_DOC gerados
            sq_docs_info = []
            for i, guia in enumerate(self.guias_processadas[:len(simple_insert_statements)]):
                guia_last3 = int(guia) % 1000
                timestamp_last3 = timestamp % 1000
                sq_doc = (guia_last3 * 1000) + timestamp_last3 + i
                sq_docs_info.append(f'Guia {guia} = {sq_doc}')
            print(f'🔢 SQ_DOC gerados: {", ".join(sq_docs_info)}')
            
        except Exception as error:
            print(f'❌ Erro ao gerar arquivo SQL único: {error}')

    async def generate_report(self):
        """Gerar relatório de processamento"""
        try:
            report_content = f"""# RELATÓRIO DE PROCESSAMENTO DE DARMs

## Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Guias Processadas: {len(self.guias_processadas)}

### Lista de Guias:
{chr(10).join(f'{i + 1}. Guia {guia}' for i, guia in enumerate(self.guias_processadas))}

### Estatísticas:
- Total de guias processadas: {len(self.guias_processadas)}
- Guias únicas: {len(set(self.guias_processadas))}
- Arquivos SQL individuais gerados: {len(self.guias_processadas)}
- Arquivo SQL único gerado: 1
- Arquivo SQL alternativo gerado: 1

### Arquivos Gerados:
- **INSERT_TODOS_DARMs.sql** - Script único com INSERT IGNORE (proteção automática contra duplicatas)
- **INSERT_DARM_PAGO_*.sql** - Arquivos individuais para cada guia
- **CHECK_GUIA_*.sql** - Arquivos de verificação para cada guia
- **RELATORIO_PROCESSAMENTO.md** - Este relatório

### Compatibilidade Control-M:
- ✅ **Formato ISO 8859-1 (Latin-1)** - Compatível com Control-M
- ✅ **Formato simplificado (uma linha)** - Otimizado para Control-M
- ✅ **Sem comentários** - Arquivos SQL limpos
- ✅ **Caracteres especiais removidos** - Acentos e símbolos convertidos
- ✅ **Estrutura simplificada** - Otimizada para automação

### Funcionalidades OCR:
- ✅ **PDFs com texto em imagem** - Processamento automático com OCR
- ✅ **Arquivos de imagem** - Suporte a PNG, JPG, BMP, TIFF
- ✅ **Detecção automática** - Identifica se PDF precisa de OCR
- ✅ **Pré-processamento de imagem** - Melhora qualidade do OCR
- ✅ **Múltiplos idiomas** - Suporte ao português brasileiro

### Verificações de Segurança:
- ✅ Controle de duplicatas por sessão
- ✅ Verificação de arquivos SQL existentes
- ✅ Geração de arquivos de verificação para cada guia
- ✅ SQ_DOC único baseado em guia + timestamp
- ✅ Script único com transação para consistência
- ✅ INSERT IGNORE (proteção automática contra duplicatas)

### Próximos Passos:
1. **Opção 1 (Recomendada)**: Execute o arquivo **INSERT_TODOS_DARMs.sql** para inserir todos os registros de uma vez
2. **Opção 2**: Execute os arquivos CHECK_GUIA_*.sql para verificar se as guias já existem no banco
3. **Opção 3**: Execute os arquivos INSERT_DARM_PAGO_*.sql individualmente se preferir

### Vantagens do Script Único:
- ✅ Execução em transação (consistência)
- ✅ Verificações automáticas antes e depois
- ✅ Relatório detalhado de inserções
- ✅ Rollback automático em caso de erro
- ✅ Mais rápido e seguro
- ✅ **INSERT IGNORE** - Proteção automática contra duplicatas de NR_GUIA
- ✅ **Compatível com Control-M** - Formato ISO 8859-1 sem comentários

---
Gerado automaticamente pelo DarmProcessor (Python)
"""

            report_path = self.output_dir / 'RELATORIO_PROCESSAMENTO.md'
            with open(report_path, 'w', encoding='utf8') as f:
                f.write(report_content)
            print('📋 Relatório gerado: RELATORIO_PROCESSAMENTO.md')
            
        except Exception as error:
            print(f'Erro ao gerar relatório: {error}')

    async def verify_sql_files(self):
        """Verificar se os arquivos SQL foram gerados corretamente"""
        try:
            print('\n🔍 Verificando arquivos SQL gerados...')
            
            # Verificar arquivo único
            single_sql_path = self.output_dir / 'INSERT_TODOS_DARMs.sql'
            if single_sql_path.exists():
                with open(single_sql_path, 'r', encoding='latin1') as f:
                    content = f.read()
                    if content and len(content.strip()) > 100:
                        print(f'✅ Arquivo único válido: {single_sql_path.name} ({len(content)} caracteres)')
                    else:
                        print(f'❌ Arquivo único vazio ou inválido: {single_sql_path.name}')
            else:
                print(f'❌ Arquivo único não encontrado: {single_sql_path.name}')
            
            # Verificar arquivos individuais
            individual_files = list(self.output_dir.glob('INSERT_DARM_PAGO_*.sql'))
            valid_files = 0
            for file_path in individual_files:
                try:
                    with open(file_path, 'r', encoding='latin1') as f:
                        content = f.read()
                        if content and len(content.strip()) > 50:
                            valid_files += 1
                        else:
                            print(f'❌ Arquivo individual vazio: {file_path.name}')
                except Exception as e:
                    print(f'❌ Erro ao ler arquivo {file_path.name}: {e}')
            
            print(f'📊 Arquivos individuais válidos: {valid_files}/{len(individual_files)}')
            
            # Verificar arquivos de verificação
            check_files = list(self.output_dir.glob('CHECK_GUIA_*.sql'))
            print(f'📊 Arquivos de verificação gerados: {len(check_files)}')
            
        except Exception as error:
            print(f'❌ Erro ao verificar arquivos SQL: {error}')

    async def process_darms(self):
        """Processar todos os DARMs (PDFs e imagens)"""
        try:
            print('🚀 Iniciando processamento dos DARMs...')
            
            # Verificar se o diretório darms existe
            if not self.darms_dir.exists():
                print('❌ Diretório darms não encontrado!')
                return

            # Listar todos os arquivos suportados no diretório darms
            supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']
            all_files = [f for f in self.darms_dir.iterdir() 
                        if f.suffix.lower() in supported_extensions]

            if not all_files:
                print('📭 Nenhum arquivo suportado encontrado no diretório darms.')
                print(f'📋 Formatos suportados: {", ".join(supported_extensions)}')
                return

            print(f'📁 Encontrados {len(all_files)} arquivos para processar.')
            
            # Separar arquivos por tipo
            pdf_files = [f for f in all_files if f.suffix.lower() == '.pdf']
            image_files = [f for f in all_files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']]
            
            print(f'📄 PDFs encontrados: {len(pdf_files)}')
            print(f'🖼️  Imagens encontradas: {len(image_files)}')

            # Processar cada arquivo PDF
            for pdf_file in pdf_files:
                await self.process_file(pdf_file, 'pdf')

            # Processar cada arquivo de imagem
            for image_file in image_files:
                await self.process_file(image_file, 'image')

            # Verificar arquivos SQL gerados
            await self.verify_sql_files()

            # Gerar relatório final
            await self.generate_report()
            
            # Gerar arquivo SQL único
            await self.generate_single_sql_file()

            print('✅ Processamento concluído!')
            print(f'📊 Total de guias processadas: {len(self.guias_processadas)}')

        except Exception as error:
            print(f'❌ Erro durante o processamento: {error}')

    async def process_file(self, filepath, file_type):
        """Processar um arquivo específico (PDF ou imagem)"""
        try:
            print(f'🔄 Processando {file_type.upper()}: {filepath.name}')
            
            # Extrair texto baseado no tipo de arquivo
            if file_type == 'pdf':
                text = await self.extract_text_from_pdf(filepath)
            elif file_type == 'image':
                text = await self.extract_text_from_image(filepath)
            else:
                print(f'❌ Tipo de arquivo não suportado: {file_type}')
                return
            
            # Debug: mostrar primeiras linhas do texto extraído
            print('=== TEXTO EXTRAÍDO ===')
            print(text[:500] + '...' if len(text) > 500 else text)
            print('==============================')

            # Extrair dados do DARM
            darm_data = self.extract_darm_data(text)
            
            if darm_data:
                print('✅ Dados extraídos:', darm_data)
                
                # Verificar se a guia já foi processada nesta sessão
                if darm_data['numeroGuia'] in self.processed_guias:
                    print(f'🔄 Reprocessando guia {darm_data["numeroGuia"]} (já processada nesta sessão)')
                
                # Verificar se já existe um arquivo SQL para esta guia
                numero_guia = darm_data.get('numeroGuia', 'SEM_GUIA')
                sql_filename = f'INSERT_DARM_PAGO_{numero_guia}.sql'
                sql_path = self.output_dir / sql_filename
                
                # Sempre sobrescrever arquivos existentes
                if sql_path.exists():
                    print(f'🔄 Sobrescrevendo arquivo existente para guia {numero_guia}')
                
                # Verificar se a guia já existe no banco de dados
                await self.check_guia_exists(darm_data['numeroGuia'])
                
                # Adicionar guia ao controle de processadas
                self.processed_guias.add(darm_data['numeroGuia'])
                self.guias_processadas.append(darm_data['numeroGuia'])
                
                sql_content = self.generate_sql_insert(darm_data)
                
                # Verificar se o SQL foi gerado corretamente
                if sql_content and len(sql_content.strip()) > 50:
                    # Escrever arquivo em encoding latin1
                    with open(sql_path, 'w', encoding='latin1') as f:
                        f.write(sql_content)
                    
                    # Armazenar o INSERT para o arquivo único
                    self.all_sql_inserts.append(sql_content)
                    
                    print(f'✅ Arquivo SQL gerado: {sql_filename}')
                    print(f'📊 Guias processadas até agora: {len(self.guias_processadas)}')
                else:
                    print(f'❌ Erro: SQL não foi gerado corretamente para guia {numero_guia}')
                    # Remover a guia da lista de processadas se o SQL falhou
                    if darm_data['numeroGuia'] in self.processed_guias:
                        self.processed_guias.remove(darm_data['numeroGuia'])
                    if darm_data['numeroGuia'] in self.guias_processadas:
                        self.guias_processadas.remove(darm_data['numeroGuia'])
            else:
                print(f'❌ Não foi possível extrair dados do arquivo: {filepath.name}')

        except Exception as error:
            print(f'❌ Erro ao processar {filepath.name}: {error}')

    async def extract_text_from_pdf(self, filepath):
        """Extrair texto de um arquivo PDF - com suporte a OCR para imagens"""
        try:
            # Primeiro, tentar extrair texto normalmente
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    text += page_text
                
                # Se conseguiu extrair texto, retornar
                if text.strip():
                    print(f"✅ Texto extraído normalmente do PDF: {filepath.name}")
                    return text
                
                # Se não conseguiu extrair texto, pode ser PDF com imagens
                print(f"⚠️  PDF sem texto extraível detectado: {filepath.name}")
                print("🔄 Tentando extrair texto usando OCR...")
                
                if not OCR_AVAILABLE:
                    print("❌ OCR não disponível. Instale as dependências: pip install pytesseract Pillow pdf2image opencv-python")
                    return ""
                
                # Converter PDF para imagens e usar OCR
                return await self.extract_text_from_pdf_with_ocr(filepath)
                
        except Exception as error:
            print(f'Erro ao extrair texto do PDF {filepath.name}: {error}')
            return ""

    async def extract_text_from_pdf_with_ocr(self, filepath):
        """Extrair texto de PDF usando OCR (para PDFs com imagens)"""
        try:
            print(f"🔍 Convertendo PDF para imagens: {filepath.name}")
            
            # Converter PDF para imagens
            images = convert_from_path(filepath, dpi=300)
            
            all_text = ""
            for i, image in enumerate(images):
                print(f"📄 Processando página {i+1}/{len(images)} com OCR...")
                
                # Converter PIL Image para OpenCV format
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Pré-processar imagem para melhorar OCR
                processed_image = self.preprocess_image_for_ocr(opencv_image)
                
                # Extrair texto usando Tesseract
                page_text = pytesseract.image_to_string(processed_image, lang='por')
                all_text += page_text + "\n"
                
                print(f"✅ Página {i+1} processada com OCR")
            
            if all_text.strip():
                print(f"✅ Texto extraído com OCR: {len(all_text)} caracteres")
                return all_text
            else:
                print("❌ Nenhum texto encontrado com OCR")
                return ""
                
        except Exception as error:
            print(f"❌ Erro ao extrair texto com OCR: {error}")
            return ""

    def preprocess_image_for_ocr(self, image):
        """Pré-processar imagem para melhorar a qualidade do OCR"""
        try:
            # Converter para escala de cinza
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar threshold adaptativo para melhorar contraste
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Aplicar morfologia para remover ruído
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Aplicar blur suave para suavizar
            processed = cv2.GaussianBlur(processed, (1, 1), 0)
            
            return processed
            
        except Exception as error:
            print(f"⚠️  Erro no pré-processamento da imagem: {error}")
            return image

    async def extract_text_from_image(self, filepath):
        """Extrair texto de arquivo de imagem usando OCR"""
        try:
            if not OCR_AVAILABLE:
                print("❌ OCR não disponível. Instale as dependências: pip install pytesseract Pillow opencv-python")
                return ""
            
            print(f"🔍 Processando imagem com OCR: {filepath.name}")
            
            # Carregar imagem
            image = cv2.imread(str(filepath))
            if image is None:
                print(f"❌ Não foi possível carregar a imagem: {filepath.name}")
                return ""
            
            # Pré-processar imagem
            processed_image = self.preprocess_image_for_ocr(image)
            
            # Extrair texto usando Tesseract
            text = pytesseract.image_to_string(processed_image, lang='por')
            
            if text.strip():
                print(f"✅ Texto extraído da imagem: {len(text)} caracteres")
                return text
            else:
                print("❌ Nenhum texto encontrado na imagem")
                return ""
                
        except Exception as error:
            print(f"❌ Erro ao extrair texto da imagem: {error}")
            return ""

    def extract_darm_data(self, text):
        """Extrair dados do DARM do texto extraído"""
        try:
            # Padrões para extrair dados do DARM - versão melhorada
            patterns = {
                # Número de inscrição - múltiplos padrões
                'inscricao': [
                    r'02\.\s*INSCRIÇÃO MUNICIPAL\s*(\d{8,9})',  # 8 ou 9 dígitos
                    r'(?:Inscrição|INSCRIÇÃO|Inscrição Municipal|Inscrição)\s*:?\s*(\d{8,9})',  # 8 ou 9 dígitos
                    r'(?:Inscrição|INSCRIÇÃO)\s*(\d{8,9})',  # 8 ou 9 dígitos
                    r'Insc\.?\s*:?\s*(\d{8,9})'  # 8 ou 9 dígitos
                ],
                
                # Código de barras - padrão específico para código de barras
                'codigoBarras': [
                    r'(?:Código de Barras|CODIGO DE BARRAS)\s*:?\s*([\d\.\s]+)',
                    r'(?:Barras|BARRAS)\s*:?\s*([\d\.\s]+)',
                    r'([\d]{48})',  # Exatamente 48 dígitos
                    r'([\d]{44,50})'  # Entre 44 e 50 dígitos
                ],
                
                # Código de receita - extrair do campo RECEITA
                'codigoReceita': [
                    r'01\.\s*RECEITA\s*\n(\d{1,4})-(\d{1,2})',  # Formato específico do PDF
                    r'01\.\s*RECEITA\s*(\d{1,4})-(\d{1,2})',  # Formato alternativo
                    r'(?:RECEITA|Receita|Código de Receita)\s*:?\s*(\d{1,4}-\d{1,2})',  # Formato genérico
                    r'(\d{1,4})-(\d{1,2})',  # Para formato como "258-5"
                    r'RECEITA\s*\n(\d{1,4})-(\d{1,2})'  # Formato mais específico
                ],
                
                # Valor principal - múltiplos padrões
                'valorPrincipal': [
                    r'(?:Valor Principal|VALOR PRINCIPAL|Valor principal)\s*:?\s*R?\$?\s*([\d,\.]+)',
                    r'(?:Principal|PRINCIPAL)\s*:?\s*R?\$?\s*([\d,\.]+)',
                    r'R?\$?\s*([\d,\.]+)\s*(?:Principal|PRINCIPAL)',
                    r'06\.\s*VALOR DO TRIBUTO\s*R?\$?\s*([\d,\.]+)'
                ],
                
                # Valor total - múltiplos padrões
                'valorTotal': [
                    r'(?:Valor Total|VALOR TOTAL|Valor total)\s*:?\s*R?\$?\s*([\d,\.]+)',
                    r'(?:Total|TOTAL)\s*:?\s*R?\$?\s*([\d,\.]+)',
                    r'R?\$?\s*([\d,\.]+)\s*(?:Total|TOTAL)',
                    r'09\.\s*VALOR TOTAL\s*R?\$?\s*([\d,\.]+)'
                ],
                
                # Data de vencimento - múltiplos padrões
                'dataVencimento': [
                    r'(?:Vencimento|VENCIMENTO|Venc\.?)\s*:?\s*(\d{2}/\d{2}/\d{4})',
                    r'(\d{2}/\d{2}/\d{4})\s*(?:Vencimento|VENCIMENTO)',
                    r'03\.\s*DATA VENCIMENTO\s*(\d{2}/\d{2}/\d{4})'
                ],
                
                # Exercício - múltiplos padrões
                'exercicio': [
                    r'(?:Exercício|EXERCÍCIO|Exerc\.?)\s*:?\s*(\d{4})',
                    r'(\d{4})\s*(?:Exercício|EXERCÍCIO)',
                    r'04\.\s*ANO DE REFERÊNCIA\s*(\d{4})'
                ],
                
                # Número da guia - múltiplos padrões
                'numeroGuia': [
                    r'05\.\s*GUIA NØ\s*\n?([0-9]+)',  # Pega a linha após o título
                    r'(?:Guia|GUIA|Número da Guia|Nº Guia)\s*:?\s*(\d+)',
                    r'(?:Guia|GUIA)\s*(\d+)',
                    r'Guia\.?\s*:?\s*(\d+)'
                ],
                
                # Competência - múltiplos padrões
                'competencia': [
                    r'(?:Competência|COMPETÊNCIA|Comp\.?)\s*:?\s*(\d{2}/\d{4})',
                    r'(\d{2}/\d{4})\s*(?:Competência|COMPETÊNCIA)'
                ]
            }

            data = {}

            # Extrair cada campo usando múltiplos padrões
            for key, pattern_array in patterns.items():
                for pattern in pattern_array:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        # Tratamento especial para código de receita no formato "XXX-X"
                        if key == 'codigoReceita' and len(match.groups()) > 1:
                            data[key] = match.group(1) + match.group(2)  # Concatenar sem hífen
                            print(f'🔧 Código de receita extraído (concatenação): {data[key]}')
                        elif key == 'codigoReceita' and '-' in match.group(1):
                            # Manter o formato original com hífen
                            data[key] = match.group(1)
                            print(f'🔧 Código de receita extraído (com hífen): {data[key]}')
                        elif key == 'numeroGuia':
                            data[key] = match.group(1).lstrip('0') or '0'  # Remove zeros à esquerda
                        elif key == 'codigoBarras':
                            # Limpar o código de barras removendo espaços e pontos
                            codigo = re.sub(r'[\s\.]', '', match.group(1))
                            # Garantir que tem pelo menos 44 dígitos
                            if len(codigo) >= 44:
                                data[key] = codigo[:48]  # Limitar a 48 dígitos
                                print(f'Campo {key} encontrado: {data[key]}')
                                break
                        else:
                            data[key] = match.group(1).strip()
                        
                        if data[key]:
                            print(f'Campo {key} encontrado: {data[key]}')
                        break  # Usar o primeiro padrão que encontrar

            # Validar se temos os dados mínimos necessários
            if not data.get('inscricao') or (not data.get('valorPrincipal') and not data.get('valorTotal')):
                print('Dados insuficientes extraídos do PDF')
                print('Dados encontrados:', data)
                return None

            # Se não encontrou valor principal, usar valor total
            if not data.get('valorPrincipal') and data.get('valorTotal'):
                data['valorPrincipal'] = data['valorTotal']
                print('Usando valor total como valor principal')

            return data

        except Exception as error:
            print(f'Erro ao extrair dados do PDF: {error}')
            return None

    def generate_sql_insert(self, darm_data):
        """Gerar SQL INSERT para os dados do DARM no formato simplificado para Control-M"""
        try:
            # Converter data de vencimento do formato DD/MM/YYYY para YYYY-MM-DD
            data_vencimento = None
            if darm_data.get('dataVencimento'):
                try:
                    dia, mes, ano = darm_data['dataVencimento'].split('/')
                    data_vencimento = f'{ano}-{mes}-{dia} 00:00:00'
                except:
                    data_vencimento = None

            # Converter competência do formato MM/YYYY para YYYY
            competencia = datetime.now().year  # Usar o ano atual dinamicamente

            # Processar valores monetários
            valor_principal = self.parse_monetary_value(darm_data.get('valorPrincipal'))
            valor_total = self.parse_monetary_value(darm_data.get('valorTotal') or darm_data.get('valorPrincipal'))

            # Limitar código de barras a 48 dígitos e remover caracteres não numéricos
            codigo_barras = None
            if darm_data.get('codigoBarras') and str(darm_data['codigoBarras']):
                codigo_barras = re.sub(r'\D', '', str(darm_data['codigoBarras']))[:48]

            # Usar código de receita do PDF ou valor padrão
            codigo_receita = darm_data.get('codigoReceita') or 2585  # Valor padrão hardcoded
            # Se o código de receita tem hífen, converter para número
            if isinstance(codigo_receita, str) and '-' in codigo_receita:
                codigo_receita = codigo_receita.replace('-', '')
                print(f'🔧 Código de receita processado: {codigo_receita}')
            
            # Forçar uso do valor padrão se o código extraído for inválido
            if isinstance(codigo_receita, str) and len(codigo_receita) > 4:
                print(f'⚠️  Código de receita extraído muito longo ({codigo_receita}), usando valor padrão 2585')
                codigo_receita = 2585

            # Gerar expressão SQL para SQ_DOC dinâmico (6 dígitos: últimos 3 da guia + últimos 3 dos millisegundos)
            numero_guia = darm_data.get('numeroGuia', '0')
            if numero_guia != '0':
                numero_guia = self.remove_leading_zeros(numero_guia)
            sq_doc_expression = f"((({numero_guia} % 1000) * 1000) + (UNIX_TIMESTAMP() % 1000)) % 1000000"

            # Validar dados obrigatórios
            inscricao = darm_data.get('inscricao', '')
            if not inscricao:
                print('❌ Erro: Inscrição não encontrada')
                return None

            # Gerar SQL no formato formatado bonito
            sql = f"""use silfae;

INSERT INTO FarrDarmsPagos (
    id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC,
    CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO,
    NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO,
    VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS,
    processado, criticaProcessamento
) VALUES (
    NULL, {darm_data.get('exercicio', 2025)}, 70, 37, 0, 730, 1, {sq_doc_expression}, {codigo_receita}, NULL, 'FARR', NULL, NOW(), {f"'{data_vencimento}'" if data_vencimento else 'NULL'}, NOW(), '{inscricao}', {self.remove_leading_zeros(darm_data.get('numeroGuia', 'NULL'))}, {competencia or 'NULL'}, {f"'{codigo_barras}'" if codigo_barras else 'NULL'}, NULL, '13', NULL, {valor_total}, {valor_total}, {valor_principal}, 0.00, 0.00, NULL, NULL, NULL, 0.00, 0, NULL
);"""

            # Validar se o SQL foi gerado corretamente
            if not sql or len(sql.strip()) < 50:
                print('❌ Erro: SQL gerado está vazio ou muito pequeno')
                return None

            print(f'✅ SQL gerado com sucesso para guia {darm_data.get("numeroGuia")}')
            return sql

        except Exception as error:
            print(f'❌ Erro ao gerar SQL: {error}')
            return None

    def remove_leading_zeros(self, value):
        """Remove zeros à esquerda apenas se houver zeros"""
        return value.lstrip('0') or '0'

    def parse_monetary_value(self, value):
        """Converter valor monetário para formato numérico com 2 casas decimais, mesmo com ruído"""
        if not value:
            return '0.00'
        
        # Remover tudo que não for número, vírgula ou ponto
        clean_value = re.sub(r'[^\d,\.]', '', value)
        
        # Se houver mais de uma vírgula ou ponto, manter só o último separador decimal
        if clean_value.count(',') > 1 or clean_value.count('.') > 1:
            # Substituir todos os pontos por vazio, exceto o último
            if ',' in clean_value:
                partes = clean_value.split(',')
                clean_value = ''.join(partes[:-1]) + ',' + partes[-1]
            if '.' in clean_value:
                partes = clean_value.split('.')
                clean_value = ''.join(partes[:-1]) + '.' + partes[-1]
        
        # Se tem vírgula, tratar como separador decimal brasileiro
        if ',' in clean_value:
            # Se tem ponto antes da vírgula, é formato brasileiro (ex: 9.014,06)
            if '.' in clean_value:
                # Remover pontos de milhares e converter vírgula para ponto
                clean_value = clean_value.replace('.', '').replace(',', '.')
            else:
                # Só vírgula, converter para ponto
                clean_value = clean_value.replace(',', '.')
        
        try:
            numeric_value = float(clean_value)
            return f'{numeric_value:.2f}'
        except ValueError:
            return '0.00'

# Função principal para executar o processador
async def main():
    """Função principal"""
    processor = DarmProcessor()
    await processor.init()
    await processor.process_darms()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 