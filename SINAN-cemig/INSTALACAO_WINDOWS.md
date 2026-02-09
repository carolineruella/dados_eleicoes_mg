# 🔧 Guia de Instalação - Windows

Este guia fornece instruções passo a passo para instalar e configurar o aplicativo SINAN-CEMIG no Windows.

## ⚠️ Pré-requisitos

- Windows 10 ou superior
- Python 3.8 ou superior
- Conexão com a internet
- ~6 GB de espaço em disco (para o Build Tools)

## 📋 Passo 1: Verificar Python

Abra o PowerShell ou Prompt de Comando e execute:

```bash
python --version
```

Se não tiver Python instalado, baixe em: https://www.python.org/downloads/

**Importante:** Durante a instalação do Python, marque a opção "Add Python to PATH"

## 🛠️ Passo 2: Instalar Microsoft C++ Build Tools

O pacote `pysus` depende do `pyreaddbc`, que precisa ser compilado. Para isso, você precisa do Microsoft C++ Build Tools.

### Opção 1: Visual Studio Build Tools (Recomendado)

1. **Download:**
   - Acesse: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Clique em "Download Build Tools"
   - Execute o arquivo `vs_BuildTools.exe`

2. **Instalação:**
   - Na janela do instalador, selecione **"Desktop development with C++"**
   - Certifique-se de que os seguintes componentes estão marcados:
     - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
     - ✅ Windows 10 SDK (ou Windows 11 SDK)
     - ✅ C++ CMake tools for Windows

   - Clique em "Install"
   - **Tempo estimado:** 20-40 minutos (dependendo da conexão)
   - **Espaço necessário:** ~5-6 GB

3. **Reinicie o computador** após a instalação

### Opção 2: Visual Studio Community (Alternativa)

Se você pretende desenvolver em C++ ou precisa do Visual Studio:

1. Download: https://visualstudio.microsoft.com/vs/community/
2. Durante a instalação, selecione "Desktop development with C++"
3. Instale e reinicie o computador

## 📦 Passo 3: Instalar Dependências Python

Após instalar o Build Tools e reiniciar o computador:

1. **Abra o PowerShell ou Prompt de Comando**

2. **Navegue até a pasta do projeto:**
   ```bash
   cd C:\Users\crptorres\Python\dados_eleicoes_mg\SINAN-cemig
   ```

3. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   ```

4. **Ative o ambiente virtual:**
   ```bash
   # PowerShell
   .\venv\Scripts\Activate.ps1

   # Ou CMD
   .\venv\Scripts\activate.bat
   ```

5. **Atualize o pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

6. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

   Este comando instalará:
   - streamlit
   - pandas
   - pysus (que inclui pyreaddbc)

## 🚀 Passo 4: Executar o Aplicativo

Com as dependências instaladas:

```bash
streamlit run app.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

## ❌ Solução de Problemas

### Erro: "Microsoft Visual C++ 14.0 or greater is required"

**Causa:** Build Tools não está instalado ou não foi detectado.

**Solução:**
1. Certifique-se de que instalou o Build Tools corretamente
2. Reinicie o computador
3. Tente novamente

Se o erro persistir:
```bash
# Desinstale o pyreaddbc
pip uninstall pyreaddbc -y

# Limpe o cache do pip
pip cache purge

# Tente instalar novamente
pip install pyreaddbc
```

### Erro: "error: command 'cl.exe' failed"

**Causa:** O compilador C++ não está no PATH.

**Solução:**
1. Abra "Developer Command Prompt for VS 2022" (procure no menu Iniciar)
2. Navegue até a pasta do projeto
3. Ative o ambiente virtual
4. Execute: `pip install -r requirements.txt`

### Erro: "No module named 'pysus'"

**Causa:** pysus não foi instalado corretamente.

**Solução:**
```bash
pip install pysus --no-cache-dir
```

### Erro ao executar streamlit

**Causa:** streamlit pode não estar no PATH.

**Solução:**
```bash
python -m streamlit run app.py
```

### O aplicativo não baixa os dados

**Causa:** Problemas com a conexão ao DATASUS ou dados indisponíveis.

**Solução:**
1. Tente outro ano
2. Verifique sua conexão com a internet
3. Tente novamente mais tarde (servidor DATASUS pode estar indisponível)

## 🔍 Verificação da Instalação

Para verificar se tudo está instalado corretamente:

```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar pacotes instalados
pip list

# Você deve ver:
# - streamlit
# - pandas
# - pysus
# - pyreaddbc
```

## 📊 Testando o Aplicativo

1. Execute o aplicativo: `streamlit run app.py`
2. No menu lateral, selecione um ano
3. Clique em "📥 Baixar Dados do SINAN"
4. Aguarde o download (pode levar alguns minutos)
5. Visualize os dados nas diferentes abas

## 💡 Dicas

### Uso do Ambiente Virtual

**Vantagens:**
- Isola as dependências do projeto
- Evita conflitos com outros projetos Python
- Facilita a reprodução do ambiente

**Comandos úteis:**
```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Desativar ambiente virtual
deactivate

# Verificar pacotes instalados no ambiente
pip list

# Congelar dependências
pip freeze > requirements.txt
```

### Atualizando os Pacotes

Para atualizar para as versões mais recentes:

```bash
pip install --upgrade streamlit pandas pysus
```

### Cache do Streamlit

Se o aplicativo estiver com comportamento estranho, limpe o cache:

1. No aplicativo, clique no menu (≡) no canto superior direito
2. Selecione "Clear cache"
3. Ou pressione `C` no teclado

## 📚 Links Úteis

### Downloads
- Python: https://www.python.org/downloads/
- Visual Studio Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Git (opcional): https://git-scm.com/downloads

### Documentação
- Streamlit: https://docs.streamlit.io/
- PySUS: https://github.com/AlertaDengue/PySUS
- Pandas: https://pandas.pydata.org/docs/

### Dados
- DATASUS: https://datasus.saude.gov.br/
- TabNet: http://tabnet.datasus.gov.br/
- API Dados Abertos: https://apidadosabertos.saude.gov.br/

## 🆘 Suporte

Se você continuar tendo problemas:

1. **Verifique os logs de erro** - copie a mensagem de erro completa
2. **Consulte a documentação** do PySUS: https://github.com/AlertaDengue/PySUS
3. **Issues do PySUS**: https://github.com/AlertaDengue/PySUS/issues

## 🔄 Alternativa: Usar Docker (Avançado)

Se você tiver problemas com a instalação, pode usar Docker:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
# Construir e executar
docker build -t sinan-app .
docker run -p 8501:8501 sinan-app
```

---

**Desenvolvido para Windows** 🪟 | **Testado em Windows 10/11** ✅
