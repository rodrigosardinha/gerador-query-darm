#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar os dados extraídos entre versão antiga e nova
"""

import re

def extrair_valores_sql(sql_content):
    """Extrair valores do SQL para comparação"""
    # Encontrar a parte VALUES
    values_match = re.search(r'VALUES\s*\(\s*(.+?)\s*\);', sql_content, re.DOTALL)
    if not values_match:
        return None
    
    values_part = values_match.group(1)
    
    # Dividir por vírgulas, mas respeitando strings
    valores = []
    current_value = ""
    in_string = False
    paren_count = 0
    
    for char in values_part:
        if char == "'" and (len(current_value) == 0 or current_value[-1] != '\\'):
            in_string = not in_string
            current_value += char
        elif char == '(' and not in_string:
            paren_count += 1
            current_value += char
        elif char == ')' and not in_string:
            paren_count -= 1
            current_value += char
        elif char == ',' and not in_string and paren_count == 0:
            valores.append(current_value.strip())
            current_value = ""
        else:
            current_value += char
    
    if current_value.strip():
        valores.append(current_value.strip())
    
    return valores

def comparar_sql_files():
    """Comparar arquivos SQL antigo e novo"""
    
    print("=== COMPARAÇÃO DE DADOS EXTRAÍDOS ===\n")
    
    # Ler arquivo antigo
    try:
        with open('inserts/INSERT_DARM_PAGO_201_V5.sql', 'r', encoding='latin1') as f:
            sql_antigo = f.read()
        print("✅ Arquivo antigo lido: INSERT_DARM_PAGO_201_V5.sql")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo antigo: {e}")
        return
    
    # Ler arquivo novo
    try:
        with open('inserts/INSERT_DARM_PAGO_201.sql', 'r', encoding='latin1') as f:
            sql_novo = f.read()
        print("✅ Arquivo novo lido: INSERT_DARM_PAGO_201.sql")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo novo: {e}")
        return
    
    # Extrair valores
    valores_antigo = extrair_valores_sql(sql_antigo)
    valores_novo = extrair_valores_sql(sql_novo)
    
    if not valores_antigo or not valores_novo:
        print("❌ Erro ao extrair valores dos SQLs")
        return
    
    print(f"\n📊 Valores extraídos:")
    print(f"   Antigo: {len(valores_antigo)} valores")
    print(f"   Novo: {len(valores_novo)} valores")
    
    # Campos importantes para verificar
    campos_importantes = [
        "AA_EXERCICIO", "CD_BANCO", "NR_BDA", "NR_COMPLEMENTO", "NR_LOTE_NSA", "TP_LOTE_D",
        "CD_RECEITA", "CD_USU_INCL", "DT_VENCTO", "NR_INSCRICAO", "NR_GUIA", "NR_COMPETENCIA",
        "NR_CODIGO_BARRAS", "ST_DOC_D", "VL_PAGO", "VL_RECEITA", "VL_PRINCIPAL"
    ]
    
    print(f"\n🔍 Comparando {len(campos_importantes)} campos importantes:")
    
    diferencas = []
    iguais = []
    
    for i, campo in enumerate(campos_importantes):
        if i < len(valores_antigo) and i < len(valores_novo):
            valor_antigo = valores_antigo[i].strip()
            valor_novo = valores_novo[i].strip()
            
            # Para SQ_DOC, comparar apenas a estrutura (não o valor exato)
            if campo == "SQ_DOC":
                if "UNIX_TIMESTAMP()" in valor_antigo and "UNIX_TIMESTAMP()" in valor_novo:
                    status = "✅ Estrutura igual"
                    iguais.append(campo)
                else:
                    status = "❌ Estrutura diferente"
                    diferencas.append((campo, valor_antigo, valor_novo))
            elif valor_antigo == valor_novo:
                status = "✅ Igual"
                iguais.append(campo)
            else:
                status = "❌ Diferente"
                diferencas.append((campo, valor_antigo, valor_novo))
            
            print(f"   {campo}: {status}")
            if status.startswith("❌"):
                print(f"      Antigo: {valor_antigo}")
                print(f"      Novo:   {valor_novo}")
    
    print(f"\n📈 RESUMO:")
    print(f"   ✅ Campos iguais: {len(iguais)}")
    print(f"   ❌ Campos diferentes: {len(diferencas)}")
    
    if len(diferencas) == 0:
        print("\n🎉 TODOS OS DADOS SÃO IDÊNTICOS!")
        print("   A extração de dados NÃO foi afetada pelas mudanças de formatação.")
    else:
        print(f"\n⚠️  DIFERENÇAS ENCONTRADAS:")
        for campo, antigo, novo in diferencas:
            print(f"   {campo}: '{antigo}' vs '{novo}'")
    
    # Verificar se há diferenças apenas na formatação
    print(f"\n🔧 ANÁLISE DE FORMATAÇÃO:")
    
    # Contar quebras de linha
    quebras_antigo = sql_antigo.count('\n')
    quebras_novo = sql_novo.count('\n')
    
    print(f"   Quebras de linha no antigo: {quebras_antigo}")
    print(f"   Quebras de linha no novo: {quebras_novo}")
    
    if quebras_antigo > quebras_novo:
        print("   ✅ Formatação simplificada aplicada corretamente")
    
    # Verificar se o conteúdo é o mesmo (ignorando formatação)
    sql_antigo_limpo = re.sub(r'\s+', ' ', sql_antigo.strip())
    sql_novo_limpo = re.sub(r'\s+', ' ', sql_novo.strip())
    
    if sql_antigo_limpo == sql_novo_limpo:
        print("   ✅ Conteúdo idêntico (apenas formatação diferente)")
    else:
        print("   ❌ Conteúdo diferente detectado")

if __name__ == "__main__":
    comparar_sql_files() 