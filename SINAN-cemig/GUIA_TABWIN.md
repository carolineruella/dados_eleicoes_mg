# 📘 Guia Completo: TabWin + SINAN

## 🎯 Objetivo

Usar o TabWin para converter arquivos .dbc do SINAN em CSV e visualizar no aplicativo Streamlit.

---

## 📦 O que foi baixado

**TabWin 4.15** - Software oficial do DATASUS

**Local:** `c:\Users\crptorres\Python\dados_eleicoes_mg\SINAN-cemig\tabwin\`

**Arquivos principais:**
- `TabWin415.exe` - Programa principal (interface grafica)
- `dbf2dbc.exe` - Conversor de linha de comando
- Arquivos `.MAP` - Mapas geograficos do Brasil (todos os estados)
- `TabWin32.hlp` - Arquivo de ajuda

---

## 🚀 Workflow Completo

### Etapa 1: Baixar Arquivos .dbc do SINAN

#### Opcao A: TabNet (Recomendado para iniciantes)

1. **Acesse:** http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def

2. **Configure a tabulacao:**
   - **Linha:** Municipio de residencia
   - **Coluna:** Ano de notificacao
   - **Conteudo:** Frequencia
   - **Periodos Disponiveis:** Selecione os anos desejados
   - **Selecoes Disponiveis:** Configure filtros (opcional)

3. **Gerar e Salvar:**
   - Clique em "Mostra"
   - Na pagina de resultado, clique em "Arquivo CSV"
   - Salve o arquivo

4. **Pular para Etapa 3** (TabNet ja exporta CSV)

#### Opcao B: FTP DATASUS (Para dados brutos completos)

1. **Acesse o FTP:**
   - Abra um navegador
   - URL: `ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/`

2. **Navegue ate os dados:**
   ```
   SINAN/
   ├── DADOS/
   │   ├── FINAIS/    ← Dados consolidados
   │   └── PRELIM/    ← Dados preliminares
   ```

3. **Localize os arquivos:**
   - Procure por agravos especificos (ex: ACGR, DENG, VIOL)
   - Arquivos tem formato: `ACGRAAMM.dbc`
     - ACGR = Codigo do agravo
     - AA = Ano (ex: 22 = 2022)
     - MM = Mes ou UF

4. **Baixe os arquivos .dbc**

---

### Etapa 2: Converter DBC para CSV com TabWin

#### Metodo 1: Interface Grafica (Mais Facil)

1. **Abrir TabWin:**
   ```
   c:\Users\crptorres\Python\dados_eleicoes_mg\SINAN-cemig\tabwin\TabWin415.exe
   ```

2. **Abrir arquivo DBC:**
   - Menu: `Arquivo > Abrir`
   - Selecione o arquivo `.dbc` baixado
   - TabWin ira exibir os dados em formato de tabela

3. **Exportar para CSV:**
   - Menu: `Arquivo > Salvar Como`
   - Em "Tipo de arquivo", selecione: **CSV (separado por virgulas)**
   - Escolha o nome e local do arquivo
   - Clique em "Salvar"

4. **Pronto!** O arquivo CSV esta pronto para uso

#### Metodo 2: Linha de Comando (Para automatizar)

O TabWin inclui `dbf2dbc.exe` que pode ser usado para conversao em lote:

```batch
# Converter DBC para DBF
cd tabwin
dbf2dbc.exe arquivo.dbc arquivo.dbf

# Depois use Python ou Excel para converter DBF em CSV
```

**Nota:** `dbf2dbc.exe` converte DBC → DBF. Para obter CSV, voce precisara de um passo adicional.

#### Metodo 3: Usar Python com dbfread (Alternativa)

Se voce ja tem o arquivo .dbf:

```python
from dbfread import DBF
import pandas as pd

# Ler DBF
table = DBF('arquivo.dbf', encoding='latin-1')
df = pd.DataFrame(iter(table))

# Salvar como CSV
df.to_csv('arquivo.csv', index=False, encoding='utf-8-sig')
```

Instalar:
```bash
pip install dbfread
```

---

### Etapa 3: Visualizar no App Streamlit

1. **Executar o app alternativo:**
   ```bash
   streamlit run app_alternativo.py
   ```

2. **Carregar o CSV:**
   - No menu lateral, selecione "Upload de arquivo CSV"
   - Clique em "Browse files"
   - Selecione o arquivo CSV criado
   - Clique em "Open"

3. **Explorar os dados:**
   - Use as abas: Visualizacao, Analise, Filtros, Graficos
   - Aplique filtros conforme necessario
   - Baixe dados filtrados se desejar

---

## 🗺️ Recursos Adicionais do TabWin

### Mapas Geograficos

O TabWin inclui mapas de todos os estados brasileiros:

- `br_municip.MAP` - Todos os municipios do Brasil
- `mg_municip.MAP` - Municipios de Minas Gerais
- `br_uf.MAP` - Estados do Brasil

**Usar mapas:**
1. No TabWin, va em `Ver > Mapa`
2. Selecione o arquivo .MAP desejado
3. Configure as variaveis geograficas

### Tabulacoes Personalizadas

O TabWin permite criar tabulacoes complexas:

1. **Arquivo de Definicao (.def):**
   - Define estrutura da tabulacao
   - Linha, coluna, conteudo
   - Filtros e selecoes

2. **Criar Definicao:**
   - Menu: `Ferramentas > Editor de Definicoes`
   - Configure parametros
   - Salve como arquivo .def

3. **Executar Definicao:**
   - `Arquivo > Executar Definicao`
   - Selecione o arquivo .def
   - TabWin processa automaticamente

---

## 📊 Estrutura de Arquivos SINAN

### Codigos de Agravos Comuns:

| Codigo | Agravo | Arquivo Padrao |
|--------|--------|----------------|
| ACGR | Acidente de Trabalho Grave | ACGRaaMM.dbc |
| ACBI | Acidente Biologico | ACBIaaMM.dbc |
| DENG | Dengue | DENGaaMM.dbc |
| CHIK | Chikungunya | CHIKaaMM.dbc |
| ZIKA | Zika Virus | ZIKAaaMM.dbc |
| VIOL | Violencia | VIOLaaMM.dbc |
| TUBE | Tuberculose | TUBEaaMM.dbc |
| HANS | Hanseniase | HANSaaMM.dbc |
| MENI | Meningite | MENIaaMM.dbc |

**Nomenclatura:**
- `aa` = Ano (ex: 22 = 2022, 23 = 2023)
- `MM` = Mes ou codigo da UF (ex: 31 = MG)

### Exemplo para Minas Gerais:
- `ACGR2231.dbc` = Acidentes de Trabalho Graves, 2022, Minas Gerais

---

## 🔧 Solucao de Problemas

### Problema: TabWin nao abre o arquivo .dbc

**Causa:** Arquivo corrompido ou formato incorreto

**Solucao:**
1. Baixe o arquivo novamente
2. Verifique se o arquivo tem extensao `.dbc`
3. Tente com outro arquivo para testar

### Problema: Erro ao salvar CSV

**Causa:** Permissoes de arquivo ou caminho invalido

**Solucao:**
1. Salve em uma pasta onde voce tem permissao de escrita
2. Use um caminho sem caracteres especiais
3. Execute TabWin como administrador (botao direito > Executar como administrador)

### Problema: CSV com caracteres estranhos

**Causa:** Problema de encoding

**Solucao:**
1. Ao abrir o CSV no Excel: `Dados > De Texto/CSV > Origem do Arquivo: 1252 (ANSI - Latin I)`
2. No pandas (Python):
   ```python
   df = pd.read_csv('arquivo.csv', encoding='latin-1')
   # ou
   df = pd.read_csv('arquivo.csv', encoding='cp1252')
   ```

### Problema: Arquivo muito grande

**Causa:** Dataset com muitos registros

**Solucao:**
1. Use filtros no TabNet antes de baixar
2. Processe por partes (por ano ou por estado)
3. Use ferramentas de Big Data se necessario

---

## 📚 Documentacao e Referencias

### TabWin:
- **Manual:** Incluido no download (`TabWin32.hlp`)
- **Historico:** Ver arquivo `HISTORIA.TXT`
- **Tutorial Online:** http://www2.datasus.gov.br/DATASUS/index.php?area=040805

### SINAN:
- **Portal:** https://portalsinan.saude.gov.br/
- **Documentacao:** `sinan_docs/` (ja baixada)
- **Dicionario de Dados:** `sinan_docs/ACGRN_DIC_DADOS.pdf`

### FTP DATASUS:
- **Raiz:** ftp://ftp.datasus.gov.br/
- **SINAN:** ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/
- **TabWin:** ftp://ftp.datasus.gov.br/tabwin/

---

## ✅ Checklist Rapido

- [ ] TabWin instalado e funcionando
- [ ] Arquivo .dbc baixado do DATASUS
- [ ] Arquivo convertido para CSV no TabWin
- [ ] App alternativo rodando (`streamlit run app_alternativo.py`)
- [ ] CSV carregado no app
- [ ] Dados sendo visualizados corretamente

---

## 🎓 Proximos Passos

### Para Analises Mais Avancadas:

1. **Python + Pandas:**
   - Carregar CSV no Jupyter Notebook
   - Realizar analises estatisticas
   - Criar visualizacoes customizadas

2. **Power BI / Tableau:**
   - Importar CSV
   - Criar dashboards interativos
   - Compartilhar relatorios

3. **R + RStudio:**
   - Usar pacote `microdatasus`
   - Analises epidemiologicas
   - Modelos estatisticos

### Para Automatizar:

1. **Script Python completo:**
   - Download automatico do FTP
   - Conversao DBC → CSV
   - Processamento e limpeza
   - Upload automatico no app

2. **Pipeline de dados:**
   - Agendamento de downloads
   - ETL automatizado
   - Banco de dados PostgreSQL/MySQL
   - API REST para consultas

---

## 📞 Suporte

**Problemas com TabWin:**
- Email: datasus@saude.gov.br
- Telefone: 136 (Ministerio da Saude)

**Problemas com o App:**
- Verifique os arquivos criados: `alternativas_pysus.md`, `RESUMO_ALTERNATIVAS.md`
- Issues no GitHub do PySUS: https://github.com/AlertaDengue/PySUS/issues

---

**Ultima atualizacao:** 2026-02-09
