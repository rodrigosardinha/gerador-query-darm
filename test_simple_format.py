#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se o formato simplificado está funcionando corretamente
"""

import asyncio
from darm_processor import DarmProcessor

async def test_simple_format():
    """Testar o formato simplificado"""
    
    print("=== TESTE DO FORMATO SIMPLIFICADO ===\n")
    
    # Criar instância do processador
    processor = DarmProcessor()
    await processor.init()
    
    # Dados de exemplo
    sample_data = {
        'inscricao': '03015483',
        'numeroGuia': '201',
        'valorPrincipal': '176.27',
        'valorTotal': '176.27',
        'dataVencimento': '17/07/2025',
        'exercicio': '2025',
        'codigoReceita': '2623',
        'codigoBarras': '012623020301548303170720250420250500002010617627'
    }
    
    print("Dados de exemplo:")
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    print("\n=== GERANDO SQL INDIVIDUAL ===")
    
    # Gerar SQL individual
    sql_individual = processor.generate_sql_insert(sample_data)
    print("SQL Individual gerado:")
    print(sql_individual)
    
    print("\n=== VERIFICANDO FORMATO ===")
    
    # Verificar se está no formato simplificado
    if 'INSERT INTO FarrDarmsPagos (id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS, processado, criticaProcessamento) VALUES' in sql_individual:
        print("✅ Formato simplificado detectado!")
        print("✅ Compatível com Control-M")
    else:
        print("❌ Formato não está simplificado")
    
    # Verificar se tem quebras de linha problemáticas
    if '\n' in sql_individual and sql_individual.count('\n') <= 2:  # Apenas use silfae; e o INSERT
        print("✅ Quebras de linha adequadas")
    else:
        print("❌ Muitas quebras de linha detectadas")
    
    print("\n=== TESTANDO ARQUIVO CONSOLIDADO ===")
    
    # Simular dados para arquivo consolidado
    processor.guias_processadas = ['201', '202']
    processor.all_sql_inserts = [sql_individual, sql_individual]
    
    # Gerar arquivo consolidado
    await processor.generate_single_sql_file()
    
    print("✅ Arquivo consolidado gerado com sucesso!")
    
    # Verificar se o arquivo foi criado
    consolidated_file = processor.output_dir / 'INSERT_TODOS_DARMs.sql'
    if consolidated_file.exists():
        print("✅ Arquivo consolidado criado no disco")
        
        # Ler e mostrar o conteúdo
        with open(consolidated_file, 'r', encoding='latin1') as f:
            content = f.read()
            print("\nConteúdo do arquivo consolidado:")
            print(content)
    else:
        print("❌ Arquivo consolidado não foi criado")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    asyncio.run(test_simple_format()) 