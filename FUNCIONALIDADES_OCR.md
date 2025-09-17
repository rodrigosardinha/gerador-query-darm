# Funcionalidades OCR - Gerador de Query DARM

## 🎯 Visão Geral

O gerador agora suporta processamento de DARMs que são imagens ou PDFs com texto em imagem usando **OCR (Optical Character Recognition)**.

## ✨ Novas Funcionalidades

### 📄 PDFs com Texto em Imagem
- **Detecção automática**: O sistema identifica quando um PDF não tem texto extraível
- **Conversão automática**: PDFs são convertidos para imagens de alta resolução (300 DPI)
- **OCR inteligente**: Processamento página por página com Tesseract
- **Pré-processamento**: Melhoria automática da qualidade da imagem

### 🖼️ Arquivos de Imagem
- **Formatos suportados**: PNG, JPG, JPEG, BMP, TIFF, TIF
- **OCR direto**: Processamento sem conversão prévia
- **Qualidade otimizada**: Pré-processamento para melhor reconhecimento

### 🔧 Recursos Técnicos
- **Múltiplos idiomas**: Suporte ao português brasileiro
- **Pré-processamento avançado**:
  - Conversão para escala de cinza
  - Threshold adaptativo
  - Remoção de ruído
  - Suavização de imagem
- **Detecção automática**: Identifica o tipo de arquivo e aplica o método adequado

## 🚀 Como Usar

### 1. Instalação das Dependências

Execute o script de instalação:
```bash
python install_ocr.py
```

### 2. Instalação do Tesseract OCR

#### Windows:
1. Baixe de: https://github.com/UB-Mannheim/tesseract/wiki
2. Instale e adicione ao PATH do sistema

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

#### macOS:
```bash
brew install tesseract tesseract-lang
```

### 3. Uso Normal

O gerador funciona exatamente como antes, mas agora suporta:
- **PDFs normais** (com texto)
- **PDFs com imagens** (OCR automático)
- **Arquivos de imagem** (PNG, JPG, etc.)

Basta colocar os arquivos na pasta `darms/` e executar:
```bash
python darm_processor.py
```

## 📋 Formatos Suportados

### PDFs:
- ✅ PDFs com texto normal
- ✅ PDFs com texto em imagem (OCR)
- ✅ PDFs escaneados
- ✅ PDFs de múltiplas páginas

### Imagens:
- ✅ PNG
- ✅ JPG/JPEG
- ✅ BMP
- ✅ TIFF/TIF

## 🔍 Processo de Detecção

1. **Análise do arquivo**: Verifica se é PDF ou imagem
2. **PDF com texto**: Extrai texto normalmente
3. **PDF sem texto**: Detecta automaticamente e usa OCR
4. **Imagem**: Usa OCR diretamente
5. **Pré-processamento**: Melhora qualidade da imagem
6. **Extração**: Reconhece texto com Tesseract
7. **Processamento**: Extrai dados do DARM normalmente

## ⚙️ Configurações Técnicas

### OCR Settings:
- **DPI**: 300 (alta resolução)
- **Idioma**: Português brasileiro (`por`)
- **Pré-processamento**: Automático
- **Threshold**: Adaptativo Gaussiano

### Pré-processamento:
- Conversão para escala de cinza
- Threshold adaptativo (11x11, offset 2)
- Morfologia para remoção de ruído
- Blur Gaussiano suave

## 🎯 Exemplos de Uso

### PDF Normal (sem OCR):
```
📄 Processando PDF: darm_normal.pdf
✅ Texto extraído normalmente do PDF: darm_normal.pdf
```

### PDF com Imagem (com OCR):
```
📄 Processando PDF: darm_imagem.pdf
⚠️  PDF sem texto extraível detectado: darm_imagem.pdf
🔄 Tentando extrair texto usando OCR...
🔍 Convertendo PDF para imagens: darm_imagem.pdf
📄 Processando página 1/1 com OCR...
✅ Página 1 processada com OCR
✅ Texto extraído com OCR: 1250 caracteres
```

### Arquivo de Imagem:
```
🖼️ Processando IMAGE: darm.png
🔍 Processando imagem com OCR: darm.png
✅ Texto extraído da imagem: 980 caracteres
```

## 🔧 Solução de Problemas

### OCR não disponível:
```
⚠️  Aviso: Algumas dependências de OCR não estão instaladas
📦 Para instalar: pip install pytesseract Pillow pdf2image opencv-python
```

### Tesseract não encontrado:
```
❌ Tesseract não encontrado no sistema
📋 Para instalar o Tesseract:
Windows: Baixe de https://github.com/UB-Mannheim/tesseract/wiki
Linux: sudo apt-get install tesseract-ocr tesseract-ocr-por
macOS: brew install tesseract tesseract-lang
```

### Imagem não carregada:
```
❌ Não foi possível carregar a imagem: arquivo.jpg
```
**Solução**: Verifique se o arquivo está corrompido ou em formato não suportado.

### Nenhum texto encontrado:
```
❌ Nenhum texto encontrado com OCR
```
**Soluções**:
- Verifique se a imagem tem boa qualidade
- Certifique-se que o texto está legível
- Tente melhorar a resolução da imagem

## 📊 Compatibilidade

### Sistemas Operacionais:
- ✅ Windows 10/11
- ✅ Linux (Ubuntu/Debian)
- ✅ macOS

### Python:
- ✅ Python 3.7+
- ✅ pip package manager

### Dependências:
- ✅ PyPDF2 (PDFs normais)
- ✅ pytesseract (OCR)
- ✅ Pillow (processamento de imagem)
- ✅ pdf2image (conversão PDF)
- ✅ opencv-python (pré-processamento)

## 🎉 Vantagens

1. **Universal**: Processa qualquer tipo de DARM
2. **Automático**: Detecta e aplica o método correto
3. **Inteligente**: Pré-processamento para melhor qualidade
4. **Compatível**: Mantém compatibilidade com Control-M
5. **Robusto**: Tratamento de erros e fallbacks
6. **Flexível**: Suporta múltiplos formatos

## 🔮 Próximas Melhorias

- [ ] Suporte a mais idiomas
- [ ] Configuração de qualidade OCR
- [ ] Processamento em lote otimizado
- [ ] Interface gráfica
- [ ] Relatórios de qualidade OCR
- [ ] Validação de dados extraídos

---

**Desenvolvido com ❤️ para facilitar o processamento de DARMs**
