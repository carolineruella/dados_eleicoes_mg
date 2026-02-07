# 📊 App Eleições 2022 - Minas Gerais

Aplicativo Streamlit para visualização e análise dos dados das eleições de 2022 em municípios selecionados de Minas Gerais.

## 🚀 Como Usar

### 1. Gerar Arquivo de Dados Filtrados

Primeiro, execute o script para baixar e filtrar os dados dos municípios desejados:

```bash
python filtrar_municipios_stream.py
```

Este script irá:
- Baixar os dados do TSE (~243 MB)
- Filtrar apenas os municípios especificados
- Gerar arquivo CSV filtrado (~189 MB)

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Aplicativo

**No Windows (PowerShell):**
```powershell
python -m streamlit run app_eleicoes_mg.py
```

**No Linux/Mac:**
```bash
streamlit run app_eleicoes_mg.py
```

O aplicativo será aberto automaticamente no navegador em `http://localhost:8501`

> **💡 Dica:** Se o comando `streamlit` não for reconhecido, use sempre `python -m streamlit`

## 📋 Funcionalidades

### 🔍 Filtros Principais
- **Cargo:** Presidente, Governador, Senador, Deputado Federal, etc.
- **Turno:** 1º ou 2º Turno

### 📈 Visão Geral
- Top 10 candidatos com gráfico de barras horizontal
- Gráfico de pizza com distribuição (Top 5 + Outros)
- Estatísticas completas: total de votos, votos válidos, nulos e brancos
- Identificação do primeiro colocado com percentual

### 🗺️ Por Município
- Análise detalhada por município de Minas Gerais (853 municípios)
- Top 15 candidatos em cada município
- Ranking completo com número de zonas e seções
- Estatísticas locais

### 🏛️ Por Zona Eleitoral
- Seleção de município e zona eleitoral
- Top 10 candidatos por zona
- Detalhamento de seções por zona
- Estatísticas específicas da zona

### 📊 Análise Detalhada
- Top 10 municípios por total de votos (eleitorado)
- Vencedores por município (Top 20 maiores)
- Comparação entre municípios

### 🗺️ Mapa Interativo
- **Visualização geográfica** dos municípios em Minas Gerais
- **Círculos proporcionais** ao total de votos por município
- **Popup interativo** com detalhes ao clicar:
  - Vencedor do município no cargo/turno selecionado
  - Total de votos e percentual
- **Estatísticas do mapa**: municípios, total e média de votos
- Baseado em **Folium** (mapas interativos)

### 📋 Dados Brutos
- Visualização completa dos dados
- Filtros avançados: município, candidato e zona
- Exportação de dados filtrados em CSV
- Limite de 10.000 linhas para exibição (download completo disponível)

## 🎯 Personalizar Municípios

Para alterar a lista de municípios filtrados, edite o arquivo `filtrar_municipios_stream.py` na seção `MUNICIPIOS_FILTRAR`:

```python
MUNICIPIOS_FILTRAR = {
    'BELO HORIZONTE',
    'CONTAGEM',
    'JUIZ DE FORA',
    # Adicione mais municípios aqui (use a grafia EXATA do TSE)
}
```

**Importante:** Os nomes devem estar em MAIÚSCULAS e sem acentos (ex: `SAO PAULO`, `RIBEIRAO PRETO`)

Após modificar, execute novamente o script de filtragem.

## 📦 Fonte dos Dados

**Fonte original:** Tribunal Superior Eleitoral (TSE)
**URL:** https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_MG.zip
**Eleição:** Todas as eleições de 2022 (Presidente, Governador, Senador, Deputados)
**Estado:** Minas Gerais (MG)
**Municípios incluídos:** 17 municípios selecionados (~1.6 milhões de registros)
**Detalhamento:** Votação por seção eleitoral (máximo nível de detalhe)

## 🛠️ Tecnologias

- **Streamlit**: Framework para criação de aplicações web
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas (gráficos)
- **Folium**: Mapas interativos com OpenStreetMap
- **Streamlit-Folium**: Integração de mapas Folium no Streamlit
- **Requests**: Download dos dados do TSE

## 🌍 Sobre o Mapa Interativo

O mapa usa coordenadas geográficas pré-definidas dos municípios (centro das cidades). O arquivo `coordenadas_municipios.json` contém:
- Latitude e longitude de cada município
- Nível de zoom recomendado

### Para geocodificar locais de votação específicos:

Execute o script `geocodificar_locais.py` para obter coordenadas exatas dos locais de votação usando a API do [geocode.maps.co](https://geocode.maps.co):

```bash
python geocodificar_locais.py
```

**Nota:** A API gratuita tem limite de requisições. O script processa devagar para respeitar os limites e usa cache para não repetir geocodificações.

## 📝 Observações

- Os dados são carregados do arquivo CSV local filtrado
- O aplicativo usa cache do Streamlit para melhor performance
- Todas as visualizações são interativas e responsivas
- O mapa mostra municípios com coordenadas aproximadas do centro
- Círculos maiores = mais votos no município
