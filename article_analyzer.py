# ============================================================================
# INSTRUÇÕES PARA CRIAR O INSTALADOR
# ============================================================================

"""
PASSO 1: Instalar dependências necessárias
pip install pyinstaller pandas

PASSO 2: Criar arquivo spec personalizado (salvar como 'article_analyzer.spec')
"""

# article_analyzer.spec
spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['article_analyzer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnalisadorArtigos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Opcional: adicione um ícone
)
"""

print("1. Salve o conteúdo acima como 'article_analyzer.spec'")
print("2. Execute: pyinstaller article_analyzer.spec")

# ============================================================================
# ARQUIVO PARA BUILD AUTOMÁTICO
# ============================================================================

# build.py - Script para automatizar a criação do executável
build_script = '''
import os
import subprocess
import shutil
import sys

def build_executable():
    print("🔨 Iniciando build do executável...")
    
    # Verifica se os arquivos necessários existem
    if not os.path.exists('article_analyzer.py'):
        print("❌ Erro: arquivo article_analyzer.py não encontrado!")
        return False
    
    # Limpa builds anteriores
    if os.path.exists('dist'):
        print("🧹 Limpando builds anteriores...")
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    try:
        # Executa o PyInstaller
        print("📦 Criando executável com PyInstaller...")
        result = subprocess.run([
            'pyinstaller', 
            '--onefile',
            '--windowed',
            '--name=AnalisadorArtigos',
            '--clean',
            'article_analyzer.py'
        ], check=True)
        
        if os.path.exists('dist/AnalisadorArtigos.exe'):
            print("✅ Executável criado com sucesso!")
            print("📁 Localização: dist/AnalisadorArtigos.exe")
            return True
        else:
            print("❌ Erro: executável não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no PyInstaller: {e}")
        return False
    except FileNotFoundError:
        print("❌ Erro: PyInstaller não encontrado. Execute: pip install pyinstaller")
        return False

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\\n🎉 Build concluído com sucesso!")
        print("📋 Próximos passos:")
        print("   1. Teste o executável em dist/AnalisadorArtigos.exe")
        print("   2. Crie o instalador com o Inno Setup (opcional)")
    else:
        print("\\n❌ Build falhou. Verifique os erros acima.")
    
    input("\\nPressione Enter para sair...")
'''

print("\n" + "="*60)
print("SCRIPT DE BUILD AUTOMÁTICO")
print("="*60)
print(build_script)

# ============================================================================
# SCRIPT INNO SETUP PARA INSTALADOR PROFISSIONAL
# ============================================================================

inno_setup_script = """
; Script do Inno Setup para Analisador de Artigos
; Salve como: installer.iss

[Setup]
AppName=Analisador de Artigos e Livros
AppVersion=1.0.0
AppPublisher=Seu Nome
AppPublisherURL=https://seusite.com
AppSupportURL=https://seusite.com/suporte
AppUpdatesURL=https://seusite.com/updates
DefaultDirName={autopf}\\Analisador de Artigos
DefaultGroupName=Analisador de Artigos
AllowNoIcons=yes
LicenseFile=license.txt
OutputDir=installer_output
OutputBaseFilename=AnalisadorArtigos_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\AnalisadorArtigos.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Analisador de Artigos"; Filename: "{app}\\AnalisadorArtigos.exe"
Name: "{group}\\{cm:UninstallProgram,Analisador de Artigos}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\Analisador de Artigos"; Filename: "{app}\\AnalisadorArtigos.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\AnalisadorArtigos.exe"; Description: "{cm:LaunchProgram,Analisador de Artigos}"; Flags: nowait postinstall skipifsilent
"""

print("\n" + "="*60)
print("SCRIPT INNO SETUP PARA INSTALADOR")
print("="*60)
print(inno_setup_script)

# ============================================================================
# ARQUIVO README PARA DISTRIBUIÇÃO
# ============================================================================

readme_content = """
# Analisador de Artigos e Livros

## Descrição
Software desktop para análise de listas de artigos científicos e livros acadêmicos em formato CSV.

## Funcionalidades
- ✅ Validação automática de arquivos CSV
- 📊 Contagem total de títulos
- 📋 Listagem completa de todos os títulos
- 🔍 Detecção de duplicados (título + autor)
- 📤 Exportação para CSV (lista completa e duplicados)

## Como usar
1. Execute o programa
2. Clique em "Procurar" para selecionar um arquivo CSV
3. Clique em "Analisar Arquivo"
4. Visualize os resultados
5. Exporte as listas conforme necessário

## Formato do arquivo CSV
O arquivo deve conter colunas com títulos e autores. Exemplos de nomes aceitos:
- Títulos: "title", "título", "titulo", "nome"
- Autores: "author", "autor", "authors", "autores"

## Requisitos do sistema
- Windows 10 ou superior
- Não requer instalação de Python ou outras dependências

## Versão
1.0.0

## Suporte
Para dúvidas ou problemas, entre em contato através do email: seuemail@exemplo.com
"""

print("\n" + "="*60)
print("ARQUIVO README.MD")
print("="*60)
print(readme_content)

# ============================================================================
# LICENÇA SIMPLES
# ============================================================================

license_content = """
LICENÇA DE SOFTWARE

Copyright (c) 2025 Analisador de Artigos e Livros

Por meio desta, é concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e arquivos de documentação associados (o "Software"), para usar o Software sem restrições, incluindo, sem limitação, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, sujeito às seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIABILIDADE, ADEQUAÇÃO A UM PROPÓSITO ESPECÍFICO E NÃO VIOLAÇÃO. EM NENHUM CASO OS AUTORES OU DETENTORES DE COPYRIGHT SERÃO RESPONSÁVEIS POR QUALQUER REIVINDICAÇÃO, DANOS OU OUTRAS RESPONSABILIDADES, SEJA EM AÇÃO DE CONTRATO, DELITO OU DE OUTRA FORMA, DECORRENTES DE, OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.
"""

print("\n" + "="*60)
print("ARQUIVO LICENSE.TXT")
print("="*60)
print(license_content)