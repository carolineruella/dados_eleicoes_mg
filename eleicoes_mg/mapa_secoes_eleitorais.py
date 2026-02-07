import pandas as pd
import folium
from folium.plugins import MarkerCluster
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import os

print("="*80)
print("MAPA INTERATIVO - LOCAIS DE VOTAÇÃO")
print("="*80)

# Configuração
CSV_FILE = "eleicoes_2022_mg_filtrados_20260207_130650.csv"
OUTPUT_MAP = "mapa_secoes_eleitorais.html"
CACHE_FILE = "geocode_cache.csv"

# Verificar se o arquivo existe
if not os.path.exists(CSV_FILE):
    print(f"\n[ERRO] Arquivo não encontrado: {CSV_FILE}")
    exit(1)

print(f"\n[1/5] Lendo dados do CSV...")
df = pd.read_csv(CSV_FILE, sep=';', encoding='utf-8-sig')
print(f"  Total de registros: {len(df):,}")

# Extrair locais únicos
print(f"\n[2/5] Extraindo locais únicos de votação...")
locais = df[['NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']].drop_duplicates()
print(f"  Locais únicos: {len(locais)}")

# Contar seções por local
secoes_por_local = df.groupby('NR_LOCAL_VOTACAO')['NR_SECAO'].nunique().to_dict()

# Adicionar contagem de seções
locais['QTD_SECOES'] = locais['NR_LOCAL_VOTACAO'].map(secoes_por_local)

# Carregar cache de geocodificação se existir
geocode_cache = {}
if os.path.exists(CACHE_FILE):
    print(f"\n[3/5] Carregando cache de geocodificação...")
    cache_df = pd.read_csv(CACHE_FILE, encoding='utf-8')
    geocode_cache = dict(zip(cache_df['endereco'], zip(cache_df['lat'], cache_df['lon'])))
    print(f"  Endereços em cache: {len(geocode_cache)}")
else:
    print(f"\n[3/5] Iniciando geocodificação...")

# Geocodificação
geolocator = Nominatim(user_agent="mapa_secoes_eleitorais", timeout=10)
coordenadas = []
novos_geocodes = []

for idx, row in locais.iterrows():
    endereco_completo = f"{row['DS_LOCAL_VOTACAO_ENDERECO']}, Passos, MG, Brasil"

    # Verificar cache
    if endereco_completo in geocode_cache:
        lat, lon = geocode_cache[endereco_completo]
        coordenadas.append({'lat': lat, 'lon': lon})
        continue

    print(f"  [{idx+1}/{len(locais)}] Geocodificando: {row['NM_LOCAL_VOTACAO']}")

    try:
        location = geolocator.geocode(endereco_completo)

        if location:
            coordenadas.append({'lat': location.latitude, 'lon': location.longitude})
            novos_geocodes.append({
                'endereco': endereco_completo,
                'lat': location.latitude,
                'lon': location.longitude
            })
            print(f"      [OK] Encontrado: {location.latitude:.6f}, {location.longitude:.6f}")
        else:
            # Tentar apenas com o nome do local
            print(f"      [AVISO] Nao encontrado, tentando com nome...")
            location = geolocator.geocode(f"{row['NM_LOCAL_VOTACAO']}, Passos, MG, Brasil")

            if location:
                coordenadas.append({'lat': location.latitude, 'lon': location.longitude})
                novos_geocodes.append({
                    'endereco': endereco_completo,
                    'lat': location.latitude,
                    'lon': location.longitude
                })
                print(f"      [OK] Encontrado: {location.latitude:.6f}, {location.longitude:.6f}")
            else:
                # Usar coordenadas padrão de Passos
                coordenadas.append({'lat': -20.7189, 'lon': -46.6097})
                novos_geocodes.append({
                    'endereco': endereco_completo,
                    'lat': -20.7189,
                    'lon': -46.6097
                })
                print(f"      [ERRO] Usando coordenadas padrao de Passos")

        # Delay para evitar rate limit
        time.sleep(1.5)

    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"      [ERRO] Erro: {e}")
        coordenadas.append({'lat': -20.7189, 'lon': -46.6097})
        novos_geocodes.append({
            'endereco': endereco_completo,
            'lat': -20.7189,
            'lon': -46.6097
        })

# Salvar novos geocodes no cache
if novos_geocodes:
    print(f"\n[4/5] Salvando cache de geocodificação...")
    novos_df = pd.DataFrame(novos_geocodes)

    if os.path.exists(CACHE_FILE):
        cache_existente = pd.read_csv(CACHE_FILE, encoding='utf-8')
        cache_atualizado = pd.concat([cache_existente, novos_df], ignore_index=True)
    else:
        cache_atualizado = novos_df

    cache_atualizado.to_csv(CACHE_FILE, index=False, encoding='utf-8')
    print(f"  Novos endereços salvos: {len(novos_geocodes)}")

# Adicionar coordenadas ao dataframe
locais['lat'] = [c['lat'] for c in coordenadas]
locais['lon'] = [c['lon'] for c in coordenadas]

# Criar mapa
print(f"\n[5/5] Criando mapa interativo...")
# Centro em Passos, MG
mapa = folium.Map(
    location=[-20.7189, -46.6097],
    zoom_start=13,
    tiles='OpenStreetMap'
)

# Adicionar cluster de marcadores
marker_cluster = MarkerCluster(name="Locais de Votação").add_to(mapa)

# Adicionar marcadores
for idx, row in locais.iterrows():
    # Criar popup com informações
    popup_html = f"""
    <div style="font-family: Arial; width: 300px;">
        <h4 style="color: #2c3e50; margin-bottom: 10px;">{row['NM_LOCAL_VOTACAO']}</h4>
        <hr style="margin: 5px 0;">
        <p style="margin: 5px 0;"><b>Endereco:</b><br>{row['DS_LOCAL_VOTACAO_ENDERECO']}</p>
        <p style="margin: 5px 0;"><b>Secoes:</b> {row['QTD_SECOES']}</p>
        <p style="margin: 5px 0;"><b>Codigo Local:</b> {row['NR_LOCAL_VOTACAO']}</p>
    </div>
    """

    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['NM_LOCAL_VOTACAO'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# Salvar mapa
mapa.save(OUTPUT_MAP)

print("\n" + "="*80)
print("MAPA CRIADO COM SUCESSO!")
print("="*80)
print(f"\nArquivo gerado: {OUTPUT_MAP}")
print(f"Locais de votação: {len(locais)}")
print(f"Total de seções: {df['NR_SECAO'].nunique()}")
print(f"\nAbra o arquivo {OUTPUT_MAP} no navegador para visualizar o mapa.")
print("="*80)
