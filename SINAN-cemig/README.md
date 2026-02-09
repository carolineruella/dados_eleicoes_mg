# SINAN-CEMIG: Acidentes de Trabalho em Minas Gerais

Aplicativo Streamlit para download e visualização de dados do SINAN (Sistema de Informação de Agravos de Notificação) relacionados a acidentes de trabalho no estado de Minas Gerais.

## 📋 Sobre o Projeto

Este aplicativo permite:
- **Baixar dados automaticamente** do SINAN via biblioteca PySUS
- Filtrar dados específicos para o estado de Minas Gerais
- Visualizar e analisar acidentes de trabalho graves
- Exportar dados em formato CSV
- Gerar gráficos e análises estatísticas

## ⚠️ Requisito Importante - Windows

**Para Windows:** Este aplicativo requer o **Microsoft C++ Build Tools** para compilar o pacote `pyreaddbc`.

### 🔧 Instalação Rápida no Windows:

1. **Baixe o Build Tools:**
   - Link direto: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Arquivo: `vs_BuildTools.exe` (~1.5 MB)

2. **Instale:**
   - Execute o instalador
   - Selecione **"Desktop development with C++"**
   - Aguarde instalação (~30 minutos, ~6 GB)
   - **Reinicie o computador**

3. **Instale as dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o aplicativo:**
   ```bash
   streamlit run app.py
   ```

### 📖 Guia Completo de Instalação

Para instruções detalhadas passo a passo, consulte: **[INSTALACAO_WINDOWS.md](INSTALACAO_WINDOWS.md)**

## 🚀 Início Rápido (Linux/Mac)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o aplicativo
streamlit run app.py
```

O aplicativo será aberto automaticamente no seu navegador em `http://localhost:8501`

## 📥 Como Obter os Dados do SINAN

### Opção 1: TabNet (Recomendada - Mais Fácil)

1. Acesse o TabNet do DATASUS: [http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def)
2. Selecione as variáveis que deseja analisar
3. Configure os filtros desejados
4. Clique em "Mostrar"
5. Use a opção para exportar para CSV
6. Faça upload do arquivo CSV no aplicativo

### Opção 2: Download Direto do DATASUS

1. Acesse: [https://datasus.saude.gov.br/](https://datasus.saude.gov.br/)
2. Navegue até: Acesso à Informação → SINAN → Dados
3. Baixe os arquivos .dbc desejados
4. Converta para CSV usando:
   - **TabWin**: [https://datasus.saude.gov.br/transferencia-de-arquivos/](https://datasus.saude.gov.br/transferencia-de-arquivos/)
   - Ferramentas online de conversão DBC para CSV
5. Faça upload do arquivo CSV convertido no aplicativo

### Opção 3: API Dados Abertos (Em desenvolvimento)

A API do DATASUS ainda está em fase de desenvolvimento para dados do SINAN. Quando disponível, será integrada ao aplicativo.

## 📊 Funcionalidades

### 1. Upload e Processamento
- Upload de arquivos CSV e TXT
- Detecção automática de encoding (UTF-8, Latin1, ISO-8859-1, CP1252)
- Filtragem automática para o estado de MG
- Salvamento local automático

### 2. Visualização Interativa
- **Aba Visualização**:
  - Tabela interativa com os dados
  - Seleção de colunas para exibir
  - Controle de número de linhas
  - Download em CSV

- **Aba Análise**:
  - Estatísticas descritivas
  - Informações sobre colunas (tipos, valores nulos)
  - Análise de valores faltantes

- **Aba Filtros**:
  - Filtros dinâmicos por coluna
  - Visualização de valores únicos
  - Download de dados filtrados

- **Aba Gráficos**:
  - Gráficos de barras para variáveis categóricas
  - Tabelas de frequência
  - Análise percentual

### 3. Gerenciamento de Arquivos
- Histórico de arquivos carregados
- Reutilização de dados já processados
- Organização automática na pasta `data/`

## 📁 Estrutura de Arquivos

```
SINAN-cemig/
├── app.py                  # Aplicativo principal Streamlit
├── requirements.txt        # Dependências (streamlit, pandas, requests)
├── README.md              # Este arquivo
└── data/                  # Pasta para dados (criada automaticamente)
    └── sinan_acidente_trabalho_mg_YYYY.csv
```

## 🔧 Dependências

O projeto utiliza apenas bibliotecas Python puras, sem necessidade de compilação:

- **streamlit**: Framework para criação de aplicativos web
- **pandas**: Manipulação e análise de dados
- **requests**: Requisições HTTP (preparado para integração futura com APIs)

## 📖 Sobre os Dados

### SINAN - Sistema de Informação de Agravos de Notificação

O SINAN é o sistema oficial do Ministério da Saúde para registro e processamento de dados sobre agravos de notificação compulsória em todo território nacional.

### Acidentes de Trabalho Graves (ACGRAVE)

O aplicativo foi desenvolvido para análise de acidentes de trabalho graves, que incluem:

- ✔️ Acidentes de trabalho com exposição a material biológico
- ✔️ Acidentes de trabalho graves e com mutilações
- ✔️ Acidentes de trabalho fatais

### Variáveis Típicas Disponíveis

- **Dados demográficos**: Idade, sexo, escolaridade
- **Dados ocupacionais**: Ocupação, atividade econômica, vínculo
- **Características do acidente**: Tipo, parte do corpo atingida, agente causador
- **Evolução**: Acompanhamento, sequelas, óbito
- **Localização**: Município de ocorrência, município de residência
- **Temporalidade**: Data de notificação, data do acidente

## 🔗 Links Úteis

### Fontes de Dados
- [DATASUS - Site Principal](https://datasus.saude.gov.br/)
- [TabNet MG - Acidentes de Trabalho](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def)
- [SINAN - Documentação](https://datasus.saude.gov.br/acesso-a-informacao/doencas-e-agravos-de-notificacao-de-2007-em-diante-sinan/)

### Ferramentas
- [TabWin - Conversão de arquivos DBC](https://datasus.saude.gov.br/transferencia-de-arquivos/)
- [API Dados Abertos MS](https://apidadosabertos.saude.gov.br/)

### Documentação Técnica
- [Dicionário de Dados SINAN](http://portalsinan.saude.gov.br/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## ⚠️ Notas Importantes

### Sobre os Dados

1. **Formato dos arquivos**: O aplicativo aceita arquivos CSV. Arquivos .dbc (formato nativo do DATASUS) precisam ser convertidos primeiro.

2. **Filtragem por UF**: O aplicativo tenta identificar automaticamente a coluna de UF. As colunas verificadas são: `SG_UF`, `UF`, `SG_UF_NOT`, `UF_NOT`, `MUNIC_NOT`.

3. **Encoding**: O aplicativo tenta múltiplos encodings automaticamente (UTF-8, Latin1, ISO-8859-1, CP1252).

### Sobre o Desempenho

1. **Arquivos grandes**: Arquivos com mais de 100.000 registros podem demorar para carregar. O aplicativo usa `low_memory=False` para lidar melhor com arquivos grandes.

2. **Cache**: O Streamlit faz cache dos dados carregados. Para recarregar, use "Clear cache" no menu do Streamlit (canto superior direito).

### Privacidade e Segurança

1. **Dados sensíveis**: Os dados do SINAN podem conter informações sensíveis. Certifique-se de seguir as diretrizes de proteção de dados.

2. **Armazenamento local**: Os arquivos são salvos localmente na pasta `data/`. Não são enviados para servidores externos.

## 🆘 Solução de Problemas

### Erro ao carregar arquivo CSV

**Problema**: "Error tokenizing data" ou erro de encoding

**Solução**:
- Verifique se o arquivo está em formato CSV válido
- Tente abrir o arquivo em um editor de texto para verificar o separador (vírgula ou ponto-e-vírgula)
- O aplicativo tenta automaticamente ambos os separadores

### Nenhum dado para MG encontrado

**Problema**: O aplicativo não encontrou registros de MG

**Solução**:
- Verifique se o arquivo realmente contém dados de Minas Gerais
- O aplicativo mostrará todos os dados se não identificar a coluna de UF
- Use a aba "Filtros" para filtrar manualmente por município ou região

### Aplicativo não inicia

**Problema**: Erro ao executar `streamlit run app.py`

**Solução**:
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt

# Verifique a instalação do streamlit
streamlit --version

# Execute novamente
streamlit run app.py
```

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Este é um projeto de análise de dados públicos de saúde.

## 📄 Licença

Este projeto utiliza dados públicos do Ministério da Saúde do Brasil. Os dados são de domínio público e seu uso deve seguir as diretrizes do DATASUS.

---

**Desenvolvido com Streamlit** 🎈 | **Dados: DATASUS/Ministério da Saúde** 🏥
