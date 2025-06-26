# 🚀 Guia do Executável - Processador de DARMs

## 📦 O que é o Executável?

O executável é uma versão standalone do Processador de DARMs que **não requer instalação de Python**. É ideal para usuários finais que não são desenvolvedores.

## 🎯 Vantagens do Executável

- ✅ **Não requer Python instalado**
- ✅ **Funciona em qualquer Windows 10/11**
- ✅ **Instalação zero - apenas executar**
- ✅ **Portátil - pode ser copiado para qualquer lugar**
- ✅ **Tamanho compacto (~12MB)**

## 📁 Estrutura do Pacote

```
darm-processor-package/
├── darm-processor.exe    # Executável principal
├── darms/                # Pasta para PDFs (vazia)
├── inserts/              # Pasta para SQLs (vazia)
└── README.txt            # Instruções de uso
```

## 🚀 Como Usar

### Passo 1: Preparar os PDFs
1. Coloque os arquivos PDF dos DARMs na pasta `darms/`
2. Os PDFs devem estar no formato padrão de DARMs

### Passo 2: Executar o Processador
1. Dê duplo clique em `darm-processor.exe`
2. Ou execute via linha de comando: `darm-processor.exe`

### Passo 3: Verificar Resultados
1. Os arquivos SQL serão gerados na pasta `inserts/`
2. Verifique os arquivos gerados:
   - `INSERT_TODOS_DARMs.sql` - Script único
   - `INSERT_DARM_PAGO_*.sql` - Scripts individuais
   - `CHECK_GUIA_*.sql` - Scripts de verificação
   - `RELATORIO_PROCESSAMENTO.md` - Relatório

## 🔧 Solução de Problemas

### ❌ "Não foi possível encontrar as pastas darms/inserts"

**Solução:** O executável cria as pastas automaticamente. Se não funcionar:

1. Crie manualmente as pastas `darms` e `inserts` ao lado do executável
2. Execute novamente o `darm-processor.exe`

### ❌ "Erro ao processar PDF"

**Possíveis causas:**
- PDF corrompido ou protegido
- Formato não suportado
- PDF não é um DARM válido

**Solução:**
- Verifique se o PDF é um DARM válido
- Tente com outros PDFs
- Verifique o relatório de processamento

### ❌ "Executável não abre"

**Possíveis causas:**
- Antivírus bloqueando
- Windows Defender SmartScreen
- Permissões insuficientes

**Solução:**
1. Clique com botão direito → "Executar como administrador"
2. Adicione exceção no antivírus
3. Clique em "Mais informações" → "Executar mesmo assim" (Windows Defender)

## 📊 Comparação: Script vs Executável

| Aspecto | Script Python | Executável |
|---------|---------------|------------|
| **Instalação** | Requer Python + pip | Zero instalação |
| **Tamanho** | ~1MB | ~12MB |
| **Dependências** | PyPDF2, pathlib2 | Nenhuma |
| **Portabilidade** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Facilidade** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Debug** | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 🎯 Quando Usar o Executável

### ✅ **Use o Executável quando:**
- Distribuindo para usuários finais
- Usuários não são desenvolvedores
- Precisa de portabilidade máxima
- Ambiente corporativo restritivo

### ⚠️ **Use o Script quando:**
- Desenvolvimento e testes
- Usuários são técnicos
- Precisa de debug detalhado
- Ambiente controlado com Python

## 🔄 Atualizações

### Para Usuários:
1. Baixe a nova versão do executável
2. Substitua o arquivo antigo
3. Mantenha suas pastas `darms` e `inserts`

### Para Desenvolvedores:
1. Atualize o código fonte
2. Execute: `python build_executable.py`
3. Distribua o novo `darm-processor-package.zip`

## 📞 Suporte

### Para Problemas com Executável:
- 📧 Email: rodrigo.sardinha@example.com
- 🐛 Issues: https://github.com/rodrigosardinha/gerador-query-darm/issues
- 📚 Documentação: README.md

### Informações Técnicas:
- **Sistema:** Windows 10/11 (64-bit)
- **Tamanho:** ~12MB
- **Dependências:** Nenhuma
- **Compatibilidade:** Windows 10, 11

## 🚀 Próximas Versões

### Planejado:
- [ ] Interface gráfica (GUI)
- [ ] Suporte a Linux/macOS
- [ ] Modo silencioso (sem console)
- [ ] Configuração via arquivo INI
- [ ] Logs detalhados

### Melhorias Técnicas:
- [ ] Compressão UPX para reduzir tamanho
- [ ] Assinatura digital
- [ ] Auto-update
- [ ] Instalador MSI

---

## ✅ Checklist de Uso

- [ ] ✅ Baixou o `darm-processor-package.zip`
- [ ] ✅ Extraiu em uma pasta
- [ ] ✅ Colocou PDFs na pasta `darms/`
- [ ] ✅ Executou `darm-processor.exe`
- [ ] ✅ Verificou arquivos SQL em `inserts/`
- [ ] ✅ Testou com pelo menos um PDF

**🎉 Pronto para processar DARMs!** 