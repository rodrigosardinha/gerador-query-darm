#!/usr/bin/env python3
"""
Script de teste para verificar se o OCR está funcionando corretamente
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório atual ao path para importar o módulo
sys.path.append(str(Path(__file__).parent))

from darm_processor import DarmProcessor

async def test_ocr_functionality():
    """Testar funcionalidades de OCR"""
    print("🧪 Testando funcionalidades de OCR...")
    print("=" * 50)
    
    processor = DarmProcessor()
    await processor.init()
    
    # Verificar se OCR está disponível
    try:
        import pytesseract
        from PIL import Image
        import cv2
        import numpy as np
        from pdf2image import convert_from_path
        print("✅ Todas as dependências de OCR estão instaladas")
    except ImportError as e:
        print(f"❌ Dependência de OCR não encontrada: {e}")
        print("📦 Execute: python install_ocr.py")
        return False
    
    # Verificar se Tesseract está instalado
    try:
        import subprocess
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Tesseract encontrado: {result.stdout.strip()}")
        else:
            print("❌ Tesseract não encontrado no sistema")
            print("📋 Instale o Tesseract OCR primeiro")
            return False
    except FileNotFoundError:
        print("❌ Tesseract não encontrado no sistema")
        print("📋 Instale o Tesseract OCR primeiro")
        return False
    
    # Testar pré-processamento de imagem
    try:
        import cv2
        import numpy as np
        
        # Criar uma imagem de teste simples
        test_image = np.ones((100, 300, 3), dtype=np.uint8) * 255
        cv2.putText(test_image, "TESTE OCR", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Testar pré-processamento
        processed = processor.preprocess_image_for_ocr(test_image)
        print("✅ Pré-processamento de imagem funcionando")
        
    except Exception as e:
        print(f"❌ Erro no pré-processamento: {e}")
        return False
    
    # Testar extração de texto com OCR
    try:
        # Criar um arquivo de imagem de teste
        test_image_path = Path("test_ocr_image.png")
        cv2.imwrite(str(test_image_path), test_image)
        
        # Testar extração de texto
        text = await processor.extract_text_from_image(test_image_path)
        
        if text.strip():
            print("✅ Extração de texto com OCR funcionando")
            print(f"📝 Texto extraído: '{text.strip()}'")
        else:
            print("⚠️  OCR funcionando, mas não extraiu texto da imagem de teste")
        
        # Limpar arquivo de teste
        test_image_path.unlink(missing_ok=True)
        
    except Exception as e:
        print(f"❌ Erro na extração de texto: {e}")
        return False
    
    print("\n🎉 Testes de OCR concluídos com sucesso!")
    print("✅ O sistema está pronto para processar imagens e PDFs com OCR")
    return True

async def test_pdf_ocr():
    """Testar processamento de PDF com OCR"""
    print("\n📄 Testando processamento de PDF com OCR...")
    print("=" * 50)
    
    processor = DarmProcessor()
    await processor.init()
    
    # Verificar se há PDFs na pasta darms
    darms_dir = processor.darms_dir
    if not darms_dir.exists():
        print("❌ Pasta 'darms' não encontrada")
        return False
    
    pdf_files = list(darms_dir.glob("*.pdf"))
    if not pdf_files:
        print("📭 Nenhum PDF encontrado na pasta 'darms'")
        print("💡 Adicione alguns PDFs para testar o OCR")
        return True
    
    print(f"📁 Encontrados {len(pdf_files)} PDFs para teste")
    
    # Testar o primeiro PDF
    test_pdf = pdf_files[0]
    print(f"🧪 Testando: {test_pdf.name}")
    
    try:
        # Tentar extrair texto normalmente primeiro
        text = await processor.extract_text_from_pdf(test_pdf)
        
        if text.strip():
            print("✅ PDF processado normalmente (sem OCR necessário)")
        else:
            print("⚠️  PDF sem texto extraível - seria processado com OCR")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao processar PDF: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Teste de Funcionalidades OCR - Gerador de Query DARM")
    print("=" * 60)
    
    try:
        # Testar funcionalidades básicas de OCR
        ocr_ok = asyncio.run(test_ocr_functionality())
        
        if ocr_ok:
            # Testar processamento de PDF
            asyncio.run(test_pdf_ocr())
        
        print("\n📊 Resumo dos Testes:")
        if ocr_ok:
            print("✅ OCR funcionando corretamente")
            print("✅ Sistema pronto para processar imagens e PDFs")
        else:
            print("❌ OCR não está funcionando")
            print("🔧 Execute: python install_ocr.py")
        
    except KeyboardInterrupt:
        print("\n\n❌ Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 60)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
