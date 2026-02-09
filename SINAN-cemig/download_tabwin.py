"""
Script para baixar o TabWin - Software oficial do DATASUS
TabWin e usado para converter arquivos .dbc para CSV e outros formatos
"""
import urllib.request
import zipfile
from pathlib import Path

# URL do TabWin
TABWIN_URL = "ftp://ftp.datasus.gov.br/tabwin/tabwin/TAB415.zip"

# Diretorio de destino
TABWIN_DIR = Path("tabwin")
TABWIN_DIR.mkdir(exist_ok=True)

# Arquivo ZIP local
ZIP_FILE = TABWIN_DIR / "TAB415.zip"

print("="*60)
print("DOWNLOAD TABWIN - Software Oficial DATASUS")
print("="*60)
print("\nTabWin e o software oficial do DATASUS para:")
print("  - Processar arquivos .dbc (DBF comprimido)")
print("  - Converter DBC para CSV, DBF, XLS")
print("  - Realizar tabulacoes de dados")
print("\n" + "="*60 + "\n")

print("[DOWNLOAD] Baixando TabWin...")
print(f"URL: {TABWIN_URL}")
print(f"Destino: {ZIP_FILE}")

try:
    # Download do arquivo
    print("\n[AGUARDE] Fazendo download... (pode demorar alguns minutos)")
    urllib.request.urlretrieve(TABWIN_URL, ZIP_FILE)

    tamanho = ZIP_FILE.stat().st_size / 1024 / 1024
    print(f"[OK] Download concluido: {tamanho:.2f} MB")

    # Extrair o ZIP
    print("\n[EXTRAINDO] Descompactando arquivos...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(TABWIN_DIR)

    # Listar arquivos extraidos
    print("\n[ARQUIVOS] Conteudo extraido:")
    arquivos = list(TABWIN_DIR.rglob("*"))
    executaveis = []

    for arquivo in sorted(arquivos):
        if arquivo.is_file() and arquivo.name != "TAB415.zip":
            size = arquivo.stat().st_size
            if size > 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.2f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size} bytes"

            print(f"  - {arquivo.name} ({size_str})")

            if arquivo.suffix.lower() == '.exe':
                executaveis.append(arquivo)

    print(f"\n[SUCESSO] TabWin extraido em: {TABWIN_DIR.absolute()}")

    if executaveis:
        print("\n" + "="*60)
        print("COMO USAR O TABWIN:")
        print("="*60)
        print("\n1. Execute o arquivo:")
        for exe in executaveis:
            print(f"   {exe.absolute()}")

        print("\n2. No TabWin:")
        print("   - Arquivo > Abrir > Selecione um arquivo .dbc")
        print("   - Arquivo > Salvar como > Escolha formato (CSV, DBF, XLS)")

        print("\n3. Para converter DBC para CSV via linha de comando:")
        print("   (Se o TabWin suportar modo batch)")

        print("\n" + "="*60)
        print("DICA: Mantenha o TabWin instalado para trabalhar com")
        print("      arquivos .dbc do DATASUS de forma rapida e confiavel")
        print("="*60)

except Exception as e:
    print(f"\n[ERRO] {e}")
    print("\nPossiveis causas:")
    print("  - Problemas de conexao com o FTP")
    print("  - Arquivo nao disponivel no servidor")
    print("  - Restricoes de firewall")

    print("\nAlternativa:")
    print("  1. Acesse manualmente: ftp://ftp.datasus.gov.br/tabwin/tabwin/")
    print("  2. Baixe o arquivo TAB415.zip")
    print("  3. Extraia na pasta 'tabwin'")
