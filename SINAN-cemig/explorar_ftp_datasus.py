"""
Script para explorar a estrutura do FTP DATASUS
"""
import ftplib

def explorar_ftp(caminho="/"):
    """Explora um caminho do FTP DATASUS"""
    try:
        print(f"\n[EXPLORANDO] {caminho}")
        print("-" * 60)

        ftp = ftplib.FTP("ftp.datasus.gov.br", timeout=30)
        ftp.login()

        if caminho != "/":
            ftp.cwd(caminho)

        # Listar conteudo
        items = []
        ftp.retrlines('LIST', lambda x: items.append(x))

        pastas = []
        arquivos = []

        for item in items:
            partes = item.split()
            if len(partes) >= 9:
                nome = partes[-1]
                tipo = partes[0]

                if tipo.startswith('d'):
                    pastas.append(nome)
                else:
                    arquivos.append(nome)

        if pastas:
            print(f"\n[PASTAS] ({len(pastas)}):")
            for pasta in pastas[:20]:  # Limitar a 20
                print(f"  📁 {pasta}")
            if len(pastas) > 20:
                print(f"  ... e mais {len(pastas) - 20} pastas")

        if arquivos:
            print(f"\n[ARQUIVOS] ({len(arquivos)}):")
            for arquivo in arquivos[:10]:  # Limitar a 10
                print(f"  📄 {arquivo}")
            if len(arquivos) > 10:
                print(f"  ... e mais {len(arquivos) - 10} arquivos")

        ftp.quit()
        return pastas, arquivos

    except Exception as e:
        print(f"[ERRO] {e}")
        return [], []

if __name__ == "__main__":
    print("=== EXPLORANDO FTP DATASUS ===")

    # Explorar raiz
    print("\n1. Explorando raiz do FTP...")
    pastas_raiz, _ = explorar_ftp("/")

    # Explorar dissemin/publicos
    if "dissemin" in pastas_raiz:
        print("\n2. Explorando /dissemin...")
        pastas_dissemin, _ = explorar_ftp("/dissemin")

        if "publicos" in pastas_dissemin:
            print("\n3. Explorando /dissemin/publicos...")
            pastas_publicos, _ = explorar_ftp("/dissemin/publicos")

            if "SINAN" in pastas_publicos:
                print("\n4. Explorando /dissemin/publicos/SINAN...")
                pastas_sinan, _ = explorar_ftp("/dissemin/publicos/SINAN")

                if "DADOS" in pastas_sinan:
                    print("\n5. Explorando /dissemin/publicos/SINAN/DADOS...")
                    explorar_ftp("/dissemin/publicos/SINAN/DADOS")

    print("\n" + "="*60)
    print("Exploracao concluida!")
