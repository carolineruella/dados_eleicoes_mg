# 📋 Resumo: Alternativas ao PySUS para SINAN

## ✅ Solucao Imediata (Recomendada)

### Use o App Alternativo com Upload de CSV

**Arquivo:** `app_alternativo.py`

**Como usar:**
```bash
streamlit run app_alternativo.py
```

**Vantagens:**
- ✅ Funciona imediatamente no Windows
- ✅ Nao precisa de compilacao C++
- ✅ Sem dependencias problematicas
- ✅ Interface identica ao app original
- ✅ Suporta upload de CSV ou arquivos locais

## 📥 Como Obter os Dados

### Opcao 1: TabNet DATASUS (Mais Facil)

**Link:** http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def

**Passos:**
1. Acesse o link
2. Configure:
   - **Linha:** Municipio de residencia
   - **Coluna:** Ano de notificacao
   - **Conteudo:** Frequencia
   - **Periodos:** Selecione os anos desejados
3. Clique em "Mostra"
4. No resultado, clique em "Arquivo CSV"
5. Salve o arquivo
6. Faca upload no `app_alternativo.py`

### Opcao 2: Download via Scripts Python

**Arquivos criados:**
- `download_sinan_ftp.py` - Download direto do FTP (em desenvolvimento)
- `explorar_ftp_datasus.py` - Explorar estrutura do FTP

**Nota:** FTP pode ter restricoes de acesso geografico

### Opcao 3: Usar R com microdatasus

Se voce tem R instalado:

```r
# Instalar pacote
install.packages("microdatasus")

# Carregar biblioteca
library(microdatasus)

# Baixar dados
dados <- fetch_datasus(
  year_start = 2020,
  year_end = 2023,
  information_system = "SINAN-ACGRAVE",
  uf = "MG"
)

# Salvar como CSV
write.csv(dados, "sinan_acgrave_mg.csv", row.names = FALSE)
```

## 🔧 Comparacao das Alternativas

| Metodo | Dificuldade | Funciona Windows | Automatico | Status |
|--------|-------------|------------------|------------|--------|
| **app_alternativo.py** | ⭐ Facil | ✅ Sim | ❌ Manual | ✅ **Pronto** |
| TabNet Download | ⭐ Facil | ✅ Sim | ❌ Manual | ✅ Disponivel |
| PySUS | ⭐⭐⭐ Dificil | ⚠️ Problemas | ✅ Sim | ❌ Requer Build Tools |
| FTP Direto | ⭐⭐ Medio | ✅ Sim | ✅ Sim | ⚠️ Em desenvolvimento |
| microdatasus (R) | ⭐⭐ Medio | ✅ Sim | ✅ Sim | ✅ Funcional |
| dbc_reader | ⭐⭐ Medio | ✅ Sim | ✅ Sim | ⚠️ A testar |

## 📚 Documentacao do SINAN

**Baixada em:** `sinan_docs/`

**Arquivos principais para Acidentes de Trabalho:**

1. **ACGRN** (Acidentes Graves):
   - `ACGRN_DIC_DADOS.pdf` - Dicionario de dados
   - `ACGRN_FICHA.pdf` - Ficha de notificacao

2. **ACBION** (Acidentes Biologicos):
   - `ACBION_DIC_DADOS.pdf` - Dicionario de dados
   - `ACBION_FICHA.pdf` - Ficha de notificacao

**Consultar:** `sinan_docs_info.py` para informacoes programaticas

## 🚀 Proximos Passos

### Para usar imediatamente:

1. **Execute o app alternativo:**
   ```bash
   streamlit run app_alternativo.py
   ```

2. **Baixe dados do TabNet:**
   - Acesse: http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def
   - Exporte como CSV

3. **Faca upload no app**

### Para desenvolvimento futuro:

1. **Testar dbc_reader:**
   ```bash
   pip install dbc-reader
   ```

2. **Explorar FTP DATASUS:**
   ```bash
   python explorar_ftp_datasus.py
   ```

3. **Implementar download automatico** (quando FTP funcionar)

## 📖 Referencias

- [Documentacao SINAN](https://portalsinan.saude.gov.br/)
- [TabNet DATASUS](http://tabnet.datasus.gov.br/)
- [PySUS GitHub](https://github.com/AlertaDengue/PySUS)
- [microdatasus (R)](https://rfsaldanha.github.io/microdatasus/)
- [dbc_reader GitHub](https://github.com/lais-huol/dbc_reader)
- [Tutorial PySUS Windows](https://medium.com/@danielly.bx/tutorial-realizando-download-de-dados-p%C3%BAblicos-do-datasus-com-pysus-no-windows-fdbc317a0c5)

## ⚠️ Observacoes Importantes

1. **PySUS no Windows:** Requer Microsoft C++ Build Tools (~6GB, 30-40 min instalacao)

2. **FTP DATASUS:** Pode ter restricoes geograficas ou temporarias

3. **TabNet:** E o metodo mais confiavel para download manual

4. **Formatos:** DATASUS usa arquivos .dbc (DBF comprimido) que precisam conversao

5. **Atualizacao:** Dados sao atualizados periodicamente pelo Ministerio da Saude

## 📞 Suporte

- **Issues PySUS:** https://github.com/AlertaDengue/PySUS/issues
- **Documentacao DATASUS:** https://datasus.saude.gov.br/
- **Portal Saude:** https://www.gov.br/saude/
