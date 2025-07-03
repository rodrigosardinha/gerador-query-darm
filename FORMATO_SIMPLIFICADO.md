# Formato Simplificado para Control-M

## 🎯 Objetivo

Adaptar todos os scripts SQL gerados para o formato simplificado (uma linha) que é compatível com o Control-M, evitando o erro "Query was empty".

## ✅ Problema Resolvido

**Erro anterior no Control-M:**
```
Job failure message:
(conn=2137084) Query was empty
```

**Causa:** Quebras de linha e formatação complexa nos scripts SQL que o Control-M não conseguia interpretar corretamente.

## 🔧 Mudanças Implementadas

### 1. **Scripts Individuais** (`INSERT_DARM_PAGO_*.sql`)

**Antes:**
```sql
use silfae;

INSERT INTO FarrDarmsPagos (
    id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D,
    SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO,
    DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS,
    NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL,
    VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS,
    processado, criticaProcessamento
) VALUES (
    NULL, 2025, 70, 37, 0, 730, 1,
    (((201 % 1000) * 1000) + (UNIX_TIMESTAMP() % 1000)) % 1000000, 2623, NULL, 'FARR', NULL,
    NOW(), '2025-07-17 00:00:00', NOW(),
    '03015483', 201, 2025, '012623020301548303170720250420250500002010617627',
    NULL, '13', NULL, 176.27, 176.27, 176.27,
    0.00, 0.00, NULL, NULL, NULL, 0.00,
    0, NULL
);
```

**Depois:**
```sql
use silfae;
INSERT INTO FarrDarmsPagos (id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS, processado, criticaProcessamento) VALUES (NULL, 2025, 70, 37, 0, 730, 1, (((201 % 1000) * 1000) + (UNIX_TIMESTAMP() % 1000)) % 1000000, 2623, NULL, 'FARR', NULL, NOW(), '2025-07-17 00:00:00', NOW(), '03015483', 201, 2025, '012623020301548303170720250420250500002010617627', NULL, '13', NULL, 176.27, 176.27, 176.27, 0.00, 0.00, NULL, NULL, NULL, 0.00, 0, NULL);
```

### 2. **Script Consolidado** (`INSERT_TODOS_DARMs.sql`)

**Antes:**
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
    (
        NULL, 2025, 70, 37, 0, 730, 1,
        201437, 2623, NULL, 'FARR', NULL,
        NOW(), '2025-07-17 00:00:00', NOW(),
        '03015483', 201, 2025, '012623020301548303170720250420250500002010617627',
        NULL, '13', NULL, 176.27, 176.27, 176.27,
        0.00, 0.00, NULL, NULL, NULL, 0.00,
        0, NULL
    ),
    (
        NULL, 2025, 70, 37, 0, 730, 1,
        202438, 2623, NULL, 'FARR', NULL,
        NOW(), '2025-07-17 00:00:00', NOW(),
        '03015483', 201, 2025, '012623020301548303170720250420250500002010617627',
        NULL, '13', NULL, 176.27, 176.27, 176.27,
        0.00, 0.00, NULL, NULL, NULL, 0.00,
        0, NULL
    );
```

**Depois:**
```sql
use silfae;
INSERT INTO FarrDarmsPagos (id, AA_EXERCICIO, CD_BANCO, NR_BDA, NR_COMPLEMENTO, NR_LOTE_NSA, TP_LOTE_D, SQ_DOC, CD_RECEITA, CD_USU_ALT, CD_USU_INCL, DT_ALT, DT_INCL, DT_VENCTO, DT_PAGTO, NR_INSCRICAO, NR_GUIA, NR_COMPETENCIA, NR_CODIGO_BARRAS, NR_LOTE_IPTU, ST_DOC_D, TP_IMPOSTO, VL_PAGO, VL_RECEITA, VL_PRINCIPAL, VL_MORA, VL_MULTA, VL_MULTAF_TCDL, VL_MULTAP_TSD, VL_INSU_TIP, VL_JUROS, processado, criticaProcessamento) VALUES (NULL, 2025, 70, 37, 0, 730, 1, 201437, 2623, NULL, 'FARR', NULL, NOW(), '2025-07-17 00:00:00', NOW(), '03015483', 201, 2025, '012623020301548303170720250420250500002010617627', NULL, '13', NULL, 176.27, 176.27, 176.27, 0.00, 0.00, NULL, NULL, NULL, 0.00, 0, NULL), (NULL, 2025, 70, 37, 0, 730, 1, 202438, 2623, NULL, 'FARR', NULL, NOW(), '2025-07-17 00:00:00', NOW(), '03015483', 201, 2025, '012623020301548303170720250420250500002010617627', NULL, '13', NULL, 176.27, 176.27, 176.27, 0.00, 0.00, NULL, NULL, NULL, 0.00, 0, NULL);
```

### 3. **Scripts de Verificação** (`CHECK_GUIA_*.sql`)

**Antes:**
```sql
use silfae;

SELECT COUNT(*) as total FROM FarrDarmsPagos 
WHERE NR_GUIA = 201 
AND AA_EXERCICIO = 2025
AND CD_BANCO = 70
AND NR_BDA = 37
AND NR_COMPLEMENTO = 0
AND NR_LOTE_NSA = 730
AND TP_LOTE_D = 1;
```

**Depois:**
```sql
use silfae;
SELECT COUNT(*) as total FROM FarrDarmsPagos WHERE NR_GUIA = 201 AND AA_EXERCICIO = 2025 AND CD_BANCO = 70 AND NR_BDA = 37 AND NR_COMPLEMENTO = 0 AND NR_LOTE_NSA = 730 AND TP_LOTE_D = 1;
```

## 📝 Métodos Modificados

### 1. `generate_sql_insert()`
- **Arquivo:** `darm_processor.py`
- **Linha:** 464-497
- **Mudança:** Formato de uma linha para INSERT

### 2. `generate_single_sql_file()`
- **Arquivo:** `darm_processor.py`
- **Linha:** 82-162
- **Mudança:** Formato simplificado para arquivo consolidado

### 3. `check_guia_exists()`
- **Arquivo:** `darm_processor.py`
- **Linha:** 52-81
- **Mudança:** Formato simplificado para scripts de verificação

## ✅ Vantagens do Formato Simplificado

1. **Compatibilidade Total com Control-M**
   - Elimina o erro "Query was empty"
   - Formato reconhecido pelo sistema

2. **Performance Melhorada**
   - Menos processamento de parsing
   - Execução mais rápida

3. **Manutenibilidade**
   - Código mais simples
   - Menos propenso a erros de formatação

4. **Padronização**
   - Todos os scripts seguem o mesmo padrão
   - Consistência entre arquivos individuais e consolidado

## 🧪 Teste de Validação

Execute o script de teste para verificar se as mudanças estão funcionando:

```bash
python test_simple_format.py
```

**Resultado esperado:**
```
✅ Formato simplificado detectado!
✅ Compatível com Control-M
✅ Quebras de linha adequadas
✅ Arquivo consolidado gerado com sucesso!
```

## 🚀 Como Usar

1. **Processar DARMs normalmente:**
   ```bash
   python darm_processor.py
   ```

2. **Todos os arquivos gerados agora estão no formato simplificado:**
   - `INSERT_DARM_PAGO_*.sql` - Scripts individuais
   - `INSERT_TODOS_DARMs.sql` - Script consolidado
   - `CHECK_GUIA_*.sql` - Scripts de verificação

3. **Executar no Control-M:**
   - Use qualquer um dos arquivos gerados
   - Todos são compatíveis com o formato do Control-M

## 📋 Checklist de Compatibilidade

- ✅ **Formato de uma linha** - Implementado
- ✅ **Encoding ISO 8859-1** - Mantido
- ✅ **Sem comentários** - Mantido
- ✅ **Caracteres especiais removidos** - Mantido
- ✅ **Estrutura simplificada** - Implementado
- ✅ **Testado com Control-M** - Funcionando

---

**Data da implementação:** Janeiro 2025  
**Versão:** 1.0.0  
**Status:** ✅ Implementado e Testado 