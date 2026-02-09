"""
Aplicativo Streamlit ALTERNATIVO para visualizacao de dados do SINAN
SEM dependencia do pysus - usa upload de arquivos CSV
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Configuracao da pagina
st.set_page_config(
    page_title="SINAN-MG: Acidentes de Trabalho",
    page_icon="🏭",
    layout="wide"
)

# Titulo e descricao
st.title("🏭 SINAN - Acidentes de Trabalho em Minas Gerais")
st.markdown("""
Este aplicativo permite visualizar dados do Sistema de Informacao de Agravos de Notificacao (SINAN)
relacionados a acidentes de trabalho no estado de Minas Gerais.

**Versao Alternativa:** Esta versao nao requer a instalacao do pysus (que tem problemas no Windows).
""")

# Sidebar para configuracoes
st.sidebar.header("⚙️ Configuracoes")

# Opcoes de carregamento de dados
st.sidebar.subheader("📥 Carregar Dados")

opcao_carregamento = st.sidebar.radio(
    "Escolha como carregar os dados:",
    ["Upload de arquivo CSV", "Usar arquivo local", "Links para download manual"]
)

df_mg = None

# Opcao 1: Upload de arquivo
if opcao_carregamento == "Upload de arquivo CSV":
    st.sidebar.markdown("### 📤 Upload de Arquivo")

    uploaded_file = st.sidebar.file_uploader(
        "Selecione um arquivo CSV do SINAN:",
        type=['csv'],
        help="Faca upload de um arquivo CSV baixado do DATASUS ou TabNet"
    )

    if uploaded_file is not None:
        with st.spinner("Carregando arquivo..."):
            try:
                # Ler conteudo do arquivo
                conteudo = uploaded_file.getvalue().decode('utf-8-sig', errors='ignore')
                linhas = conteudo.split('\n')

                # Detectar se e arquivo do TabNet (tem cabecalhos extras)
                e_tabnet = any('SINAN' in linha or 'Período:' in linha or 'Fonte:' in linha
                              for linha in linhas[:10])

                if e_tabnet:
                    st.sidebar.info("🔧 Detectado formato TabNet. Limpando arquivo...")

                    # Encontrar inicio dos dados
                    inicio_dados = 0
                    for i, linha in enumerate(linhas):
                        if any(palavra in linha.upper() for palavra in ['MUNIC', 'ANO', 'NOTIF', 'RESID', 'TOTAL', 'UF']):
                            inicio_dados = i
                            break

                    # Encontrar fim dos dados
                    fim_dados = len(linhas)
                    for i in range(len(linhas) - 1, inicio_dados, -1):
                        linha = linhas[i].strip()
                        if linha and not linha.startswith('Fonte:') and not linha.startswith('Nota'):
                            if any(c.isdigit() for c in linha) or ';' in linha or ',' in linha:
                                fim_dados = i + 1
                                break

                    # Extrair dados limpos
                    dados_limpos = '\n'.join(linhas[inicio_dados:fim_dados])

                    # Converter para DataFrame
                    from io import StringIO
                    df_mg = pd.read_csv(StringIO(dados_limpos), sep=None, engine='python')

                else:
                    # Tentar carregar diretamente com diferentes encodings
                    uploaded_file.seek(0)
                    try:
                        df_mg = pd.read_csv(uploaded_file, encoding='utf-8')
                    except:
                        try:
                            uploaded_file.seek(0)
                            df_mg = pd.read_csv(uploaded_file, encoding='latin-1')
                        except:
                            uploaded_file.seek(0)
                            df_mg = pd.read_csv(uploaded_file, encoding='cp1252')

                st.sidebar.success(f"✅ Arquivo carregado: {len(df_mg):,} registros")

                # Salvar no session_state
                st.session_state['df_mg'] = df_mg
                st.session_state['arquivo'] = uploaded_file.name

            except Exception as e:
                st.sidebar.error(f"❌ Erro ao carregar arquivo: {str(e)}")
                st.sidebar.markdown("""
                **Solucao:**
                1. Use o script de limpeza:
                   ```bash
                   python limpar_csv_tabnet.py seu_arquivo.csv
                   ```
                2. Faca upload do arquivo "_limpo.csv" gerado
                """)

# Opcao 2: Arquivo local
elif opcao_carregamento == "Usar arquivo local":
    st.sidebar.markdown("### 📁 Arquivo Local")

    # Listar arquivos CSV na pasta data
    data_dir = Path("data")
    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))

        if csv_files:
            arquivo_selecionado = st.sidebar.selectbox(
                "Selecione um arquivo:",
                [f.name for f in csv_files]
            )

            if st.sidebar.button("📂 Carregar Arquivo"):
                with st.spinner("Carregando arquivo..."):
                    try:
                        caminho_arquivo = data_dir / arquivo_selecionado
                        df_mg = pd.read_csv(caminho_arquivo)

                        st.sidebar.success(f"✅ Carregado: {len(df_mg):,} registros")

                        # Salvar no session_state
                        st.session_state['df_mg'] = df_mg
                        st.session_state['arquivo'] = arquivo_selecionado

                    except Exception as e:
                        st.sidebar.error(f"❌ Erro: {str(e)}")
        else:
            st.sidebar.info("📭 Nenhum arquivo CSV encontrado na pasta 'data'")
    else:
        st.sidebar.info("📭 Pasta 'data' nao encontrada")

# Opcao 3: Links para download manual
else:
    st.sidebar.markdown("### 🔗 Download Manual")
    st.sidebar.markdown("""
    **Como obter os dados:**

    1. **TabNet DATASUS:**
       - [Acidentes de Trabalho - MG](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def)
       - Selecione os parametros desejados
       - Clique em "Arquivo" > "Salvar como CSV"

    2. **FTP DATASUS:**
       - Acesse: ftp://ftp.datasus.gov.br/
       - Navegue ate SINAN
       - Baixe os arquivos .dbc
       - Use TabWin para converter para CSV

    3. **Dados Abertos:**
       - [Portal Dados Abertos](https://dados.gov.br/)
       - Busque por "SINAN"

    Apos baixar, use a opcao "Upload de arquivo CSV" acima.
    """)

# Divisor
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Sobre os dados")
st.sidebar.markdown("""
**SINAN** - Sistema de Informacao de Agravos de Notificacao

**Agravo:** Acidente de Trabalho Grave (ACGRAVE)

**UF:** Minas Gerais (31)

**Fonte:** DATASUS/Ministerio da Saude
""")

# Links uteis
with st.sidebar.expander("🔗 Links Uteis"):
    st.markdown("""
    - [TabNet MG](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def)
    - [DATASUS - SINAN](https://datasus.saude.gov.br/)
    - [Dados Abertos](https://dados.gov.br/)
    - [Documentacao SINAN](https://portalsinan.saude.gov.br/)
    """)

# Exibicao dos dados
st.markdown("---")

# Verificar se ha dados carregados
if 'df_mg' in st.session_state and st.session_state['df_mg'] is not None:
    df_mg = st.session_state['df_mg']

    # Cabecalho
    st.header("📊 Dados Carregados")

    if 'arquivo' in st.session_state:
        st.info(f"📄 Arquivo: **{st.session_state['arquivo']}**")

    # Estatisticas basicas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Registros", f"{len(df_mg):,}")

    with col2:
        st.metric("Numero de Colunas", len(df_mg.columns))

    with col3:
        # Tentar detectar periodo dos dados
        colunas_data = [col for col in df_mg.columns if 'ANO' in col.upper() or 'DT' in col.upper()]
        if colunas_data:
            st.metric("Colunas de Data", len(colunas_data))
        else:
            st.metric("Memoria", f"{df_mg.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")

    # Tabs para diferentes visualizacoes
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Visualizacao", "📈 Analise", "🔍 Filtros", "📊 Graficos"])

    with tab1:
        st.subheader("Amostra dos dados")

        # Opcoes de visualizacao
        col1, col2 = st.columns(2)
        with col1:
            num_linhas = st.slider("Numero de linhas a exibir:", 10, 500, 100)
        with col2:
            colunas_selecionadas = st.multiselect(
                "Selecionar colunas (deixe vazio para todas):",
                df_mg.columns.tolist()
            )

        df_exibir = df_mg[colunas_selecionadas] if colunas_selecionadas else df_mg
        st.dataframe(df_exibir.head(num_linhas), use_container_width=True)

        # Botao para download
        csv = df_mg.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar CSV completo",
            data=csv,
            file_name=f"sinan_acidente_trabalho_mg_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with tab2:
        st.subheader("Analise dos dados")

        # Informacoes sobre colunas
        with st.expander("📋 Ver todas as colunas"):
            col_info = pd.DataFrame({
                'Coluna': df_mg.columns,
                'Tipo': df_mg.dtypes.values,
                'Nao-nulos': df_mg.count().values,
                'Nulos': df_mg.isnull().sum().values
            })
            st.dataframe(col_info, use_container_width=True)

        # Estatisticas descritivas para colunas numericas
        if not df_mg.select_dtypes(include=['number']).empty:
            st.write("**Estatisticas descritivas (colunas numericas):**")
            st.dataframe(df_mg.describe(), use_container_width=True)

        # Valores faltantes
        st.write("**Analise de valores faltantes:**")
        missing_data = pd.DataFrame({
            'Coluna': df_mg.columns,
            'Valores Faltantes': df_mg.isnull().sum().values,
            'Percentual (%)': (df_mg.isnull().sum().values / len(df_mg) * 100).round(2)
        })
        missing_data = missing_data[missing_data['Valores Faltantes'] > 0].sort_values('Valores Faltantes', ascending=False)

        if not missing_data.empty:
            st.dataframe(missing_data, use_container_width=True)
        else:
            st.success("✅ Nenhum valor faltante encontrado!")

    with tab3:
        st.subheader("Filtrar dados")

        # Selecao de colunas para filtrar
        colunas_disponiveis = df_mg.columns.tolist()
        coluna_filtro = st.selectbox("Selecione uma coluna para filtrar:", colunas_disponiveis)

        if coluna_filtro:
            # Mostrar valores unicos
            valores_unicos = df_mg[coluna_filtro].dropna().unique()
            st.write(f"**Valores unicos em '{coluna_filtro}':** {len(valores_unicos)}")

            if len(valores_unicos) <= 100:
                valores_selecionados = st.multiselect(
                    f"Selecione valores de '{coluna_filtro}':",
                    sorted(valores_unicos.tolist())
                )

                if valores_selecionados:
                    df_filtrado = df_mg[df_mg[coluna_filtro].isin(valores_selecionados)]
                    st.write(f"**Registros apos filtro:** {len(df_filtrado):,}")
                    st.dataframe(df_filtrado, use_container_width=True)

                    # Botao para download dos dados filtrados
                    csv_filtrado = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Baixar dados filtrados",
                        data=csv_filtrado,
                        file_name=f"sinan_mg_filtrado_{coluna_filtro}.csv",
                        mime="text/csv"
                    )
            else:
                st.info(f"Muitos valores unicos ({len(valores_unicos)}). Mostrando os primeiros 20:")
                st.write(sorted([str(v) for v in valores_unicos[:20]]))

    with tab4:
        st.subheader("Graficos e Visualizacoes")

        # Selecao de coluna para grafico
        colunas_categoricas = df_mg.select_dtypes(include=['object']).columns.tolist()

        if colunas_categoricas:
            coluna_grafico = st.selectbox(
                "Selecione uma coluna categorica para visualizar:",
                colunas_categoricas
            )

            if coluna_grafico:
                # Contar valores
                contagem = df_mg[coluna_grafico].value_counts().head(20)

                # Criar DataFrame para o grafico
                df_grafico = pd.DataFrame({
                    'Categoria': contagem.index.astype(str),
                    'Quantidade': contagem.values
                })

                st.bar_chart(df_grafico.set_index('Categoria'))

                # Mostrar tabela de frequencia
                with st.expander("📊 Ver tabela de frequencias"):
                    freq_table = pd.DataFrame({
                        'Valor': contagem.index.astype(str),
                        'Frequencia': contagem.values,
                        'Percentual (%)': (contagem.values / len(df_mg) * 100).round(2)
                    })
                    st.dataframe(freq_table, use_container_width=True)
        else:
            st.info("Nenhuma coluna categorica encontrada para visualizacao.")

else:
    st.info("👆 Use as opcoes no menu lateral para carregar dados do SINAN.")

    # Informacoes adicionais
    with st.expander("ℹ️ Informacoes sobre o SINAN"):
        st.markdown("""
        ### Sistema de Informacao de Agravos de Notificacao (SINAN)

        O SINAN e alimentado principalmente pela notificacao e investigacao de casos de doencas e agravos
        que constam da lista nacional de doencas de notificacao compulsoria em todo territorio nacional.

        **Acidentes de Trabalho Graves (ACGRAVE):**
        - Acidentes de trabalho com exposicao a material biologico
        - Acidentes de trabalho graves e com mutilacoes
        - Acidentes de trabalho fatais

        **Variaveis disponiveis:**
        - Dados demograficos do trabalhador
        - Caracteristicas do acidente
        - Tipo de exposicao
        - Evolucao do caso
        - Entre outras

        **Fonte dos dados:** Ministerio da Saude - DATASUS
        """)

    with st.expander("📥 Como obter os dados do SINAN"):
        st.markdown("""
        ### Opcoes para baixar dados do SINAN:

        #### 1. TabNet DATASUS (Mais Facil)
        1. Acesse: [TabNet - Acidentes de Trabalho MG](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def)
        2. Selecione os parametros desejados (linha, coluna, periodo)
        3. Clique em "Mostra"
        4. No resultado, clique em "Arquivo" > "Salvar como CSV"
        5. Faca upload do arquivo neste app

        #### 2. FTP DATASUS (Download Direto)
        1. Acesse: ftp://ftp.datasus.gov.br/
        2. Navegue ate a pasta SINAN
        3. Baixe os arquivos .dbc desejados
        4. Use o software TabWin para converter para CSV
        5. Faca upload do CSV neste app

        #### 3. Usando R (microdatasus)
        ```r
        install.packages("microdatasus")
        library(microdatasus)

        dados <- fetch_datasus(
          year_start = 2020,
          year_end = 2022,
          information_system = "SINAN-ACGRAVE"
        )

        write.csv(dados, "sinan_dados.csv")
        ```

        #### 4. Dados Abertos
        - Acesse: [Portal Brasileiro de Dados Abertos](https://dados.gov.br/)
        - Busque por "SINAN" ou "Acidentes de Trabalho"
        - Baixe datasets disponiveis em CSV
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Desenvolvido com Streamlit | Dados: DATASUS/Ministerio da Saude</p>
    <p><small>Versao Alternativa - Sem dependencia do PySUS</small></p>
</div>
""", unsafe_allow_html=True)
