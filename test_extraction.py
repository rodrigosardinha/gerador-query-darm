#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para a extração do código de receita
"""

import re

def test_real_extraction():
    """Testar extração com o texto real do PDF"""
    
    # Texto real extraído do PDF
    text = """01. RECEITA
262-302. INSCRIÇÃO MUNICIPAL
0301548303. DATA VENCIMENTO
10/07/2025
04. ANO DE REFERÊNCIA
202505. GUIA NØ
0000149
06. VALOR DO TRIBUTO
R$ 32,05
07. VALOR MORA
*************08. VALOR MULTA
*************
09. VALOR TOTAL
R$ 32,0510. NOME/NOME EMPRESARIAL
AM PATT PUBLICIDADE LTDA11. INFORMAÇÕES COMPLEMENTARES
TAXA DE AUTORIZAÇÃO DE PUBLICIDADE
NÚMERO DO REQUERIMENTO - 2025001228
DATA DO DEFERIMENTO - 25/06/2025
TIPO - INTEGRAL
TIPO DE ENGENHO - PAINEL
LOCAL DE EXIBIÇÃO - ÁREA PÚBLICA"""
    
    print("=== TESTE DE EXTRAÇÃO REAL ===\n")
    print("Texto do PDF:")
    print(text)
    print("\n" + "="*50 + "\n")
    
    # Padrões atuais
    patterns = [
        r'(?:RECEITA|Receita)\s*(\d+-\d+)',
        r'01\.\s*RECEITA\s*(\d+-\d+)',
        r'(\d+)-(\d+)'  # Para formato como "262-3"
    ]
    
    for i, pattern in enumerate(patterns, 1):
        print(f"Testando padrão {i}: {pattern}")
        matches = re.findall(pattern, text, re.IGNORECASE)
        print(f"  Matches encontrados: {matches}")
        
        for match in matches:
            if isinstance(match, tuple):
                print(f"  Grupos: {match}")
                if len(match) == 2:
                    result = match[0] + match[1]
                    print(f"  Resultado (concatenação): {result}")
            else:
                print(f"  Match simples: {match}")
                if '-' in match:
                    result = match.replace('-', '')
                    print(f"  Resultado (remove hífen): {result}")
        print()

def test_specific_pattern():
    """Testar padrão específico para o problema"""
    
    text = "262-302. INSCRIÇÃO MUNICIPAL"
    
    print("=== TESTE PADRÃO ESPECÍFICO ===\n")
    print(f"Texto: '{text}'")
    
    # Padrão que pode estar causando problema
    pattern = r'(\d+)-(\d+)'
    
    matches = re.findall(pattern, text)
    print(f"Matches com {pattern}: {matches}")
    
    for match in matches:
        print(f"  Grupo 1: {match[0]}")
        print(f"  Grupo 2: {match[1]}")
        result = match[0] + match[1]
        print(f"  Resultado: {result}")

if __name__ == "__main__":
    test_real_extraction()
    test_specific_pattern() 