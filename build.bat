@echo off
chcp 65001 >nul
title Article Analyzer - Automatic Build v2.0

echo.
echo ================================================================
echo 🚀 AUTOMATIC BUILD - ARTICLE ANALYZER v2.0
echo ================================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo 💡 SOLUTIONS:
    echo    1. Download Python at: https://python.org
    echo    2. Mark "Add Python to PATH" during installation
    echo    3. Restart your computer after installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found

:: Checks if the main file exists
if not exist "article_analyzer.py" (
    echo.
    echo ❌ File "article_analyzer.py" not found!
    echo.
    echo 💡 SOLUTIONS:
    echo    1. Make sure all files are in the correct folder
    echo    2. Run this script in the project folder
    echo.
    pause
    exit /b 1
)

echo ✅ Main file found

:: Run the Python build script
echo.
echo 🔨 Starting build process...
echo.

python build.py

:: Checks if the build was successful
if exist "dist\AnalisadorArtigos.exe" (
    echo.
    echo ================================================================
    echo ✅ BUILD COMPLETED SUCCESSFULLY!
    echo ================================================================
    echo.
    echo 📁 Executable created: dist\AnalisadorArtigos.exe
    echo.
    
    for %%F in (dist\AnalisadorArtigos.exe) do (
        set /a size_kb=%%~zF/1024
    )
    echo 📏 Size: !size_kb! KB
    echo.
    
    :: Ask if you want to open the folder
    set /p open_folder="📂 Open dist folder? (s/N): "
    if /i "!open_folder!"=="s" (
        explorer dist
    )
    
    :: Ask if you want to test
    set /p test_exe="🧪 Test executable? (s/N): "
    if /i "!test_exe!"=="s" (
        start "" "dist\AnalisadorArtigos.exe"
    )
    
) else (
    echo.
    echo ================================================================
    echo ❌ BUILD FAILED
    echo ================================================================
    echo.
    echo 🔧 POSSIBLE SOLUTIONS:
    echo    1. Run as Administrator
    echo    2. Temporarily disable your antivirus
    echo    3. Check if there is enough disk space
    echo    4. Try to run: pip install --upgrade pyinstaller
    echo.
)

echo.
echo ================================================================
echo 📋 ADDITIONAL INFORMATION
echo ================================================================
echo.
echo To create a professional installer:
echo 1. Download Inno Setup: https://jrsoftware.org/isinfo.php
echo 2. Open the file "installer.iss"
echo 3. Compile the installer
echo.
echo For distribution:
echo • Executable: dist\AnalisadorArtigos.exe
echo • Documentation: README.md
echo • License: LICENSE.txt
echo.

pause