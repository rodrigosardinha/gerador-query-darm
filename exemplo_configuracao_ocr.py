#!/usr/bin/env python3
"""
Exemplo de configuração e uso das funcionalidades de OCR
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório atual ao path para importar o módulo
sys.path.append(str(Path(__file__).parent))

from darm_processor import DarmProcessor
from config import OCR_CONFIG, IMAGE_PREPROCESSING_CONFIG

def mostrar_configuracoes_ocr():
    """Mostrar configurações atuais de OCR"""
    print("🔧 Configurações de OCR Atuais")
    print("=" * 50)
    
    print("📋 OCR_CONFIG:")
    for key, value in OCR_CONFIG.items():
        print(f"   {key}: {value}")
    
    print("\n🖼️ IMAGE_PREPROCESSING_CONFIG:")
    for key, value in IMAGE_PREPROCESSING_CONFIG.items():
        print(f"   {key}: {value}")

def exemplo_configuracao_personalizada():
    """Exemplo de como personalizar configurações de OCR"""
    print("\n⚙️ Exemplo de Configuração Personalizada")
    print("=" * 50)
    
    # Exemplo de configurações personalizadas
    config_personalizada = {
        'language': 'por+eng',      # Português + Inglês
        'dpi': 400,                 # Maior resolução
        'confidence_threshold': 80,  # Maior confiança
        'max_pages': 5,             # Menos páginas
        'timeout_per_page': 120,    # Mais tempo por página
    }
    
    print("📝 Configurações personalizadas:")
    for key, value in config_personalizada.items():
        print(f"   {key}: {value}")
    
    print("\n💡 Para aplicar essas configurações:")
    print("   1. Edite o arquivo config.py")
    print("   2. Modifique os valores em OCR_CONFIG")
    print("   3. Reinicie o processador")

async def exemplo_processamento_com_configuracao():
    """Exemplo de processamento com configurações específicas"""
    print("\n🚀 Exemplo de Processamento com Configuração")
    print("=" * 50)
    
    processor = DarmProcessor()
    await processor.init()
    
    # Verificar se OCR está disponível
    try:
        import pytesseract
        print("✅ OCR disponível")
    except ImportError:
        print("❌ OCR não disponível")
        print("📦 Execute: python install_ocr.py")
        return
    
    # Verificar configurações atuais
    print(f"🔧 Configurações atuais:")
    print(f"   - Idioma: {OCR_CONFIG['language']}")
    print(f"   - DPI: {OCR_CONFIG['dpi']}")
    print(f"   - Pré-processamento: {OCR_CONFIG['preprocessing']}")
    print(f"   - Confiança mínima: {OCR_CONFIG['confidence_threshold']}%")
    
    # Verificar arquivos disponíveis
    darms_dir = processor.darms_dir
    if not darms_dir.exists():
        print("❌ Pasta 'darms' não encontrada")
        return
    
    # Listar arquivos suportados
    supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']
    all_files = [f for f in darms_dir.iterdir() 
                if f.suffix.lower() in supported_extensions]
    
    if not all_files:
        print("📭 Nenhum arquivo suportado encontrado")
        print("💡 Adicione arquivos na pasta 'darms' para testar")
        return
    
    print(f"\n📁 Arquivos encontrados: {len(all_files)}")
    
    # Processar primeiro arquivo como exemplo
    test_file = all_files[0]
    file_type = 'pdf' if test_file.suffix.lower() == '.pdf' else 'image'
    
    print(f"\n🧪 Processando exemplo: {test_file.name}")
    print(f"📋 Tipo: {file_type.upper()}")
    
    try:
        # Extrair texto
        if file_type == 'pdf':
            text = await processor.extract_text_from_pdf(test_file)
        else:
            text = await processor.extract_text_from_image(test_file)
        
        if text.strip():
            print(f"✅ Texto extraído: {len(text)} caracteres")
            
            # Mostrar primeiras linhas
            lines = text.split('\n')[:5]
            print("📝 Primeiras linhas:")
            for i, line in enumerate(lines, 1):
                if line.strip():
                    print(f"   {i}: {line.strip()}")
            
            # Extrair dados do DARM
            darm_data = processor.extract_darm_data(text)
            if darm_data:
                print("\n✅ Dados do DARM extraídos:")
                for key, value in darm_data.items():
                    print(f"   {key}: {value}")
            else:
                print("\n❌ Não foi possível extrair dados do DARM")
        else:
            print("❌ Nenhum texto extraído")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def dicas_otimizacao():
    """Dicas para otimizar o OCR"""
    print("\n💡 Dicas para Otimizar o OCR")
    print("=" * 40)
    
    print("🎯 Para melhor qualidade:")
    print("   - Use imagens com resolução mínima de 300 DPI")
    print("   - Certifique-se que o texto está bem contrastado")
    print("   - Evite imagens muito pequenas ou borradas")
    print("   - Use formato PNG para melhor qualidade")
    
    print("\n⚙️ Configurações recomendadas:")
    print("   - DPI: 300-400 para PDFs")
    print("   - Confiança: 60-80%")
    print("   - Pré-processamento: Habilitado")
    print("   - Idioma: 'por' para português")
    
    print("\n🔧 Para problemas de qualidade:")
    print("   - Aumente o DPI para 400-600")
    print("   - Reduza o threshold de confiança para 50%")
    print("   - Verifique se o Tesseract está atualizado")
    print("   - Teste diferentes configurações de pré-processamento")

def main():
    """Função principal"""
    print("🔧 Exemplo de Configuração OCR - Gerador de Query DARM")
    print("=" * 70)
    
    try:
        # Mostrar configurações atuais
        mostrar_configuracoes_ocr()
        
        # Exemplo de configuração personalizada
        exemplo_configuracao_personalizada()
        
        # Exemplo de processamento
        asyncio.run(exemplo_processamento_com_configuracao())
        
        # Dicas de otimização
        dicas_otimizacao()
        
        print("\n📋 Resumo:")
        print("✅ Exemplo de configuração executado")
        print("🔧 Configure OCR conforme suas necessidades")
        print("💡 Consulte FUNCIONALIDADES_OCR.md para mais detalhes")
        
    except KeyboardInterrupt:
        print("\n\n❌ Exemplo cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 70)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
