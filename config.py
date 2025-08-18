#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações do Processador de DARMs

Este arquivo contém todas as configurações personalizáveis do processador,
permitindo fácil adaptação para diferentes ambientes e necessidades.
"""

# =============================================================================
# CONFIGURAÇÕES DO BANCO DE DADOS
# =============================================================================

# Parâmetros do banco de dados
DB_CONFIG = {
    'database': 'silfae',           # Nome do banco de dados
    'exercicio': 2025,              # Ano de exercício
    'cd_banco': 70,                 # Código do banco
    'nr_bda': 37,                   # Número BDA
    'nr_complemento': 0,            # Número complemento
    'nr_lote_nsa': 730,             # Número do lote NSA
    'tp_lote_d': 1,                 # Tipo do lote
    'cd_usu_incl': 'FARR',          # Código do usuário que incluiu
    'st_doc_d': '13',               # Status do documento
}

# =============================================================================
# CONFIGURAÇÕES DE PROCESSAMENTO
# =============================================================================

# Diretórios
DIRECTORIES = {
    'darms': 'darms',               # Pasta com os PDFs dos DARMs
    'output': 'inserts',            # Pasta de saída dos arquivos SQL
}

# Configurações de processamento
PROCESSING_CONFIG = {
    'encoding': 'latin1',           # Encoding dos arquivos SQL (ISO 8859-1)
    'max_codigo_barras': 48,        # Tamanho máximo do código de barras
    'default_codigo_receita': 2585, # Código de receita padrão
    'default_valor_mora': 0.00,     # Valor padrão para mora
    'default_valor_multa': 0.00,    # Valor padrão para multa
    'default_valor_juros': 0.00,    # Valor padrão para juros
}

# =============================================================================
# CONFIGURAÇÕES DE EXTRAÇÃO DE DADOS
# =============================================================================

# Padrões de regex para extração de dados
EXTRACTION_PATTERNS = {
    'inscricao': [
        r'(?:Inscrição|INSCRIÇÃO|Inscrição Municipal|Inscrição)\s*:?\s*(\d+)',
        r'(?:Inscrição|INSCRIÇÃO)\s*(\d+)',
        r'Insc\.?\s*:?\s*(\d+)',
        r'02\.\s*INSCRIÇÃO MUNICIPAL\s*(\d+)'
    ],
    
    'codigoBarras': [
        r'([\d\.\s]+)'
    ],
    
    'codigoReceita': [
        r'(?:RECEITA|Receita)\s*(\d+-\d+)',
        r'01\.\s*RECEITA\s*(\d+-\d+)',
        r'(\d+)-(\d+)'
    ],
    
    'valorPrincipal': [
        r'(?:Valor Principal|VALOR PRINCIPAL|Valor principal)\s*:?\s*R?\$?\s*([\d,\.]+)',
        r'(?:Principal|PRINCIPAL)\s*:?\s*R?\$?\s*([\d,\.]+)',
        r'R?\$?\s*([\d,\.]+)\s*(?:Principal|PRINCIPAL)',
        r'06\.\s*VALOR DO TRIBUTO\s*R?\$?\s*([\d,\.]+)'
    ],
    
    'valorTotal': [
        r'(?:Valor Total|VALOR TOTAL|Valor total)\s*:?\s*R?\$?\s*([\d,\.]+)',
        r'(?:Total|TOTAL)\s*:?\s*R?\$?\s*([\d,\.]+)',
        r'R?\$?\s*([\d,\.]+)\s*(?:Total|TOTAL)',
        r'09\.\s*VALOR TOTAL\s*R?\$?\s*([\d,\.]+)'
    ],
    
    'dataVencimento': [
        r'(?:Vencimento|VENCIMENTO|Venc\.?)\s*:?\s*(\d{2}/\d{2}/\d{4})',
        r'(\d{2}/\d{2}/\d{4})\s*(?:Vencimento|VENCIMENTO)',
        r'03\.\s*DATA VENCIMENTO\s*(\d{2}/\d{2}/\d{4})'
    ],
    
    'exercicio': [
        r'(?:Exercício|EXERCÍCIO|Exerc\.?)\s*:?\s*(\d{4})',
        r'(\d{4})\s*(?:Exercício|EXERCÍCIO)',
        r'04\.\s*ANO DE REFERÊNCIA\s*(\d{4})'
    ],
    
    'numeroGuia': [
        r'05\.\s*GUIA NØ\s*\n?([0-9]+)',
        r'(?:Guia|GUIA|Número da Guia|Nº Guia)\s*:?\s*(\d+)',
        r'(?:Guia|GUIA)\s*(\d+)',
        r'Guia\.?\s*:?\s*(\d+)'
    ],
    
    'competencia': [
        r'(?:Competência|COMPETÊNCIA|Comp\.?)\s*:?\s*(\d{2}/\d{4})',
        r'(\d{2}/\d{4})\s*(?:Competência|COMPETÊNCIA)'
    ]
}

# =============================================================================
# CONFIGURAÇÕES DE LOG E RELATÓRIOS
# =============================================================================

# Configurações de log
LOGGING_CONFIG = {
    'show_debug': True,             # Mostrar informações de debug
    'show_extracted_text': True,    # Mostrar texto extraído do PDF
    'show_sql_content': False,      # Mostrar conteúdo SQL gerado
    'log_level': 'INFO',            # Nível de log (DEBUG, INFO, WARNING, ERROR)
}

# Configurações de relatório
REPORT_CONFIG = {
    'include_timestamp': True,      # Incluir timestamp no relatório
    'include_statistics': True,     # Incluir estatísticas no relatório
    'include_file_list': True,      # Incluir lista de arquivos no relatório
    'report_format': 'markdown',    # Formato do relatório (markdown, txt)
}

# =============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO
# =============================================================================

# Validações de dados
VALIDATION_CONFIG = {
    'require_inscricao': True,      # Inscrição é obrigatória
    'require_valor': True,          # Valor é obrigatório
    'require_guia': False,          # Guia é obrigatória
    'min_valor': 0.01,             # Valor mínimo
    'max_valor': 999999.99,        # Valor máximo
    'validate_dates': True,         # Validar datas
}

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# Configurações de segurança
SECURITY_CONFIG = {
    'check_duplicates': True,       # Verificar duplicatas
    'backup_existing_files': False, # Fazer backup de arquivos existentes
    'max_file_size_mb': 50,         # Tamanho máximo de arquivo PDF (MB)
    'allowed_extensions': ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'], # Extensões permitidas
}

# =============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# =============================================================================

# Configurações de performance
PERFORMANCE_CONFIG = {
    'batch_size': 100,              # Tamanho do lote para processamento
    'max_workers': 4,               # Número máximo de workers (para processamento paralelo)
    'timeout_seconds': 30,          # Timeout para processamento de cada PDF
    'memory_limit_mb': 512,         # Limite de memória (MB)
}

# =============================================================================
# CONFIGURAÇÕES DE OCR
# =============================================================================

# Configurações de OCR (Optical Character Recognition)
OCR_CONFIG = {
    'enabled': True,                # Habilitar funcionalidades de OCR
    'language': 'por',              # Idioma para OCR (por = português)
    'dpi': 300,                     # Resolução para conversão de PDF (DPI)
    'preprocessing': True,          # Habilitar pré-processamento de imagem
    'threshold_method': 'adaptive', # Método de threshold (adaptive, otsu, binary)
    'kernel_size': 1,               # Tamanho do kernel para morfologia
    'blur_kernel': 1,               # Tamanho do kernel para blur
    'confidence_threshold': 60,     # Limite de confiança do OCR (%)
    'max_pages': 10,                # Número máximo de páginas para processar
    'timeout_per_page': 60,         # Timeout por página (segundos)
}

# Configurações de pré-processamento de imagem
IMAGE_PREPROCESSING_CONFIG = {
    'convert_to_grayscale': True,   # Converter para escala de cinza
    'apply_threshold': True,        # Aplicar threshold
    'remove_noise': True,           # Remover ruído
    'smooth_image': True,           # Suavizar imagem
    'enhance_contrast': True,       # Melhorar contraste
    'resize_if_needed': True,       # Redimensionar se necessário
    'max_width': 2000,              # Largura máxima da imagem
    'max_height': 3000,             # Altura máxima da imagem
}

# =============================================================================
# CONFIGURAÇÕES DE OUTPUT
# =============================================================================

# Configurações de saída
OUTPUT_CONFIG = {
    'generate_single_file': True,   # Gerar arquivo único
    'generate_individual_files': True, # Gerar arquivos individuais
    'generate_check_files': True,   # Gerar arquivos de verificação
    'generate_report': True,        # Gerar relatório
    'file_naming_pattern': 'INSERT_DARM_PAGO_{guia}.sql', # Padrão de nomenclatura
    'single_file_name': 'INSERT_TODOS_DARMs.sql', # Nome do arquivo único
    'report_file_name': 'RELATORIO_PROCESSAMENTO.md', # Nome do relatório
}

# =============================================================================
# MENSAGENS E TEXTO
# =============================================================================

# Mensagens do sistema
MESSAGES = {
    'pt_BR': {
        'processing_start': '🚀 Iniciando processamento dos DARMs...',
        'processing_complete': '✅ Processamento concluído!',
        'no_pdfs_found': '📭 Nenhum arquivo PDF encontrado no diretório darms.',
        'directory_not_found': '❌ Diretório darms não encontrado!',
        'file_processed': '✅ Arquivo SQL gerado: {filename}',
        'file_skipped': '⚠️  ATENÇÃO: Arquivo SQL já existe para guia {guia}. Pulando...',
        'data_extraction_failed': '❌ Não foi possível extrair dados do arquivo: {filename}',
        'insufficient_data': 'Dados insuficientes extraídos do PDF',
        'using_total_as_principal': 'Usando valor total como valor principal',
    },
    'en': {
        'processing_start': '🚀 Starting DARM processing...',
        'processing_complete': '✅ Processing completed!',
        'no_pdfs_found': '📭 No PDF files found in darms directory.',
        'directory_not_found': '❌ Darms directory not found!',
        'file_processed': '✅ SQL file generated: {filename}',
        'file_skipped': '⚠️  WARNING: SQL file already exists for guide {guia}. Skipping...',
        'data_extraction_failed': '❌ Could not extract data from file: {filename}',
        'insufficient_data': 'Insufficient data extracted from PDF',
        'using_total_as_principal': 'Using total value as principal value',
    }
}

# Idioma padrão
DEFAULT_LANGUAGE = 'pt_BR'

# =============================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# =============================================================================

def get_message(key, language=None):
    """Obter mensagem no idioma especificado"""
    if language is None:
        language = DEFAULT_LANGUAGE
    
    return MESSAGES.get(language, MESSAGES[DEFAULT_LANGUAGE]).get(key, key)

def get_config_section(section_name):
    """Obter uma seção específica de configuração"""
    config_sections = {
        'db': DB_CONFIG,
        'directories': DIRECTORIES,
        'processing': PROCESSING_CONFIG,
        'patterns': EXTRACTION_PATTERNS,
        'logging': LOGGING_CONFIG,
        'report': REPORT_CONFIG,
        'validation': VALIDATION_CONFIG,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'output': OUTPUT_CONFIG,
        'ocr': OCR_CONFIG,
        'image_preprocessing': IMAGE_PREPROCESSING_CONFIG,
    }
    
    return config_sections.get(section_name, {})

def validate_config():
    """Validar configurações"""
    errors = []
    
    # Validar configurações do banco
    if DB_CONFIG['exercicio'] < 2000 or DB_CONFIG['exercicio'] > 2100:
        errors.append("Exercício deve estar entre 2000 e 2100")
    
    if DB_CONFIG['cd_banco'] <= 0:
        errors.append("Código do banco deve ser maior que zero")
    
    # Validar configurações de processamento
    if PROCESSING_CONFIG['max_codigo_barras'] <= 0:
        errors.append("Tamanho máximo do código de barras deve ser maior que zero")
    
    # Validar configurações de validação
    if VALIDATION_CONFIG['min_valor'] < 0:
        errors.append("Valor mínimo não pode ser negativo")
    
    if VALIDATION_CONFIG['max_valor'] <= VALIDATION_CONFIG['min_valor']:
        errors.append("Valor máximo deve ser maior que o valor mínimo")
    
    return errors

# =============================================================================
# EXEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    print("🔧 Configurações do Processador de DARMs")
    print("=" * 40)
    
    # Validar configurações
    errors = validate_config()
    if errors:
        print("❌ Erros de configuração encontrados:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Configurações válidas!")
    
    # Mostrar configurações principais
    print(f"\n📊 Configurações Principais:")
    print(f"   - Banco de dados: {DB_CONFIG['database']}")
    print(f"   - Exercício: {DB_CONFIG['exercicio']}")
    print(f"   - Encoding: {PROCESSING_CONFIG['encoding']}")
    print(f"   - Idioma: {DEFAULT_LANGUAGE}")
    
    # Mostrar mensagem de exemplo
    print(f"\n💬 Exemplo de mensagem:")
    print(f"   {get_message('processing_start')}") 