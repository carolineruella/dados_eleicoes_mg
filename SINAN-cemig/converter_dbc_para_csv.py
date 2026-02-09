"""
Script para converter arquivos DBC (DATASUS) para CSV
Usa o dbf2dbc.exe do TabWin e dbfread para conversao
"""
import subprocess
import os
from pathlib import Path
import sys

# Caminhos
DBC_DIR = Path("data/dbc_files")
DBF_DIR = Path("data/dbf_files")
CSV_DIR = Path("data/csv_files")
TABWIN_DIR = Path("tabwin")
DBF2DBC_EXE = TABWIN_DIR / "dbf2dbc.exe"

# Criar diretorios
DBF_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)

def converter_dbc_para_dbf(arquivo_dbc):
    """
    Converte DBC para DBF usando dbf2dbc.exe do TabWin
    """
    arquivo_dbc = Path(arquivo_dbc)
    arquivo_dbf = DBF_DIR / arquivo_dbc.name.replace('.dbc', '.dbf')

    print(f"\n[PASSO 1] Convertendo DBC -> DBF")
    print(f"  Origem: {arquivo_dbc.name}")
    print(f"  Destino: {arquivo_dbf.name}")

    if not DBF2DBC_EXE.exists():
        print(f"  [ERRO] dbf2dbc.exe nao encontrado em: {DBF2DBC_EXE}")
        print(f"  Execute: python download_tabwin.py")
        return None

    try:
        # Executar dbf2dbc.exe
        # Sintaxe: dbf2dbc.exe <arquivo.dbc> <arquivo.dbf>
        cmd = [str(DBF2DBC_EXE), str(arquivo_dbc.absolute()), str(arquivo_dbf.absolute())]

        print(f"  [EXECUTANDO] {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=TABWIN_DIR)

        if arquivo_dbf.exists():
            tamanho = arquivo_dbf.stat().st_size / 1024 / 1024
            print(f"  [OK] DBF criado: {tamanho:.2f} MB")
            return arquivo_dbf
        else:
            print(f"  [ERRO] Arquivo DBF nao foi criado")
            if result.stdout:
                print(f"  STDOUT: {result.stdout}")
            if result.stderr:
                print(f"  STDERR: {result.stderr}")
            return None

    except Exception as e:
        print(f"  [ERRO] {e}")
        return None

def converter_dbf_para_csv(arquivo_dbf):
    """
    Converte DBF para CSV usando dbfread
    """
    arquivo_dbf = Path(arquivo_dbf)
    arquivo_csv = CSV_DIR / arquivo_dbf.name.replace('.dbf', '.csv')

    print(f"\n[PASSO 2] Convertendo DBF -> CSV")
    print(f"  Origem: {arquivo_dbf.name}")
    print(f"  Destino: {arquivo_csv.name}")

    try:
        # Tentar importar dbfread
        try:
            from dbfread import DBF
            import pandas as pd
        except ImportError:
            print(f"  [ERRO] Biblioteca 'dbfread' nao instalada")
            print(f"  Instale com: pip install dbfread")
            return None

        # Ler DBF
        print(f"  [LENDO] Arquivo DBF...")
        table = DBF(str(arquivo_dbf), encoding='latin-1', char_decode_errors='ignore')

        # Converter para DataFrame
        print(f"  [CONVERTENDO] Para DataFrame...")
        df = pd.DataFrame(iter(table))

        print(f"  [INFO] {len(df):,} registros, {len(df.columns)} colunas")

        # Salvar CSV
        print(f"  [SALVANDO] CSV...")
        df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')

        tamanho = arquivo_csv.stat().st_size / 1024 / 1024
        print(f"  [OK] CSV criado: {tamanho:.2f} MB")

        # Mostrar primeiras colunas
        print(f"  [COLUNAS] {', '.join(df.columns.tolist()[:10])}{'...' if len(df.columns) > 10 else ''}")

        return arquivo_csv

    except Exception as e:
        print(f"  [ERRO] {e}")
        return None

def converter_arquivo(arquivo_dbc):
    """
    Pipeline completo: DBC -> DBF -> CSV
    """
    print(f"\n{'='*70}")
    print(f"CONVERTENDO: {arquivo_dbc.name}")
    print(f"{'='*70}")

    # Passo 1: DBC -> DBF
    arquivo_dbf = converter_dbc_para_dbf(arquivo_dbc)
    if not arquivo_dbf:
        return None

    # Passo 2: DBF -> CSV
    arquivo_csv = converter_dbf_para_csv(arquivo_dbf)
    if not arquivo_csv:
        return None

    print(f"\n[SUCESSO] CSV final: {arquivo_csv}")
    return arquivo_csv

def processar_todos_dbc():
    """
    Processa todos os arquivos DBC na pasta
    """
    arquivos_dbc = list(DBC_DIR.glob("*.dbc"))

    if not arquivos_dbc:
        print(f"[ERRO] Nenhum arquivo DBC encontrado em: {DBC_DIR}")
        return

    print(f"{'='*70}")
    print(f"CONVERSOR DBC -> CSV (DATASUS)")
    print(f"{'='*70}")
    print(f"\nEncontrados {len(arquivos_dbc)} arquivos DBC")
    print(f"Origem: {DBC_DIR.absolute()}")
    print(f"Destino: {CSV_DIR.absolute()}\n")

    sucessos = []
    falhas = []

    for arquivo_dbc in sorted(arquivos_dbc):
        resultado = converter_arquivo(arquivo_dbc)
        if resultado:
            sucessos.append(resultado)
        else:
            falhas.append(arquivo_dbc)

    # Resumo final
    print(f"\n{'='*70}")
    print(f"RESUMO FINAL")
    print(f"{'='*70}")
    print(f"Total: {len(arquivos_dbc)} arquivos")
    print(f"Sucesso: {len(sucessos)}")
    print(f"Falhas: {len(falhas)}")

    if sucessos:
        print(f"\n[ARQUIVOS CSV CRIADOS]")
        for csv in sucessos:
            tamanho = csv.stat().st_size / 1024 / 1024
            print(f"  - {csv.name} ({tamanho:.2f} MB)")

        print(f"\n[PROXIMO PASSO]")
        print(f"1. Execute o app: streamlit run app_alternativo.py")
        print(f"2. Selecione 'Usar arquivo local'")
        print(f"3. Escolha um dos arquivos CSV criados")

    if falhas:
        print(f"\n[FALHAS]")
        for arquivo in falhas:
            print(f"  - {arquivo.name}")

        print(f"\n[ALTERNATIVA MANUAL]")
        print(f"Para arquivos que falharam:")
        print(f"1. Abra: tabwin\\TabWin415.exe")
        print(f"2. Arquivo > Abrir > Selecione o .dbc")
        print(f"3. Arquivo > Salvar Como > CSV")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    # Verificar se dbfread esta instalado
    try:
        import dbfread
        import pandas as pd
    except ImportError:
        print("[AVISO] Biblioteca 'dbfread' nao encontrada")
        print("Instalando dbfread...")
        print()

        resposta = input("Instalar dbfread agora? (s/n): ")
        if resposta.lower() == 's':
            subprocess.run([sys.executable, "-m", "pip", "install", "dbfread"])
            print("\n[OK] dbfread instalado. Execute o script novamente.\n")
        else:
            print("\nInstale manualmente com: pip install dbfread\n")
        sys.exit(0)

    # Processar arquivos
    if len(sys.argv) > 1:
        # Arquivo especifico
        arquivo = Path(sys.argv[1])
        converter_arquivo(arquivo)
    else:
        # Todos os arquivos
        processar_todos_dbc()
