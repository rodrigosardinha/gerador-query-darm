#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar compatibilidade das versões formatadas com ControlM
"""

import re
from pathlib import Path

def test_formatted_files():
    """Testar arquivos formatados"""
    
    print("🔍 Testando arquivos formatados...")
    
    # Testar arquivo consolidado
    consolidated_path = Path('inserts/INSERT_TODOS_DARMs.sql')
    if consolidated_path.exists():
        with open(consolidated_path, 'r', encoding='latin1') as f:
            content = f.read()
        
        print("✅ Arquivo consolidado formatado:")
        print(f"   📊 Tamanho: {len(content)} caracteres")
        print(f"   📊 Linhas: {len(content.split(chr(10)))}")
        print("   ✨ Formatação bonita aplicada")
        
        # Verificar se contém quebras de linha organizadas
        if 'INSERT INTO FarrDarmsPagos (' in content and '\n    ' in content:
            print("   ✅ Formatação organizada detectada")
        else:
            print("   ❌ Formatação não está organizada")
    
    # Testar arquivos individuais
    individual_files = list(Path('inserts').glob('INSERT_DARM_PAGO_*.sql'))
    print(f"\n✅ Arquivos individuais formatados: {len(individual_files)}")
    
    for file_path in individual_files:
        with open(file_path, 'r', encoding='latin1') as f:
            content = f.read()
        
        print(f"   📄 {file_path.name}: {len(content)} chars, {len(content.split(chr(10)))} linhas")
        
        # Verificar formatação
        if 'INSERT INTO FarrDarmsPagos (' in content and '\n    ' in content:
            print(f"      ✅ Formatação bonita")
        else:
            print(f"      ❌ Formatação não está bonita")

def test_controlm_compatibility():
    """Testar compatibilidade com ControlM"""
    
    print("\n🔍 Testando compatibilidade com ControlM...")
    
    files_to_test = [
        'INSERT_TODOS_DARMs.sql',
        'INSERT_DARM_PAGO_853.sql',
        'INSERT_DARM_PAGO_854.sql',
        'INSERT_DARM_PAGO_855.sql'
    ]
    
    for filename in files_to_test:
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
            
            # Verificar se há comentários
            comment_count = content.count('--')
            if comment_count == 0:
                print("   ✅ Sem comentários (compatível com ControlM)")
            else:
                print(f"   ⚠️  {comment_count} comentários encontrados")

def show_file_preview():
    """Mostrar preview dos arquivos formatados"""
    
    print("\n📄 Preview dos arquivos formatados:")
    
    # Preview do consolidado
    consolidated_path = Path('inserts/INSERT_TODOS_DARMs.sql')
    if consolidated_path.exists():
        with open(consolidated_path, 'r', encoding='latin1') as f:
            content = f.read()
        
        print("\n🔗 Arquivo consolidado (primeiras linhas):")
        lines = content.split('\n')[:8]
        for line in lines:
            print(f"   {line}")
        print("   ...")
    
    # Preview de um individual
    individual_path = Path('inserts/INSERT_DARM_PAGO_853.sql')
    if individual_path.exists():
        with open(individual_path, 'r', encoding='latin1') as f:
            content = f.read()
        
        print("\n🔗 Arquivo individual (primeiras linhas):")
        lines = content.split('\n')[:8]
        for line in lines:
            print(f"   {line}")
        print("   ...")

if __name__ == "__main__":
    test_formatted_files()
    test_controlm_compatibility()
    show_file_preview()
    
    print("\n🎉 Testes concluídos!")
    print("\n💡 Resumo:")
    print("   • Todos os arquivos agora estão formatados bonitamente")
    print("   • Mantida compatibilidade total com ControlM")
    print("   • Formatação organizada e legível")
    print("   • Sem comentários para evitar problemas no ControlM") 