#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de build para o Processador de DARMs
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        for path in Path('.').glob(dir_pattern):
            if path.is_dir():
                print(f"🧹 Removendo {path}...")
                shutil.rmtree(path)

def build_package():
    """Constrói o pacote Python"""
    # Limpar builds anteriores
    clean_build_dirs()
    
    # Verificar se setuptools está instalado
    try:
        import setuptools
    except ImportError:
        print("❌ setuptools não encontrado. Instalando...")
        run_command("pip install setuptools wheel", "Instalando setuptools e wheel")
    
    # Construir o pacote
    print("📦 Construindo pacote...")
    run_command("python setup.py sdist bdist_wheel", "Construindo distribuição")
    
    # Verificar se os arquivos foram criados
    dist_dir = Path("dist")
    if dist_dir.exists():
        files = list(dist_dir.glob("*"))
        print(f"✅ Arquivos criados em dist/:")
        for file in files:
            print(f"   📄 {file.name} ({file.stat().st_size / 1024:.1f} KB)")

def install_package():
    """Instala o pacote localmente para teste"""
    print("🔧 Instalando pacote localmente...")
    run_command("pip install -e .", "Instalação em modo desenvolvimento")

def create_executable():
    """Cria executável usando PyInstaller (se disponível)"""
    try:
        import PyInstaller
        print("📦 Criando executável com PyInstaller...")
        run_command("pyinstaller --onefile --name darm-processor darm_processor.py", "Criando executável")
    except ImportError:
        print("⚠️  PyInstaller não encontrado. Para criar executável, instale com: pip install pyinstaller")

def create_docker_image():
    """Cria imagem Docker (se Docker estiver disponível)"""
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p darms inserts

# Expor volume para dados
VOLUME ["/app/darms", "/app/inserts"]

# Comando padrão
CMD ["python", "darm_processor.py"]
"""
    
    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    
    print("🐳 Dockerfile criado!")
    print("Para construir a imagem Docker, execute:")
    print("docker build -t darm-processor .")

def main():
    """Função principal"""
    print("🚀 Iniciando processo de build do Processador de DARMs")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("darm_processor.py").exists():
        print("❌ Erro: darm_processor.py não encontrado!")
        print("Execute este script no diretório raiz do projeto.")
        sys.exit(1)
    
    # Menu de opções
    print("\n📋 Opções de build:")
    print("1. Construir pacote Python (sdist + wheel)")
    print("2. Instalar localmente (modo desenvolvimento)")
    print("3. Criar executável (requer PyInstaller)")
    print("4. Criar Dockerfile")
    print("5. Executar tudo")
    print("0. Sair")
    
    choice = input("\nEscolha uma opção (0-5): ").strip()
    
    if choice == "1":
        build_package()
    elif choice == "2":
        install_package()
    elif choice == "3":
        create_executable()
    elif choice == "4":
        create_docker_image()
    elif choice == "5":
        build_package()
        install_package()
        create_docker_image()
        print("\n🎉 Processo completo!")
        print("\n📦 Para distribuir:")
        print("   - Pacote Python: arquivos em dist/")
        print("   - Executável: arquivo em dist/ (se PyInstaller instalado)")
        print("   - Docker: docker build -t darm-processor .")
    elif choice == "0":
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main() 