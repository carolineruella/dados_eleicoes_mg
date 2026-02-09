"""
Aplicativo Streamlit para download e visualização de dados do SINAN
relacionados a acidentes de trabalho no estado de Minas Gerais (MG)

Fonte dos dados: Ministério da Saúde - DATASUS
Biblioteca: pysus (https://github.com/AlertaDengue/PySUS)
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="SINAN-MG: Acidentes de Trabalho",
    page_icon="🏭",
    layout="wide"
)

# Título e descrição
st.title("🏭 SINAN - Acidentes de Trabalho em Minas Gerais")
st.markdown("""
Este aplicativo permite baixar e visualizar dados do Sistema de Informação de Agravos de Notificação (SINAN)
relacionados a acidentes de trabalho no estado de Minas Gerais.
""")

# Sidebar para configurações
st.sidebar.header("⚙️ Configurações")

# Seleção do ano
ano_atual = datetime.now().year
anos_disponiveis = list(range(2007, ano_atual + 1))
ano_selecionado = st.sidebar.selectbox(
    "Selecione o ano:",
    anos_disponiveis,
    index=len(anos_disponiveis) - 1
)

# Diretório para salvar os dados
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# Botão para baixar dados
if st.sidebar.button("📥 Baixar Dados do SINAN", type="primary"):
    with st.spinner(f"Baixando dados do SINAN para MG - Ano {ano_selecionado}..."):
        try:
            # Importar pysus
            from pysus.online_data import SINAN

            # Inicializar o cliente SINAN
            sinan = SINAN()

            st.info(f"🔍 Buscando dados de Acidentes de Trabalho Graves para o ano {ano_selecionado}...")

            # Baixar dados do SINAN
            # Agravo: ACGRAVE = Acidente de Trabalho Grave
            df = sinan.load("ACGRAVE", ano_selecionado)

            if df is not None and not df.empty:
                st.success(f"✅ Dados baixados com sucesso! Total de registros: {len(df):,}")

                # Filtrar apenas para Minas Gerais
                # Tentar diferentes colunas que podem conter UF
                colunas_uf = ['SG_UF', 'UF', 'SG_UF_NOT', 'UF_NOT', 'MUNIC_NOT']
                df_mg = None

                for coluna in colunas_uf:
                    if coluna in df.columns:
                        # MG pode estar como 'MG' ou '31' (código IBGE)
                        if df[coluna].dtype == 'object':
                            df_temp = df[df[coluna].str.contains('MG|31', na=False, case=False)]
                        else:
                            df_temp = df[df[coluna] == 31]

                        if len(df_temp) > 0:
                            df_mg = df_temp
                            st.success(f"✅ Filtrado por coluna '{coluna}': {len(df_mg):,} registros encontrados para MG")
                            break

                if df_mg is None or len(df_mg) == 0:
                    st.warning("⚠️ Não foi possível filtrar automaticamente para MG. Mostrando todos os dados.")
                    df_mg = df
                    st.info("💡 Você pode usar a aba 'Filtros' para filtrar manualmente por município ou região.")

                # Salvar dados
                arquivo_saida = os.path.join(data_dir, f"sinan_acidente_trabalho_mg_{ano_selecionado}.csv")
                df_mg.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')

                # Armazenar no session_state
                st.session_state['df_mg'] = df_mg
                st.session_state['ano'] = ano_selecionado

                st.info(f"💾 Arquivo salvo em: {arquivo_saida}")

            else:
                st.error("❌ Nenhum dado foi retornado. Verifique se há dados disponíveis para este ano.")

        except ImportError as e:
            st.error("❌ Erro: Biblioteca pysus não está instalada corretamente.")
            st.markdown("""
            ### 🔧 Como resolver:

            O erro ocorre porque o pacote `pyreaddbc` (dependência do pysus) precisa ser compilado.

            **Siga estes passos:**

            1. **Instale o Microsoft C++ Build Tools:**
               - Baixe em: https://visualstudio.microsoft.com/visual-cpp-build-tools/
               - Execute o instalador
               - Selecione "Desktop development with C++"
               - Instale (pode demorar ~30 minutos)

            2. **Após a instalação, reinstale o pysus:**
               ```bash
               pip uninstall pysus pyreaddbc -y
               pip install pysus
               ```

            3. **Reinicie este aplicativo**

            ---

            **Alternativa:** Use a versão do app que suporta upload de arquivos CSV.
            """)

        except Exception as e:
            st.error(f"❌ Erro ao baixar dados: {str(e)}")
            st.info("""
            **Possíveis causas:**
            - Dados não disponíveis para o ano selecionado
            - Problemas de conexão com o servidor DATASUS
            - Formato de dados diferente do esperado

            **Sugestão:** Tente outro ano ou use a opção de upload de arquivo CSV.
            """)

# Divisor
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Sobre os dados")
st.sidebar.markdown("""
**SINAN** - Sistema de Informação de Agravos de Notificação

**Agravo:** Acidente de Trabalho Grave (ACGRAVE)

**UF:** Minas Gerais (31)

**Fonte:** DATASUS/Ministério da Saúde
""")

# Links úteis
with st.sidebar.expander("🔗 Links Úteis"):
    st.markdown("""
    - [DATASUS - SINAN](https://datasus.saude.gov.br/)
    - [PySUS - GitHub](https://github.com/AlertaDengue/PySUS)
    - [TabNet MG](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/acgrMG.def)
    - [Build Tools Download](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
    """)

# Exibição dos dados
st.markdown("---")
st.header("📊 Dados Carregados")

if 'df_mg' in st.session_state and st.session_state['df_mg'] is not None:
    df_mg = st.session_state['df_mg']

    # Estatísticas básicas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Registros", f"{len(df_mg):,}")

    with col2:
        st.metric("Número de Colunas", len(df_mg.columns))

    with col3:
        st.metric("Ano", st.session_state.get('ano', 'N/A'))

    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Visualização", "📈 Análise", "🔍 Filtros", "📊 Gráficos"])

    with tab1:
        st.subheader("Amostra dos dados")

        # Opções de visualização
        col1, col2 = st.columns(2)
        with col1:
            num_linhas = st.slider("Número de linhas a exibir:", 10, 500, 100)
        with col2:
            colunas_selecionadas = st.multiselect(
                "Selecionar colunas (deixe vazio para todas):",
                df_mg.columns.tolist()
            )

        df_exibir = df_mg[colunas_selecionadas] if colunas_selecionadas else df_mg
        st.dataframe(df_exibir.head(num_linhas), use_container_width=True)

        # Botão para download
        csv = df_mg.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar CSV completo",
            data=csv,
            file_name=f"sinan_acidente_trabalho_mg_{st.session_state.get('ano', '')}.csv",
            mime="text/csv"
        )

    with tab2:
        st.subheader("Análise dos dados")

        # Informações sobre colunas
        with st.expander("📋 Ver todas as colunas"):
            col_info = pd.DataFrame({
                'Coluna': df_mg.columns,
                'Tipo': df_mg.dtypes.values,
                'Não-nulos': df_mg.count().values,
                'Nulos': df_mg.isnull().sum().values
            })
            st.dataframe(col_info, use_container_width=True)

        # Estatísticas descritivas para colunas numéricas
        if not df_mg.select_dtypes(include=['number']).empty:
            st.write("**Estatísticas descritivas (colunas numéricas):**")
            st.dataframe(df_mg.describe(), use_container_width=True)

        # Valores faltantes
        st.write("**Análise de valores faltantes:**")
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

        # Seleção de colunas para filtrar
        colunas_disponiveis = df_mg.columns.tolist()
        coluna_filtro = st.selectbox("Selecione uma coluna para filtrar:", colunas_disponiveis)

        if coluna_filtro:
            # Mostrar valores únicos
            valores_unicos = df_mg[coluna_filtro].dropna().unique()
            st.write(f"**Valores únicos em '{coluna_filtro}':** {len(valores_unicos)}")

            if len(valores_unicos) <= 100:
                valores_selecionados = st.multiselect(
                    f"Selecione valores de '{coluna_filtro}':",
                    sorted(valores_unicos)
                )

                if valores_selecionados:
                    df_filtrado = df_mg[df_mg[coluna_filtro].isin(valores_selecionados)]
                    st.write(f"**Registros após filtro:** {len(df_filtrado):,}")
                    st.dataframe(df_filtrado, use_container_width=True)

                    # Botão para download dos dados filtrados
                    csv_filtrado = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Baixar dados filtrados",
                        data=csv_filtrado,
                        file_name=f"sinan_mg_filtrado_{coluna_filtro}.csv",
                        mime="text/csv"
                    )
            else:
                st.info(f"Muitos valores únicos ({len(valores_unicos)}). Mostrando os primeiros 20:")
                st.write(sorted(valores_unicos)[:20])

    with tab4:
        st.subheader("Gráficos e Visualizações")

        # Seleção de coluna para gráfico
        colunas_categoricas = df_mg.select_dtypes(include=['object']).columns.tolist()

        if colunas_categoricas:
            coluna_grafico = st.selectbox(
                "Selecione uma coluna categórica para visualizar:",
                colunas_categoricas
            )

            if coluna_grafico:
                # Contar valores
                contagem = df_mg[coluna_grafico].value_counts().head(20)

                # Criar DataFrame para o gráfico
                df_grafico = pd.DataFrame({
                    'Categoria': contagem.index,
                    'Quantidade': contagem.values
                })

                st.bar_chart(df_grafico.set_index('Categoria'))

                # Mostrar tabela de frequência
                with st.expander("📊 Ver tabela de frequências"):
                    freq_table = pd.DataFrame({
                        'Valor': contagem.index,
                        'Frequência': contagem.values,
                        'Percentual (%)': (contagem.values / len(df_mg) * 100).round(2)
                    })
                    st.dataframe(freq_table, use_container_width=True)
        else:
            st.info("Nenhuma coluna categórica encontrada para visualização.")

else:
    st.info("👆 Use o botão 'Baixar Dados do SINAN' no menu lateral para começar.")

    # Informações adicionais
    with st.expander("ℹ️ Informações sobre o SINAN"):
        st.markdown("""
        ### Sistema de Informação de Agravos de Notificação (SINAN)

        O SINAN é alimentado principalmente pela notificação e investigação de casos de doenças e agravos
        que constam da lista nacional de doenças de notificação compulsória em todo território nacional.

        **Acidentes de Trabalho Graves (ACGRAVE):**
        - Acidentes de trabalho com exposição a material biológico
        - Acidentes de trabalho graves e com mutilações
        - Acidentes de trabalho fatais

        **Variáveis disponíveis:**
        - Dados demográficos do trabalhador
        - Características do acidente
        - Tipo de exposição
        - Evolução do caso
        - Entre outras

        **Fonte dos dados:** Ministério da Saúde - DATASUS
        """)

    with st.expander("🔧 Requisitos do Sistema"):
        st.markdown("""
        ### Para usar este aplicativo, você precisa:

        1. **Python 3.8 ou superior**

        2. **Microsoft C++ Build Tools** (somente Windows):
           - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
           - Necessário para compilar o pacote `pyreaddbc`
           - Selecione "Desktop development with C++" durante a instalação

        3. **Bibliotecas Python:**
           ```bash
           pip install -r requirements.txt
           ```

        ### Instalação Passo a Passo:

        **Windows:**
        1. Instale o Visual Studio Build Tools
        2. Reinicie o computador
        3. Execute: `pip install -r requirements.txt`
        4. Execute: `streamlit run app.py`

        **Linux/Mac:**
        1. Execute: `pip install -r requirements.txt`
        2. Execute: `streamlit run app.py`
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Desenvolvido com Streamlit | Dados: DATASUS/Ministério da Saúde</p>
    <p><small>Biblioteca: PySUS (AlertaDengue)</small></p>
</div>
""", unsafe_allow_html=True)
