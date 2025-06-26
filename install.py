#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Rápida - Processador de DARMs

Este script automatiza a instalação e configuração do ambiente
para o processador de DARMs em Python.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Verificar versão do Python"""
    print("🐍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("   ⚠️  É necessário Python 3.7 ou superior")
        print("   💡 Baixe em: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def check_pip():
    """Verificar se pip está disponível"""
    print("\n📦 Verificando pip...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pip está disponível")
            return True
        else:
            print("❌ pip não está disponível")
            return False
    except Exception:
        print("❌ Erro ao verificar pip")
        return False

def install_dependencies():
    """Instalar dependências"""
    print("\n📥 Instalando dependências...")
    
    try:
        # Instalar PyPDF2
        print("   📄 Instalando PyPDF2...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyPDF2==3.0.1'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ PyPDF2 instalado com sucesso")
        else:
            print(f"   ❌ Erro ao instalar PyPDF2: {result.stderr}")
            return False
        
        # Instalar pathlib2 (se necessário)
        print("   📁 Instalando pathlib2...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'pathlib2==2.3.7'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ pathlib2 instalado com sucesso")
        else:
            print(f"   ⚠️  pathlib2 não instalado (pode não ser necessário): {result.stderr}")
        
        print("✅ Todas as dependências instaladas")
        return True
        
    except Exception as error:
        print(f"❌ Erro durante instalação: {error}")
        return False

def create_directories():
    """Criar diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    try:
        # Diretório darms
        darms_dir = Path('darms')
        if not darms_dir.exists():
            darms_dir.mkdir()
            print("   ✅ Diretório 'darms/' criado")
        else:
            print("   ℹ️  Diretório 'darms/' já existe")
        
        # Diretório inserts
        inserts_dir = Path('inserts')
        if not inserts_dir.exists():
            inserts_dir.mkdir()
            print("   ✅ Diretório 'inserts/' criado")
        else:
            print("   ℹ️  Diretório 'inserts/' já existe")
        
        return True
        
    except Exception as error:
        print(f"❌ Erro ao criar diretórios: {error}")
        return False

def create_sample_files():
    """Criar arquivos de exemplo"""
    print("\n📝 Criando arquivos de exemplo...")
    
    try:
        # Arquivo .gitignore
        gitignore_content = """# Arquivos temporários
*.tmp
*.temp

# Arquivos de log
*.log

# Arquivos de backup
*.bak
*.backup

# Diretórios de saída (opcional)
# inserts/

# Arquivos PDF (opcional)
# darms/*.pdf
"""
        
        gitignore_path = Path('.gitignore')
        if not gitignore_path.exists():
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("   ✅ Arquivo .gitignore criado")
        
        # Arquivo README.md principal
        readme_content = """# Processador de DARMs - Versão Python

Este projeto processa arquivos PDF de DARMs (Documento de Arrecadação de Receitas Municipais) 
e gera scripts SQL para inserção no banco de dados.

## 🚀 Início Rápido

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Colocar PDFs na pasta `darms/`**

3. **Executar o processador:**
   ```bash
   python darm_processor.py
   ```

4. **Verificar resultados na pasta `inserts/`**

## 📚 Documentação

- [README_Python.md](README_Python.md) - Documentação completa
- [config.py](config.py) - Configurações do sistema
- [exemplo_uso.py](exemplo_uso.py) - Exemplos de uso
- [test_darm_processor.py](test_darm_processor.py) - Testes do sistema

## 🔧 Testes

Execute os testes para verificar se tudo está funcionando:

```bash
python test_darm_processor.py
```

## 📁 Estrutura

```
gera-query-pagar-darm/
├── darms/                    # PDFs dos DARMs
├── inserts/                  # Arquivos SQL gerados
├── darm_processor.py         # Script principal
├── config.py                 # Configurações
├── requirements.txt          # Dependências
├── README_Python.md          # Documentação
├── exemplo_uso.py            # Exemplos
├── test_darm_processor.py    # Testes
└── install.py                # Instalação
```

## 🆚 Comparação com JavaScript

Esta versão Python mantém todas as funcionalidades da versão JavaScript original,
com melhorias em:

- ✅ Melhor tratamento de PDFs
- ✅ Código mais limpo e legível
- ✅ Melhor tratamento de erros
- ✅ Configurações centralizadas
- ✅ Testes automatizados
- ✅ Documentação completa

---
**Desenvolvido em Python** - Compatível com a versão JavaScript original
"""
        
        readme_path = Path('README.md')
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print("   ✅ Arquivo README.md criado")
        
        return True
        
    except Exception as error:
        print(f"❌ Erro ao criar arquivos de exemplo: {error}")
        return False

def run_tests():
    """Executar testes básicos"""
    print("\n🧪 Executando testes básicos...")
    
    try:
        # Teste de importação
        print("   🔍 Testando importações...")
        
        import asyncio
        print("   ✅ asyncio importado")
        
        import re
        print("   ✅ re importado")
        
        from datetime import datetime
        print("   ✅ datetime importado")
        
        from pathlib import Path
        print("   ✅ pathlib importado")
        
        # Tentar importar PyPDF2
        try:
            import PyPDF2
            print("   ✅ PyPDF2 importado")
        except ImportError:
            print("   ❌ PyPDF2 não encontrado")
            return False
        
        # Teste de configuração
        try:
            from config import validate_config
            errors = validate_config()
            if not errors:
                print("   ✅ Configurações válidas")
            else:
                print(f"   ⚠️  Configurações com avisos: {errors}")
        except Exception as error:
            print(f"   ❌ Erro nas configurações: {error}")
            return False
        
        print("✅ Testes básicos passaram")
        return True
        
    except Exception as error:
        print(f"❌ Erro durante testes: {error}")
        return False

def show_next_steps():
    """Mostrar próximos passos"""
    print("\n🎯 Próximos Passos")
    print("=" * 20)
    print("1. 📁 Coloque arquivos PDF na pasta 'darms/'")
    print("2. 🚀 Execute: python darm_processor.py")
    print("3. 📊 Verifique os resultados na pasta 'inserts/'")
    print("4. 🧪 Execute testes: python test_darm_processor.py")
    print("5. 📚 Leia a documentação: README_Python.md")
    print()
    print("💡 Dicas:")
    print("   - Use 'python exemplo_uso.py' para ver exemplos")
    print("   - Configure parâmetros em 'config.py'")
    print("   - Verifique logs no console durante execução")

def main():
    """Função principal de instalação"""
    print("🚀 Instalação do Processador de DARMs - Versão Python")
    print("=" * 60)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Verificar pip
    if not check_pip():
        print("\n❌ pip não está disponível")
        print("💡 Instale pip: https://pip.pypa.io/en/stable/installation/")
        return False
    
    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha na instalação das dependências")
        return False
    
    # Criar diretórios
    if not create_directories():
        print("\n❌ Falha na criação dos diretórios")
        return False
    
    # Criar arquivos de exemplo
    if not create_sample_files():
        print("\n❌ Falha na criação dos arquivos de exemplo")
        return False
    
    # Executar testes
    if not run_tests():
        print("\n❌ Falha nos testes básicos")
        return False
    
    print("\n🎉 Instalação concluída com sucesso!")
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Instalação falhou. Verifique os erros acima.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalação interrompida pelo usuário")
        sys.exit(1)
    except Exception as error:
        print(f"\n❌ Erro inesperado: {error}")
        sys.exit(1) 