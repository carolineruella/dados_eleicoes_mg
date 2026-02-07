@echo off
echo Ativando ambiente virtual...
call d:\venv_eleicoes\Scripts\activate.bat

echo.
echo Iniciando aplicacao Streamlit...
streamlit run app.py

pause
