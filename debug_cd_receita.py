#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug para analisar o problema do CD_RECEITA
"""

import re
from datetime import datetime

def debug_cd_receita():
    """Debug do CD_RECEITA"""
    
    print("=== DEBUG CD_RECEITA ===\n")
    
    # Simular dados extraídos do PDF
    darm_data = {
        'inscricao': '0301548303',
        'numeroGuia': '149',
        'codigoReceita': '2623',  # Valor extraído do PDF
        'valorPrincipal': '32.05',
        'valorTotal': '32.05',
        'dataVencimento': '10/07/2025',
        'exercicio': '2025',
        'codigoBarras': '012623020301548303100720250420250500001490632050'
    }
    
    print("Dados extraídos do PDF:")
    for key, value in darm_data.items():
        print(f"  {key}: {value}")
    
    print(f"\nCD_RECEITA extraído: {darm_data.get('codigoReceita')}")
    print(f"Tipo do CD_RECEITA: {type(darm_data.get('codigoReceita'))}")
    
    # Simular a geração do SQL individual
    codigo_receita_individual = darm_data.get('codigoReceita') or 2585
    print(f"\nCD_RECEITA para arquivo individual: {codigo_receita_individual}")
    
    # Simular a geração do SQL consolidado
    # O problema pode estar aqui - vamos verificar se há alguma transformação
    
    # Simular o SQL individual gerado
    sql_individual = f"""use silfae;

INSERT INTO FarrDarmsPagos (
    id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D,
    SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO,
    DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS,
    NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL,
    VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS,
    processado, criticaProcessamento
) VALUES (
    NULL, 2025, 70, 37, 0, 730, 1,
    (((149 % 1000) * 1000) + (UNIX_TIMESTAMP() % 1000)) % 1000000, {codigo_receita_individual}, NULL, 'FARR', NULL,
    NOW(), '2025-07-10 00:00:00', NOW(),
    '0301548303', 149, 2025, '012623020301548303100720250420250500001490632050',
    NULL, '13', NULL, 32.05, 32.05, 32.05,
    0.00, 0.00, NULL, NULL, NULL, 0.00,
    0, NULL
);"""
    
    print(f"\nSQL Individual gerado:")
    print(f"CD_RECEITA no SQL: {codigo_receita_individual}")
    
    # Simular o processamento do arquivo consolidado
    print(f"\n=== PROCESSAMENTO DO ARQUIVO CONSOLIDADO ===")
    
    # Extrair apenas a parte VALUES do INSERT
    values_match = re.search(r'VALUES\s*\(\s*(.+?)\s*\);', sql_individual, re.DOTALL)
    if values_match:
        values_part = values_match.group(1)
        print(f"Parte VALUES extraída: {values_part}")
        
        # Verificar se há alguma transformação no CD_RECEITA
        cd_receita_match = re.search(r',\s*(\d+),\s*NULL,\s*\'FARR\'', values_part)
        if cd_receita_match:
            cd_receita_consolidado = cd_receita_match.group(1)
            print(f"CD_RECEITA encontrado no VALUES: {cd_receita_consolidado}")
            
            if cd_receita_consolidado != str(codigo_receita_individual):
                print(f"❌ PROBLEMA ENCONTRADO!")
                print(f"   Individual: {codigo_receita_individual}")
                print(f"   Consolidado: {cd_receita_consolidado}")
            else:
                print(f"✅ CD_RECEITA consistente: {cd_receita_consolidado}")

def test_real_files():
    """Testar os arquivos reais gerados"""
    
    print("\n=== TESTE DOS ARQUIVOS REAIS ===\n")
    
    # Ler arquivo individual
    try:
        with open('inserts/INSERT_DARM_PAGO_149.sql', 'r', encoding='latin1') as f:
            individual_content = f.read()
        
        # Extrair CD_RECEITA do arquivo individual
        individual_match = re.search(r',\s*(\d+),\s*NULL,\s*\'FARR\'', individual_content)
        if individual_match:
            cd_receita_individual = individual_match.group(1)
            print(f"CD_RECEITA no arquivo individual: {cd_receita_individual}")
        
    except Exception as e:
        print(f"Erro ao ler arquivo individual: {e}")
    
    # Ler arquivo consolidado
    try:
        with open('inserts/INSERT_TODOS_DARMs.sql', 'r', encoding='latin1') as f:
            consolidated_content = f.read()
        
        # Extrair CD_RECEITA do arquivo consolidado
        consolidated_match = re.search(r',\s*(\d+),\s*NULL,\s*\'FARR\'', consolidated_content)
        if consolidated_match:
            cd_receita_consolidated = consolidated_match.group(1)
            print(f"CD_RECEITA no arquivo consolidado: {cd_receita_consolidated}")
        
        # Comparar
        if 'cd_receita_individual' in locals() and 'cd_receita_consolidated' in locals():
            if cd_receita_individual != cd_receita_consolidated:
                print(f"❌ INCONSISTÊNCIA ENCONTRADA!")
                print(f"   Individual: {cd_receita_individual}")
                print(f"   Consolidado: {cd_receita_consolidated}")
                print(f"   Diferença: {int(cd_receita_consolidated) - int(cd_receita_individual)}")
            else:
                print(f"✅ CD_RECEITA consistente: {cd_receita_individual}")
        
    except Exception as e:
        print(f"Erro ao ler arquivo consolidado: {e}")

if __name__ == "__main__":
    debug_cd_receita()
    test_real_files() 