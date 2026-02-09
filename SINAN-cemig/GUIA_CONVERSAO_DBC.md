# 🔄 Guia de Conversão: DBC → CSV

## ✅ Arquivos Baixados

Você tem **6 arquivos DBC** prontos para converter:

```
data/dbc_files/
├── ACGRBR20.dbc  (2020) - 7.64 MB
├── ACGRBR21.dbc  (2021) - 10.03 MB
├── ACGRBR22.dbc  (2022) - 14.27 MB
├── ACGRBR23.dbc  (2023) - 21.52 MB
├── ACGRBR24.dbc  (2024) - 24.98 MB
└── ACGRBR25.dbc  (2025) - 16.72 MB
```

---

## 🎯 Método Recomendado: TabWin GUI

### Passo a Passo:

#### 1. Abrir TabWin
```
Caminho: c:\Users\crptorres\Python\dados_eleicoes_mg\SINAN-cemig\tabwin\TabWin415.exe
```

Clique duas vezes no arquivo `TabWin415.exe`

#### 2. Abrir arquivo DBC

1. No TabWin, clique em: **Arquivo** → **Abrir**
2. Navegue até: `c:\Users\crptorres\Python\dados_eleicoes_mg\SINAN-cemig\data\dbc_files\`
3. Selecione o arquivo (ex: `ACGRBR22.dbc`)
4. Clique em **Abrir**

**Aguarde:** Arquivos grandes podem demorar 1-2 minutos para carregar

#### 3. Visualizar os Dados

Após abrir, você verá uma tabela com os dados:
- Colunas: variáveis do SINAN (DT_NOTIFIC, SG_UF, MUNIC_RES, etc.)
- Linhas: cada notificação de acidente de trabalho

#### 4. Exportar para CSV

1. Clique em: **Arquivo** → **Salvar Como**
2. Em "Salvar como tipo", selecione: **CSV (separado por vírgulas) (*.csv)**
3. Navegue até: `c:\Users\crptorres\Python\dados_eleicoes_mg\SINAN-cemig\data\csv_files\`
4. Digite o nome: `ACGRBR22.csv` (ou mantenha o sugerido)
5. Clique em **Salvar**

#### 5. Repetir para Outros Anos

Repita os passos 2-4 para cada arquivo DBC que deseja converter.

**Dica:** Comece com um ano específico (ex: 2022 ou 2023) para testar.

---

## ⚡ Conversão Rápida em Lote

### Opção A: Processar todos de uma vez

1. Abra o TabWin
2. Para cada arquivo DBC:
   - Arquivo → Abrir → Selecione o .dbc
   - Aguarde carregar
   - Arquivo → Salvar Como → CSV
   - Salve em `data/csv_files/`
3. Resultado: 6 arquivos CSV prontos para análise

**Tempo estimado:** 10-15 minutos (dependendo do PC)

---

## 📊 Depois da Conversão

### Visualizar no App Streamlit

1. **Execute o app:**
   ```bash
   streamlit run app_alternativo.py
   ```

2. **No menu lateral:**
   - Selecione: "Usar arquivo local"
   - Escolha um dos CSV criados (ex: ACGRBR22.csv)
   - Clique em "Carregar Arquivo"

3. **Explore os dados:**
   - Aba "Visualização": Ver amostra dos dados
   - Aba "Análise": Estatísticas descritivas
   - Aba "Filtros": Filtrar por município, UF, etc.
   - Aba "Gráficos": Visualizações

---

## 🔍 Filtrar Apenas Minas Gerais

Após carregar o CSV (que contém dados de TODO o Brasil), filtre para MG:

### No App:

1. Vá para a aba **"Filtros"**
2. Selecione a coluna: **`SG_UF_NOT`** ou **`SG_UF`** ou **`MUNIC_NOT`**
3. Valores possíveis para MG:
   - `MG` (se for texto)
   - `31` (se for código IBGE)
4. Selecione o valor correspondente a MG
5. Clique em "Baixar dados filtrados" para salvar apenas MG

### Com Python (alternativa):

```python
import pandas as pd

# Carregar CSV
df = pd.read_csv('data/csv_files/ACGRBR22.csv')

# Filtrar para Minas Gerais
# Tentar diferentes colunas
if 'SG_UF_NOT' in df.columns:
    df_mg = df[df['SG_UF_NOT'] == 'MG']
elif 'SG_UF' in df.columns:
    df_mg = df[df['SG_UF'] == 'MG']
else:
    # Usar código IBGE (31 = MG)
    df_mg = df[df['MUNIC_NOT'].astype(str).str.startswith('31')]

print(f"Total Brasil: {len(df):,}")
print(f"Apenas MG: {len(df_mg):,}")

# Salvar apenas MG
df_mg.to_csv('data/csv_files/ACGRBR22_MG.csv', index=False)
```

---

## 📋 Checklist de Conversão

- [ ] TabWin aberto
- [ ] Arquivo DBC carregado
- [ ] Dados visualizados na tela
- [ ] Exportado como CSV
- [ ] CSV salvo em `data/csv_files/`
- [ ] App Streamlit rodando
- [ ] CSV carregado no app
- [ ] Dados filtrados para MG (se necessário)

---

## ⚠️ Solução de Problemas

### TabWin não abre o arquivo

**Erro:** "Arquivo inválido" ou "Erro ao ler arquivo"

**Soluções:**
1. Verifique se o arquivo .dbc foi baixado completamente
2. Tente com outro arquivo DBC
3. Baixe o arquivo novamente

### TabWin trava ou congela

**Causa:** Arquivo muito grande (ex: ACGRBR24.dbc - 25 MB)

**Soluções:**
1. Aguarde mais tempo (até 5 minutos)
2. Feche outros programas para liberar memória
3. Tente com um arquivo menor primeiro (ex: ACGRBR20.dbc)

### CSV com caracteres estranhos

**Causa:** Problema de encoding

**Solução:**
```python
import pandas as pd

# Tentar diferentes encodings
df = pd.read_csv('arquivo.csv', encoding='latin-1')
# ou
df = pd.read_csv('arquivo.csv', encoding='cp1252')

# Salvar com UTF-8
df.to_csv('arquivo_utf8.csv', encoding='utf-8-sig', index=False)
```

### Arquivo CSV muito grande

**Problema:** CSVs de 100+ MB são lentos para carregar

**Soluções:**
1. Filtrar para apenas MG antes de carregar no app
2. Usar apenas colunas necessárias
3. Trabalhar com Jupyter Notebook para análises complexas

---

## 📈 Próximos Passos

### Análise Simples:
1. Converter 1-2 arquivos DBC → CSV
2. Carregar no app Streamlit
3. Explorar gráficos e tabelas

### Análise Completa:
1. Converter todos os 6 arquivos
2. Filtrar cada um para apenas MG
3. Combinar anos para análise temporal
4. Criar relatórios

### Análise Avançada:
1. Combinar múltiplos anos em um único DataFrame
2. Análise de tendências temporais
3. Geocodificação (mapas)
4. Modelos estatísticos

---

## 💡 Dicas Finais

1. **Comece pequeno:** Teste com ACGRBR22.dbc (tamanho médio, dados recentes)

2. **Organize os arquivos:**
   - DBC originais em `data/dbc_files/`
   - CSV convertidos em `data/csv_files/`
   - CSV filtrados (apenas MG) em `data/csv_mg/`

3. **Documente:** Anote quais anos você já converteu e analisou

4. **Backup:** Mantenha os arquivos DBC originais (não delete após converter)

5. **Performance:** CSVs são mais rápidos que DBC para carregar repetidamente

---

## 🆘 Precisa de Ajuda?

### Recursos:
- Manual do TabWin: `tabwin/TabWin32.hlp`
- Documentação SINAN: `sinan_docs/`
- Dicionário de Dados: `sinan_docs/ACGRN_DIC_DADOS.pdf`

### Alternativas se TabWin não funcionar:
1. Usar TabNet (já exporta CSV) - mais fácil mas dados agregados
2. Usar R + microdatasus (requer R instalado)
3. Pedir ajuda em fóruns DATASUS

---

**Pronto para começar!** 🚀

Abra o TabWin e converta seu primeiro arquivo DBC → CSV!
