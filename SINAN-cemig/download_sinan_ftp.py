"""
Script alternativo para download de dados do SINAN sem usar pysus
Usa conexao FTP direta ao servidor DATASUS
"""
import ftplib
import os
from pathlib import Path
import sys

# Configuracoes
FTP_HOST = "ftp.datasus.gov.br"
SINAN_BASE_PATH = "/dissemin/publicos/SINAN/DADOS/FINAIS/"

# Agravos disponiveis (codigos de pastas no FTP)
AGRAVOS_DISPONIVEIS = {
    "ACGR": "Acidente de Trabalho Grave",
    "ACBI": "Acidente com Material Biologico",
    "DENG": "Dengue",
    "TUBE": "Tuberculose",
    "HANS": "Hanseniase",
    "MENI": "Meningite",
    "VIOL": "Violencia",
    "HEPA": "Hepatites Virais",
    "LEPT": "Leptospirose",
    "LEIS": "Leishmaniose Visceral",
    "LEITA": "Leishmaniose Tegumentar",
    "RAIV": "Raiva"
}

def listar_arquivos_ftp(agravo="ACGR", ano=None):
    """
    Lista arquivos disponiveis no FTP do DATASUS para um agravo

    Args:
        agravo (str): Codigo do agravo (ex: ACGR, DENG)
        ano (int): Ano opcional para filtrar

    Returns:
        list: Lista de arquivos disponiveis
    """
    try:
        print(f"[CONECTANDO] Conectando ao FTP DATASUS...")
        ftp = ftplib.FTP(FTP_HOST, timeout=30)
        ftp.login()

        # Navegar para o diretorio do agravo
        caminho = f"{SINAN_BASE_PATH}{agravo}/"
        print(f"[NAVEGANDO] Acessando: {caminho}")
        ftp.cwd(caminho)

        # Listar arquivos
        arquivos = []
        ftp.retrlines('LIST', lambda x: arquivos.append(x))

        # Processar lista
        arquivos_dbc = []
        for linha in arquivos:
            partes = linha.split()
            if len(partes) >= 9:
                nome_arquivo = partes[-1]
                if nome_arquivo.upper().endswith('.DBC'):
                    # Extrair ano do nome do arquivo (geralmente tem formato ACGRAAMM.dbc)
                    if ano is None or str(ano)[2:] in nome_arquivo:
                        arquivos_dbc.append(nome_arquivo)

        ftp.quit()

        print(f"[OK] Encontrados {len(arquivos_dbc)} arquivos")
        return arquivos_dbc

    except Exception as e:
        print(f"[ERRO] Erro ao listar arquivos: {e}")
        return []

def download_arquivo_ftp(agravo, nome_arquivo, destino="data"):
    """
    Faz download de um arquivo do FTP DATASUS

    Args:
        agravo (str): Codigo do agravo
        nome_arquivo (str): Nome do arquivo a baixar
        destino (str): Pasta de destino

    Returns:
        str: Caminho do arquivo baixado ou None se houver erro
    """
    try:
        # Criar diretorio de destino
        Path(destino).mkdir(exist_ok=True)

        # Conectar ao FTP
        print(f"[DOWNLOAD] Iniciando download de {nome_arquivo}...")
        ftp = ftplib.FTP(FTP_HOST, timeout=60)
        ftp.login()

        # Navegar para o diretorio
        caminho = f"{SINAN_BASE_PATH}{agravo}/"
        ftp.cwd(caminho)

        # Baixar arquivo
        arquivo_local = os.path.join(destino, nome_arquivo)
        with open(arquivo_local, 'wb') as f:
            ftp.retrbinary(f'RETR {nome_arquivo}', f.write)

        ftp.quit()

        tamanho = os.path.getsize(arquivo_local) / 1024 / 1024
        print(f"[OK] Download concluido: {arquivo_local} ({tamanho:.2f} MB)")
        return arquivo_local

    except Exception as e:
        print(f"[ERRO] Erro ao baixar arquivo: {e}")
        return None

def baixar_sinan_ano(agravo, ano, destino="data"):
    """
    Baixa todos os arquivos de um agravo para um ano especifico

    Args:
        agravo (str): Codigo do agravo
        ano (int): Ano desejado
        destino (str): Pasta de destino

    Returns:
        list: Lista de arquivos baixados
    """
    print(f"\n{'='*60}")
    print(f"Baixando dados de {AGRAVOS_DISPONIVEIS.get(agravo, agravo)} - Ano {ano}")
    print(f"{'='*60}\n")

    # Listar arquivos disponiveis
    arquivos = listar_arquivos_ftp(agravo, ano)

    if not arquivos:
        print(f"[AVISO] Nenhum arquivo encontrado para {agravo}/{ano}")
        return []

    print(f"\n[INFO] Arquivos disponiveis:")
    for i, arquivo in enumerate(arquivos, 1):
        print(f"  {i}. {arquivo}")

    # Baixar todos os arquivos
    arquivos_baixados = []
    for arquivo in arquivos:
        caminho = download_arquivo_ftp(agravo, arquivo, destino)
        if caminho:
            arquivos_baixados.append(caminho)

    print(f"\n[SUCESSO] {len(arquivos_baixados)} arquivo(s) baixado(s)")
    return arquivos_baixados

def listar_agravos_disponiveis():
    """Lista todos os agravos disponiveis no SINAN"""
    print("\n=== AGRAVOS DISPONIVEIS NO SINAN ===\n")
    for codigo, nome in AGRAVOS_DISPONIVEIS.items():
        print(f"  {codigo}: {nome}")
    print()

if __name__ == "__main__":
    # Exemplo de uso
    print("=== DOWNLOAD SINAN - FTP DIRETO ===\n")

    if len(sys.argv) > 1:
        # Uso via linha de comando
        agravo = sys.argv[1].upper()
        ano = int(sys.argv[2]) if len(sys.argv) > 2 else 2022

        if agravo not in AGRAVOS_DISPONIVEIS:
            print(f"[ERRO] Agravo '{agravo}' nao encontrado")
            listar_agravos_disponiveis()
            sys.exit(1)

        baixar_sinan_ano(agravo, ano)

    else:
        # Uso interativo
        listar_agravos_disponiveis()

        print("Exemplo de uso:")
        print("  python download_sinan_ftp.py ACGR 2022")
        print("\nOu execute diretamente:")

        # Demonstracao: listar arquivos de Acidentes de Trabalho Grave
        agravo = "ACGR"
        ano = 2022

        print(f"\n>>> Listando arquivos de {AGRAVOS_DISPONIVEIS[agravo]} ({ano})...\n")
        arquivos = listar_arquivos_ftp(agravo, ano)

        if arquivos:
            print("\nPara baixar, execute:")
            print(f"  python download_sinan_ftp.py {agravo} {ano}")
        else:
            print("\nNenhum arquivo encontrado. Tente outro ano.")
