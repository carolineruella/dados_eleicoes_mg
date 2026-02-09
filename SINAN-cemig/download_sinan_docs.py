"""
Script para baixar documentacao do SINAN do FTP do DATASUS
"""
import urllib.request
import zipfile
import os
from pathlib import Path

# URL do arquivo
FTP_URL = "ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DOCS/Docs_TAB_SINAN.zip"

# Diretorio de destino
DOCS_DIR = Path("sinan_docs")
DOCS_DIR.mkdir(exist_ok=True)

# Arquivo ZIP local
ZIP_FILE = DOCS_DIR / "Docs_TAB_SINAN.zip"

print("[DOWNLOAD] Baixando documentacao do SINAN...")
print(f"URL: {FTP_URL}")
print(f"Destino: {ZIP_FILE}")

try:
    # Download do arquivo
    urllib.request.urlretrieve(FTP_URL, ZIP_FILE)
    print(f"[OK] Download concluido: {ZIP_FILE.stat().st_size / 1024 / 1024:.2f} MB")

    # Extrair o ZIP
    print("\n[EXTRAINDO] Descompactando arquivos...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(DOCS_DIR)

    # Listar arquivos extraidos
    print("\n[ARQUIVOS] Lista de arquivos extraidos:")
    for file in sorted(DOCS_DIR.rglob("*")):
        if file.is_file() and file.name != "Docs_TAB_SINAN.zip":
            size = file.stat().st_size
            if size > 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.2f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size} bytes"
            print(f"  - {file.name} ({size_str})")

    print(f"\n[SUCESSO] Documentacao extraida em: {DOCS_DIR.absolute()}")

except Exception as e:
    print(f"[ERRO] {e}")
    print("\nDica: Verifique sua conexao com a internet e tente novamente.")
