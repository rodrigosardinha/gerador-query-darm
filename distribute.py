#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de distribuição para o Processador de DARMs
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime

def create_version_info():
    """Cria arquivo de informações da versão"""
    version_info = f"""# Informações da Versão - Processador de DARMs

Versão: 1.0.0
Data de Build: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Python: {sys.version}
Autor: Rodrigo Sardinha

## Arquivos Incluídos:
- darm_processor.py (Script principal)
- config.py (Configurações)
- requirements.txt (Dependências)
- README.md (Documentação)
- Exemplos de uso

## Instruções de Instalação:
1. Instale Python 3.7 ou superior
2. Execute: pip install -r requirements.txt
3. Execute: python darm_processor.py

## Estrutura de Diretórios:
- darms/ (Coloque os PDFs aqui)
- inserts/ (Arquivos SQL gerados)

## Suporte:
- GitHub: https://github.com/rodrigosardinha/gerador-query-darm
- Email: rodrigo.sardinha@example.com
"""
    
    with open("VERSION_INFO.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    
    return "VERSION_INFO.txt"

def create_installer_script():
    """Cria script de instalação para Windows"""
    installer_content = """@echo off
echo ========================================
echo    Processador de DARMs - Instalador
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.7 ou superior
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Instalar dependências
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para usar o processador:
echo 1. Coloque os PDFs dos DARMs na pasta 'darms'
echo 2. Execute: python darm_processor.py
echo 3. Os arquivos SQL serao gerados na pasta 'inserts'
echo.
pause
"""
    
    with open("install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    return "install.bat"

def create_installer_script_linux():
    """Cria script de instalação para Linux/macOS"""
    installer_content = """#!/bin/bash

echo "========================================"
echo "   Processador de DARMs - Instalador"
echo "========================================"
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não encontrado!"
    echo "Por favor, instale Python 3.7 ou superior"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

echo "Python encontrado!"
echo

# Instalar dependências
echo "Instalando dependências..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências!"
    exit 1
fi

echo
echo "========================================"
echo "   Instalação concluída com sucesso!"
echo "========================================"
echo
echo "Para usar o processador:"
echo "1. Coloque os PDFs dos DARMs na pasta 'darms'"
echo "2. Execute: python3 darm_processor.py"
echo "3. Os arquivos SQL serão gerados na pasta 'inserts'"
echo
"""
    
    with open("install.sh", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    # Tornar executável
    os.chmod("install.sh", 0o755)
    
    return "install.sh"

def create_package_structure():
    """Cria estrutura de pacote para distribuição"""
    package_dir = Path("dist/gerador-query-darm-1.0.0")
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivos principais
    files_to_copy = [
        "darm_processor.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "exemplo_uso.py",
        "test_darm_processor.py"
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, package_dir)
    
    # Criar diretórios
    (package_dir / "darms").mkdir(exist_ok=True)
    (package_dir / "inserts").mkdir(exist_ok=True)
    
    # Criar arquivos .gitkeep
    (package_dir / "darms" / ".gitkeep").touch()
    (package_dir / "inserts" / ".gitkeep").touch()
    
    return package_dir

def create_zip_package(package_dir):
    """Cria arquivo ZIP do pacote"""
    zip_filename = f"gerador-query-darm-1.0.0.zip"
    zip_path = Path("dist") / zip_filename
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    return zip_path

def create_executable_package():
    """Cria pacote com executável (se PyInstaller estiver disponível)"""
    try:
        import PyInstaller
        print("📦 Criando executável...")
        
        # Usar o script específico para executável
        from build_executable import create_package_with_executable
        zip_path = create_package_with_executable()
        
        if zip_path and zip_path.exists():
            print("✅ Pacote executável criado com sucesso!")
            return zip_path
        else:
            print("❌ Erro ao criar pacote executável")
            return None
            
    except ImportError:
        print("⚠️  PyInstaller não encontrado. Pulando criação de executável.")
        print("💡 Para instalar: pip install pyinstaller")
        return None
    except Exception as e:
        print(f"❌ Erro ao criar executável: {e}")
        return None

def main():
    """Função principal"""
    print("🚀 Iniciando processo de distribuição do Processador de DARMs")
    print("=" * 60)
    
    # Criar diretório dist se não existir
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Limpar builds anteriores
    if dist_dir.exists():
        for item in dist_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    
    print("📦 Criando estrutura do pacote...")
    package_dir = create_package_structure()
    
    print("📄 Criando arquivos de instalação...")
    version_file = create_version_info()
    installer_windows = create_installer_script()
    installer_linux = create_installer_script_linux()
    
    # Copiar arquivos de instalação para o pacote
    shutil.copy2(version_file, package_dir)
    shutil.copy2(installer_windows, package_dir)
    shutil.copy2(installer_linux, package_dir)
    
    print("🗜️  Criando arquivo ZIP...")
    zip_path = create_zip_package(package_dir)
    
    print("📦 Tentando criar executável...")
    exe_path = create_executable_package()
    
    # Relatório final
    print("\n" + "=" * 60)
    print("🎉 DISTRIBUIÇÃO CONCLUÍDA!")
    print("=" * 60)
    
    print(f"\n📁 Arquivos criados em dist/:")
    print(f"   📦 {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)")
    
    if exe_path and exe_path.exists():
        print(f"   🚀 {exe_path.name} ({exe_path.stat().st_size / 1024 / 1024:.1f} MB)")
    
    print(f"\n📋 Conteúdo do pacote:")
    print(f"   📄 darm_processor.py (Script principal)")
    print(f"   ⚙️  config.py (Configurações)")
    print(f"   📦 requirements.txt (Dependências)")
    print(f"   📚 README.md (Documentação)")
    print(f"   🧪 exemplo_uso.py (Exemplos)")
    print(f"   🧪 test_darm_processor.py (Testes)")
    print(f"   📄 VERSION_INFO.txt (Informações da versão)")
    print(f"   🔧 install.bat (Instalador Windows)")
    print(f"   🔧 install.sh (Instalador Linux/macOS)")
    print(f"   📁 darms/ (Pasta para PDFs)")
    print(f"   📁 inserts/ (Pasta para SQLs)")
    
    print(f"\n🚀 Como distribuir:")
    print(f"   1. Envie o arquivo {zip_path.name} para os usuários")
    print(f"   2. Os usuários devem extrair e executar install.bat (Windows) ou install.sh (Linux)")
    print(f"   3. Após instalação, executar: python darm_processor.py")
    
    # Limpar arquivos temporários
    for temp_file in [version_file, installer_windows, installer_linux]:
        if Path(temp_file).exists():
            Path(temp_file).unlink()
    
    print(f"\n✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    main() 