#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do Processador de DARMs em Python

Este script demonstra como usar o DarmProcessor para processar arquivos PDF
de DARMs e gerar scripts SQL para inserção no banco de dados.
"""

import asyncio
import os
from pathlib import Path
from darm_processor import DarmProcessor

async def exemplo_basico():
    """Exemplo básico de uso do processador"""
    print("🚀 Exemplo Básico - Processamento de DARMs")
    print("=" * 50)
    
    # Criar instância do processador
    processor = DarmProcessor()
    
    # Inicializar
    await processor.init()
    
    # Processar DARMs
    await processor.process_darms()
    
    print("\n✅ Processamento básico concluído!")

async def exemplo_com_verificacoes():
    """Exemplo com verificações adicionais"""
    print("\n🔍 Exemplo com Verificações - Processamento de DARMs")
    print("=" * 50)
    
    # Criar instância do processador
    processor = DarmProcessor()
    
    # Verificar se o diretório darms existe
    if not processor.darms_dir.exists():
        print(f"❌ Diretório {processor.darms_dir} não encontrado!")
        print("📁 Criando diretório...")
        processor.darms_dir.mkdir(exist_ok=True)
        print("💡 Coloque os arquivos PDF dos DARMs na pasta 'darms/' e execute novamente.")
        return
    
    # Verificar se há arquivos PDF
    pdf_files = list(processor.darms_dir.glob("*.pdf"))
    if not pdf_files:
        print("📭 Nenhum arquivo PDF encontrado na pasta 'darms/'")
        print("💡 Adicione arquivos PDF de DARMs e execute novamente.")
        return
    
    print(f"📁 Encontrados {len(pdf_files)} arquivos PDF:")
    for pdf_file in pdf_files:
        print(f"   - {pdf_file.name}")
    
    # Inicializar
    await processor.init()
    
    # Processar DARMs
    await processor.process_darms()
    
    print("\n✅ Processamento com verificações concluído!")

async def exemplo_estatisticas():
    """Exemplo mostrando estatísticas do processamento"""
    print("\n📊 Exemplo de Estatísticas - Processamento de DARMs")
    print("=" * 50)
    
    # Criar instância do processador
    processor = DarmProcessor()
    
    # Inicializar
    await processor.init()
    
    # Processar DARMs
    await processor.process_darms()
    
    # Mostrar estatísticas
    print(f"\n📈 Estatísticas do Processamento:")
    print(f"   - Total de guias processadas: {len(processor.guias_processadas)}")
    print(f"   - Guias únicas: {len(set(processor.guias_processadas))}")
    print(f"   - Arquivos SQL gerados: {len(processor.all_sql_inserts)}")
    
    if processor.guias_processadas:
        print(f"   - Primeira guia: {processor.guias_processadas[0]}")
        print(f"   - Última guia: {processor.guias_processadas[-1]}")
    
    print("\n✅ Estatísticas geradas!")

def mostrar_estrutura_projeto():
    """Mostrar a estrutura esperada do projeto"""
    print("\n📁 Estrutura do Projeto")
    print("=" * 30)
    print("gera-query-pagar-darm/")
    print("├── darms/                    # PDFs dos DARMs")
    print("│   ├── darm1.pdf")
    print("│   ├── darm2.pdf")
    print("│   └── ...")
    print("├── inserts/                  # Arquivos SQL gerados")
    print("│   ├── INSERT_TODOS_DARMs.sql")
    print("│   ├── INSERT_DARM_PAGO_*.sql")
    print("│   ├── CHECK_GUIA_*.sql")
    print("│   └── RELATORIO_PROCESSAMENTO.md")
    print("├── darm_processor.py         # Script principal")
    print("├── requirements.txt          # Dependências")
    print("├── README_Python.md          # Documentação")
    print("└── exemplo_uso.py            # Este arquivo")

def mostrar_comandos():
    """Mostrar comandos úteis"""
    print("\n💻 Comandos Úteis")
    print("=" * 20)
    print("1. Instalar dependências:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Executar processador:")
    print("   python darm_processor.py")
    print()
    print("3. Executar exemplo:")
    print("   python exemplo_uso.py")
    print()
    print("4. Verificar arquivos gerados:")
    print("   dir inserts/")
    print()

async def main():
    """Função principal do exemplo"""
    print("🎯 Processador de DARMs - Exemplos de Uso")
    print("=" * 50)
    
    # Mostrar estrutura do projeto
    mostrar_estrutura_projeto()
    
    # Mostrar comandos úteis
    mostrar_comandos()
    
    # Executar exemplos
    try:
        await exemplo_basico()
        await exemplo_com_verificacoes()
        await exemplo_estatisticas()
        
        print("\n🎉 Todos os exemplos executados com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Coloque arquivos PDF na pasta 'darms/'")
        print("2. Execute: python darm_processor.py")
        print("3. Verifique os resultados na pasta 'inserts/'")
        
    except Exception as error:
        print(f"\n❌ Erro durante a execução: {error}")
        print("\n🔧 Verifique se:")
        print("- As dependências estão instaladas (pip install -r requirements.txt)")
        print("- Os arquivos PDF estão na pasta 'darms/'")
        print("- Você tem permissão de escrita na pasta do projeto")

if __name__ == "__main__":
    # Executar o exemplo
    asyncio.run(main()) 