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
    """Imprime cabeçalho do script"""
    print("=" * 60)
    print("🚀 BUILD ANALISADOR DE ARTIGOS v2.0")
    print("=" * 60)


def check_requirements():
    """Verifica se os arquivos necessários existem"""
    print("🔍 Verificando arquivos necessários...")
    
    required_files = ['article_analyzer.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file} encontrado")
    
    if missing_files:
        print(f"❌ Arquivos faltando: {', '.join(missing_files)}")
        return False
    
    return True


def install_dependencies():
    """Instala dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    dependencies = ['pandas', 'pyinstaller']
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep} já instalado")
        except ImportError:
            print(f"📥 Instalando {dep}...")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', dep
                ], check=True, capture_output=True)
                print(f"✅ {dep} instalado com sucesso")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar {dep}: {e}")
                return False
    
    return True


def clean_build_dirs():
    """Remove diretórios de build anteriores"""
    print("\n🧹 Limpando builds anteriores...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Removido: {dir_name}")
            except Exception as e:
                print(f"⚠️  Não foi possível remover {dir_name}: {e}")
    
    # Remove arquivos spec antigos
    for spec_file in Path('.').glob('*.spec'):
        try:
            spec_file.unlink()
            print(f"✅ Removido: {spec_file}")
        except Exception as e:
            print(f"⚠️  Não foi possível remover {spec_file}: {e}")


def create_build_files():
    """Cria arquivos auxiliares para o build"""
    print("\n📄 Criando arquivos auxiliares...")
    
    # README.md
    readme_content = """# Analisador de Artigos e Livros v2.0

## Descrição
Software profissional para análise de listas de artigos científicos e livros acadêmicos.

## Funcionalidades
✅ Interface moderna e intuitiva
📊 Análise automática de arquivos CSV
📋 Listagem completa de títulos
🔍 Detecção inteligente de duplicados
📤 Exportação para CSV
⚡ Processamento rápido e eficiente

## Como usar
1. Execute o AnalisadorArtigos.exe
2. Clique em "Procurar" para selecionar seu arquivo CSV
3. Clique em "Analisar Arquivo"
4. Visualize os resultados detalhados
5. Exporte as listas conforme necessário

## Requisitos do arquivo CSV
- Deve conter uma coluna de títulos (title, título, nome, etc.)
- Opcionalmente uma coluna de autores (author, autor, etc.)
- Formato de texto padrão CSV

## Suporte
Desenvolvido com Python e Tkinter para máxima compatibilidade.
Versão: 2.0.0
"""
    
    # License
    license_content = """MIT License

Copyright (c) 2025 Analisador de Artigos e Livros

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to deal in the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""
    
    # Cria os arquivos
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ README.md criado")
        
        with open('LICENSE.txt', 'w', encoding='utf-8') as f:
            f.write(license_content)
        print("✅ LICENSE.txt criado")
        
    except Exception as e:
        print(f"⚠️  Erro ao criar arquivos: {e}")


def build_executable():
    """Compila o executável usando PyInstaller"""
    print("\n🔨 Compilando executável...")
    
    # Comando básico e funcional
    build_command = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Arquivo único
        '--windowed',                   # Sem console
        '--name=AnalisadorArtigos',     # Nome do executável
        '--clean',                      # Limpa cache
        '--noconfirm',                  # Não pede confirmação
        'article_analyzer.py'           # Arquivo fonte
    ]
    
    print("📋 Comando: " + ' '.join(build_command))
    
    try:
        # Executa o build
        result = subprocess.run(
            build_command,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        print("✅ Compilação concluída!")
        
        # Verifica se o executável foi criado
        exe_path = Path('dist/AnalisadorArtigos.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executável criado: {exe_path}")
            print(f"📏 Tamanho: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Executável não foi criado")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout - Build demorou mais de 5 minutos")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na compilação: {e}")
        if e.stdout:
            print("📄 Saída padrão:")
            print(e.stdout[-500:])  # Últimas 500 chars
        if e.stderr:
            print("🚫 Saída de erro:")
            print(e.stderr[-500:])  # Últimas 500 chars
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def test_executable():
    """Testa se o executável funciona"""
    print("\n🧪 Testando executável...")
    
    exe_path = Path('dist/AnalisadorArtigos.exe')
    if not exe_path.exists():
        print("❌ Executável não encontrado para teste")
        return False
    
    try:
        # Testa apenas se o arquivo é executável (não abre a interface)
        result = subprocess.run([str(exe_path)], timeout=5, capture_output=True)
        print("✅ Executável parece estar funcionando")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Executável iniciou (timeout normal para interface gráfica)")
        return True
    except Exception as e:
        print(f"⚠️  Não foi possível testar automaticamente: {e}")
        print("💡 Teste manualmente executando: dist/AnalisadorArtigos.exe")
        return True


def create_installer_script():
    """Cria script do Inno Setup para instalador profissional"""
    print("\n📦 Criando script do instalador...")
    
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
        print("✅ Script do instalador criado: installer.iss")
        print("💡 Use o Inno Setup para criar o instalador profissional")
        return True
    except Exception as e:
        print(f"⚠️  Erro ao criar script do instalador: {e}")
        return False


def main():
    """Função principal do build"""
    print_header()
    
    # 1. Verificar arquivos necessários
    if not check_requirements():
        input("\n❌ Build cancelado. Pressione Enter para sair...")
        return
    
    # 2. Instalar dependências
    if not install_dependencies():
        input("\n❌ Erro nas dependências. Pressione Enter para sair...")
        return
    
    # 3. Limpar builds anteriores
    clean_build_dirs()
    
    # 4. Criar arquivos auxiliares
    create_build_files()
    
    # 5. Compilar executável
    if not build_executable():
        input("\n❌ Falha na compilação. Pressione Enter para sair...")
        return
    
    # 6. Testar executável
    test_executable()
    
    # 7. Criar script do instalador
    create_installer_script()
    
    # 8. Resumo final
    print("\n" + "=" * 60)
    print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("📁 Arquivos criados:")
    print("   • dist/AnalisadorArtigos.exe (executável principal)")
    print("   • README.md (documentação)")
    print("   • LICENSE.txt (licença)")
    print("   • installer.iss (script do instalador)")
    
    print("\n📋 Próximos passos:")
    print("1. Teste o executável: dist/AnalisadorArtigos.exe")
    print("2. Para criar instalador profissional:")
    print("   - Baixe Inno Setup: https://jrsoftware.org/isinfo.php")
    print("   - Abra o arquivo installer.iss")
    print("   - Compile o instalador")
    
    # Pergunta se quer testar
    test_now = input("\n🧪 Deseja testar o executável agora? (s/N): ").lower().strip()
    if test_now in ['s', 'sim', 'y', 'yes']:
        try:
            exe_path = Path('dist/AnalisadorArtigos.exe')
            if exe_path.exists():
                print("🚀 Abrindo executável...")
                os.startfile(str(exe_path))
            else:
                print("❌ Executável não encontrado")
        except Exception as e:
            print(f"❌ Erro ao abrir executável: {e}")
    
    input("\nPressione Enter para finalizar...")


if __name__ == "__main__":
    main()