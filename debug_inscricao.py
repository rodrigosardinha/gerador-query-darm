#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para testar a extração da inscrição municipal
"""

import re

def test_inscricao_extraction():
    """Testar diferentes padrões de extração de inscrição"""
    
    # Texto extraído do PDF (conforme mostrado na execução)
    text = """01. RECEITA
262-302. INSCRIÇÃO MUNICIPAL
0301548303. DATA VENCIMENTO
15/07/2025
04. ANO DE REFERÊNCIA
202505. GUIA NØ
0000186
06. VALOR DO TRIBUTO
R$ 16,02
07. VALOR MORA
*************08. VALOR MULTA
*************
09. VALOR TOTAL
R$ 16,0210. NOME/NOME EMPRESARIAL
AM PATT PUBLICIDADE LTDA11. INFORMAÇÕES COMPLEMENTARES
TAXA DE AUTORIZAÇÃO DE PUBLICIDADE
NÚMERO DO REQUERIMENTO - 2025002025
DATA DO DEFERIMENTO - 30/06/2025
TIPO - INTEGRAL
TIPO DE ENGENHO - PAINEL
LOCAL DE EXIBIÇÃO - ÁREA PÚBLICA"""

    print("=== DEBUG: EXTRAÇÃO DE INSCRIÇÃO ===")
    print(f"Texto completo:\n{text}")
    print("\n" + "="*50)
    
    # Padrões atuais do código
    patterns = [
        r'(?:Inscrição|INSCRIÇÃO|Inscrição Municipal|Inscrição)\s*:?\s*(\d+)',
        r'(?:Inscrição|INSCRIÇÃO)\s*(\d+)',
        r'Insc\.?\s*:?\s*(\d+)',
        r'02\.\s*INSCRIÇÃO MUNICIPAL\s*(\d+)'
    ]
    
    print("Testando padrões atuais:")
    for i, pattern in enumerate(patterns, 1):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"✅ Padrão {i}: '{pattern}' -> '{match.group(1)}'")
        else:
            print(f"❌ Padrão {i}: '{pattern}' -> NÃO ENCONTRADO")
    
    print("\n" + "="*50)
    
    # Testar padrões alternativos
    print("Testando padrões alternativos:")
    
    # Padrão mais específico para o formato do PDF
    alt_patterns = [
        r'02\.\s*INSCRIÇÃO MUNICIPAL\s*\n?(\d+)',  # Com quebra de linha opcional
        r'02\.\s*INSCRIÇÃO MUNICIPAL\s*(\d{8,10})',  # Especificar tamanho
        r'INSCRIÇÃO MUNICIPAL\s*\n?(\d+)',  # Sem o "02."
        r'INSCRIÇÃO MUNICIPAL\s*(\d+)',  # Padrão simples
        r'02\.\s*INSCRIÇÃO MUNICIPAL\s*(\d{8})',  # Exatamente 8 dígitos
    ]
    
    for i, pattern in enumerate(alt_patterns, 1):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"✅ Alt Padrão {i}: '{pattern}' -> '{match.group(1)}'")
        else:
            print(f"❌ Alt Padrão {i}: '{pattern}' -> NÃO ENCONTRADO")
    
    print("\n" + "="*50)
    
    # Testar extração manual
    print("Análise manual do texto:")
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'INSCRIÇÃO' in line.upper():
            print(f"Linha {i+1}: '{line}'")
            # Tentar extrair números da linha
            numbers = re.findall(r'\d+', line)
            print(f"  Números encontrados: {numbers}")
            
            # Verificar se há números na próxima linha
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_numbers = re.findall(r'\d+', next_line)
                print(f"  Próxima linha ({i+2}): '{next_line}'")
                print(f"  Números na próxima linha: {next_numbers}")

if __name__ == "__main__":
    test_inscricao_extraction() 