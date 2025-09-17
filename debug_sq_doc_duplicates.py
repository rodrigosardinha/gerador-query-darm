#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para identificar SQ_DOCs duplicados
"""

import re
from collections import Counter
from pathlib import Path

def find_duplicate_sq_docs():
    """Encontrar SQ_DOCs duplicados"""
    
    consolidated_path = Path('inserts/INSERT_TODOS_DARMs.sql')
    
    with open(consolidated_path, 'r', encoding='latin1') as f:
        content = f.read()
    
    print("🔍 Analisando SQ_DOCs duplicados...")
    
    # Extrair todos os números de 6 dígitos
    all_6_digit_numbers = re.findall(r'\b\d{6}\b', content)
    print(f"📊 Todos os números de 6 dígitos: {all_6_digit_numbers}")
    
    # Contar ocorrências
    counter = Counter(all_6_digit_numbers)
    duplicates = {item: count for item, count in counter.items() if count > 1}
    
    if duplicates:
        print(f"❌ SQ_DOCs duplicados encontrados:")
        for sq_doc, count in duplicates.items():
            print(f"   - {sq_doc}: {count} vezes")
    else:
        print("✅ Nenhum SQ_DOC duplicado encontrado")
    
    # Mostrar todos os números únicos
    unique_numbers = set(all_6_digit_numbers)
    print(f"\n📊 Números únicos: {sorted(unique_numbers)}")
    
    # Verificar se os SQ_DOCs estão na posição correta
    print("\n🔍 Verificando posição dos SQ_DOCs...")
    
    # Extrair cada INSERT individualmente
    insert_pattern = r'\(([^)]+)\)'
    inserts = re.findall(insert_pattern, content)
    
    for i, insert in enumerate(inserts):
        values = [v.strip() for v in insert.split(',')]
        if len(values) >= 8:
            sq_doc = values[7]
            nr_guia = values[16] if len(values) > 16 else "N/A"
            print(f"INSERT {i+1}: SQ_DOC={sq_doc}, NR_GUIA={nr_guia}")

if __name__ == "__main__":
    find_duplicate_sq_docs() 