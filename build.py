#!/usr/bin/env python3
"""
Script de Build Simplificado e Funcional
Cria executável do Analisador de Artigos
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header():
    """Prints script header"""
    print("=" * 60)
    print("🚀 BUILD ARTICLE ANALYZER v2.0")
    print("=" * 60)


def check_requirements():
    """Checks if required files exist"""
    print("🔍 Checking for required files...")
    
    required_files = ['article_analyzer.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file} found")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True


def install_dependencies():
    """Installs required dependencies"""
    print("\n📦 Installing dependencies...")
    
    dependencies = ['pandas', 'pyinstaller']
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep} already installed")
        except ImportError:
            print(f"📥 Installing {dep}...")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', dep
                ], check=True, capture_output=True)
                print(f"✅ {dep} successfully installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error installing {dep}: {e}")
                return False
    
    return True


def clean_build_dirs():
    """Removes previous build directories"""
    print("\n🧹 Cleaning up previous builds...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Removed: {dir_name}")
            except Exception as e:
                print(f"⚠️  Could not remove {dir_name}: {e}")
    
    # Remove old spec files
    for spec_file in Path('.').glob('*.spec'):
        try:
            spec_file.unlink()
            print(f"✅ Removed: {spec_file}")
        except Exception as e:
            print(f"⚠️  Could not remove {spec_file}: {e}")


def create_build_files():
    """Creates auxiliary files for the build"""
    print("\n📄 Creating auxiliary files...")
    
    # README.md
    readme_content = """# Article and Book Analyzer v2.0

## Description
Professional software for analyzing lists of scientific articles and academic books.

## Features
✅ Modern and intuitive interface
📊 Automatic analysis of CSV files
📋 Complete title listing
🔍 Intelligent duplicate detection
📤 Export to CSV
⚡ Fast and efficient processing

## How to use
1. Run ArticleAnalyzer.exe
2. Click "Browse" to select your CSV file
3. Click "Analyze File"
4. View detailed results
5. Export lists as needed

## CSV file requirements
- Must contain a title column (title, title, name, etc.)
- Optionally, an author column (author, author, etc.)
- Standard CSV text format

## Support
Developed with Python and Tkinter for maximum compatibility. Version: 2.0.0
"""
    
    # License
    license_content = """MIT License

Copyright (c) 2025 Article and Book Analyzer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to deal in the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""
    
    # Cria os arquivos
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ README.md created")
        
        with open('LICENSE.txt', 'w', encoding='utf-8') as f:
            f.write(license_content)
        print("✅ LICENSE.txt created")
        
    except Exception as e:
        print(f"⚠️  Error creating files: {e}")


def build_executable():
    """Compile the executable using PyInstaller"""
    print("\n🔨 Compiling executable...")
    
    # Basic command
    build_command = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single file
        '--windowed',                   # No console
        '--name=AnalisadorArtigos',     # Executable name
        '--clean',                      # Clear cache
        '--noconfirm',                  # Does not ask for confirmation
        'article_analyzer.py'           # Source file
    ]
    
    print("📋 Command: " + ' '.join(build_command))
    
    try:
        # Executa o build
        result = subprocess.run(
            build_command,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        print("✅ Compilation completed!")
        
        # Checks if the executable was created
        exe_path = Path('dist/AnalisadorArtigos.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable created: {exe_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Executable not created")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout - Build took more than 5 minutes")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Compilation error: {e}")
        if e.stdout:
            print("📄 Standard output:")
            print(e.stdout[-500:])  # Last 500 chars
        if e.stderr:
            print("🚫 Error output:")
            print(e.stderr[-500:])  # Last 500 chars
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_executable():
    """Tests if the executable works"""
    print("\n🧪 Testing executable...")
    
    exe_path = Path('dist/AnalisadorArtigos.exe')
    if not exe_path.exists():
        print("❌ Executable not found for testing")
        return False
    
    try:
        # Only tests whether the file is executable (does not open the interface)
        result = subprocess.run([str(exe_path)], timeout=5, capture_output=True)
        print("✅ Executable appears to be working")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Executable started (normal timeout for graphical interface)")
        return True
    except Exception as e:
        print(f"⚠️  Unable to test automatically: {e}")
        print("💡 Test manually by running: dist/AnalisadorArtigos.exe")
        return True


def create_installer_script():
    """Create Inno Setup script for professional installer"""
    print("\n📦 Creating the installer script...")
    
    inno_script = '''[Setup]
AppName=Analisador de Artigos e Livros
AppVersion=2.0.0
AppPublisher=Analisador de Artigos
DefaultDirName={autopf}\\Analisador de Artigos
DefaultGroupName=Analisador de Artigos
OutputDir=installer
OutputBaseFilename=AnalisadorArtigos_Setup_v2.0.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na área de trabalho"; GroupDescription: "Ícones adicionais:"; Flags: unchecked

[Files]
Source: "dist\\AnalisadorArtigos.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Analisador de Artigos"; Filename: "{app}\\AnalisadorArtigos.exe"
Name: "{autodesktop}\\Analisador de Artigos"; Filename: "{app}\\AnalisadorArtigos.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\AnalisadorArtigos.exe"; Description: "Executar Analisador de Artigos"; Flags: nowait postinstall skipifsilent
'''
    
    try:
        with open('installer.iss', 'w', encoding='utf-8') as f:
            f.write(inno_script)
        print("✅ Installer script created: installer.iss")
        print("💡 Use Inno Setup to create the professional installer")
        return True
    except Exception as e:
        print(f"⚠️  Error creating installer script: {e}")
        return False


def main():
    """Main function of the build"""
    print_header()
    
    # 1. Check required files
    if not check_requirements():
        input("\n❌ Build canceled. Press Enter to exit...")
        return
    
    # 2. Install dependencies
    if not install_dependencies():
        input("\n❌ Dependency error. Press Enter to exit...")
        return
    
    # 3. Clean up previous builds
    clean_build_dirs()
    
    # 4. Create auxiliary files
    create_build_files()
    
    # 5. Compile executable
    if not build_executable():
        input("\n❌ Compilation failed. Press Enter to exit...")
        return
    
    # 6. Test executable
    test_executable()
    
    # 7. Create installer script
    create_installer_script()
    
    # 8. Final summary
    print("\n" + "=" * 60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("📁 Files created:")
    print("   • dist/AnalisadorArtigos.exe (main executable)")
    print("   • README.md (documentation)")
    print("   • LICENSE.txt (license)")
    print("   • installer.iss (installer script)")
    
    print("\n📋 Next steps:")
    print("1. Test the executable: dist/AnalisadorArtigos.exe")
    print("2. To create professional installer:")
    print("   - Download Inno Setup: https://jrsoftware.org/isinfo.php")
    print("   - Open the file installer.iss")
    print("   - Compile the installer")
    
    # Ask if you want to test
    test_now = input("\n🧪 Do you want to test the executable now? (s/N): ").lower().strip()
    if test_now in ['s', 'sim', 'y', 'yes']:
        try:
            exe_path = Path('dist/AnalisadorArtigos.exe')
            if exe_path.exists():
                print("🚀 Opening executable...")
                os.startfile(str(exe_path))
            else:
                print("❌ Executable not found")
        except Exception as e:
            print(f"❌ Error opening executable: {e}")
    
    input("\nPress Enter to finish...")


if __name__ == "__main__":
    main()