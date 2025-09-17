#!/usr/bin/env python3
"""
Exemplo de uso do Gerador de Query DARM com funcionalidades de OCR
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório atual ao path para importar o módulo
sys.path.append(str(Path(__file__).parent))

from darm_processor import DarmProcessor

async def exemplo_processamento_ocr():
    """Exemplo de processamento com OCR"""
    print("🖼️ Exemplo de Processamento com OCR - Gerador de Query DARM")
    print("=" * 70)
    
    # Inicializar o processador
    processor = DarmProcessor()
    await processor.init()
    
    print("📁 Verificando arquivos disponíveis...")
    
    # Verificar se há arquivos na pasta darms
    darms_dir = processor.darms_dir
    if not darms_dir.exists():
        print("❌ Pasta 'darms' não encontrada!")
        return
    
    # Listar todos os arquivos suportados
    supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']
    all_files = [f for f in darms_dir.iterdir() 
                if f.suffix.lower() in supported_extensions]
    
    if not all_files:
        print("📭 Nenhum arquivo suportado encontrado na pasta 'darms'")
        print("💡 Adicione alguns arquivos para testar:")
        print("   - PDFs normais (com texto)")
        print("   - PDFs com texto em imagem")
        print("   - Imagens: PNG, JPG, BMP, TIFF")
        return
    
    print(f"📁 Encontrados {len(all_files)} arquivos para processamento:")
    
    # Separar arquivos por tipo
    pdf_files = [f for f in all_files if f.suffix.lower() == '.pdf']
    image_files = [f for f in all_files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']]
    
    print(f"   📄 PDFs: {len(pdf_files)}")
    for pdf in pdf_files:
        print(f"      - {pdf.name}")
    
    print(f"   🖼️  Imagens: {len(image_files)}")
    for img in image_files:
        print(f"      - {img.name}")
    
    print("\n🚀 Iniciando processamento...")
    
    # Processar cada arquivo
    for file_path in all_files:
        file_type = 'pdf' if file_path.suffix.lower() == '.pdf' else 'image'
        print(f"\n🔄 Processando {file_type.upper()}: {file_path.name}")
        
        try:
            # Extrair texto baseado no tipo
            if file_type == 'pdf':
                text = await processor.extract_text_from_pdf(file_path)
            else:
                text = await processor.extract_text_from_image(file_path)
            
            if text.strip():
                print(f"✅ Texto extraído: {len(text)} caracteres")
                
                # Extrair dados do DARM
                darm_data = processor.extract_darm_data(text)
                
                if darm_data:
                    print("✅ Dados do DARM extraídos:")
                    for key, value in darm_data.items():
                        print(f"   {key}: {value}")
                    
                    # Gerar SQL
                    sql_content = processor.generate_sql_insert(darm_data)
                    if sql_content:
                        print("✅ SQL gerado com sucesso!")
                    else:
                        print("❌ Erro ao gerar SQL")
                else:
                    print("❌ Não foi possível extrair dados do DARM")
            else:
                print("❌ Nenhum texto extraído")
                
        except Exception as e:
            print(f"❌ Erro ao processar {file_path.name}: {e}")
    
    print("\n🎉 Processamento concluído!")
    print("📊 Verifique a pasta 'inserts' para os arquivos SQL gerados")

async def exemplo_ocr_especifico():
    """Exemplo específico de uso de OCR"""
    print("\n🔍 Exemplo Específico de OCR")
    print("=" * 40)
    
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
    
    # Exemplo de pré-processamento de imagem
    try:
        import cv2
        import numpy as np
        
        print("🛠️  Exemplo de pré-processamento de imagem...")
        
        # Criar imagem de exemplo
        img = np.ones((200, 400, 3), dtype=np.uint8) * 255
        cv2.putText(img, "DARMs com OCR", (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
        
        # Aplicar pré-processamento
        processed = processor.preprocess_image_for_ocr(img)
        print("✅ Pré-processamento aplicado")
        
        # Salvar imagem processada
        cv2.imwrite("exemplo_processado.png", processed)
        print("💾 Imagem processada salva como 'exemplo_processado.png'")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")

def main():
    """Função principal"""
    print("🚀 Exemplo de Uso com OCR - Gerador de Query DARM")
    print("=" * 70)
    
    try:
        # Executar exemplo principal
        asyncio.run(exemplo_processamento_ocr())
        
        # Executar exemplo específico de OCR
        asyncio.run(exemplo_ocr_especifico())
        
        print("\n📋 Resumo:")
        print("✅ Exemplo executado com sucesso")
        print("📁 Verifique a pasta 'inserts' para os resultados")
        print("💡 Para mais informações, consulte FUNCIONALIDADES_OCR.md")
        
    except KeyboardInterrupt:
        print("\n\n❌ Exemplo cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 70)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
