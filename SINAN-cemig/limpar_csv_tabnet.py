"""
Script para limpar arquivos CSV exportados do TabNet DATASUS
TabNet inclui cabecalhos, rodapes e metadados que causam erros ao carregar
"""
import pandas as pd
import sys
from pathlib import Path

def limpar_csv_tabnet(arquivo_entrada, arquivo_saida=None):
    """
    Limpa um arquivo CSV do TabNet removendo linhas de cabecalho e rodape

    Args:
        arquivo_entrada (str): Caminho do arquivo CSV original
        arquivo_saida (str): Caminho do arquivo limpo (opcional)

    Returns:
        str: Caminho do arquivo limpo
    """
    print(f"[LIMPANDO] {arquivo_entrada}")

    # Se nao especificar saida, criar nome automatico
    if arquivo_saida is None:
        caminho = Path(arquivo_entrada)
        arquivo_saida = caminho.parent / f"{caminho.stem}_limpo{caminho.suffix}"

    try:
        # Ler arquivo como texto
        with open(arquivo_entrada, 'r', encoding='utf-8-sig') as f:
            linhas = f.readlines()

        # Tentar diferentes encodings se utf-8 falhar
        if not linhas:
            try:
                with open(arquivo_entrada, 'r', encoding='latin-1') as f:
                    linhas = f.readlines()
            except:
                with open(arquivo_entrada, 'r', encoding='cp1252') as f:
                    linhas = f.readlines()

        print(f"[INFO] Total de linhas: {len(linhas)}")

        # Encontrar inicio dos dados (primeira linha com ponto-e-virgula ou virgula)
        inicio_dados = 0
        for i, linha in enumerate(linhas):
            # Linha com delimitador e que nao seja titulo/metadado
            if (';' in linha or ',' in linha) and not linha.strip().startswith('"SINAN'):
                # Verificar se tem formato de cabecalho de coluna
                if any(palavra in linha.upper() for palavra in ['MUNIC', 'ANO', 'NOTIF', 'RESID', 'TOTAL']):
                    inicio_dados = i
                    print(f"[INFO] Inicio dos dados na linha {inicio_dados + 1}")
                    break

        # Encontrar fim dos dados (ultima linha antes de rodapes)
        fim_dados = len(linhas)
        for i in range(len(linhas) - 1, inicio_dados, -1):
            linha = linhas[i].strip()
            # Linhas de rodape geralmente comecam com "Fonte:", "Notas:", ou estao vazias
            if linha and not linha.startswith('Fonte:') and not linha.startswith('Nota'):
                # Verificar se tem dados (numeros ou texto relevante)
                if any(c.isdigit() for c in linha) or ';' in linha or ',' in linha:
                    fim_dados = i + 1
                    print(f"[INFO] Fim dos dados na linha {fim_dados}")
                    break

        # Extrair dados limpos
        dados_limpos = linhas[inicio_dados:fim_dados]

        if not dados_limpos:
            print("[ERRO] Nenhum dado encontrado no arquivo")
            return None

        # Salvar arquivo limpo
        with open(arquivo_saida, 'w', encoding='utf-8-sig', newline='') as f:
            f.writelines(dados_limpos)

        print(f"[OK] Arquivo limpo salvo: {arquivo_saida}")
        print(f"[INFO] Linhas mantidas: {len(dados_limpos)}")

        # Tentar carregar para validar
        try:
            df = pd.read_csv(arquivo_saida, sep=None, engine='python')
            print(f"[VALIDACAO] ✅ CSV valido: {len(df)} registros, {len(df.columns)} colunas")
            print(f"[COLUNAS] {', '.join(df.columns.tolist()[:5])}{'...' if len(df.columns) > 5 else ''}")
        except Exception as e:
            print(f"[AVISO] Arquivo salvo mas pode precisar de ajustes: {e}")

        return str(arquivo_saida)

    except Exception as e:
        print(f"[ERRO] {e}")
        return None

def processar_pasta(pasta="data"):
    """Processa todos os CSV em uma pasta"""
    pasta_path = Path(pasta)

    if not pasta_path.exists():
        print(f"[ERRO] Pasta nao encontrada: {pasta}")
        return

    csv_files = list(pasta_path.glob("*.csv"))

    if not csv_files:
        print(f"[INFO] Nenhum arquivo CSV encontrado em {pasta}")
        return

    print(f"[INFO] Encontrados {len(csv_files)} arquivos CSV\n")

    for arquivo in csv_files:
        if '_limpo' not in arquivo.name:  # Pular arquivos ja limpos
            print(f"\n{'='*60}")
            limpar_csv_tabnet(str(arquivo))
            print(f"{'='*60}\n")

if __name__ == "__main__":
    print("="*60)
    print("LIMPADOR DE CSV DO TABNET DATASUS")
    print("="*60)
    print()

    if len(sys.argv) > 1:
        # Modo linha de comando
        arquivo = sys.argv[1]
        arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else None

        resultado = limpar_csv_tabnet(arquivo, arquivo_saida)

        if resultado:
            print(f"\n✅ Sucesso! Use o arquivo limpo no app:")
            print(f"   {resultado}")
    else:
        # Modo interativo
        print("Uso:")
        print("  python limpar_csv_tabnet.py arquivo.csv [arquivo_saida.csv]")
        print()
        print("Ou processe todos os CSV na pasta 'data':")

        resposta = input("\nProcessar todos os CSV na pasta 'data'? (s/n): ")
        if resposta.lower() == 's':
            processar_pasta()
        else:
            print("\nExemplo:")
            print("  python limpar_csv_tabnet.py tabnet_export.csv tabnet_limpo.csv")
