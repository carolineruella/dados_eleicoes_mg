@echo off
echo Criando ambiente virtual no disco D:...
python -m venv d:\venv_eleicoes

echo.
echo Ativando ambiente virtual...
call d:\venv_eleicoes\Scripts\activate.bat

echo.
echo Instalando dependencias...
pip install --no-cache-dir -r requirements.txt

echo.
echo Ambiente configurado com sucesso!
echo.
echo Para usar, execute: d:\venv_eleicoes\Scripts\activate.bat
pause
