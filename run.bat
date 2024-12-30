@echo off
:: Verifica se o pipenv está instalado
pipenv --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [Erro] Pipenv não está instalado. Instale o Pipenv com "pip install pipenv".
    pause
    exit /b
)

:: Ativa o ambiente virtual e instala as dependências
echo [Info] Instalando dependências do projeto...
pipenv install

IF ERRORLEVEL 1 (
    echo [Erro] Falha ao instalar dependências. Verifique seu arquivo Pipfile.
    pause
    exit /b
)

:: Executa o aplicativo Flask
echo [Info] Iniciando o servidor Flask...
pipenv run python main.py

IF ERRORLEVEL 1 (
    echo [Erro] Ocorreu um erro ao executar o aplicativo Flask.
    pause
    exit /b
)

pause
