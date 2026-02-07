import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Configuração da página
st.set_page_config(
    page_title="Eleições 2022 - Minas Gerais",
    page_icon="🗳️",
    layout="wide"
)

# Título principal
st.title("📊 Eleições 2022 - Minas Gerais")
st.markdown("### Municípios Selecionados - Votação Agregada por Local de Votação")

# Arquivo de dados local (agregado por endereço e candidato)
DATA_FILE = "eleicoes_2022_mg_filtrados_*_agregado.csv"

@st.cache_data
def load_data():
    """Carrega os dados filtrados do arquivo CSV local"""
    try:
        # Procurar arquivo filtrado
        arquivos = glob.glob(DATA_FILE)

        if not arquivos:
            st.error(f"❌ Arquivo de dados agregado não encontrado: {DATA_FILE}")
            st.info("Execute o script 'filtrar_municipios_stream.py' para gerar o arquivo de dados agregado.")
            return None

        # Usar o arquivo mais recente se houver múltiplos
        arquivo_mais_recente = max(arquivos, key=os.path.getmtime)

        with st.spinner(f"📂 Carregando dados de {os.path.basename(arquivo_mais_recente)}..."):
            df = pd.read_csv(arquivo_mais_recente, encoding='utf-8-sig', sep=';')
            return df

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None

@st.cache_data
def load_geocoded_data():
    """Carrega os dados geocodificados com informações de bairro"""
    try:
        # Procurar arquivo geocodificado mais recente
        arquivos_geo = glob.glob("locais_votacao_geocodificados_*.csv")

        if not arquivos_geo:
            return None

        # Usar o arquivo mais recente
        arquivo_geo = max(arquivos_geo, key=os.path.getmtime)
        df_geo = pd.read_csv(arquivo_geo, encoding='utf-8-sig')

        return df_geo
    except Exception as e:
        return None

def geocodificar_endereco(endereco, municipio, geolocator):
    """Geocodifica um endereço usando Nominatim"""
    endereco_completo = f"{endereco}, {municipio}, MG, Brasil"

    try:
        location = geolocator.geocode(endereco_completo, timeout=10)

        if location:
            return location.latitude, location.longitude
        else:
            # Tentar apenas com o município
            location = geolocator.geocode(f"{municipio}, MG, Brasil", timeout=10)
            if location:
                return location.latitude, location.longitude

        return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        st.warning(f"Erro ao geocodificar {endereco}: {str(e)}")
        return None, None

# Carregar dados
df = load_data()

# Carregar dados geocodificados com bairros
df_geo = load_geocoded_data()
if df_geo is not None and 'BAIRRO' in df_geo.columns:
    # Fazer merge para adicionar coluna de bairro aos dados principais
    df = df.merge(
        df_geo[['NR_LOCAL_VOTACAO', 'NM_MUNICIPIO', 'BAIRRO']],
        on=['NR_LOCAL_VOTACAO', 'NM_MUNICIPIO'],
        how='left'
    )
    st.success(f"✅ {len(df):,} registros carregados com sucesso! (com informações de bairro)")
else:
    st.success(f"✅ {len(df):,} registros carregados com sucesso!")

if df is not None:

    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")

    # Filtro por Cargo
    cargos_disponiveis = sorted(df['DS_CARGO'].unique())
    cargo_selecionado = st.sidebar.selectbox(
        "📌 Cargo:",
        cargos_disponiveis,
        index=cargos_disponiveis.index('PRESIDENTE') if 'PRESIDENTE' in cargos_disponiveis else 0
    )

    # Filtro por Turno
    turnos_disponiveis = sorted(df['NR_TURNO'].unique())
    turno_selecionado = st.sidebar.selectbox(
        "🗳️ Turno:",
        turnos_disponiveis,
        format_func=lambda x: f"{x}º Turno"
    )

    # Filtrar dados
    df_filtrado = df[
        (df['DS_CARGO'] == cargo_selecionado) &
        (df['NR_TURNO'] == turno_selecionado)
    ].copy()

    st.sidebar.info(f"**{len(df_filtrado):,}** registros após filtros")

    # Mostrar informações sobre o dataset
    with st.expander("ℹ️ Informações sobre os dados", expanded=False):
        st.write(f"**Cargo:** {cargo_selecionado}")
        st.write(f"**Turno:** {turno_selecionado}º")
        st.write(f"**Total de registros (agregados por local):** {len(df_filtrado):,}")
        st.write(f"**Municípios:** {df_filtrado['NM_MUNICIPIO'].nunique()}")
        st.write(f"**Zonas eleitorais:** {df_filtrado['NR_ZONA'].nunique()}")
        st.write(f"**Locais de votação únicos:** {df_filtrado['DS_LOCAL_VOTACAO_ENDERECO'].nunique() if 'DS_LOCAL_VOTACAO_ENDERECO' in df_filtrado.columns else 'N/A'}")
        st.write("**Primeiras linhas:**")
        st.dataframe(df_filtrado.head(10), use_container_width=True)

    # Tabs para organizar visualizações
    tab1, tab2 = st.tabs([
        "🗺️ Por Município",
        "🗺️ Mapa Interativo"
    ])

    with tab1:
        st.header("Resultados por Município")

        # Selecionar município
        municipios = sorted(df_filtrado['NM_MUNICIPIO'].unique())
        municipio_selecionado = st.selectbox("Selecione um município:", municipios)

        if municipio_selecionado:
            df_municipio = df_filtrado[df_filtrado['NM_MUNICIPIO'] == municipio_selecionado].copy()

            # Filtro por bairro (se disponível nos dados geocodificados)
            if 'BAIRRO' in df_municipio.columns:
                # Remover valores nulos e preencher com "Não especificado"
                df_municipio['BAIRRO'] = df_municipio['BAIRRO'].fillna('Não especificado')

                bairros_disponiveis = sorted(df_municipio['BAIRRO'].unique())
                bairros_selecionados = st.multiselect(
                    "🏘️ Filtrar por Bairro (opcional):",
                    options=bairros_disponiveis,
                    default=[]
                )

                # Aplicar filtro de bairro se selecionado
                if bairros_selecionados:
                    df_municipio = df_municipio[df_municipio['BAIRRO'].isin(bairros_selecionados)]
                    st.info(f"📍 Exibindo resultados de {len(bairros_selecionados)} bairro(s) selecionado(s)")

            votos_municipio = df_municipio.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().sort_values(ascending=False)

            # Remover nulos e brancos para visualização
            votos_municipio_validos = votos_municipio[~votos_municipio.index.isin(['#NULO#', '#BRANCO#'])]

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = px.bar(
                    x=votos_municipio_validos.head(15).index,
                    y=votos_municipio_validos.head(15).values,
                    title=f"Top 15 em {municipio_selecionado}",
                    labels={'x': 'Candidato', 'y': 'Votos'},
                    color=votos_municipio_validos.head(15).values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=500, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🏆 Ranking Completo")
                for i, (cand, votos) in enumerate(votos_municipio_validos.items(), 1):
                    if i <= 10:
                        st.write(f"**{i}º** {cand}: {votos:,.0f} votos")

                total_municipio = votos_municipio.sum()
                st.markdown("---")
                st.write(f"**Total de votos:** {total_municipio:,.0f}")
                st.write(f"**Zonas:** {df_municipio['NR_ZONA'].nunique()}")
                st.write(f"**Seções:** {df_municipio['NR_SECAO'].nunique()}")
                if 'BAIRRO' in df_municipio.columns:
                    bairros_count = df_municipio['BAIRRO'].nunique()
                    st.write(f"**Bairros:** {bairros_count}")

    with tab2:
        st.header("🗺️ Mapa Interativo - Locais de Votação")

        # Selecionar município para exibir
        municipios_mapa = sorted(df_filtrado['NM_MUNICIPIO'].unique())
        municipio_mapa = st.selectbox("Selecione um município para visualizar:", municipios_mapa, key='mun_mapa')

        # Filtrar dados do município
        df_municipio_mapa = df_filtrado[df_filtrado['NM_MUNICIPIO'] == municipio_mapa]

        # Extrair informações únicas dos locais
        # Incluir BAIRRO se disponível
        group_cols = ['NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']
        if 'BAIRRO' in df_municipio_mapa.columns:
            group_cols.append('BAIRRO')

        locais_info = df_municipio_mapa.groupby(group_cols).agg({
            'NR_SECAO': 'nunique',
            'QT_VOTOS': 'sum'
        }).reset_index()

        if 'BAIRRO' in group_cols:
            locais_info.columns = ['NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO', 'BAIRRO', 'QTD_SECOES', 'TOTAL_VOTOS']
        else:
            locais_info.columns = ['NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO', 'QTD_SECOES', 'TOTAL_VOTOS']

        # Tentar carregar cache de geocodificação
        cache_geo = None
        geocode_cache_dict = {}

        try:
            if os.path.exists('geocode_cache.csv'):
                cache_geo = pd.read_csv('geocode_cache.csv', encoding='utf-8')
                geocode_cache_dict = dict(zip(cache_geo['endereco'], zip(cache_geo['lat'], cache_geo['lon'])))
                st.success(f"✅ Cache carregado: {len(geocode_cache_dict)} endereços")
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar cache: {str(e)}")

        # Verificar quais locais não têm coordenadas
        locais_com_coords = []
        locais_sem_coords = []

        for idx, row in locais_info.iterrows():
            endereco_completo = f"{row['DS_LOCAL_VOTACAO_ENDERECO']}, {municipio_mapa}, MG, Brasil"

            if endereco_completo in geocode_cache_dict:
                lat, lon = geocode_cache_dict[endereco_completo]
                local_data = {
                    'nr_local': row['NR_LOCAL_VOTACAO'],
                    'nome': row['NM_LOCAL_VOTACAO'],
                    'endereco': row['DS_LOCAL_VOTACAO_ENDERECO'],
                    'secoes': row['QTD_SECOES'],
                    'votos': row['TOTAL_VOTOS'],
                    'lat': lat,
                    'lon': lon
                }
                # Adicionar bairro se disponível
                if 'BAIRRO' in row:
                    local_data['bairro'] = row['BAIRRO'] if pd.notna(row['BAIRRO']) else 'Não especificado'
                locais_com_coords.append(local_data)
            else:
                locais_sem_coords.append(row)

        # Mostrar status de geocodificação
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Locais com coordenadas", len(locais_com_coords))
        with col2:
            st.metric("Locais sem coordenadas", len(locais_sem_coords))

        # Botão para geocodificar locais faltantes
        if len(locais_sem_coords) > 0:
            st.warning(f"⚠️ {len(locais_sem_coords)} locais ainda não foram geocodificados.")

            if st.button(f"🌍 Geocodificar {len(locais_sem_coords)} locais automaticamente", key='geocode_btn'):
                geolocator = Nominatim(user_agent="app_eleicoes_mg", timeout=10)

                progress_bar = st.progress(0)
                status_text = st.empty()

                novos_geocodes = []

                for i, row in enumerate(locais_sem_coords):
                    status_text.text(f"Geocodificando {i+1}/{len(locais_sem_coords)}: {row['NM_LOCAL_VOTACAO']}")
                    progress_bar.progress((i + 1) / len(locais_sem_coords))

                    lat, lon = geocodificar_endereco(row['DS_LOCAL_VOTACAO_ENDERECO'], municipio_mapa, geolocator)

                    if lat and lon:
                        endereco_completo = f"{row['DS_LOCAL_VOTACAO_ENDERECO']}, {municipio_mapa}, MG, Brasil"

                        local_data = {
                            'nr_local': row['NR_LOCAL_VOTACAO'],
                            'nome': row['NM_LOCAL_VOTACAO'],
                            'endereco': row['DS_LOCAL_VOTACAO_ENDERECO'],
                            'secoes': row['QTD_SECOES'],
                            'votos': row['TOTAL_VOTOS'],
                            'lat': lat,
                            'lon': lon
                        }
                        # Adicionar bairro se disponível
                        if 'BAIRRO' in row:
                            local_data['bairro'] = row['BAIRRO'] if pd.notna(row['BAIRRO']) else 'Não especificado'
                        locais_com_coords.append(local_data)

                        novos_geocodes.append({
                            'endereco': endereco_completo,
                            'lat': lat,
                            'lon': lon
                        })

                    # Delay para respeitar limites da API
                    time.sleep(1.5)

                # Salvar novos geocodes no cache
                if novos_geocodes:
                    novos_df = pd.DataFrame(novos_geocodes)

                    if cache_geo is not None:
                        cache_atualizado = pd.concat([cache_geo, novos_df], ignore_index=True)
                    else:
                        cache_atualizado = novos_df

                    cache_atualizado.to_csv('geocode_cache.csv', index=False, encoding='utf-8')
                    st.success(f"✅ {len(novos_geocodes)} novos endereços geocodificados e salvos no cache!")

                status_text.empty()
                progress_bar.empty()
                st.rerun()

        # Criar e exibir mapa se houver locais com coordenadas
        if locais_com_coords:
                df_locais = pd.DataFrame(locais_com_coords)

                # Calcular centro do mapa (média das coordenadas)
                centro_lat = df_locais['lat'].mean()
                centro_lon = df_locais['lon'].mean()

                # Criar mapa
                m = folium.Map(
                    location=[centro_lat, centro_lon],
                    zoom_start=13,
                    tiles='OpenStreetMap'
                )

                # Criar cluster de marcadores
                marker_cluster = MarkerCluster(name="Locais de Votação").add_to(m)

                # Adicionar marcadores para cada local
                for idx, local in df_locais.iterrows():
                    # Calcular vencedor no local
                    df_local = df_municipio_mapa[df_municipio_mapa['NR_LOCAL_VOTACAO'] == local['nr_local']]
                    votos_local = df_local.groupby('NM_VOTAVEL')['QT_VOTOS'].sum()
                    votos_validos = votos_local[~votos_local.index.isin(['#NULO#', '#BRANCO#'])]

                    vencedor = "N/A"
                    votos_vencedor = 0
                    percentual = 0

                    if len(votos_validos) > 0:
                        vencedor = votos_validos.idxmax()
                        votos_vencedor = votos_validos.max()
                        percentual = (votos_vencedor / local['votos'] * 100) if local['votos'] > 0 else 0

                    # Popup com informações
                    bairro_info = ""
                    if 'bairro' in local and pd.notna(local.get('bairro')):
                        bairro_info = f'<p style="margin: 5px 0;"><b>Bairro:</b> {local["bairro"]}</p>'

                    popup_html = f"""
                    <div style="font-family: Arial; width: 300px;">
                        <h4 style="color: #2c3e50; margin-bottom: 10px;">{local['nome']}</h4>
                        <hr style="margin: 5px 0;">
                        <p style="margin: 5px 0;"><b>Endereco:</b><br>{local['endereco']}</p>
                        {bairro_info}
                        <p style="margin: 5px 0;"><b>Secoes:</b> {local['secoes']}</p>
                        <p style="margin: 5px 0;"><b>Total de Votos:</b> {local['votos']:,.0f}</p>
                        <hr style="margin: 5px 0;">
                        <p style="margin: 5px 0;"><b>1º Colocado ({cargo_selecionado}):</b><br>{vencedor}</p>
                        <p style="margin: 5px 0;"><b>Votos:</b> {votos_vencedor:,.0f} ({percentual:.1f}%)</p>
                    </div>
                    """

                    # Cor do marcador baseada na quantidade de seções
                    if local['secoes'] >= 10:
                        cor = 'red'
                    elif local['secoes'] >= 5:
                        cor = 'orange'
                    else:
                        cor = 'blue'

                    folium.Marker(
                        location=[local['lat'], local['lon']],
                        popup=folium.Popup(popup_html, max_width=320),
                        tooltip=f"{local['nome']} ({local['secoes']} seções)",
                        icon=folium.Icon(color=cor, icon='info-sign')
                    ).add_to(marker_cluster)

                # Adicionar legenda
                st.info(f"💡 **Dica:** Clique nos marcadores para ver detalhes. Cores: 🔵 Azul (1-4 seções) | 🟠 Laranja (5-9 seções) | 🔴 Vermelho (10+ seções)")

                # Exibir mapa
                st_folium(m, width=1200, height=600)

                # Estatísticas do mapa
                st.subheader(f"📊 Estatísticas - {municipio_mapa}")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Locais de Votação", len(df_locais))
                with col2:
                    st.metric("Total de Seções", int(df_locais['secoes'].sum()))
                with col3:
                    st.metric("Total de Votos", f"{int(df_locais['votos'].sum()):,}")
                with col4:
                    media_secoes = df_locais['secoes'].mean()
                    st.metric("Média Seções/Local", f"{media_secoes:.1f}")

                # Tabela com detalhes dos locais
                st.subheader("📋 Detalhes dos Locais de Votação")

                # Preparar dados para exibição
                cols_exibir = ['nome', 'endereco']
                col_names = ['Local', 'Endereço']

                # Incluir bairro se disponível
                if 'bairro' in df_locais.columns:
                    cols_exibir.append('bairro')
                    col_names.append('Bairro')

                cols_exibir.extend(['secoes', 'votos'])
                col_names.extend(['Seções', 'Total Votos'])

                df_exibir = df_locais[cols_exibir].copy()
                df_exibir.columns = col_names
                df_exibir = df_exibir.sort_values('Seções', ascending=False)

                st.dataframe(df_exibir, use_container_width=True, height=300)

        else:
            st.info("📍 Nenhum local geocodificado ainda. Use o botão acima para geocodificar automaticamente.")

# Footer
st.markdown("---")

# Mostrar nome do arquivo sendo usado
arquivos = glob.glob(DATA_FILE)
if arquivos:
    arquivo_atual = os.path.basename(max(arquivos, key=os.path.getmtime))
    st.markdown(f"**Arquivo de dados:** `{arquivo_atual}`")

st.markdown("""
**Fonte original:** Tribunal Superior Eleitoral (TSE)
**URL:** https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_MG.zip
**Estado:** Minas Gerais (MG)
**Municípios:** Dados filtrados para municípios selecionados
**Detalhamento:** Votação por seção eleitoral
""")
