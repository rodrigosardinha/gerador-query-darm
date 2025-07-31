#!/usr/bin/env python3
"""
Script de teste para verificar a geração de SQL
"""

import asyncio
import os
from pathlib import Path
from darm_processor import DarmProcessor

async def test_sql_generation():
    """Testar a geração de SQL"""
    print("🧪 Testando geração de SQL...")
    
    # Criar processador
    processor = DarmProcessor()
    
    # Inicializar
    await processor.init()
    
    # Dados de teste
    test_data = {
        'inscricao': '12345678',
        'numeroGuia': '12345',
        'valorPrincipal': '1000,50',
        'valorTotal': '1000,50',
        'dataVencimento': '15/01/2025',
        'exercicio': 2025,
        'codigoReceita': '2585',
        'codigoBarras': '123456789012345678901234567890123456789012345678'
    }
    
    # Testar geração de SQL
    print("\n📝 Testando geração de SQL individual...")
    sql_content = processor.generate_sql_insert(test_data)
    
    if sql_content:
        print("✅ SQL gerado com sucesso!")
        print(f"📏 Tamanho: {len(sql_content)} caracteres")
        print("📄 Primeiras 200 caracteres:")
        print(sql_content[:200] + "...")
        
        # Salvar arquivo de teste
        test_file = processor.output_dir / 'TESTE_SQL.sql'
        with open(test_file, 'w', encoding='latin1') as f:
            f.write(sql_content)
        print(f"💾 Arquivo de teste salvo: {test_file}")
        
        # Verificar se o arquivo foi salvo corretamente
        if test_file.exists():
            with open(test_file, 'r', encoding='latin1') as f:
                saved_content = f.read()
                if saved_content == sql_content:
                    print("✅ Arquivo salvo corretamente em Latin-1")
                else:
                    print("❌ Problema na gravação do arquivo")
        else:
            print("❌ Arquivo não foi criado")
    else:
        print("❌ Falha na geração do SQL")
    
    # Testar processamento de valores monetários
    print("\n💰 Testando processamento de valores monetários...")
    test_values = [
        '1000,50',
        '1.000,50',
        '1000.50',
        '1,000.50',
        'R$ 1.000,50',
        'R$ 1000,50'
    ]
    
    for value in test_values:
        processed = processor.parse_monetary_value(value)
        print(f"  {value} -> {processed}")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    asyncio.run(test_sql_generation()) 