@echo off
chcp 65001 >nul
echo ================================================================
echo 🚀 CRIADOR DE INSTALADOR - ANALISADOR DE ARTIGOS
echo ================================================================
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo 💡 Baixe e instale Python em: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

:: Verifica se o arquivo principal existe
if not exist "article_analyzer.py" (
    echo ❌ Arquivo article_analyzer.py não encontrado!
    echo 💡 Certifique-se de que todos os arquivos estão na pasta correta
    pause
    exit /b 1
)

echo ✅ Arquivo principal encontrado

:: Instala dependências
echo.
echo 📦 Instalando dependências...
pip install pyinstaller pandas >nul 2>&1
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    echo 💡 Tente executar manualmente: pip install pyinstaller pandas
    pause
    exit /b 1
)

echo ✅ Dependências instaladas

:: Executa o script de build
echo.
echo 🔨 Executando build...
python build.py

:: Verifica se o executável foi criado
if exist "dist\AnalisadorArtigos.exe" (
    echo.
    echo ✅ Executável criado com sucesso!
    
    :: Pergunta se quer criar o instalador
    echo.
    set /p criar_inst="🤔 Deseja criar um instalador profissional? (s/N): "
    
    if /i "%criar_inst%"=="s" (
        echo.
        echo 📋 Para criar o instalador profissional:
        echo 1. Baixe o Inno Setup em: https://jrsoftware.org/isinfo.php
        echo 2. Instale o Inno Setup
        echo 3. Abra o arquivo 'installer.iss' com o Inno Setup
        echo 4. Clique em 'Build' para criar o instalador
        echo.
        echo 📁 Arquivos necessários já foram criados:
        echo    - dist\AnalisadorArtigos.exe
        echo    - installer.iss
        echo    - README.md
        echo    - license.txt
    )
    
    echo.
    echo 🎉 Processo concluído!
    echo 📁 Seu executável está em: dist\AnalisadorArtigos.exe
    
    :: Pergunta se quer testar o executável
    set /p testar="🧪 Deseja testar o executável agora? (s/N): "
    if /i "%testar%"=="s" (
        start "" "dist\AnalisadorArtigos.exe"
    )
    
) else (
    echo ❌ Falha ao criar o executável
    echo 💡 Verifique os erros acima e tente novamente
)

echo.
echo ================================================================
pause