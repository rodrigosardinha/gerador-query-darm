# Processador de DARMs - Versão Python

Este é um processador de DARMs (Documento de Arrecadação de Receitas Municipais) desenvolvido em Python, que extrai dados de arquivos PDF e gera scripts SQL para inserção no banco de dados.

## 🚀 Funcionalidades

- **Extração de PDFs**: Processa arquivos PDF de DARMs automaticamente
- **Geração de SQL**: Cria scripts SQL individuais e consolidados
- **Controle de Duplicatas**: Evita processamento de guias já existentes
- **Relatórios**: Gera relatórios detalhados do processamento
- **Compatibilidade Control-M**: Arquivos SQL em formato ISO 8859-1

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Estrutura do Projeto

```
gera-query-pagar-darm/
├── darms/                    # Diretório com os PDFs dos DARMs
├── inserts/                  # Diretório de saída dos arquivos SQL
├── darm_processor.py         # Script principal em Python
├── requirements.txt          # Dependências do projeto
├── README_Python.md          # Este arquivo
└── index.js                  # Versão original em JavaScript
```

## 🎯 Como Usar

1. **Coloque os PDFs dos DARMs** na pasta `darms/`

2. **Execute o processador**:
   ```bash
   python darm_processor.py
   ```

3. **Verifique os resultados** na pasta `inserts/`:
   - `INSERT_TODOS_DARMs.sql` - Script único com todos os INSERTs
   - `INSERT_DARM_PAGO_*.sql` - Scripts individuais por guia
   - `CHECK_GUIA_*.sql` - Scripts de verificação
   - `RELATORIO_PROCESSAMENTO.md` - Relatório detalhado

## 📊 Dados Extraídos

O processador extrai automaticamente os seguintes dados dos PDFs:

- **Número de Inscrição**: Identificação do contribuinte
- **Número da Guia**: Identificador único do DARM
- **Código de Receita**: Tipo de tributo
- **Valor Principal**: Valor do tributo
- **Valor Total**: Valor total a pagar
- **Data de Vencimento**: Data limite para pagamento
- **Exercício**: Ano de referência
- **Competência**: Período de competência
- **Código de Barras**: Código para pagamento

## 🔧 Configurações

### Parâmetros do Banco de Dados

Os seguintes valores são configurados automaticamente:

- **AA_EXERCICIO**: 2025 (ano atual)
- **CD_BANCO**: 70
- **NR_BDA**: 37
- **NR_COMPLEMENTO**: 0
- **NR_LOTE_NSA**: 730
- **TP_LOTE_D**: 1
- **CD_USU_INCL**: 'FARR'

### Geração de SQ_DOC

O SQ_DOC é gerado automaticamente usando a fórmula:
```
SQ_DOC = ((últimos 3 dígitos da guia * 1000) + (últimos 3 dígitos do timestamp)) % 1000000
```

## 📝 Formato dos Arquivos SQL

### Arquivo Único (INSERT_TODOS_DARMs.sql)

```sql
use silfae;

INSERT INTO FarrDarmsPagos (
    id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D,
    SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO,
    DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS,
    NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL,
    VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS,
    processado, criticaProcessamento
) VALUES 
(valores...),
(valores...);
```

### Arquivo Individual (INSERT_DARM_PAGO_*.sql)

```sql
use silfae;

INSERT INTO FarrDarmsPagos (
    -- campos...
) VALUES (
    -- valores específicos da guia
);
```

## 🔍 Verificações de Segurança

1. **Controle de Duplicatas**: Evita processar a mesma guia múltiplas vezes
2. **Verificação de Arquivos**: Não sobrescreve arquivos SQL existentes
3. **Validação de Dados**: Verifica se os dados mínimos foram extraídos
4. **Scripts de Verificação**: Gera scripts para verificar existência no banco

## 📈 Relatórios

O processador gera um relatório detalhado (`RELATORIO_PROCESSAMENTO.md`) contendo:

- Lista de guias processadas
- Estatísticas do processamento
- Arquivos gerados
- Verificações de segurança
- Próximos passos recomendados

## 🚨 Tratamento de Erros

- **PDFs corrompidos**: Log de erro e continuação do processamento
- **Dados incompletos**: Registro no log e pulo do arquivo
- **Erros de escrita**: Tratamento de exceções com mensagens claras
- **Encoding**: Uso de ISO 8859-1 para compatibilidade com Control-M

## 🔄 Diferenças da Versão JavaScript

### Vantagens da Versão Python:

1. **Melhor tratamento de PDFs**: PyPDF2 é mais robusto para extração de texto
2. **Código mais limpo**: Sintaxe mais legível e organizada
3. **Melhor tratamento de erros**: Exceções mais específicas
4. **Compatibilidade**: Funciona em Windows, Linux e macOS
5. **Dependências menores**: Menos pacotes externos necessários

### Funcionalidades Mantidas:

- ✅ Todas as funcionalidades da versão JavaScript
- ✅ Geração de arquivos SQL individuais e consolidados
- ✅ Controle de duplicatas
- ✅ Relatórios detalhados
- ✅ Compatibilidade com Control-M
- ✅ Verificações de segurança

## 🛠️ Solução de Problemas

### Erro: "PyPDF2 not found"
```bash
pip install PyPDF2==3.0.1
```

### Erro: "Permission denied"
Verifique se você tem permissão de escrita na pasta do projeto.

### PDFs não são processados
Verifique se os arquivos estão na pasta `darms/` e têm extensão `.pdf`.

### Caracteres especiais incorretos
Os arquivos SQL são gerados em ISO 8859-1 para compatibilidade com Control-M.

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique o relatório gerado (`RELATORIO_PROCESSAMENTO.md`)
2. Consulte os logs no console
3. Verifique se os PDFs estão no formato correto

## 📄 Licença

Este projeto é de uso interno para processamento de DARMs municipais.

---

**Desenvolvido em Python** - Versão compatível com a versão JavaScript original 