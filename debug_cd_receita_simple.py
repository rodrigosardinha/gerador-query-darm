#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug simples para o problema do CD_RECEITA
"""

def test_cd_receita_logic():
    """Testar a lógica do código de receita"""
    
    print("=== TESTE DA LÓGICA DO CD_RECEITA ===\n")
    
    # Simular dados extraídos do PDF
    darm_data = {
        'codigoReceita': '26-30',  # Formato extraído do PDF
        'numeroGuia': '1549'
    }
    
    print(f"Dados extraídos: {darm_data}")
    
    # Aplicar a lógica atual do código
    codigo_receita = darm_data.get('codigoReceita') or 2585
    print(f"1. Código de receita inicial: {codigo_receita}")
    
    # Se o código de receita tem hífen, converter para número
    if isinstance(codigo_receita, str) and '-' in codigo_receita:
        codigo_receita = codigo_receita.replace('-', '')
        print(f"2. Após remover hífen: {codigo_receita}")
    
    print(f"3. Resultado final: {codigo_receita}")
    print(f"4. Tipo: {type(codigo_receita)}")
    
    # Testar com valor padrão
    print(f"\n--- Teste com valor padrão ---")
    darm_data2 = {}
    codigo_receita2 = darm_data2.get('codigoReceita') or 2585
    print(f"Valor padrão: {codigo_receita2}")
    
    # Testar com None
    print(f"\n--- Teste com None ---")
    darm_data3 = {'codigoReceita': None}
    codigo_receita3 = darm_data3.get('codigoReceita') or 2585
    print(f"Com None: {codigo_receita3}")
    
    # Testar com string vazia
    print(f"\n--- Teste com string vazia ---")
    darm_data4 = {'codigoReceita': ''}
    codigo_receita4 = darm_data4.get('codigoReceita') or 2585
    print(f"Com string vazia: {codigo_receita4}")

if __name__ == "__main__":
    test_cd_receita_logic()
