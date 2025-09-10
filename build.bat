@echo off
chcp 65001 >nul
title Analisador de Artigos - Build Automático v2.0

echo.
echo ================================================================
echo 🚀 BUILD AUTOMÁTICO - ANALISADOR DE ARTIGOS v2.0
echo ================================================================
echo.

:: Verifica se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 💡 SOLUÇÕES:
    echo    1. Baixe Python em: https://python.org
    echo    2. Marque "Add Python to PATH" durante a instalação
    echo    3. Reinicie o computador após instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado

:: Verifica se o arquivo principal existe
if not exist "article_analyzer.py" (
    echo.
    echo ❌ Arquivo "article_analyzer.py" não encontrado!
    echo.
    echo 💡 SOLUÇÕES:
    echo    1. Certifique-se de que todos os arquivos estão na pasta correta
    echo    2. Execute este script na pasta do projeto
    echo.
    pause
    exit /b 1
)

echo ✅ Arquivo principal encontrado

:: Executa o script de build Python
echo.
echo 🔨 Iniciando processo de build...
echo.

python build.py

:: Verifica se o build foi bem-sucedido
if exist "dist\AnalisadorArtigos.exe" (
    echo.
    echo ================================================================
    echo ✅ BUILD CONCLUÍDO COM SUCESSO!
    echo ================================================================
    echo.
    echo 📁 Executável criado: dist\AnalisadorArtigos.exe
    echo.
    
    for %%F in (dist\AnalisadorArtigos.exe) do (
        set /a size_kb=%%~zF/1024
    )
    echo 📏 Tamanho: !size_kb! KB
    echo.
    
    :: Pergunta se quer abrir a pasta
    set /p open_folder="📂 Abrir pasta dist? (s/N): "
    if /i "!open_folder!"=="s" (
        explorer dist
    )
    
    :: Pergunta se quer testar
    set /p test_exe="🧪 Testar executável? (s/N): "
    if /i "!test_exe!"=="s" (
        start "" "dist\AnalisadorArtigos.exe"
    )
    
) else (
    echo.
    echo ================================================================
    echo ❌ BUILD FALHOU
    echo ================================================================
    echo.
    echo 🔧 POSSÍVEIS SOLUÇÕES:
    echo    1. Execute como Administrador
    echo    2. Desative temporariamente o antivírus
    echo    3. Verifique se há espaço em disco suficiente
    echo    4. Tente executar: pip install --upgrade pyinstaller
    echo.
)

echo.
echo ================================================================
echo 📋 INFORMAÇÕES ADICIONAIS
echo ================================================================
echo.
echo Para criar um instalador profissional:
echo 1. Baixe o Inno Setup: https://jrsoftware.org/isinfo.php
echo 2. Abra o arquivo "installer.iss"
echo 3. Compile o instalador
echo.
echo Para distribuição:
echo • Executável: dist\AnalisadorArtigos.exe
echo • Documentação: README.md
echo • Licença: LICENSE.txt
echo.

pause