import os
import sys
import subprocess
import platform

def check_system_info():
    """Verifica informações do sistema"""
    print("="*60)
    print("🔍 DIAGNÓSTICO DO SISTEMA")
    print("="*60)
    
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Python executável: {sys.executable}")
    print(f"📂 Diretório atual: {os.getcwd()}")
    
    # Verifica variáveis de ambiente
    path_env = os.environ.get('PATH', '')
    python_path = os.path.dirname(sys.executable)
    scripts_path = os.path.join(python_path, 'Scripts')
    
    print(f"📍 Python PATH: {python_path}")
    print(f"📍 Scripts PATH: {scripts_path}")
    
    if scripts_path.lower() in path_env.lower():
        print("✅ Scripts está no PATH")
    else:
        print("❌ Scripts NÃO está no PATH")
    
    return python_path, scripts_path

def check_pip():
    """Verifica se pip funciona"""
    print(f"\n🔧 VERIFICANDO PIP")
    print("-"*30)
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                               capture_output=True, text=True, check=True)
        print(f"✅ pip: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Erro no pip: {e}")
        return False

def install_pyinstaller():
    """Instala PyInstaller usando diferentes métodos"""
    print(f"\n📦 INSTALANDO PYINSTALLER")
    print("-"*30)
    
    methods = [
        {
            'name': 'pip module',
            'cmd': [sys.executable, '-m', 'pip', 'install', 'pyinstaller']
        },
        {
            'name': 'pip upgrade',
            'cmd': [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pyinstaller']
        },
        {
            'name': 'pip force reinstall',
            'cmd': [sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'pyinstaller']
        },
        {
            'name': 'pip user install',
            'cmd': [sys.executable, '-m', 'pip', 'install', '--user', 'pyinstaller']
        }
    ]
    
    for method in methods:
        print(f"🔨 Tentando {method['name']}...")
        try:
            result = subprocess.run(method['cmd'], 
                                   capture_output=True, 
                                   text=True, 
                                   check=True,
                                   timeout=120)  # 2 minutos
            print(f"✅ {method['name']} - SUCESSO!")
            print(f"📄 Output: {result.stdout[:100]}...")
            return True
        except subprocess.TimeoutExpired:
            print(f"⏱️  {method['name']} - TIMEOUT")
        except subprocess.CalledProcessError as e:
            print(f"❌ {method['name']} - ERRO: {e.returncode}")
            if e.stderr:
                print(f"🚫 Stderr: {e.stderr[:200]}")
        except Exception as e:
            print(f"❌ {method['name']} - ERRO: {e}")
    
    return False

def find_pyinstaller():
    """Procura PyInstaller no sistema"""
    print(f"\n🔍 PROCURANDO PYINSTALLER")
    print("-"*30)
    
    # Locais possíveis
    python_path = os.path.dirname(sys.executable)
    possible_locations = [
        os.path.join(python_path, 'Scripts', 'pyinstaller.exe'),
        os.path.join(python_path, 'Scripts', 'pyinstaller'),
        os.path.join(os.path.expanduser('~'), '.local', 'bin', 'pyinstaller'),
        'pyinstaller.exe',
        'pyinstaller'
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            print(f"✅ Encontrado: {location}")
            return location
        else:
            print(f"❌ Não encontrado: {location}")
    
    # Tenta via Python
    try:
        result = subprocess.run([sys.executable, '-c', 'import PyInstaller; print(PyInstaller.__file__)'],
                               capture_output=True, text=True)
        if result.returncode == 0:
            pyinstaller_path = result.stdout.strip()
            print(f"✅ PyInstaller módulo encontrado: {pyinstaller_path}")
            
            # Tenta encontrar o executável
            module_dir = os.path.dirname(pyinstaller_path)
            exe_path = os.path.join(module_dir, '..', '..', 'Scripts', 'pyinstaller.exe')
            exe_path = os.path.normpath(exe_path)
            
            if os.path.exists(exe_path):
                print(f"✅ Executável PyInstaller: {exe_path}")
                return exe_path
    except Exception as e:
        print(f"❌ Erro ao procurar módulo: {e}")
    
    return None

def test_pyinstaller(pyinstaller_path=None):
    """Testa se PyInstaller funciona"""
    print(f"\n🧪 TESTANDO PYINSTALLER")
    print("-"*30)
    
    test_commands = []
    
    if pyinstaller_path:
        test_commands.append([pyinstaller_path, '--version'])
    
    test_commands.extend([
        ['pyinstaller', '--version'],
        [sys.executable, '-m', 'PyInstaller', '--version'],
        [sys.executable, '-c', 'import PyInstaller; print("PyInstaller importado com sucesso")']
    ])
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"🔸 Teste {i}: {' '.join(cmd[:2])}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                   check=True, timeout=10)
            print(f"✅ Teste {i} - SUCESSO!")
            print(f"📄 Output: {result.stdout.strip()}")
            return cmd[0] if len(cmd) > 1 else cmd
        except Exception as e:
            print(f"❌ Teste {i} - FALHOU: {e}")
    
    return None

def create_manual_build():
    """Cria script manual de build"""
    print(f"\n📝 CRIANDO SCRIPT MANUAL")
    print("-"*30)
    
    manual_script = f'''@echo off
echo Executando PyInstaller via Python...
"{sys.executable}" -m PyInstaller --onefile --windowed --name=AnalisadorArtigos article_analyzer.py
pause
'''
    
    with open('build_manual.bat', 'w') as f:
        f.write(manual_script)
    
    print("✅ Arquivo 'build_manual.bat' criado")
    
    # Também cria versão Python
    python_script = f'''#!/usr/bin/env python3
import subprocess
import sys

print("Executando PyInstaller via módulo Python...")
try:
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--onefile', '--windowed', 
        '--name=AnalisadorArtigos',
        'article_analyzer.py'
    ], check=True)
    print("✅ Build concluído!")
except Exception as e:
    print(f"❌ Erro: {{e}}")
    
    # Tenta versão console
    print("Tentando versão console...")
    try:
        subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--onefile', '--console', 
            '--name=AnalisadorArtigos_Console',
            'article_analyzer.py'
        ], check=True)
        print("✅ Build console concluído!")
    except Exception as e2:
        print(f"❌ Erro console: {{e2}}")

input("Pressione Enter para sair...")
'''
    
    with open('build_via_python.py', 'w') as f:
        f.write(python_script)
    
    print("✅ Arquivo 'build_via_python.py' criado")

def main():
    """Função principal"""
    print("🏥 DIAGNÓSTICO E REPARO - PYINSTALLER")
    
    # 1. Informações do sistema
    python_path, scripts_path = check_system_info()
    
    # 2. Verifica pip
    if not check_pip():
        print("❌ pip não funciona - instale/repare Python")
        input("Pressione Enter para sair...")
        return
    
    # 3. Procura PyInstaller existente
    pyinstaller_path = find_pyinstaller()
    
    # 4. Se não encontrou, instala
    if not pyinstaller_path:
        print("📦 PyInstaller não encontrado - instalando...")
        if install_pyinstaller():
            pyinstaller_path = find_pyinstaller()
    
    # 5. Testa PyInstaller
    working_command = test_pyinstaller(pyinstaller_path)
    
    # 6. Resultados e soluções
    print("\n" + "="*60)
    print("📋 RESUMO E SOLUÇÕES")
    print("="*60)
    
    if working_command:
        print("✅ PyInstaller está funcionando!")
        print(f"🎯 Comando que funciona: {' '.join(working_command) if isinstance(working_command, list) else working_command}")
        
        # Testa build rápido
        print("\n🚀 Testando build rápido...")
        try:
            if isinstance(working_command, list) and len(working_command) > 2:
                # É comando do tipo "python -m PyInstaller"
                test_cmd = working_command[:3] + ['--onefile', '--console', '--name=TesteRapido', 'article_analyzer.py']
            else:
                test_cmd = [working_command, '--onefile', '--console', '--name=TesteRapido', 'article_analyzer.py']
            
            subprocess.run(test_cmd, check=True, timeout=60, capture_output=True)
            if os.path.exists('dist/TesteRapido.exe'):
                print("✅ Build de teste funcionou!")
                os.remove('dist/TesteRapido.exe')
            else:
                print("⚠️  Build completou mas executável não foi criado")
        except Exception as e:
            print(f"❌ Build de teste falhou: {e}")
    
    else:
        print("❌ PyInstaller não está funcionando")
        print("\n🔧 SOLUÇÕES RECOMENDADAS:")
        print("1. Execute: build_manual.bat")
        print("2. Execute: build_via_python.py") 
        print("3. Reinstale Python completamente")
        print("4. Use ambiente virtual (venv)")
        print("5. Tente executar como administrador")
    
    # 7. Cria scripts manuais
    create_manual_build()
    
    print(f"\n📁 ARQUIVOS CRIADOS:")
    print("- build_manual.bat (método alternativo)")
    print("- build_via_python.py (método Python direto)")
    
    print(f"\n💡 PRÓXIMOS PASSOS:")
    if working_command:
        print("1. Use o comando que funcionou no teste")
        print("2. Execute build_via_python.py para build automático")
    else:
        print("1. Execute build_manual.bat")
        print("2. Se não funcionar, reinstale Python")
        print("3. Verifique se o antivírus não está bloqueando")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()