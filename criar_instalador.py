#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar um instalador completo do Processador de DARMs
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def criar_instalador():
    """Criar instalador completo do Processador de DARMs"""
    
    print("🚀 Criando Instalador do Processador de DARMs")
    print("=" * 50)
    
    # Diretórios
    base_dir = Path(".")
    dist_dir = base_dir / "dist"
    installer_dir = base_dir / "Instalador"
    
    # Criar diretório do instalador
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    # 1. Copiar executável
    print("📦 Copiando executável...")
    exe_source = dist_dir / "Processador-DARM.exe"
    exe_dest = installer_dir / "Processador-DARM.exe"
    shutil.copy2(exe_source, exe_dest)
    
    # 2. Criar estrutura de diretórios
    print("📁 Criando estrutura de diretórios...")
    (installer_dir / "darms").mkdir()
    (installer_dir / "inserts").mkdir()
    
    # 3. Criar arquivo README para o usuário
    print("📝 Criando documentação...")
    readme_content = """# 🏛️ Processador de DARMs - Instalador

## 📋 Como Usar

### 1. Executar o Processador
- Execute o arquivo `Processador-DARM.exe`
- O programa irá processar automaticamente todos os PDFs na pasta `darms/`

### 2. Preparar os DARMs
- Coloque os arquivos PDF dos DARMs na pasta `darms/`
- Formatos suportados: PDF, PNG, JPG, JPEG, BMP, TIFF, TIF

### 3. Verificar Resultados
- Os arquivos SQL serão gerados na pasta `inserts/`
- Verifique o relatório `RELATORIO_PROCESSAMENTO.md`

## 📁 Estrutura de Pastas

```
Processador-DARM/
├── Processador-DARM.exe    # Executável principal
├── darms/                  # Coloque seus PDFs aqui
│   └── (seus arquivos PDF)
├── inserts/                # Arquivos SQL gerados
│   ├── INSERT_TODOS_DARMs.sql
│   ├── INSERT_DARM_PAGO_*.sql
│   ├── CHECK_GUIA_*.sql
│   └── RELATORIO_PROCESSAMENTO.md
└── README.txt              # Este arquivo
```

## 🔧 Funcionalidades

- ✅ **Extração automática** de dados de PDFs
- ✅ **Suporte a OCR** para PDFs com imagens
- ✅ **Geração de SQL** compatível com Control-M
- ✅ **Correção automática** de inscrições municipais
- ✅ **Relatórios detalhados** do processamento
- ✅ **Controle de duplicatas** automático

## 🚨 Solução de Problemas

### Erro: "Nenhum arquivo encontrado"
- Verifique se os PDFs estão na pasta `darms/`
- Certifique-se que os arquivos têm extensão `.pdf`

### Erro: "Dados insuficientes"
- Verifique se o PDF contém dados válidos de DARM
- Tente com um PDF diferente

### Problemas de permissão
- Execute como administrador se necessário
- Verifique se tem permissão de escrita na pasta

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique este README primeiro
- Consulte o relatório de processamento
- Entre em contato com o suporte técnico

---
**Versão**: 1.0.0
**Data**: {data_atual}
**Compatibilidade**: Windows 10/11
""".format(data_atual=datetime.now().strftime("%d/%m/%Y"))
    
    with open(installer_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 4. Criar script de instalação para Windows
    print("💻 Criando script de instalação...")
    install_bat = """@echo off
echo ========================================
echo  Processador de DARMs - Instalacao
echo ========================================
echo.

echo Criando estrutura de pastas...
if not exist "darms" mkdir "darms"
if not exist "inserts" mkdir "inserts"

echo.
echo Instalacao concluida!
echo.
echo Como usar:
echo 1. Coloque os PDFs dos DARMs na pasta 'darms'
echo 2. Execute 'Processador-DARM.exe'
echo 3. Verifique os resultados na pasta 'inserts'
echo.
echo Pressione qualquer tecla para sair...
pause >nul
"""
    
    with open(installer_dir / "INSTALAR.bat", "w", encoding="utf-8") as f:
        f.write(install_bat)
    
    # 5. Criar arquivo de exemplo
    print("📄 Criando arquivo de exemplo...")
    exemplo_content = """# Exemplo de DARM Processado

Este arquivo demonstra como o Processador de DARMs funciona.

## Como testar:

1. Coloque um PDF de DARM na pasta `darms/`
2. Execute `Processador-DARM.exe`
3. Verifique os arquivos SQL gerados na pasta `inserts/`

## Arquivos gerados:

- `INSERT_TODOS_DARMs.sql` - Script único com todos os registros
- `INSERT_DARM_PAGO_*.sql` - Scripts individuais por guia
- `CHECK_GUIA_*.sql` - Scripts de verificação
- `RELATORIO_PROCESSAMENTO.md` - Relatório detalhado

## Dados extraídos:

- Inscrição Municipal
- Número da Guia
- Código de Receita
- Valores (Principal, Total)
- Data de Vencimento
- Exercício
- Código de Barras
- Competência

---
Processador de DARMs v1.0.0
"""
    
    with open(installer_dir / "EXEMPLO.txt", "w", encoding="utf-8") as f:
        f.write(exemplo_content)
    
    # 6. Criar arquivo ZIP do instalador
    print("📦 Criando arquivo ZIP do instalador...")
    zip_filename = f"Processador-DARM-Instalador-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"
    zip_path = base_dir / zip_filename
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(installer_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(installer_dir)
                zipf.write(file_path, arcname)
    
    # 7. Mostrar informações do instalador
    print("\n✅ Instalador criado com sucesso!")
    print(f"📁 Localização: {installer_dir}")
    print(f"📦 Arquivo ZIP: {zip_filename}")
    print(f"📊 Tamanho do ZIP: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    print("\n📋 Conteúdo do instalador:")
    for item in installer_dir.rglob("*"):
        if item.is_file():
            print(f"   - {item.relative_to(installer_dir)}")
    
    print(f"\n🎯 Para distribuir:")
    print(f"   1. Envie o arquivo: {zip_filename}")
    print(f"   2. O usuário deve extrair e executar INSTALAR.bat")
    print(f"   3. Depois executar Processador-DARM.exe")
    
    return zip_filename

if __name__ == "__main__":
    criar_instalador()

