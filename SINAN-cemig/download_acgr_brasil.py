"""
Script para baixar arquivos DBC de Acidentes de Trabalho Graves (ACGR) do Brasil
Dados preliminares do SINAN - Anos 2020 a 2025
"""
import urllib.request
import os
from pathlib import Path

# Base URL do FTP DATASUS
BASE_URL = "ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/PRELIM/"

# Arquivos a baixar (ACGR = Acidentes de Trabalho Graves, BR = Brasil)
ARQUIVOS = [
    "ACGRBR20.dbc",  # 2020
    "ACGRBR21.dbc",  # 2021
    "ACGRBR22.dbc",  # 2022
    "ACGRBR23.dbc",  # 2023
    "ACGRBR24.dbc",  # 2024
    "ACGRBR25.dbc",  # 2025
]

# Diretorio de destino
DEST_DIR = Path("data/dbc_files")
DEST_DIR.mkdir(parents=True, exist_ok=True)

def download_arquivo(arquivo):
    """Download de um arquivo DBC"""
    url = BASE_URL + arquivo
    destino = DEST_DIR / arquivo

    print(f"\n[DOWNLOAD] {arquivo}")
    print(f"  URL: {url}")
    print(f"  Destino: {destino}")

    try:
        # Download
        print(f"  [AGUARDE] Baixando...")
        urllib.request.urlretrieve(url, destino)

        # Verificar tamanho
        tamanho = destino.stat().st_size
        if tamanho > 1024 * 1024:
            tamanho_str = f"{tamanho / 1024 / 1024:.2f} MB"
        elif tamanho > 1024:
            tamanho_str = f"{tamanho / 1024:.2f} KB"
        else:
            tamanho_str = f"{tamanho} bytes"

        print(f"  [OK] Concluido: {tamanho_str}")
        return True

    except urllib.error.URLError as e:
        print(f"  [ERRO] URL nao encontrada: {e}")
        return False
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False

def main():
    print("="*70)
    print("DOWNLOAD DE DADOS SINAN - ACIDENTES DE TRABALHO GRAVES (BRASIL)")
    print("="*70)
    print(f"\nDados preliminares - Anos 2020 a 2025")
    print(f"Destino: {DEST_DIR.absolute()}\n")
    print("="*70)

    sucessos = 0
    falhas = 0

    for arquivo in ARQUIVOS:
        if download_arquivo(arquivo):
            sucessos += 1
        else:
            falhas += 1

    # Resumo
    print(f"\n{'='*70}")
    print("RESUMO DO DOWNLOAD")
    print(f"{'='*70}")
    print(f"  ✅ Sucesso: {sucessos}/{len(ARQUIVOS)}")
    print(f"  ❌ Falhas: {falhas}/{len(ARQUIVOS)}")

    if sucessos > 0:
        print(f"\n[INFO] Arquivos salvos em: {DEST_DIR.absolute()}")
        print("\n[PROXIMO PASSO] Converter DBC para CSV:")
        print("\nOpcao 1 - Usar TabWin (Interface Grafica):")
        print("  1. Abra: tabwin/TabWin415.exe")
        print("  2. Arquivo > Abrir > Selecione o .dbc")
        print("  3. Arquivo > Salvar Como > CSV")
        print("\nOpcao 2 - Usar dbf2dbc (Linha de Comando):")
        print("  cd tabwin")
        print(f"  dbf2dbc.exe {DEST_DIR.absolute()}\\ACGRBR20.dbc output.dbf")
        print("\nOpcao 3 - Tentar biblioteca Python (experimental):")
        print("  pip install dbfread")
        print("  # Primeiro precisa converter DBC -> DBF com dbf2dbc.exe")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
