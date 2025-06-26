#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Processador de DARMs em Python

Este script testa as funcionalidades principais do DarmProcessor
para garantir que tudo está funcionando corretamente.
"""

import asyncio
import os
import tempfile
import shutil
from pathlib import Path
from darm_processor import DarmProcessor
from config import validate_config, get_message

class DarmProcessorTester:
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        
    async def run_all_tests(self):
        """Executar todos os testes"""
        print("🧪 Iniciando Testes do Processador de DARMs")
        print("=" * 50)
        
        try:
            # Teste 1: Validação de configurações
            await self.test_config_validation()
            
            # Teste 2: Criação de diretórios
            await self.test_directory_creation()
            
            # Teste 3: Inicialização do processador
            await self.test_processor_initialization()
            
            # Teste 4: Extração de dados
            await self.test_data_extraction()
            
            # Teste 5: Geração de SQL
            await self.test_sql_generation()
            
            # Teste 6: Processamento completo
            await self.test_complete_processing()
            
            # Mostrar resultados
            self.show_test_results()
            
        except Exception as error:
            print(f"❌ Erro durante os testes: {error}")
        finally:
            # Limpar arquivos temporários
            self.cleanup()
    
    async def test_config_validation(self):
        """Teste de validação de configurações"""
        print("\n🔧 Teste 1: Validação de Configurações")
        
        try:
            errors = validate_config()
            if not errors:
                self.test_results.append(("Validação de Configurações", "✅ PASSOU"))
                print("   ✅ Configurações válidas")
            else:
                self.test_results.append(("Validação de Configurações", "❌ FALHOU"))
                print(f"   ❌ Erros encontrados: {errors}")
        except Exception as error:
            self.test_results.append(("Validação de Configurações", "❌ ERRO"))
            print(f"   ❌ Erro: {error}")
    
    async def test_directory_creation(self):
        """Teste de criação de diretórios"""
        print("\n📁 Teste 2: Criação de Diretórios")
        
        try:
            # Criar diretório temporário para testes
            self.temp_dir = tempfile.mkdtemp()
            test_darms_dir = Path(self.temp_dir) / "darms"
            test_output_dir = Path(self.temp_dir) / "inserts"
            
            # Criar diretórios
            test_darms_dir.mkdir(exist_ok=True)
            test_output_dir.mkdir(exist_ok=True)
            
            # Verificar se foram criados
            if test_darms_dir.exists() and test_output_dir.exists():
                self.test_results.append(("Criação de Diretórios", "✅ PASSOU"))
                print("   ✅ Diretórios criados com sucesso")
            else:
                self.test_results.append(("Criação de Diretórios", "❌ FALHOU"))
                print("   ❌ Falha na criação dos diretórios")
                
        except Exception as error:
            self.test_results.append(("Criação de Diretórios", "❌ ERRO"))
            print(f"   ❌ Erro: {error}")
    
    async def test_processor_initialization(self):
        """Teste de inicialização do processador"""
        print("\n🚀 Teste 3: Inicialização do Processador")
        
        try:
            processor = DarmProcessor()
            
            # Modificar diretórios para usar os temporários
            if self.temp_dir:
                processor.darms_dir = Path(self.temp_dir) / "darms"
                processor.output_dir = Path(self.temp_dir) / "inserts"
            
            # Inicializar
            await processor.init()
            
            self.test_results.append(("Inicialização do Processador", "✅ PASSOU"))
            print("   ✅ Processador inicializado com sucesso")
            
        except Exception as error:
            self.test_results.append(("Inicialização do Processador", "❌ ERRO"))
            print(f"   ❌ Erro: {error}")
    
    async def test_data_extraction(self):
        """Teste de extração de dados"""
        print("\n📊 Teste 4: Extração de Dados")
        
        try:
            processor = DarmProcessor()
            
            # Texto de exemplo (simulando PDF)
            sample_text = """
            DARM - Documento de Arrecadação de Receitas Municipais
            
            02. INSCRIÇÃO MUNICIPAL 123456
            01. RECEITA 262-3
            03. DATA VENCIMENTO 15/12/2024
            04. ANO DE REFERÊNCIA 2024
            05. GUIA NØ
            123456789
            06. VALOR DO TRIBUTO R$ 1.234,56
            09. VALOR TOTAL R$ 1.234,56
            
            Código de Barras: 123456789012345678901234567890123456789012345678
            """
            
            # Extrair dados
            data = processor.extract_darm_data(sample_text)
            
            if data and data.get('inscricao') and data.get('valorPrincipal'):
                self.test_results.append(("Extração de Dados", "✅ PASSOU"))
                print("   ✅ Dados extraídos com sucesso")
                print(f"      - Inscrição: {data.get('inscricao')}")
                print(f"      - Valor: {data.get('valorPrincipal')}")
                print(f"      - Guia: {data.get('numeroGuia')}")
            else:
                self.test_results.append(("Extração de Dados", "❌ FALHOU"))
                print("   ❌ Falha na extração de dados")
                
        except Exception as error:
            self.test_results.append(("Extração de Dados", "❌ ERRO"))
            print(f"   ❌ Erro: {error}")
    
    async def test_sql_generation(self):
        """Teste de geração de SQL"""
        print("\n💾 Teste 5: Geração de SQL")
        
        try:
            processor = DarmProcessor()
            
            # Dados de exemplo
            sample_data = {
                'inscricao': '123456',
                'numeroGuia': '123456789',
                'valorPrincipal': '1234.56',
                'valorTotal': '1234.56',
                'dataVencimento': '15/12/2024',
                'exercicio': '2024',
                'codigoReceita': '2623',
                'codigoBarras': '123456789012345678901234567890123456789012345678'
            }
            
            # Gerar SQL
            sql = processor.generate_sql_insert(sample_data)
            
            if sql and 'INSERT INTO FarrDarmsPagos' in sql:
                self.test_results.append(("Geração de SQL", "✅ PASSOU"))
                print("   ✅ SQL gerado com sucesso")
                print(f"      - Tamanho: {len(sql)} caracteres")
            else:
                self.test_results.append(("Geração de SQL", "❌ FALHOU"))
                print("   ❌ Falha na geração do SQL")
                
        except Exception as error:
            self.test_results.append(("Geração de SQL", "❌ ERRO"))
            print(f"   ❌ Erro: {error}")
    
    async def test_complete_processing(self):
        """Teste de processamento completo"""
        print("\n🔄 Teste 6: Processamento Completo")
        
        try:
            processor = DarmProcessor()
            
            # Modificar diretórios para usar os temporários
            if self.temp_dir:
                processor.darms_dir = Path(self.temp_dir) / "darms"
                processor.output_dir = Path(self.temp_dir) / "inserts"
            
            # Inicializar
            await processor.init()
            
            # Simular processamento (sem PDFs reais)
            processor.guias_processadas = ['123456', '789012']
            processor.all_sql_inserts = [
                "INSERT INTO FarrDarmsPagos (...) VALUES (...);",
                "INSERT INTO FarrDarmsPagos (...) VALUES (...);"
            ]
            
            # Gerar arquivo único
            await processor.generate_single_sql_file()
            
            # Gerar relatório
            await processor.generate_report()
            
            # Verificar se os arquivos foram criados
            output_dir = processor.output_dir
            single_file = output_dir / "INSERT_TODOS_DARMs.sql"
            report_file = output_dir / "RELATORIO_PROCESSAMENTO.md"
            
            if single_file.exists() and report_file.exists():
                self.test_results.append(("Processamento Completo", "✅ PASSOU"))
                print("   ✅ Processamento completo realizado com sucesso")
                print(f"      - Arquivo SQL: {single_file.name}")
                print(f"      - Relatório: {report_file.name}")
            else:
                self.test_results.append(("Processamento Completo", "❌ FALHOU"))
                print("   ❌ Falha no processamento completo")
                
        except Exception as error:
            self.test_results.append(("Processamento Completo", "❌ ERRO"))
            print(f"   ❌ Erro: {error}")
    
    def show_test_results(self):
        """Mostrar resultados dos testes"""
        print("\n📋 Resultados dos Testes")
        print("=" * 30)
        
        passed = 0
        failed = 0
        errors = 0
        
        for test_name, result in self.test_results:
            print(f"{result} {test_name}")
            if "✅ PASSOU" in result:
                passed += 1
            elif "❌ FALHOU" in result:
                failed += 1
            elif "❌ ERRO" in result:
                errors += 1
        
        print(f"\n📊 Resumo:")
        print(f"   ✅ Passou: {passed}")
        print(f"   ❌ Falhou: {failed}")
        print(f"   💥 Erro: {errors}")
        print(f"   📈 Total: {len(self.test_results)}")
        
        if failed == 0 and errors == 0:
            print("\n🎉 Todos os testes passaram!")
        else:
            print(f"\n⚠️  {failed + errors} teste(s) com problema(s)")
    
    def cleanup(self):
        """Limpar arquivos temporários"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"\n🧹 Arquivos temporários removidos: {self.temp_dir}")
            except Exception as error:
                print(f"\n⚠️  Erro ao remover arquivos temporários: {error}")

def test_messages():
    """Teste das mensagens do sistema"""
    print("\n💬 Teste de Mensagens")
    print("=" * 20)
    
    try:
        # Teste mensagem em português
        msg_pt = get_message('processing_start', 'pt_BR')
        print(f"   Português: {msg_pt}")
        
        # Teste mensagem em inglês
        msg_en = get_message('processing_start', 'en')
        print(f"   Inglês: {msg_en}")
        
        # Teste mensagem padrão
        msg_default = get_message('processing_start')
        print(f"   Padrão: {msg_default}")
        
        print("   ✅ Mensagens funcionando corretamente")
        
    except Exception as error:
        print(f"   ❌ Erro nas mensagens: {error}")

async def main():
    """Função principal dos testes"""
    print("🧪 Teste do Processador de DARMs - Versão Python")
    print("=" * 60)
    
    # Teste das mensagens
    test_messages()
    
    # Executar testes do processador
    tester = DarmProcessorTester()
    await tester.run_all_tests()
    
    print("\n📝 Próximos Passos:")
    print("1. Se todos os testes passaram, o processador está funcionando")
    print("2. Coloque arquivos PDF na pasta 'darms/'")
    print("3. Execute: python darm_processor.py")
    print("4. Verifique os resultados na pasta 'inserts/'")

if __name__ == "__main__":
    # Executar testes
    asyncio.run(main()) 