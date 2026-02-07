import requests
import zipfile
import csv
import io
from datetime import datetime
from collections import defaultdict

# Lista de municípios para filtrar (normalizados - sem acentos)
'''MUNICIPIOS_FILTRAR = {
    'BELO HORIZONTE',
    'RIBEIRAO DAS NEVES',
    'SABARA',
    'CONTAGEM',
    'NOVA LIMA',
    'SAO JOAQUIM DE BICAS',
    'JUIZ DE FORA',
    'BARBACENA',
    'SAO JOAO DEL REI',
    'PASSOS',
    'PEDRALVA',
    'UBERLANDIA',
    'GOVERNADOR VALADARES',
    'MONTES CLAROS',
    'TEOFILO OTONI',
    'PIRAPORA',
    'VICOSA',
    'CAMPO DO MEIO',
    'ARACUAI',
    'PATOS DE MINAS',
    'ARAXA',
    'IPATINGA',
    'CONGONHAS',
    'SERRO',
    'CONCEICAO DO MATO DENTRO',
    'SANTA BARBARA',
    'ALMENARA',
    'FELISBURGO'
}'''

MUNICIPIOS_FILTRAR = {
    'PASSOS'}

print("="*80)
print("FILTRO DE DADOS ELEITORAIS - TSE 2022")
print("="*80)
print(f"\nMunicipios a filtrar: {len(MUNICIPIOS_FILTRAR)}")

# URL dos dados
DATA_URL = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_MG.zip"
OUTPUT_FILE = f"eleicoes_2022_mg_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print("\n" + "="*80)
print("Baixando e processando arquivo (streaming)...")
print("="*80)

try:
    # Download com streaming
    print("[1/4] Iniciando download...")
    response = requests.get(DATA_URL, stream=True, timeout=180)
    response.raise_for_status()

    # Salvar ZIP temporariamente
    print("[2/4] Salvando arquivo temporario...")
    zip_path = "temp_votacao.zip"
    total_size = 0
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            total_size += len(chunk)
            if total_size % (10 * 1024 * 1024) == 0:  # A cada 10MB
                print(f"  Baixados: {total_size / 1024 / 1024:.1f} MB")

    print(f"[OK] Download concluido: {total_size / 1024 / 1024:.2f} MB")

    # Processar ZIP
    print("[3/4] Extraindo e filtrando dados...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        csv_file = [f for f in zf.namelist() if f.endswith('.csv')][0]
        print(f"  Processando: {csv_file}")

        with zf.open(csv_file) as csvf:
            # Ler como texto
            text_file = io.TextIOWrapper(csvf, encoding='latin-1')
            reader = csv.DictReader(text_file, delimiter=';')

            # Criar arquivo de saida
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as outf:
                writer = None
                total_linhas = 0
                linhas_filtradas = 0
                municipios_encontrados = set()

                for row in reader:
                    total_linhas += 1

                    # Verificar se o municipio esta na lista
                    if row['NM_MUNICIPIO'] in MUNICIPIOS_FILTRAR:
                        # Criar writer na primeira linha filtrada
                        if writer is None:
                            writer = csv.DictWriter(outf, fieldnames=reader.fieldnames, delimiter=';')
                            writer.writeheader()

                        writer.writerow(row)
                        linhas_filtradas += 1
                        municipios_encontrados.add(row['NM_MUNICIPIO'])

                    # Progresso a cada 100k linhas
                    if total_linhas % 100000 == 0:
                        print(f"  Processadas: {total_linhas:,} | Filtradas: {linhas_filtradas:,}")

    print(f"[OK] Total processado: {total_linhas:,} linhas")
    print(f"[OK] Total filtrado: {linhas_filtradas:,} linhas")
    print(f"[OK] Municipios encontrados: {len(municipios_encontrados)}")

    # Limpar arquivo temporario
    print("[4/4] Limpando arquivos temporarios...")
    import os
    os.remove(zip_path)

    # AGREGAÇÃO DOS DADOS POR ENDEREÇO E CANDIDATO
    print("\n" + "="*80)
    print("[5/5] Agregando dados por endereço e candidato...")
    print("="*80)

    # Ler o arquivo filtrado e agregar
    agregacao = defaultdict(lambda: defaultdict(int))
    linhas_originais = {}  # Para manter os outros campos

    with open(OUTPUT_FILE, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = reader.fieldnames

        for row in reader:
            # Chave de agrupamento: endereço + candidato
            endereco = row.get('DS_LOCAL_VOTACAO_ENDERECO', '')
            candidato = row.get('NM_VOTAVEL', '')
            numero = row.get('NR_VOTAVEL', '')
            municipio = row.get('NM_MUNICIPIO', '')

            chave = (endereco, candidato, numero, municipio)

            # Somar votos
            votos = int(row.get('QT_VOTOS', 0))
            agregacao[chave]['QT_VOTOS'] += votos

            # Guardar a primeira linha para manter outros campos
            if chave not in linhas_originais:
                linhas_originais[chave] = row.copy()

    # Salvar arquivo agregado
    OUTPUT_FILE_AGREGADO = OUTPUT_FILE.replace('.csv', '_agregado.csv')

    with open(OUTPUT_FILE_AGREGADO, 'w', newline='', encoding='utf-8-sig') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        linhas_agregadas = 0
        for chave, valores in sorted(agregacao.items()):
            row_original = linhas_originais[chave].copy()
            row_original['QT_VOTOS'] = str(valores['QT_VOTOS'])
            writer.writerow(row_original)
            linhas_agregadas += 1

    print(f"[OK] Linhas originais: {linhas_filtradas:,}")
    print(f"[OK] Linhas agregadas: {linhas_agregadas:,}")
    print(f"[OK] Redução: {linhas_filtradas - linhas_agregadas:,} linhas ({(1 - linhas_agregadas/linhas_filtradas)*100:.1f}%)")

    print("\n" + "="*80)
    print("RESULTADO")
    print("="*80)
    print(f"\nMunicipios encontrados ({len(municipios_encontrados)}):")
    for mun in sorted(municipios_encontrados):
        print(f"  [OK] {mun}")

    nao_encontrados = MUNICIPIOS_FILTRAR - municipios_encontrados
    if nao_encontrados:
        print(f"\nMunicipios NAO encontrados ({len(nao_encontrados)}):")
        for mun in sorted(nao_encontrados):
            print(f"  [X] {mun}")

    print("\n" + "="*80)
    print("[OK] PROCESSO CONCLUIDO!")
    print("="*80)
    print(f"\nArquivo filtrado: {OUTPUT_FILE}")
    print(f"Linhas: {linhas_filtradas:,}")
    print(f"\nArquivo agregado: {OUTPUT_FILE_AGREGADO}")
    print(f"Linhas: {linhas_agregadas:,}")

except Exception as e:
    print(f"\n[ERRO] {e}")
    import traceback
    traceback.print_exc()
