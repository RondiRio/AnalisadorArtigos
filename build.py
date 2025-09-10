# import os
# import subprocess
# import shutil
# import sys

# def build_executable():
#     print("🔨 Iniciando build do executável...")
    
#     # Verifica se os arquivos necessários existem
#     if not os.path.exists('article_analyzer.py'):
#         print("❌ Erro: arquivo article_analyzer.py não encontrado!")
#         return False
    
#     # Limpa builds anteriores
#     if os.path.exists('dist'):
#         print("🧹 Limpando builds anteriores...")
#         shutil.rmtree('dist')
#     if os.path.exists('build'):
#         shutil.rmtree('build')
    
#     try:
#         # Executa o PyInstaller
#         print("📦 Criando executável com PyInstaller...")
#         result = subprocess.run([
#             'pyinstaller', 
#             '--onefile',
#             '--windowed',
#             '--name=AnalisadorArtigos',
#             '--clean',
#             '--add-data=README.md;.',
#             'article_analyzer.py'
#         ], check=True, capture_output=True, text=True)
        
#         print("PyInstaller output:")
#         print(result.stdout)
#         if result.stderr:
#             print("Warnings/Errors:")
#             print(result.stderr)
        
#         if os.path.exists('dist/AnalisadorArtigos.exe'):
#             print("✅ Executável criado com sucesso!")
#             print("📁 Localização: dist/AnalisadorArtigos.exe")
            
#             # Verifica o tamanho do arquivo
#             size = os.path.getsize('dist/AnalisadorArtigos.exe')
#             size_mb = size / (1024 * 1024)
#             print(f"📏 Tamanho: {size_mb:.2f} MB")
            
#             return True
#         else:
#             print("❌ Erro: executável não foi criado")
#             return False
            
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Erro no PyInstaller: {e}")
#         print("Stdout:", e.stdout if hasattr(e, 'stdout') else "N/A")
#         print("Stderr:", e.stderr if hasattr(e, 'stderr') else "N/A")
#         return False
#     except FileNotFoundError:
#         print("❌ Erro: PyInstaller não encontrado.")
#         print("💡 Solução: Execute 'pip install pyinstaller'")
#         return False

# def create_installer_files():
#     """Cria arquivos necessários para o instalador"""
#     print("\n📄 Criando arquivos auxiliares...")
    
#     # README.md
#     readme_content = """# Analisador de Artigos e Livros

# ## Descrição
# Software desktop para análise de listas de artigos científicos e livros acadêmicos em formato CSV.

# ## Funcionalidades
# - ✅ Validação automática de arquivos CSV
# - 📊 Contagem total de títulos
# - 📋 Listagem completa de todos os títulos
# - 🔍 Detecção de duplicados (título + autor)
# - 📤 Exportação para CSV (lista completa e duplicados)

# ## Como usar
# 1. Execute o programa
# 2. Clique em "Procurar" para selecionar um arquivo CSV
# 3. Clique em "Analisar Arquivo"
# 4. Visualize os resultados
# 5. Exporte as listas conforme necessário

# ## Formato do arquivo CSV
# O arquivo deve conter colunas com títulos e autores. Exemplos de nomes aceitos:
# - Títulos: "title", "título", "titulo", "nome"
# - Autores: "author", "autor", "authors", "autores"

# ## Requisitos do sistema
# - Windows 10 ou superior
# - Não requer instalação de Python

# ## Versão
# 1.0.0
# """
    
#     # License.txt
#     license_content = """LICENÇA DE SOFTWARE

# Copyright (c) 2025 Analisador de Artigos e Livros

# Por meio desta, é concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software para usar sem restrições.

# O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO.
# """
    
#     # Cria os arquivos
#     with open('README.md', 'w', encoding='utf-8') as f:
#         f.write(readme_content)
    
#     with open('license.txt', 'w', encoding='utf-8') as f:
#         f.write(license_content)
    
#     print("✅ Arquivos README.md e license.txt criados")

# def test_executable():
#     """Testa se o executável foi criado corretamente"""
#     exe_path = 'dist/AnalisadorArtigos.exe'
#     if os.path.exists(exe_path):
#         print(f"\n🧪 Testando executável...")
#         try:
#             # Apenas verifica se o arquivo pode ser executado
#             result = subprocess.run([exe_path, '--help'], 
#                                   capture_output=True, 
#                                   text=True, 
#                                   timeout=5)
#             print("✅ Executável parece estar funcionando")
#         except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
#             print("⚠️  Não foi possível testar o executável automaticamente")
#             print("   Teste manualmente executando: dist/AnalisadorArtigos.exe")

# def main():
#     print("="*60)
#     print("🚀 BUILD AUTOMÁTICO - ANALISADOR DE ARTIGOS")
#     print("="*60)
    
#     # Verifica dependências
#     try:
#         import pandas
#         print("✅ pandas encontrado")
#     except ImportError:
#         print("❌ pandas não encontrado. Execute: pip install pandas")
#         return
    
#     # Cria arquivos auxiliares
#     create_installer_files()
    
#     # Faz o build
#     success = build_executable()
    
#     if success:
#         test_executable()
#         print("\n" + "="*60)
#         print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
#         print("="*60)
#         print("📋 Próximos passos:")
#         print("   1. Teste o executável: dist/AnalisadorArtigos.exe")
#         print("   2. Para criar instalador profissional:")
#         print("      - Baixe o Inno Setup (https://jrsoftware.org/isinfo.php)")
#         print("      - Use o arquivo installer.iss fornecido")
#         print("   3. Distribua o executável ou o instalador")
#         print("\n📁 Arquivos criados:")
#         print("   - dist/AnalisadorArtigos.exe (executável)")
#         print("   - README.md (documentação)")
#         print("   - license.txt (licença)")
#     else:
#         print("\n" + "="*60)
#         print("❌ BUILD FALHOU")
#         print("="*60)
#         print("🔧 Possíveis soluções:")
#         print("   1. Verifique se article_analyzer.py existe")
#         print("   2. Execute: pip install pyinstaller pandas")
#         print("   3. Verifique os erros acima")
    
#     input("\nPressione Enter para sair...")

# if __name__ == "__main__":
#     main()

# import os
# import subprocess
# import shutil
# import sys
# import time

# def check_python_version():
#     """Verifica a versão do Python"""
#     version = sys.version_info
#     print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
#     if version.major < 3 or (version.major == 3 and version.minor < 8):
#         print("⚠️  Recomendado Python 3.8 ou superior")
#     return True

# def install_dependencies():
#     """Instala dependências com tratamento de erros"""
#     print("📦 Verificando e instalando dependências...")
    
#     dependencies = ['pandas', 'pyinstaller']
    
#     for dep in dependencies:
#         try:
#             __import__(dep)
#             print(f"✅ {dep} já instalado")
#         except ImportError:
#             print(f"📥 Instalando {dep}...")
#             try:
#                 subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
#                              check=True, capture_output=True)
#                 print(f"✅ {dep} instalado com sucesso")
#             except subprocess.CalledProcessError as e:
#                 print(f"❌ Erro ao instalar {dep}: {e}")
#                 return False
    
#     return True

# def clean_previous_builds():
#     """Remove builds anteriores"""
#     folders_to_clean = ['dist', 'build', '__pycache__']
#     files_to_clean = ['AnalisadorArtigos.spec']
    
#     for folder in folders_to_clean:
#         if os.path.exists(folder):
#             print(f"🧹 Removendo pasta {folder}...")
#             try:
#                 shutil.rmtree(folder)
#             except Exception as e:
#                 print(f"⚠️  Não foi possível remover {folder}: {e}")
    
#     for file in files_to_clean:
#         if os.path.exists(file):
#             print(f"🧹 Removendo arquivo {file}...")
#             try:
#                 os.remove(file)
#             except Exception as e:
#                 print(f"⚠️  Não foi possível remover {file}: {e}")

# def create_spec_file():
#     """Cria um arquivo spec personalizado"""
#     spec_content = """# -*- mode: python ; coding: utf-8 -*-

# block_cipher = None

# a = Analysis(
#     ['article_analyzer.py'],
#     pathex=[],
#     binaries=[],
#     datas=[],
#     hiddenimports=['pandas._libs.tslibs.timedeltas'],
#     hookspath=[],
#     hooksconfig={},
#     runtime_hooks=[],
#     excludes=[],
#     win_no_prefer_redirects=False,
#     win_private_assemblies=False,
#     cipher=block_cipher,
#     noarchive=False,
# )

# pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# exe = EXE(
#     pyz,
#     a.scripts,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     [],
#     name='AnalisadorArtigos',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     runtime_tmpdir=None,
#     console=False,
#     disable_windowed_traceback=False,
#     argv_emulation=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
# )
# """
    
#     with open('AnalisadorArtigos.spec', 'w', encoding='utf-8') as f:
#         f.write(spec_content)
    
#     print("✅ Arquivo spec criado")

# def build_with_different_methods():
#     """Tenta diferentes métodos de build"""
#     methods = [
#         {
#             'name': 'Método 1: Comando simples',
#             'args': [
#                 'pyinstaller',
#                 '--onefile',
#                 '--windowed',
#                 '--name=AnalisadorArtigos',
#                 '--clean',
#                 '--noconfirm',
#                 'article_analyzer.py'
#             ]
#         },
#         {
#             'name': 'Método 2: Com spec file',
#             'args': [
#                 'pyinstaller',
#                 '--clean',
#                 '--noconfirm',
#                 'AnalisadorArtigos.spec'
#             ]
#         },
#         {
#             'name': 'Método 3: Modo console (debug)',
#             'args': [
#                 'pyinstaller',
#                 '--onefile',
#                 '--console',
#                 '--name=AnalisadorArtigos_Debug',
#                 '--clean',
#                 '--noconfirm',
#                 'article_analyzer.py'
#             ]
#         },
#         {
#             'name': 'Método 4: Sem otimizações',
#             'args': [
#                 'pyinstaller',
#                 '--onefile',
#                 '--windowed',
#                 '--name=AnalisadorArtigos',
#                 '--clean',
#                 '--noconfirm',
#                 '--noupx',
#                 'article_analyzer.py'
#             ]
#         }
#     ]
    
#     for i, method in enumerate(methods, 1):
#         print(f"\n🔨 Tentando {method['name']}...")
        
#         # Cria spec file se necessário
#         if 'spec' in method['name'].lower():
#             create_spec_file()
        
#         try:
#             result = subprocess.run(
#                 method['args'],
#                 check=True,
#                 capture_output=True,
#                 text=True,
#                 timeout=300  # 5 minutos timeout
#             )
            
#             # Verifica se o executável foi criado
#             possible_names = ['AnalisadorArtigos.exe', 'AnalisadorArtigos_Debug.exe']
#             executable_created = False
            
#             for name in possible_names:
#                 if os.path.exists(f'dist/{name}'):
#                     print(f"✅ {method['name']} - SUCESSO!")
#                     print(f"📁 Executável criado: dist/{name}")
                    
#                     # Testa o tamanho
#                     size = os.path.getsize(f'dist/{name}')
#                     size_mb = size / (1024 * 1024)
#                     print(f"📏 Tamanho: {size_mb:.2f} MB")
                    
#                     executable_created = True
#                     break
            
#             if executable_created:
#                 return True
                
#         except subprocess.TimeoutExpired:
#             print(f"⏱️  {method['name']} - TIMEOUT (mais de 5 minutos)")
#         except subprocess.CalledProcessError as e:
#             print(f"❌ {method['name']} - ERRO")
#             if e.stdout:
#                 print(f"📄 Stdout: {e.stdout[:200]}...")
#             if e.stderr:
#                 print(f"🚫 Stderr: {e.stderr[:200]}...")
#         except Exception as e:
#             print(f"❌ {method['name']} - ERRO INESPERADO: {e}")
        
#         # Limpa entre tentativas
#         time.sleep(1)
#         clean_previous_builds()
    
#     return False

# def create_simple_bat():
#     """Cria um bat file simplificado para casos extremos"""
#     bat_content = """@echo off
# echo Metodo alternativo - PyInstaller basico
# pyinstaller --onefile --console article_analyzer.py
# pause
# """
    
#     with open('build_simples.bat', 'w') as f:
#         f.write(bat_content)
    
#     print("📝 Arquivo 'build_simples.bat' criado como alternativa")

# def main():
#     print("="*60)
#     print("🔧 BUILD CORRIGIDO - ANALISADOR DE ARTIGOS")
#     print("="*60)
    
#     # Verifica arquivo principal
#     if not os.path.exists('article_analyzer.py'):
#         print("❌ Arquivo article_analyzer.py não encontrado!")
#         input("Pressione Enter para sair...")
#         return
    
#     # Verifica Python
#     check_python_version()
    
#     # Instala dependências
#     if not install_dependencies():
#         print("❌ Falha ao instalar dependências")
#         input("Pressione Enter para sair...")
#         return
    
#     # Limpa builds anteriores
#     clean_previous_builds()
    
#     # Cria arquivos auxiliares
#     create_installer_files()
    
#     # Tenta build com diferentes métodos
#     print("\n🚀 Iniciando processo de build...")
#     success = build_with_different_methods()
    
#     if success:
#         print("\n" + "="*60)
#         print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
#         print("="*60)
        
#         # Lista arquivos criados
#         if os.path.exists('dist'):
#             print("📁 Arquivos criados:")
#             for file in os.listdir('dist'):
#                 if file.endswith('.exe'):
#                     filepath = os.path.join('dist', file)
#                     size = os.path.getsize(filepath)
#                     size_mb = size / (1024 * 1024)
#                     print(f"   🚀 {file} ({size_mb:.1f} MB)")
        
#         # Pergunta sobre teste
#         test = input("\n🧪 Deseja testar o executável agora? (s/N): ").lower()
#         if test == 's':
#             for file in os.listdir('dist'):
#                 if file.endswith('.exe'):
#                     try:
#                         subprocess.Popen([os.path.join('dist', file)])
#                         print(f"🚀 Executando {file}...")
#                         break
#                     except Exception as e:
#                         print(f"❌ Erro ao executar: {e}")
    
#     else:
#         print("\n" + "="*60)
#         print("❌ TODOS OS MÉTODOS FALHARAM")
#         print("="*60)
#         print("🔧 Soluções alternativas:")
#         print("1. Execute 'build_simples.bat' (foi criado)")
#         print("2. Tente: pip uninstall pyinstaller && pip install pyinstaller")
#         print("3. Tente: pip install --upgrade pyinstaller")
#         print("4. Reinicie o computador e tente novamente")
#         print("5. Use Python 3.9 ou 3.10 (versões mais estáveis)")
        
#         create_simple_bat()
    
#     input("\nPressione Enter para sair...")

# def create_installer_files():
#     """Cria arquivos necessários"""
#     readme_content = """# Analisador de Artigos e Livros

# Software desktop para análise de listas de artigos científicos e livros acadêmicos.

# ## Como usar
# 1. Execute o programa
# 2. Selecione um arquivo CSV
# 3. Analise os resultados
# 4. Exporte as listas

# ## Versão: 1.0.0
# """
    
#     license_content = """MIT License

# Copyright (c) 2025 Analisador de Artigos

# Permissão concedida para uso gratuito.
# """
    
#     try:
#         with open('README.md', 'w', encoding='utf-8') as f:
#             f.write(readme_content)
        
#         with open('license.txt', 'w', encoding='utf-8') as f:
#             f.write(license_content)
        
#         print("✅ Arquivos auxiliares criados")
#     except Exception as e:
#         print(f"⚠️  Erro ao criar arquivos auxiliares: {e}")

# if __name__ == "__main__":
#     main()


import os
import subprocess
import sys
import platform

def find_venv():
    """Encontra e ativa a venv automaticamente"""
    print("🔍 Procurando ambiente virtual (venv)...")
    
    # Possíveis localizações da venv
    possible_venv_paths = [
        '../venv',           # Um nível acima
        '../env',            # Um nível acima
        '../.venv',          # Um nível acima (oculta)
        '../../venv',        # Dois níveis acima
        '../../env',         # Dois níveis acima
        'venv',              # Pasta atual
        'env',               # Pasta atual
        '.venv'              # Pasta atual (oculta)
    ]
    
    for venv_path in possible_venv_paths:
        if platform.system() == "Windows":
            python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
            pip_exe = os.path.join(venv_path, 'Scripts', 'pip.exe')
            pyinstaller_exe = os.path.join(venv_path, 'Scripts', 'pyinstaller.exe')
        else:
            python_exe = os.path.join(venv_path, 'bin', 'python')
            pip_exe = os.path.join(venv_path, 'bin', 'pip')
            pyinstaller_exe = os.path.join(venv_path, 'bin', 'pyinstaller')
        
        if os.path.exists(python_exe):
            print(f"✅ venv encontrada em: {os.path.abspath(venv_path)}")
            print(f"🐍 Python: {python_exe}")
            
            return {
                'path': os.path.abspath(venv_path),
                'python': python_exe,
                'pip': pip_exe,
                'pyinstaller': pyinstaller_exe if os.path.exists(pyinstaller_exe) else None
            }
    
    print("❌ Nenhuma venv encontrada nos locais comuns")
    return None

def install_pyinstaller_in_venv(venv_info):
    """Instala PyInstaller na venv encontrada"""
    print(f"\n📦 Instalando PyInstaller na venv...")
    
    try:
        # Primeiro verifica se já está instalado
        result = subprocess.run([
            venv_info['python'], '-c', 
            'import PyInstaller; print("PyInstaller já instalado:", PyInstaller.__version__)'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
            return True
        
        # Se não está instalado, instala
        print("📥 Instalando PyInstaller...")
        result = subprocess.run([
            venv_info['python'], '-m', 'pip', 'install', 'pyinstaller'
        ], capture_output=True, text=True, check=True)
        
        print("✅ PyInstaller instalado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar PyInstaller: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def build_with_venv(venv_info):
    """Faz o build usando a venv"""
    print(f"\n🔨 Fazendo build com venv...")
    
    # Diferentes métodos de build
    build_methods = [
        {
            'name': 'PyInstaller direto da venv',
            'cmd': [venv_info['pyinstaller'], '--onefile', '--windowed', '--name=AnalisadorArtigos', 'article_analyzer.py']
        },
        {
            'name': 'Python -m PyInstaller',
            'cmd': [venv_info['python'], '-m', 'PyInstaller', '--onefile', '--windowed', '--name=AnalisadorArtigos', 'article_analyzer.py']
        },
        {
            'name': 'Versão console (fallback)',
            'cmd': [venv_info['python'], '-m', 'PyInstaller', '--onefile', '--console', '--name=AnalisadorArtigos_Console', 'article_analyzer.py']
        }
    ]
    
    for method in build_methods:
        # Pula se o executável não existe
        if method['name'] == 'PyInstaller direto da venv' and not venv_info['pyinstaller']:
            continue
        
        if method['name'] == 'PyInstaller direto da venv' and not os.path.exists(venv_info['pyinstaller']):
            continue
        
        print(f"\n🚀 Tentando: {method['name']}...")
        
        try:
            # Limpa build anterior
            if os.path.exists('dist'):
                import shutil
                shutil.rmtree('dist')
            if os.path.exists('build'):
                import shutil
                shutil.rmtree('build')
            
            result = subprocess.run(
                method['cmd'],
                capture_output=True,
                text=True,
                check=True,
                cwd=os.getcwd()
            )
            
            # Verifica se o executável foi criado
            possible_exes = ['AnalisadorArtigos.exe', 'AnalisadorArtigos_Console.exe']
            for exe_name in possible_exes:
                exe_path = f'dist/{exe_name}'
                if os.path.exists(exe_path):
                    size = os.path.getsize(exe_path)
                    size_mb = size / (1024 * 1024)
                    print(f"✅ {method['name']} - SUCESSO!")
                    print(f"📁 Executável: {exe_path}")
                    print(f"📏 Tamanho: {size_mb:.2f} MB")
                    return True
            
            print(f"⚠️  {method['name']} - Comando executou mas executável não foi criado")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ {method['name']} - ERRO: {e.returncode}")
            if e.stdout:
                print(f"📄 Stdout: {e.stdout[:200]}...")
            if e.stderr:
                print(f"🚫 Stderr: {e.stderr[:200]}...")
        except Exception as e:
            print(f"❌ {method['name']} - ERRO INESPERADO: {e}")
    
    return False

def create_venv_batch():
    """Cria um arquivo batch que usa a venv automaticamente"""
    venv_info = find_venv()
    if not venv_info:
        return
    
    batch_content = f'''@echo off
echo Usando venv em: {venv_info['path']}

:: Ativa a venv e executa PyInstaller
"{venv_info['python']}" -m pip install pyinstaller
"{venv_info['python']}" -m PyInstaller --onefile --windowed --name=AnalisadorArtigos article_analyzer.py

echo.
echo Build concluído!
pause
'''
    
    with open('build_com_venv.bat', 'w') as f:
        f.write(batch_content)
    
    print("✅ Arquivo 'build_com_venv.bat' criado")

def main():
    print("="*60)
    print("🔧 BUILD COM AMBIENTE VIRTUAL (VENV)")
    print("="*60)
    
    # Verifica se o arquivo principal existe
    if not os.path.exists('article_analyzer.py'):
        print("❌ Arquivo 'article_analyzer.py' não encontrado!")
        print("💡 Certifique-se de estar na pasta correta")
        input("Pressione Enter para sair...")
        return
    
    print("✅ Arquivo principal encontrado")
    
    # Encontra a venv
    venv_info = find_venv()
    if not venv_info:
        print("\n❌ Ambiente virtual não encontrado!")
        print("\n🔧 SOLUÇÕES:")
        print("1. Ative sua venv manualmente: venv\\Scripts\\activate")
        print("2. Execute os comandos na pasta onde a venv está")
        print("3. Crie uma nova venv: python -m venv venv")
        input("\nPressione Enter para sair...")
        return
    
    # Instala PyInstaller se necessário
    if not install_pyinstaller_in_venv(venv_info):
        print("❌ Falha ao instalar PyInstaller")
        create_venv_batch()  # Cria batch como alternativa
        input("Pressione Enter para sair...")
        return
    
    # Faz o build
    success = build_with_venv(venv_info)
    
    if success:
        print("\n" + "="*60)
        print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("="*60)
        
        # Lista arquivos criados
        if os.path.exists('dist'):
            print("📁 Arquivos criados:")
            for file in os.listdir('dist'):
                if file.endswith('.exe'):
                    filepath = os.path.join('dist', file)
                    size = os.path.getsize(filepath)
                    size_mb = size / (1024 * 1024)
                    print(f"   🚀 {file} ({size_mb:.1f} MB)")
        
        # Pergunta sobre teste
        test = input("\n🧪 Deseja testar o executável agora? (s/N): ").lower()
        if test == 's':
            for file in os.listdir('dist'):
                if file.endswith('.exe'):
                    try:
                        subprocess.Popen([os.path.join('dist', file)])
                        print(f"🚀 Executando {file}...")
                        break
                    except Exception as e:
                        print(f"❌ Erro ao executar: {e}")
    else:
        print("\n" + "="*60)
        print("❌ BUILD FALHOU")
        print("="*60)
        create_venv_batch()
        print("🔧 Tente executar: build_com_venv.bat")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()