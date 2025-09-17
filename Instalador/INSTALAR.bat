@echo off
echo ========================================
echo  Processador de DARMs - Instalacao
echo ========================================
echo.

echo Criando estrutura de pastas...
if not exist "darms" mkdir "darms"
if not exist "inserts" mkdir "inserts"

echo.
echo Instalacao concluida!
echo.
echo Como usar:
echo 1. Coloque os PDFs dos DARMs na pasta 'darms'
echo 2. Execute 'Processador-DARM.exe'
echo 3. Verifique os resultados na pasta 'inserts'
echo.
echo Pressione qualquer tecla para sair...
pause >nul
