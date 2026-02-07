# Script de configuração do ambiente virtual
Write-Host "=== Configuração do Ambiente Virtual ===" -ForegroundColor Cyan
Write-Host ""

# Criar ambiente virtual
Write-Host "1. Criando ambiente virtual em D:\venv_eleicoes..." -ForegroundColor Yellow
python -m venv D:\venv_eleicoes

if ($LASTEXITCODE -eq 0) {
    Write-Host "   Ambiente virtual criado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "   Erro ao criar ambiente virtual!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Instalar dependências
Write-Host "2. Instalando dependências (sem cache)..." -ForegroundColor Yellow
& "D:\venv_eleicoes\Scripts\python.exe" -m pip install --no-cache-dir -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "   Dependências instaladas com sucesso!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "   Erro ao instalar dependências!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Configuração Concluída ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para usar o ambiente virtual:" -ForegroundColor White
Write-Host "  1. Execute: D:\venv_eleicoes\Scripts\activate.bat" -ForegroundColor Gray
Write-Host "  2. Ou execute: run_app.bat" -ForegroundColor Gray
Write-Host ""
