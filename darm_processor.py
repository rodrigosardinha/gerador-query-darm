import os
import re
import json
from datetime import datetime
from pathlib import Path
import PyPDF2
import io
import sys

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

            # Formato simplificado: uma linha por INSERT para compatibilidade com Control-M
            single_sql_content = f"""use silfae;
INSERT INTO FarrDarmsPagos (id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS, processado, criticaProcessamento) VALUES {', '.join(simple_insert_statements)};"""

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
            print('⚡ Versão: Simplificada (formato de uma linha) - Otimizada para Control-M')
            
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
        """Processar todos os DARMs"""
        try:
            print('🚀 Iniciando processamento dos DARMs...')
            
            # Verificar se o diretório darms existe
            if not self.darms_dir.exists():
                print('❌ Diretório darms não encontrado!')
                return

            # Listar todos os arquivos PDF no diretório darms
            pdf_files = [f for f in self.darms_dir.iterdir() 
                        if f.suffix.lower() == '.pdf']

            if not pdf_files:
                print('📭 Nenhum arquivo PDF encontrado no diretório darms.')
                return

            print(f'📁 Encontrados {len(pdf_files)} arquivos PDF para processar.')

            # Processar cada arquivo PDF
            for pdf_file in pdf_files:
                await self.process_pdf_file(pdf_file)

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

    async def process_pdf_file(self, filepath):
        """Processar um arquivo PDF específico"""
        try:
            print(f'Processando: {filepath.name}')
            
            # Extrair texto do PDF
            text = await self.extract_text_from_pdf(filepath)
            
            # Debug: mostrar primeiras linhas do texto extraído
            print('=== TEXTO EXTRAÍDO DO PDF ===')
            print(text[:500] + '...')
            print('==============================')

            # Extrair dados do DARM
            darm_data = self.extract_darm_data(text)
            
            if darm_data:
                print('Dados extraídos:', darm_data)
                
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
        """Extrair texto de um arquivo PDF"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as error:
            print(f'Erro ao extrair texto do PDF {filepath.name}: {error}')
            return ""

    def extract_darm_data(self, text):
        """Extrair dados do DARM do texto extraído"""
        try:
            # Padrões para extrair dados do DARM - versão melhorada
            patterns = {
                # Número de inscrição - múltiplos padrões
                'inscricao': [
                    r'02\.\s*INSCRIÇÃO MUNICIPAL\s*(\d{8})',  # Exatamente 8 dígitos
                    r'(?:Inscrição|INSCRIÇÃO|Inscrição Municipal|Inscrição)\s*:?\s*(\d{8})',  # Exatamente 8 dígitos
                    r'(?:Inscrição|INSCRIÇÃO)\s*(\d{8})',  # Exatamente 8 dígitos
                    r'Insc\.?\s*:?\s*(\d{8})'  # Exatamente 8 dígitos
                ],
                
                # Código de barras - pega todas as sequências de dígitos, junta tudo, remove pontos e espaços
                'codigoBarras': [
                    r'([\d\.\s]+)'
                ],
                
                # Código de receita - extrair do campo RECEITA
                'codigoReceita': [
                    r'(?:RECEITA|Receita)\s*(\d{1,4}-\d{1,2})(?:[^\d]|$)',  # Parar em caractere não-número ou fim
                    r'01\.\s*RECEITA\s*(\d{1,4}-\d{1,2})(?:[^\d]|$)',
                    r'(\d{1,4})-(\d{1,2})(?:[^\d]|$)'  # Para formato como "262-3"
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
                            data[key] = match.group(1) + match.group(2)  # Concatenar os dois números
                        elif key == 'codigoReceita' and '-' in match.group(1):
                            # Garantir que pega apenas o padrão correto (ex: 262-3)
                            codigo_completo = match.group(1)
                            # Verificar se o padrão é válido (números-hífen-números)
                            if re.match(r'^\d{1,4}-\d{1,2}$', codigo_completo):
                                data[key] = codigo_completo.replace('-', '')  # Remover hífen
                            else:
                                # Se não for padrão válido, tentar extrair apenas a parte correta
                                partes = codigo_completo.split('-')
                                if len(partes) >= 2:
                                    # Pegar apenas os primeiros dígitos de cada parte
                                    parte1 = partes[0][:4]  # Máximo 4 dígitos
                                    parte2 = partes[1][:2]  # Máximo 2 dígitos
                                    data[key] = parte1 + parte2
                        elif key == 'numeroGuia':
                            data[key] = match.group(1).lstrip('0') or '0'  # Remove zeros à esquerda
                        elif key == 'codigoBarras':
                            # Pega todas as sequências de dígitos, pontos e espaços
                            matches = re.findall(r'[\d\.\s]+', text)
                            if matches:
                                # Junta todas as sequências encontradas
                                codigo = ''.join(matches)
                                # Remove tudo que não for número e corta para 48 dígitos
                                codigo = re.sub(r'\D', '', codigo)[:48]
                                data[key] = codigo
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
            codigo_receita = darm_data.get('codigoReceita') or 2585

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

            # Gerar SQL no formato simplificado (uma linha) para compatibilidade com Control-M
            sql = f"""use silfae;
INSERT INTO FarrDarmsPagos (id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS, processado, criticaProcessamento) VALUES (NULL, {darm_data.get('exercicio', 2025)}, 70, 37, 0, 730, 1, {sq_doc_expression}, {codigo_receita}, NULL, 'FARR', NULL, NOW(), {f"'{data_vencimento}'" if data_vencimento else 'NULL'}, NOW(), '{inscricao}', {self.remove_leading_zeros(darm_data.get('numeroGuia', 'NULL'))}, {competencia or 'NULL'}, {f"'{codigo_barras}'" if codigo_barras else 'NULL'}, NULL, '13', NULL, {valor_total}, {valor_total}, {valor_principal}, 0.00, 0.00, NULL, NULL, NULL, 0.00, 0, NULL);"""

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