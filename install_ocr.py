#!/usr/bin/env python3
"""
Script de instalação das dependências de OCR para o Gerador de Query DARM
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Instalar um pacote Python"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package}: {e}")
        return False

def check_tesseract():
    """Verificar se o Tesseract está instalado no sistema"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract encontrado no sistema!")
            print(f"📋 Versão: {result.stdout.strip()}")
            return True
        else:
            print("❌ Tesseract não encontrado no sistema")
            return False
    except FileNotFoundError:
        print("❌ Tesseract não encontrado no sistema")
        return False

def main():
    """Função principal de instalação"""
    print("🚀 Instalando dependências de OCR para o Gerador de Query DARM")
    print("=" * 60)
    
    # Lista de pacotes Python necessários
    python_packages = [
        "pytesseract==0.3.10",
        "Pillow==10.0.1", 
        "pdf2image==1.16.3",
        "opencv-python==4.8.1.78"
    ]
    
    print("📋 Pacotes Python a serem instalados:")
    for package in python_packages:
        print(f"   - {package}")
    print()
    
    # Verificar Tesseract
    print("🔍 Verificando Tesseract OCR...")
    tesseract_available = check_tesseract()
    
    if not tesseract_available:
        print("\n⚠️  ATENÇÃO: Tesseract OCR não encontrado no sistema!")
        print("📋 Para instalar o Tesseract:")
        print()
        print("Windows:")
        print("   1. Baixe de: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Instale e adicione ao PATH do sistema")
        print()
        print("Linux (Ubuntu/Debian):")
        print("   sudo apt-get install tesseract-ocr tesseract-ocr-por")
        print()
        print("macOS:")
        print("   brew install tesseract tesseract-lang")
        print()
        print("Após instalar o Tesseract, execute este script novamente.")
        return False
    
    # Instalar pacotes Python
    print("\n📦 Instalando pacotes Python...")
    success_count = 0
    for package in python_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Resultado da instalação:")
    print(f"   ✅ Pacotes instalados com sucesso: {success_count}/{len(python_packages)}")
    
    if success_count == len(python_packages):
        print("\n🎉 Todas as dependências foram instaladas com sucesso!")
        print("✅ O gerador agora suporta:")
        print("   - PDFs com texto em imagem (OCR)")
        print("   - Arquivos de imagem (PNG, JPG, BMP, TIFF)")
        print("   - Detecção automática de tipo de arquivo")
        print("   - Pré-processamento de imagem para melhor OCR")
        return True
    else:
        print("\n❌ Alguns pacotes não puderam ser instalados.")
        print("🔧 Verifique sua conexão com a internet e tente novamente.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 Instalação concluída! Você pode agora usar o gerador com OCR.")
        else:
            print("\n❌ Instalação incompleta. Verifique os erros acima.")
        input("\nPressione Enter para sair...")
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
