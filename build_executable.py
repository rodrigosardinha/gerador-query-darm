#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar executável com PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def create_executable():
    """Cria executável com PyInstaller"""
    if not check_pyinstaller():
        print("❌ PyInstaller não encontrado!")
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    print("🚀 Criando executável com PyInstaller...")
    
    # Limpar builds anteriores
    for path in ['build', 'dist']:
        if Path(path).exists():
            shutil.rmtree(path)
    
    # Usar arquivo .spec se existir
    spec_file = Path("darm_processor.spec")
    if spec_file.exists():
        print("📄 Usando arquivo .spec personalizado...")
        cmd = ["pyinstaller", "--clean", "--noconfirm", "darm_processor.spec"]
    else:
        print("📄 Usando configuração padrão...")
        # Comando PyInstaller com configurações otimizadas
        cmd = [
            "pyinstaller",
            "--onefile",                    # Arquivo único
            "--name=darm-processor",        # Nome do executável
            "--add-data=config.py;.",       # Incluir arquivo de configuração
            "--add-data=requirements.txt;.", # Incluir requirements
            "--hidden-import=PyPDF2",       # Incluir PyPDF2 explicitamente
            "--hidden-import=pathlib",      # Incluir pathlib explicitamente
            "--clean",                      # Limpar cache
            "--noconfirm",                  # Não confirmar sobrescrita
            "darm_processor.py"
        ]
    
    print(f"Executando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Executável criado com sucesso!")
        
        # Verificar se o executável foi criado
        exe_path = Path("dist/darm-processor.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executável: {exe_path} ({size_mb:.1f} MB)")
            
            # Criar estrutura de diretórios ao lado do executável
            exe_dir = exe_path.parent
            (exe_dir / "darms").mkdir(exist_ok=True)
            (exe_dir / "inserts").mkdir(exist_ok=True)
            
            print(f"📁 Pastas criadas em {exe_dir}:")
            print(f"   📁 darms/ (para PDFs)")
            print(f"   📁 inserts/ (para SQLs gerados)")
            
            return exe_path
        else:
            print("❌ Executável não foi criado!")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def create_package_with_executable():
    """Cria um pacote completo com executável e pastas"""
    exe_path = create_executable()
    
    if not exe_path:
        return None
    
    # Criar diretório do pacote
    package_dir = Path("dist/darm-processor-package")
    package_dir.mkdir(exist_ok=True)
    
    # Copiar executável
    shutil.copy2(exe_path, package_dir / "darm-processor.exe")
    
    # Criar pastas necessárias
    (package_dir / "darms").mkdir(exist_ok=True)
    (package_dir / "inserts").mkdir(exist_ok=True)
    
    # Criar arquivo README para o pacote
    readme_content = """# Processador de DARMs - Executável

## Como usar:

1. **Coloque os PDFs dos DARMs na pasta `darms/`**
2. **Execute `darm-processor.exe`**
3. **Os arquivos SQL serão gerados na pasta `inserts/`**

## Estrutura:
```
darm-processor-package/
├── darm-processor.exe    # Executável principal
├── darms/                # Coloque os PDFs aqui
└── inserts/              # Arquivos SQL gerados
```

## Observações:
- O executável funciona independentemente
- Não requer instalação de Python
- Compatível com Windows 10/11
- Tamanho: ~50MB

## Suporte:
- GitHub: https://github.com/rodrigosardinha/gerador-query-darm
- Email: rodrigo.sardinha@example.com
"""
    
    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Criar arquivo ZIP do pacote
    import zipfile
    zip_path = Path("dist/darm-processor-package.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Pacote completo criado: {zip_path}")
    print(f"📦 Tamanho: {zip_path.stat().st_size / (1024 * 1024):.1f} MB")
    
    return zip_path

def main():
    """Função principal"""
    print("🚀 Gerador de Executável - Processador de DARMs")
    print("=" * 50)
    
    print("\n📋 Opções:")
    print("1. Criar apenas executável")
    print("2. Criar pacote completo (executável + pastas)")
    print("3. Limpar arquivos de build")
    print("0. Sair")
    
    choice = input("\nEscolha uma opção (0-3): ").strip()
    
    if choice == "1":
        create_executable()
    elif choice == "2":
        create_package_with_executable()
    elif choice == "3":
        # Limpar arquivos de build
        for path in ['build', 'dist', '*.spec']:
            for item in Path('.').glob(path):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        print("🧹 Arquivos de build removidos!")
    elif choice == "0":
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main() 