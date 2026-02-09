"""
Informacoes sobre a documentacao do SINAN para Acidentes de Trabalho
Baseado nos arquivos baixados de ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DOCS/
"""

# Caminhos para a documentacao
DOCS_BASE = "sinan_docs/Docs_TAB_SINAN/Documentacao/AGRAVOS"

# Tipos de Acidentes de Trabalho no SINAN
ACIDENTES_TRABALHO = {
    "ACGRN": {
        "nome": "Acidente de Trabalho Grave",
        "descricao": "Notificacao de acidentes de trabalho graves, com mutilacoes ou fatais",
        "codigo_sinan": "ACGRAVE",  # Nome usado na API pysus
        "documentos": {
            "dicionario_dados": f"{DOCS_BASE}/ACGRN_DIC_DADOS.pdf",
            "ficha_notificacao": f"{DOCS_BASE}/ACGRN_FICHA.pdf"
        },
        "informacoes": {
            "tipos_incluidos": [
                "Acidentes de trabalho graves",
                "Acidentes com mutilacoes",
                "Acidentes fatais",
                "Acidentes com afastamento prolongado"
            ],
            "variaveis_principais": [
                "Dados demograficos do trabalhador",
                "Caracteristicas do acidente",
                "Local do acidente",
                "Causa do acidente",
                "Parte do corpo atingida",
                "Tipo de lesao",
                "Evolucao do caso",
                "Situacao no mercado de trabalho",
                "CNAE da atividade economica"
            ]
        }
    },
    "ACBION": {
        "nome": "Acidente com Material Biologico",
        "descricao": "Notificacao de acidentes de trabalho com exposicao a material biologico",
        "codigo_sinan": "ACBIO",  # Nome usado na API pysus
        "documentos": {
            "dicionario_dados": f"{DOCS_BASE}/ACBION_DIC_DADOS.pdf",
            "ficha_notificacao": f"{DOCS_BASE}/ACBION_FICHA.pdf"
        },
        "informacoes": {
            "tipos_incluidos": [
                "Exposicao a sangue",
                "Exposicao a fluidos corporais",
                "Acidentes perfurocortantes",
                "Contato com mucosas",
                "Exposicao em profissionais de saude"
            ],
            "variaveis_principais": [
                "Dados demograficos do trabalhador",
                "Tipo de exposicao",
                "Material biologico envolvido",
                "Uso de EPI",
                "Situacao vacinal",
                "Fonte/paciente origem",
                "Profilaxias realizadas",
                "Acompanhamento sorologico"
            ]
        }
    }
}

# Outras doencas/agravos disponiveis no SINAN
OUTROS_AGRAVOS = {
    "DENGON": "Dengue",
    "VIOLEN": "Violencia Interpessoal/Autoprovocada",
    "TUBEN": "Tuberculose",
    "HANSN": "Hanseniase",
    "MENIN": "Meningite",
    "HEPANET": "Hepatites Virais",
    "HIVAN": "HIV/AIDS",
    "LEPTON": "Leptospirose",
    "FTIFON": "Febre Tifoide",
    "LEISHN": "Leishmaniose Visceral",
    "LTAN": "Leishmaniose Tegumentar",
    "RAIVAN": "Raiva",
    "ANIMPN": "Animais Peconhentos",
    "IEXOGN": "Intoxicacao Exogena"
}

def get_info_acidente(tipo="ACGRN"):
    """
    Retorna informacoes sobre um tipo de acidente de trabalho

    Args:
        tipo (str): Codigo do agravo (ACGRN ou ACBION)

    Returns:
        dict: Informacoes sobre o agravo
    """
    return ACIDENTES_TRABALHO.get(tipo.upper())

def listar_documentos():
    """Lista todos os documentos disponiveis"""
    documentos = []
    for codigo, info in ACIDENTES_TRABALHO.items():
        for tipo_doc, caminho in info["documentos"].items():
            documentos.append({
                "agravo": codigo,
                "nome_agravo": info["nome"],
                "tipo_documento": tipo_doc,
                "caminho": caminho
            })
    return documentos

def get_variaveis_principais(tipo="ACGRN"):
    """Retorna as variaveis principais de um tipo de acidente"""
    info = get_info_acidente(tipo)
    if info:
        return info["informacoes"]["variaveis_principais"]
    return []

if __name__ == "__main__":
    # Teste do modulo
    print("=== TIPOS DE ACIDENTES DE TRABALHO NO SINAN ===\n")

    for codigo, info in ACIDENTES_TRABALHO.items():
        print(f"Codigo: {codigo}")
        print(f"Nome: {info['nome']}")
        print(f"Descricao: {info['descricao']}")
        print(f"Codigo API: {info['codigo_sinan']}")
        print(f"Documentos:")
        for tipo_doc, caminho in info['documentos'].items():
            print(f"  - {tipo_doc}: {caminho}")
        print()

    print("\n=== DOCUMENTOS DISPONIVEIS ===\n")
    for doc in listar_documentos():
        print(f"{doc['agravo']} - {doc['nome_agravo']}")
        print(f"  Tipo: {doc['tipo_documento']}")
        print(f"  Arquivo: {doc['caminho']}")
        print()
