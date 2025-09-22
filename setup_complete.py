#!/usr/bin/env python3
"""
Setup Completo do Analisador de Artigos v2.0
Configura, compila e prepara tudo para distribuição
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path


def create_project_structure():
    """Cria a estrutura de pastas do projeto"""
    print("📁 Criando estrutura do projeto...")
    
    folders = [
        'dist',
        'build', 
        'installer',
        'docs',
        'assets'
    ]
    
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✅ Pasta criada: {folder}")


def create_version_info():
    """Cria arquivo de informações de versão para Windows"""
    version_info = """# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Analisador de Artigos'),
        StringStruct(u'FileDescription', u'Analisador de Artigos e Livros'),
        StringStruct(u'FileVersion', u'2.0.0.0'),
        StringStruct(u'InternalName', u'AnalisadorArtigos'),
        StringStruct(u'LegalCopyright', u'© 2025 Analisador de Artigos'),
        StringStruct(u'OriginalFilename', u'AnalisadorArtigos.exe'),
        StringStruct(u'ProductName', u'Analisador de Artigos e Livros'),
        StringStruct(u'ProductVersion', u'2.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    try:
        with open('version_info.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)
        print("✅ Arquivo de versão criado")
    except Exception as e:
        print(f"⚠️  Erro ao criar arquivo de versão: {e}")


def create_config_file():
    """Cria arquivo de configuração JSON"""
    config = {
        "app": {
            "name": "Analisador de Artigos e Livros",
            "version": "2.0.0",
            "author": "Analisador de Artigos",
            "description": "Software profissional para análise de listas acadêmicas"
        },
        "build": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "dependencies": ["pandas", "pyinstaller"],
            "exclude_modules": [
                "matplotlib", "scipy", "numpy.distutils", "unittest", "test"
            ]
        },
        "installer": {
            "create_desktop_shortcut": False,
            "create_start_menu": True,
            "install_path": "{autopf}\\Analisador de Artigos"
        }
    }
    
    try:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("✅ Configuration file created")
    except Exception as e:
        print(f"⚠️  Error creating configuration: {e}")


def create_documentation():
    """Cria documentação completa"""
    print("📚 Creating documentation...")
    
    # Manual do usuário
    user_manual = """# User Manual - Article Analyzer v2.0

## Introduction
Article Analyzer is professional software designed to assist researchers, librarians, and academics in analyzing lists of scientific articles and books.

## Main Features

### ✅ Automatic Analysis
- Automatic detection of title and author columns
- CSV format validation
- Fast processing of large lists

### 🔍 Duplicate Detection
- Intelligent identification of duplicate records
- Comparison by title and author
- Detailed duplicate report

### 📊 Detailed Reports
- Total record count
- Complete formatted list
- Duplication statistics
- Modern visual interface

### 📤 Export
- Export the complete list
- Export only duplicates
- Excel-compatible CSV format
- Automatic numbering

## How to Use

### 1. Prepare the CSV File
Your file must contain at least one column with headings. Examples of accepted names:
- **Titles**: title, title, title, name, name
- **Authors**: author, author, authors, authors

### 2. Open the Software
Run the file `AnalisadorArtigos.exe`

### 3. Select File
1. Click "📂 Browse"
2. Navigate to your CSV file
3. Select the file and click "Open"

### 4. Analyze
1. Click "🔍 Analyze File"
2. Wait for processing
3. View the results on the screen

### 5. Export Results
- **Full List**: Click "📋 Export Full List"
- **Duplicates Only**: Click "🔍 Export Duplicates"

## Supported Formats
- CSV (UTF-8)
- CSV (Latin1/ANSI)
- Separators: comma, semicolon

## System Requirements
- Windows 10 or higher
- 100 MB of free space
- 4 GB of RAM (recommended)

## Troubleshooting

### File not recognized
- Check if the file is a valid CSV file
- Make sure there are title columns
- Try saving again as a UTF-8 CSV file

### Error opening file
- Check file permissions
- Close the file in Excel before analyzing
- Try copying the file to another location

### Duplicates not detected
- Check if there is an author column
- Titles must be identical for detection
- Extra spaces may affect the comparison

## Support
For questions or problems, see the README.md file or contact the developer.

---
**Article Analyzer v2.0** - Professional software for academic analysis
"""
    
    try:
        docs_path = Path('docs')
        docs_path.mkdir(exist_ok=True)
        
        with open(docs_path / 'manual_usuario.md', 'w', encoding='utf-8') as f:
            f.write(user_manual)
        print("✅ User manual created")
        
    except Exception as e:
        print(f"⚠️  Error creating documentation: {e}")


def create_all_files():
    """Creates all necessary project files"""
    print("📄 Creating all project files...")
    
    create_project_structure()
    create_version_info()
    create_config_file()
    create_documentation()


def run_full_build():
    """Run the full build using the build.py script"""
    print("\n🚀 Starting full build...")
    
    try:
        # Run the build script
        result = subprocess.run([sys.executable, 'build.py'], 
                               check=True, capture_output=True, text=True)
        
        print("✅ Build executado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build error: {e}")
        if e.stdout:
            print("📄 Output:", e.stdout[-300:])
        if e.stderr:
            print("🚫 Error:", e.stderr[-300:])
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def create_distribution_package():
    """Creates complete package for distribution"""
    print("\n📦 Creating a distribution package...")
    
    # Checks if the executable exists
    exe_path = Path('dist/AnalisadorArtigos.exe')
    if not exe_path.exists():
        print("❌ Executável não encontrado. Execute o build primeiro.")
        return False
    
    # Create distribution folder
    dist_folder = Path('AnalisadorArtigos_v2.0_Distribuicao')
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir()
    
    # Copy necessary files
    files_to_copy = [
        ('dist/AnalisadorArtigos.exe', 'AnalisadorArtigos.exe'),
        ('README.md', 'README.md'),
        ('LICENSE.txt', 'LICENSE.txt'),
        ('docs/manual_usuario.md', 'Manual_do_Usuario.md'),
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        if src_path.exists():
            shutil.copy2(src_path, dist_folder / dst)
            print(f"✅ Copied: {dst}")
    
    # Creates quick instructions file
    quick_start = """# QUICK START

## To use the software:
1. Run: ArticleAnalyzer.exe
2. Select your CSV file
3. Click "Analyze File"
4. View the results
5. Export the lists

## For more information:
- Read the User_Manual.md
- See the README.md

Version: 2.0.0
"""
    
    with open(dist_folder / 'INICIO_RAPIDO.txt', 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print(f"✅ Distribution package created: {dist_folder}")
    return True


def main():
    """Função principal do setup completo"""
    print("=" * 60)
    print("🏗️  COMPLETE SETUP - ARTICLE ANALYZER v2.0")
    print("=" * 60)
    
    # Verifica se o arquivo principal existe
    if not Path('article_analyzer.py').exists():
        print("❌ File article_analyzer.py not found!")
        print("💡 Make sure you are in the correct project folder")
        input("Press Enter to exit...")
        return
    
    # 1. Criar estrutura e arquivos
    print("\n📋 PHASE 1: Project Structure")
    create_all_files()
    
    # 2. Executar build
    print("\n📋 PHASE 2: Compilation")
    if not run_full_build():
        print("❌ Build failed. Check the errors above.")
        input("Press Enter to exit...")
        return
    
    # 3. Criar pacote de distribuição
    print("\n📋 PHASE 3: Distribution Package")
    if not create_distribution_package():
        print("❌ Failed to create distribution package.")
    
    # 4. Resumo final
    print("\n" + "=" * 60)
    print("🎉 COMPLETE SETUP FINISHED!")
    print("=" * 60)
    
    print("📁 Files created:")
    print("   • dist/AnalisadorArtigos.exe (main executable)")
    print("   • AnalisadorArtigos_v2.0_Distribuicao/ (full package)")
    print("   • docs/manual_usuario.md (documentation)")
    print("   • config.json (settings)")
    print("   • installer.iss (installer script)")
    
    print("\n📦 Ready for distribution:")
    print("   • Standalone executable: dist/AnalisadorArtigos.exe")
    print("   • Complete package: AnalisadorArtigos_v2.0_Distribuicao/")
    print("   • Installer (use Inno Setup): installer.iss")
    
    print("\n🚀 Next steps:")
    print("1. Test the executable")
    print("2. Distribute the complete package")
    print("3. For professional installer, use Inno Setup")
    
    # Pergunta final
    choice = input("\n🧪 What do you want to do now?\n"
                  "1. Test executable\n"
                  "2. Open distribution folder\n"
                  "3. Exit\n"
                  "Choose a number (1-3): ").strip()
    
    if choice == '1':
        try:
            exe_path = Path('dist/AnalisadorArtigos.exe')
            if exe_path.exists():
                print("🚀 Opening executable...")
                if os.name == 'nt':  # Windows
                    os.startfile(str(exe_path))
                else:
                    subprocess.run([str(exe_path)])
            else:
                print("❌ Executable not found")
        except Exception as e:
            print(f"❌ Error opening executable: {e}")
    
    elif choice == '2':
        try:
            dist_folder = Path('AnalisadorArtigos_v2.0_Distribuicao')
            if dist_folder.exists():
                if os.name == 'nt':  # Windows
                    os.startfile(str(dist_folder))
                else:
                    subprocess.run(['xdg-open', str(dist_folder)])
            else:
                print("❌ Distribution folder not found")
        except Exception as e:
            print(f"❌ Error opening folder: {e}")
    
    print("\n✅ Setup completed successfully!")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()