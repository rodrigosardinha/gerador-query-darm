#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para regenerar o arquivo consolidado com a correção do CD_RECEITA
"""

import asyncio
import re
from pathlib import Path
from darm_processor import DarmProcessor

async def regenerate_consolidated():
    """Regenerar arquivo consolidado"""
    processor = DarmProcessor()
    await processor.init()
    
    # Carregar INSERTs dos arquivos individuais existentes
    output_dir = Path(__file__).parent / 'inserts'
    sql_files = [f for f in output_dir.iterdir() 
                if f.name.startswith('INSERT_DARM_PAGO_') and f.suffix.lower() == '.sql']
    
    for sql_file in sql_files:
        with open(sql_file, 'r', encoding='latin1') as f:
            content = f.read()
            processor.all_sql_inserts.append(content)
            
        # Extrair número da guia do nome do arquivo
        match = re.search(r'INSERT_DARM_PAGO_(\d+)\.sql', sql_file.name)
        if match:
            guia = match.group(1)
            processor.guias_processadas.append(guia)
    
    print(f"Carregados {len(processor.all_sql_inserts)} INSERTs dos arquivos individuais")
    
    # Gerar arquivo consolidado
    await processor.generate_single_sql_file()

if __name__ == "__main__":
    asyncio.run(regenerate_consolidated()) 