@echo off
echo Executando PyInstaller via Python...
"C:\xampp\htdocs\Softwares Clientes\.venv\Scripts\python.exe" -m PyInstaller --onefile --windowed --name=AnalisadorArtigos article_analyzer.py
pause
