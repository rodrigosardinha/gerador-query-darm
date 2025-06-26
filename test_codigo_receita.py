#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para identificar problema na extração do CD_RECEITA
"""

import re

def test_codigo_receita_extraction():
    """Testar extração do código de receita"""
    
    # Simular texto do PDF
    sample_texts = [
        "01. RECEITA 262-3",
        "RECEITA 262-3",
        "262-3",
        "01. RECEITA 2623",
        "RECEITA 2623"
    ]
    
    # Padrões de regex do código atual
    patterns = [
        r'(?:RECEITA|Receita)\s*(\d+-\d+)',
        r'01\.\s*RECEITA\s*(\d+-\d+)',
        r'(\d+)-(\d+)'  # Para formato como "262-3"
    ]
    
    print("=== TESTE DE EXTRAÇÃO DO CÓDIGO DE RECEITA ===\n")
    
    for i, text in enumerate(sample_texts, 1):
        print(f"Teste {i}: '{text}'")
        
        data = {}
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                print(f"  Padrão encontrado: {pattern}")
                print(f"  Grupos: {match.groups()}")
                
                # Aplicar a lógica atual
                if len(match.groups()) > 1:
                    data['codigoReceita'] = match.group(1) + match.group(2)
                    print(f"  Resultado (concatenação): {data['codigoReceita']}")
                elif '-' in match.group(1):
                    data['codigoReceita'] = match.group(1).replace('-', '')
                    print(f"  Resultado (remove hífen): {data['codigoReceita']}")
                else:
                    data['codigoReceita'] = match.group(1).strip()
                    print(f"  Resultado (normal): {data['codigoReceita']}")
                break
        else:
            print("  ❌ Nenhum padrão encontrado")
        
        print()

def test_problematic_case():
    """Testar o caso problemático específico"""
    
    print("=== CASO PROBLEMÁTICO ESPECÍFICO ===\n")
    
    # Simular o texto que está causando problema
    text = "01. RECEITA 262-3"
    
    print(f"Texto: '{text}'")
    
    # Testar cada padrão individualmente
    patterns = [
        r'(?:RECEITA|Receita)\s*(\d+-\d+)',
        r'01\.\s*RECEITA\s*(\d+-\d+)',
        r'(\d+)-(\d+)'  # Para formato como "262-3"
    ]
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\nPadrão {i}: {pattern}")
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  ✅ Match encontrado")
            print(f"  Grupos: {match.groups()}")
            print(f"  Group(0): '{match.group(0)}'")
            print(f"  Group(1): '{match.group(1)}'")
            if len(match.groups()) > 1:
                print(f"  Group(2): '{match.group(2)}'")
        else:
            print(f"  ❌ Nenhum match")

if __name__ == "__main__":
    test_codigo_receita_extraction()
    test_problematic_case() 