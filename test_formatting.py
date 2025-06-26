#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar a formatação do arquivo consolidado
"""

def test_formatting():
    """Testar formatação do arquivo consolidado"""
    
    # Simular dados
    simple_insert_statements = [
        "(NULL, 2025, 70, 37, 0, 730, 1, 149063, 2623, NULL, 'FARR', NULL, NOW(), '2025-07-10 00:00:00', NOW(), '0301548303', 149, 2025, '012623020301548303100720250420250500001490632050', NULL, '13', NULL, 32.05, 32.05, 32.05, 0.00, 0.00, NULL, NULL, NULL, 0.00, 0, NULL)"
    ]
    
    # Formatação atual
    formatted_inserts = []
    for stmt in simple_insert_statements:
        formatted_inserts.append(f"    {stmt}")

    single_sql_content = f"""use silfae;

INSERT INTO FarrDarmsPagos (
    id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D,
    SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO,
    DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS,
    NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL,
    VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS,
    processado, criticaProcessamento
) VALUES
{',\n'.join(formatted_inserts)};"""

    print("=== TESTE DE FORMATAÇÃO ===")
    print(single_sql_content)
    print("=== FIM DO TESTE ===")

if __name__ == "__main__":
    test_formatting() 