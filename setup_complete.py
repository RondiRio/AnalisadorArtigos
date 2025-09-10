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
        print("✅ Arquivo de configuração criado")
    except Exception as e:
        print(f"⚠️  Erro ao criar configuração: {e}")


def create_documentation():
    """Cria documentação completa"""
    print("📚 Criando documentação...")
    
    # Manual do usuário
    user_manual = """# Manual do Usuário - Analisador de Artigos v2.0

## Introdução
O Analisador de Artigos é um software profissional desenvolvido para auxiliar pesquisadores, bibliotecários e acadêmicos na análise de listas de artigos científicos e livros.

## Funcionalidades Principais

### ✅ Análise Automática
- Detecção automática de colunas de títulos e autores
- Validação de formato CSV
- Processamento rápido de grandes listas

### 🔍 Detecção de Duplicados
- Identificação inteligente de registros duplicados
- Comparação por título e autor
- Relatório detalhado de duplicatas

### 📊 Relatórios Detalhados
- Contagem total de registros
- Lista completa formatada
- Estatísticas de duplicação
- Interface visual moderna

### 📤 Exportação
- Exportação da lista completa
- Exportação apenas dos duplicados
- Formato CSV compatível com Excel
- Numeração automática

## Como Usar

### 1. Preparar o Arquivo CSV
Seu arquivo deve conter pelo menos uma coluna com títulos. Exemplos de nomes aceitos:
- **Títulos**: title, título, titulo, nome, name
- **Autores**: author, autor, authors, autores

### 2. Abrir o Software
Execute o arquivo `AnalisadorArtigos.exe`

### 3. Selecionar Arquivo
1. Clique em "📂 Procurar"
2. Navegue até seu arquivo CSV
3. Selecione o arquivo e clique em "Abrir"

### 4. Analisar
1. Clique em "🔍 Analisar Arquivo"
2. Aguarde o processamento
3. Visualize os resultados na tela

### 5. Exportar Resultados
- **Lista Completa**: Clique em "📋 Exportar Lista Completa"
- **Apenas Duplicados**: Clique em "🔍 Exportar Duplicados"

## Formatos Suportados
- CSV (UTF-8)
- CSV (Latin1/ANSI)
- Separadores: vírgula, ponto-e-vírgula

## Requisitos do Sistema
- Windows 10 ou superior
- 100 MB de espaço livre
- 4 GB de RAM (recomendado)

## Solução de Problemas

### Arquivo não é reconhecido
- Verifique se o arquivo é CSV válido
- Certifique-se de que há colunas de títulos
- Tente salvar novamente como CSV UTF-8

### Erro ao abrir arquivo
- Verifique permissões do arquivo
- Feche o arquivo no Excel antes de analisar
- Tente copiar o arquivo para outro local

### Duplicados não detectados
- Verifique se há coluna de autores
- Títulos devem ser idênticos para detecção
- Espaços extras podem afetar a comparação

## Suporte
Para dúvidas ou problemas, consulte o arquivo README.md ou contate o desenvolvedor.

---
**Analisador de Artigos v2.0** - Software profissional para análise acadêmica
"""
    
    try:
        docs_path = Path('docs')
        docs_path.mkdir(exist_ok=True)
        
        with open(docs_path / 'manual_usuario.md', 'w', encoding='utf-8') as f:
            f.write(user_manual)
        print("✅ Manual do usuário criado")
        
    except Exception as e:
        print(f"⚠️  Erro ao criar documentação: {e}")


def create_all_files():
    """Cria todos os arquivos necessários do projeto"""
    print("📄 Criando todos os arquivos do projeto...")
    
    create_project_structure()
    create_version_info()
    create_config_file()
    create_documentation()


def run_full_build():
    """Executa o build completo usando o script build.py"""
    print("\n🚀 Iniciando build completo...")
    
    try:
        # Executa o script de build
        result = subprocess.run([sys.executable, 'build.py'], 
                               check=True, capture_output=True, text=True)
        
        print("✅ Build executado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        if e.stdout:
            print("📄 Saída:", e.stdout[-300:])
        if e.stderr:
            print("🚫 Erro:", e.stderr[-300:])
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def create_distribution_package():
    """Cria pacote completo para distribuição"""
    print("\n📦 Criando pacote de distribuição...")
    
    # Verifica se o executável existe
    exe_path = Path('dist/AnalisadorArtigos.exe')
    if not exe_path.exists():
        print("❌ Executável não encontrado. Execute o build primeiro.")
        return False
    
    # Cria pasta de distribuição
    dist_folder = Path('AnalisadorArtigos_v2.0_Distribuicao')
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir()
    
    # Copia arquivos necessários
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
            print(f"✅ Copiado: {dst}")
    
    # Cria arquivo de instruções rápidas
    quick_start = """# INÍCIO RÁPIDO

## Para usar o software:
1. Execute: AnalisadorArtigos.exe
2. Selecione seu arquivo CSV
3. Clique em "Analisar Arquivo"
4. Visualize os resultados
5. Exporte as listas

## Para mais informações:
- Leia o Manual_do_Usuario.md
- Consulte o README.md

Versão: 2.0.0
"""
    
    with open(dist_folder / 'INICIO_RAPIDO.txt', 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print(f"✅ Pacote de distribuição criado: {dist_folder}")
    return True


def main():
    """Função principal do setup completo"""
    print("=" * 60)
    print("🏗️  SETUP COMPLETO - ANALISADOR DE ARTIGOS v2.0")
    print("=" * 60)
    
    # Verifica se o arquivo principal existe
    if not Path('article_analyzer.py').exists():
        print("❌ Arquivo article_analyzer.py não encontrado!")
        print("💡 Certifique-se de que está na pasta correta do projeto")
        input("Pressione Enter para sair...")
        return
    
    # 1. Criar estrutura e arquivos
    print("\n📋 FASE 1: Estrutura do Projeto")
    create_all_files()
    
    # 2. Executar build
    print("\n📋 FASE 2: Compilação")
    if not run_full_build():
        print("❌ Falha no build. Verifique os erros acima.")
        input("Pressione Enter para sair...")
        return
    
    # 3. Criar pacote de distribuição
    print("\n📋 FASE 3: Pacote de Distribuição")
    if not create_distribution_package():
        print("❌ Falha ao criar pacote de distribuição.")
    
    # 4. Resumo final
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETO FINALIZADO!")
    print("=" * 60)
    
    print("📁 Arquivos criados:")
    print("   • dist/AnalisadorArtigos.exe (executável principal)")
    print("   • AnalisadorArtigos_v2.0_Distribuicao/ (pacote completo)")
    print("   • docs/manual_usuario.md (documentação)")
    print("   • config.json (configurações)")
    print("   • installer.iss (script do instalador)")
    
    print("\n📦 Pronto para distribuição:")
    print("   • Executável standalone: dist/AnalisadorArtigos.exe")
    print("   • Pacote completo: AnalisadorArtigos_v2.0_Distribuicao/")
    print("   • Instalador (use Inno Setup): installer.iss")
    
    print("\n🚀 Próximos passos:")
    print("1. Teste o executável")
    print("2. Distribua o pacote completo")
    print("3. Para instalador profissional, use o Inno Setup")
    
    # Pergunta final
    choice = input("\n🧪 O que deseja fazer agora?\n"
                  "1. Testar executável\n"
                  "2. Abrir pasta de distribuição\n"
                  "3. Sair\n"
                  "Escolha (1-3): ").strip()
    
    if choice == '1':
        try:
            exe_path = Path('dist/AnalisadorArtigos.exe')
            if exe_path.exists():
                print("🚀 Abrindo executável...")
                if os.name == 'nt':  # Windows
                    os.startfile(str(exe_path))
                else:
                    subprocess.run([str(exe_path)])
            else:
                print("❌ Executável não encontrado")
        except Exception as e:
            print(f"❌ Erro ao abrir executável: {e}")
    
    elif choice == '2':
        try:
            dist_folder = Path('AnalisadorArtigos_v2.0_Distribuicao')
            if dist_folder.exists():
                if os.name == 'nt':  # Windows
                    os.startfile(str(dist_folder))
                else:
                    subprocess.run(['xdg-open', str(dist_folder)])
            else:
                print("❌ Pasta de distribuição não encontrada")
        except Exception as e:
            print(f"❌ Erro ao abrir pasta: {e}")
    
    print("\n✅ Setup finalizado com sucesso!")
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()