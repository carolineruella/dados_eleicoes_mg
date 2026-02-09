# Alternativas ao PySUS para Download de Dados do SINAN

## Problema com PySUS
O `pysus` depende do `pyreaddbc`, que requer compilacao C++ no Windows, causando erros de instalacao.

## Alternativas Disponiveis

### 1. dbc_reader (Python) - Recomendado para Windows

**Repositorio:** https://github.com/lais-huol/dbc_reader

Biblioteca Python especifica para ler arquivos .dbc do DATASUS sem precisar do pyreaddbc.

**Instalacao:**
```bash
pip install dbc-reader
```

**Uso:**
```python
from dbc_reader import read_dbc

# Ler arquivo DBC diretamente
df = read_dbc('arquivo.dbc')
```

### 2. Download Direto via FTP + Processamento Manual

**FTP DATASUS:** ftp://ftp.datasus.gov.br/dissemin/publicos/

**Estrutura para SINAN:**
- ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/FINAIS/

**Exemplo de Download:**
```python
import urllib.request
import ftplib

# Conectar ao FTP
ftp = ftplib.FTP('ftp.datasus.gov.br')
ftp.login()
ftp.cwd('/dissemin/publicos/SINAN/DADOS/FINAIS/')

# Listar arquivos
files = ftp.nlst()
print(files)

# Download de arquivo
with open('local_file.dbc', 'wb') as f:
    ftp.retrbinary('RETR arquivo.dbc', f.write)
```

### 3. microdatasus (R) - Mais Estavel

**Repositorio:** https://rfsaldanha.github.io/microdatasus/

Se voce tem R instalado, esta e uma alternativa mais estavel que o PySUS.

**Instalacao (R):**
```r
install.packages("microdatasus")
```

**Uso (R):**
```r
library(microdatasus)

# Download de dados SINAN
dados <- fetch_datasus(
  year_start = 2020,
  year_end = 2022,
  information_system = "SINAN-DENGUE",
  vars = c("DT_NOTIFIC", "DT_SIN_PRI", "SEM_NOT", "NU_ANO")
)
```

### 4. TabWin (Software Oficial DATASUS)

**Download:** http://www2.datasus.gov.br/DATASUS/index.php?area=040805

Software oficial do DATASUS para processar arquivos .dbc

**Processo:**
1. Baixar arquivos .dbc do FTP
2. Abrir no TabWin
3. Exportar como CSV

### 5. API REST (Limitada)

O DATASUS tem uma API REST limitada:

**Base URL:** https://apidadosabertos.saude.gov.br/

**Limitacoes:** Nao inclui todos os datasets do SINAN

### 6. Solucao Hibrida - Download Manual + Upload no App

Adicionar ao app Streamlit a opcao de upload de arquivos CSV:

```python
uploaded_file = st.file_uploader("Carregar CSV do SINAN", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
```

## Estrutura do FTP DATASUS para SINAN

```
ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/
├── DADOS/
│   ├── FINAIS/        # Dados finalizados
│   │   ├── ACGR/      # Acidente de Trabalho Grave
│   │   ├── ACBI/      # Acidente Biologico
│   │   ├── DENG/      # Dengue
│   │   └── ...
│   └── PRELIM/        # Dados preliminares
├── DOCS/              # Documentacao
└── TAB/               # Tabelas auxiliares
```

## Comparacao das Alternativas

| Alternativa | Dificuldade | Windows | Dados Atualizados | Automatizado |
|------------|-------------|---------|-------------------|--------------|
| dbc_reader | Baixa | ✅ Sim | ✅ Sim | ✅ Sim |
| FTP Direto | Media | ✅ Sim | ✅ Sim | ✅ Sim |
| microdatasus (R) | Media | ✅ Sim | ✅ Sim | ✅ Sim |
| TabWin | Baixa | ✅ Sim | ✅ Sim | ❌ Manual |
| PySUS | Alta | ⚠️ Problemas | ✅ Sim | ✅ Sim |
| Upload Manual | Muito Baixa | ✅ Sim | Depende | ❌ Manual |

## Recomendacao

**Para Windows:** Use `dbc_reader` ou FTP direto + processamento
**Para Linux/Mac:** Use `pysus` (funciona melhor)
**Para Prototipagem Rapida:** Upload manual de CSV
**Para Producao:** FTP direto com agendamento

## Fontes

- [PySUS no Windows - Tutorial](https://medium.com/@danielly.bx/tutorial-realizando-download-de-dados-p%C3%BAblicos-do-datasus-com-pysus-no-windows-fdbc317a0c5)
- [microdatasus R Package](https://medium.com/@danielly.bx/realizando-download-de-dados-p%C3%BAblicos-do-datasus-com-o-pacote-microdatasus-do-r-218cf4181e47)
- [Converter DBC para CSV](https://medium.com/@felipezeiser/como-converter-os-dados-dbc-do-datasus-no-python-fb3b6a65918e)
- [dbc_reader GitHub](https://github.com/lais-huol/dbc_reader)
- [DATASUS - Dados Abertos](https://dadosabertos.social/t/como-obter-e-tratar-dados-do-datasus/66)
