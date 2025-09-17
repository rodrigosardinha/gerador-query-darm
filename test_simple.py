#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_cd_receita():
    """Teste simples do código de receita"""
    
    print("=== TESTE SIMPLES ===\n")
    
    # Simular dados do PDF
    darm_data = {
        'codigoReceita': '258-5',  # Formato do PDF
        'numeroGuia': '1549'
    }
    
    print(f"Dados do PDF: {darm_data}")
    
    # Aplicar a lógica atual
    codigo_receita = darm_data.get('codigoReceita') or 2585
    print(f"1. Código inicial: {codigo_receita}")
    
    # Remover hífen se existir
    if isinstance(codigo_receita, str) and '-' in codigo_receita:
        codigo_receita = codigo_receita.replace('-', '')
        print(f"2. Após remover hífen: {codigo_receita}")
    
    print(f"3. Resultado final: {codigo_receita}")
    
    # Testar com valor padrão
    print(f"\n--- Teste com valor padrão ---")
    darm_data2 = {}
    codigo_receita2 = darm_data2.get('codigoReceita') or 2585
    print(f"Valor padrão: {codigo_receita2}")

if __name__ == "__main__":
    test_cd_receita()
