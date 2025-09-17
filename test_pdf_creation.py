#!/usr/bin/env python3
"""
Script para criar um PDF de teste simples com dados de DARM
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_test_pdf():
    """Criar um PDF de teste com dados de DARM"""
    
    # Criar o PDF
    filename = "darms/DARM_TESTE_SIMPLES.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Configurar fonte
    c.setFont("Helvetica", 12)
    
    # Título
    c.drawString(50, height - 50, "DARM - Documento de Arrecadação de Receitas Municipais")
    c.setFont("Helvetica", 10)
    
    # Dados do DARM
    y_position = height - 100
    line_height = 20
    
    data = [
        "Inscrição Municipal: 123456789",
        "Código de Barras: 021234560126230315122024042024051234567890612345",
        "Código de Receita: 26-30",
        "Valor Principal: R$ 1.234,56",
        "Valor Total: R$ 1.234,56",
        "Data de Vencimento: 15/12/2024",
        "Exercício: 2024",
        "Número da Guia: 123456789"
    ]
    
    for line in data:
        c.drawString(50, y_position, line)
        y_position -= line_height
    
    c.save()
    print(f"✅ PDF de teste criado: {filename}")
    return filename

if __name__ == "__main__":
    # Garantir que a pasta darms existe
    os.makedirs("darms", exist_ok=True)
    
    # Criar PDF de teste
    pdf_file = create_test_pdf()
    print(f"📄 PDF criado com sucesso: {pdf_file}")
    print("🚀 Agora você pode testar o processador com este PDF!")
