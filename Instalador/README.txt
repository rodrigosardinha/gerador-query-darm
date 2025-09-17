# 🏛️ Processador de DARMs - Instalador

## 📋 Como Usar

### 1. Executar o Processador
- Execute o arquivo `Processador-DARM.exe`
- O programa irá processar automaticamente todos os PDFs na pasta `darms/`

### 2. Preparar os DARMs
- Coloque os arquivos PDF dos DARMs na pasta `darms/`
- Formatos suportados: PDF, PNG, JPG, JPEG, BMP, TIFF, TIF

### 3. Verificar Resultados
- Os arquivos SQL serão gerados na pasta `inserts/`
- Verifique o relatório `RELATORIO_PROCESSAMENTO.md`

## 📁 Estrutura de Pastas

```
Processador-DARM/
├── Processador-DARM.exe    # Executável principal
├── darms/                  # Coloque seus PDFs aqui
│   └── (seus arquivos PDF)
├── inserts/                # Arquivos SQL gerados
│   ├── INSERT_TODOS_DARMs.sql
│   ├── INSERT_DARM_PAGO_*.sql
│   ├── CHECK_GUIA_*.sql
│   └── RELATORIO_PROCESSAMENTO.md
└── README.txt              # Este arquivo
```

## 🔧 Funcionalidades

- ✅ **Extração automática** de dados de PDFs
- ✅ **Suporte a OCR** para PDFs com imagens
- ✅ **Geração de SQL** compatível com Control-M
- ✅ **Correção automática** de inscrições municipais
- ✅ **Relatórios detalhados** do processamento
- ✅ **Controle de duplicatas** automático

## 🚨 Solução de Problemas

### Erro: "Nenhum arquivo encontrado"
- Verifique se os PDFs estão na pasta `darms/`
- Certifique-se que os arquivos têm extensão `.pdf`

### Erro: "Dados insuficientes"
- Verifique se o PDF contém dados válidos de DARM
- Tente com um PDF diferente

### Problemas de permissão
- Execute como administrador se necessário
- Verifique se tem permissão de escrita na pasta

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique este README primeiro
- Consulte o relatório de processamento
- Entre em contato com o suporte técnico

---
**Versão**: 1.0.0
**Data**: 10/09/2025
**Compatibilidade**: Windows 10/11
