import pandas as pd
import requests
import time
import json
import glob
import os
from datetime import datetime

# API de geocodificação
GEOCODE_API = "https://geocode.maps.co/search"

print("="*80)
print("GEOCODIFICACAO DE LOCAIS DE VOTACAO")
print("="*80)

# Carregar dados agregados
print("\n[1/4] Carregando dados agregados...")

# Buscar arquivo agregado mais recente
DATA_FILE_PATTERN = "eleicoes_2022_mg_filtrados_*_agregado.csv"
arquivos = glob.glob(DATA_FILE_PATTERN)

if not arquivos:
    print(f"[ERRO] Nenhum arquivo agregado encontrado com o padrão: {DATA_FILE_PATTERN}")
    print("Execute o script 'filtrar_municipios_stream.py' primeiro para gerar os dados agregados.")
    exit(1)

# Usar o arquivo mais recente
arquivo_mais_recente = max(arquivos, key=os.path.getmtime)
print(f"Usando arquivo: {os.path.basename(arquivo_mais_recente)}")

df = pd.read_csv(arquivo_mais_recente, sep=';', encoding='utf-8-sig')
print(f"Total de registros: {len(df):,}")

# Identificar locais únicos
print("\n[2/4] Identificando locais de votacao unicos...")
df_locais = df[['NM_MUNICIPIO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO', 'NR_LOCAL_VOTACAO']].drop_duplicates()
print(f"Locais unicos: {len(df_locais):,}")

# Criar arquivo de cache se não existir
cache_file = 'geocode_cache.json'
try:
    with open(cache_file, 'r', encoding='utf-8') as f:
        geocode_cache = json.load(f)
    print(f"Cache carregado: {len(geocode_cache)} enderecos")
except FileNotFoundError:
    geocode_cache = {}
    print("Criando novo cache de geocodificacao")

print("\n[3/4] Geocodificando enderecos...")
print("IMPORTANTE: API gratuita tem limite de requisicoes. Processando devagar...")

resultados = []
total = len(df_locais)
processados = 0
novos_geocodes = 0
erros = 0

for idx, row in df_locais.iterrows():
    processados += 1

    # Criar chave de cache
    endereco_completo = f"{row['DS_LOCAL_VOTACAO_ENDERECO']}, {row['NM_MUNICIPIO']}, MG, Brasil"
    cache_key = f"{row['NR_LOCAL_VOTACAO']}_{row['NM_MUNICIPIO']}"

    # Verificar cache
    if cache_key in geocode_cache:
        coords = geocode_cache[cache_key]
        resultados.append({
            'NR_LOCAL_VOTACAO': row['NR_LOCAL_VOTACAO'],
            'NM_MUNICIPIO': row['NM_MUNICIPIO'],
            'NM_LOCAL_VOTACAO': row['NM_LOCAL_VOTACAO'],
            'DS_LOCAL_VOTACAO_ENDERECO': row['DS_LOCAL_VOTACAO_ENDERECO'],
            'BAIRRO': coords.get('bairro', 'Não especificado'),
            'latitude': coords['lat'],
            'longitude': coords['lon'],
            'fonte': 'cache'
        })
        if processados % 50 == 0:
            print(f"  [{processados}/{total}] {row['NM_MUNICIPIO']} - {row['NM_LOCAL_VOTACAO'][:50]}... (cache)")
        continue

    try:
        # Geocodificar usando API
        params = {
            'q': endereco_completo,
            'format': 'json',
            'limit': 1
        }

        response = requests.get(GEOCODE_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])

            # Extrair bairro do address (neighbourhood, suburb, ou quarter)
            address = data[0].get('address', {})
            bairro = (address.get('neighbourhood') or
                     address.get('suburb') or
                     address.get('quarter') or
                     address.get('city_district') or
                     'Não especificado')

            # Salvar em cache
            geocode_cache[cache_key] = {'lat': lat, 'lon': lon, 'bairro': bairro}

            resultados.append({
                'NR_LOCAL_VOTACAO': row['NR_LOCAL_VOTACAO'],
                'NM_MUNICIPIO': row['NM_MUNICIPIO'],
                'NM_LOCAL_VOTACAO': row['NM_LOCAL_VOTACAO'],
                'DS_LOCAL_VOTACAO_ENDERECO': row['DS_LOCAL_VOTACAO_ENDERECO'],
                'BAIRRO': bairro,
                'latitude': lat,
                'longitude': lon,
                'fonte': 'api'
            })

            novos_geocodes += 1
            print(f"  [{processados}/{total}] OK: {row['NM_MUNICIPIO']} - {row['NM_LOCAL_VOTACAO'][:40]}... ({lat:.6f}, {lon:.6f}) - Bairro: {bairro}")

            # Salvar cache a cada 10 novos geocodes
            if novos_geocodes % 10 == 0:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(geocode_cache, f, ensure_ascii=False, indent=2)
                print(f"  -> Cache salvo ({len(geocode_cache)} enderecos)")

            # Aguardar para não ultrapassar limite da API (1 req/segundo para API gratuita)
            time.sleep(1.5)
        else:
            print(f"  [{processados}/{total}] SKIP: {row['NM_MUNICIPIO']} - Sem resultado")
            erros += 1

    except Exception as e:
        print(f"  [{processados}/{total}] ERRO: {row['NM_MUNICIPIO']} - {str(e)[:50]}")
        erros += 1
        time.sleep(2)

    # Pausar a cada 50 requisições
    if novos_geocodes > 0 and novos_geocodes % 50 == 0:
        print(f"\n  >> Pausando 10 segundos para respeitar limite da API...\n")
        time.sleep(10)

# Salvar cache final
print("\nSalvando cache final...")
with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(geocode_cache, f, ensure_ascii=False, indent=2)

print("\n[4/4] Salvando resultados...")
df_geo = pd.DataFrame(resultados)

if len(df_geo) > 0:
    output_file = f"locais_votacao_geocodificados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_geo.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("\n" + "="*80)
    print("ESTATISTICAS")
    print("="*80)
    print(f"\nTotal de locais processados: {processados}")
    print(f"Geocodificados com sucesso: {len(df_geo)}")
    print(f"Novos geocodes (API): {novos_geocodes}")
    print(f"Do cache: {len(df_geo) - novos_geocodes}")
    print(f"Erros/Skips: {erros}")

    print(f"\nMunicipios geocodificados:")
    for mun, count in df_geo['NM_MUNICIPIO'].value_counts().items():
        print(f"  - {mun}: {count} locais")

    print("\n" + "="*80)
    print("CONCLUIDO!")
    print("="*80)
    print(f"\nArquivo gerado: {output_file}")
    print(f"Cache salvo: {cache_file}")
    print("\nUse estes dados no aplicativo Streamlit para visualizar o mapa.")
else:
    print("\n[ERRO] Nenhum local foi geocodificado com sucesso!")
