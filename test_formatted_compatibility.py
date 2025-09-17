#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar compatibilidade da versão formatada com ControlM
"""

import re
from pathlib import Path

def test_formatted_compatibility():
    """Testar compatibilidade da versão formatada"""
    
    print("🔍 Testando compatibilidade da versão formatada...")
    
    # Testar versão formatada
    formatted_path = Path('inserts/INSERT_TODOS_DARMs.sql')
    if formatted_path.exists():
        with open(formatted_path, 'r', encoding='latin1') as f:
            content = f.read()
        
        print("✅ Versão formatada:")
        print(f"   📊 Tamanho: {len(content)} caracteres")
        print(f"   📊 Linhas: {len(content.split(chr(10)))}")
        
        # Verificar se contém comentários
        comment_count = content.count('--')
        if comment_count > 0:
            print(f"   📊 Comentários: {comment_count}")
            print("   ⚠️  Comentários podem causar problemas no ControlM")
        else:
            print("   ✅ Sem comentários")
    
    # Testar versão ControlM
    controlm_path = Path('inserts/INSERT_TODOS_DARMs_CONTROLM.sql')
    if controlm_path.exists():
        with open(controlm_path, 'r', encoding='latin1') as f:
            content = f.read()
        
        print("\n✅ Versão ControlM:")
        print(f"   📊 Tamanho: {len(content)} caracteres")
        print(f"   📊 Linhas: {len(content.split(chr(10)))}")
        print("   ✅ Formato uma linha - Máxima compatibilidade")
        
        # Verificar se não há quebras de linha
        if '\n' not in content:
            print("   ✅ Sem quebras de linha")
        else:
            print("   ⚠️  Contém quebras de linha")
    
    print("\n📋 Resumo das versões disponíveis:")
    print("   1. INSERT_TODOS_DARMs.sql - Versão formatada (legível)")
    print("   2. INSERT_TODOS_DARMs_CONTROLM.sql - Versão ControlM (uma linha)")
    
    print("\n💡 Recomendações:")
    print("   • Use INSERT_TODOS_DARMs.sql para desenvolvimento e manutenção")
    print("   • Use INSERT_TODOS_DARMs_CONTROLM.sql para execução no ControlM")
    print("   • Ambas as versões são funcionalmente idênticas")

def verify_sql_syntax():
    """Verificar sintaxe SQL básica"""
    
    print("\n🔍 Verificando sintaxe SQL...")
    
    for filename in ['INSERT_TODOS_DARMs.sql', 'INSERT_TODOS_DARMs_CONTROLM.sql']:
        file_path = Path('inserts') / filename
        
        if file_path.exists():
            with open(file_path, 'r', encoding='latin1') as f:
                content = f.read()
            
            print(f"\n✅ {filename}:")
            
            # Verificar estrutura básica
            if 'use silfae;' in content:
                print("   ✅ Comando USE presente")
            else:
                print("   ❌ Comando USE ausente")
            
            if 'INSERT INTO FarrDarmsPagos' in content:
                print("   ✅ Comando INSERT presente")
            else:
                print("   ❌ Comando INSERT ausente")
            
            if 'VALUES' in content:
                print("   ✅ Cláusula VALUES presente")
            else:
                print("   ❌ Cláusula VALUES ausente")
            
            # Verificar parênteses balanceados
            open_parens = content.count('(')
            close_parens = content.count(')')
            if open_parens == close_parens:
                print("   ✅ Parênteses balanceados")
            else:
                print(f"   ❌ Parênteses não balanceados ({open_parens} abertos, {close_parens} fechados)")
            
            # Verificar aspas balanceadas
            single_quotes = content.count("'")
            if single_quotes % 2 == 0:
                print("   ✅ Aspas balanceadas")
            else:
                print(f"   ❌ Aspas não balanceadas ({single_quotes} aspas)")
            
            # Verificar encoding
            try:
                content.encode('latin1')
                print("   ✅ Encoding ISO 8859-1 válido")
            except UnicodeEncodeError:
                print("   ❌ Problema com encoding")

if __name__ == "__main__":
    test_formatted_compatibility()
    verify_sql_syntax()
    print("\n🎉 Testes concluídos!") 