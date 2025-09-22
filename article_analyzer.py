"""
Analisador de Artigos e Livros - Versão 2.1
Interface moderna e funcional para análise de listas acadêmicas com tradução automática
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import sys
import requests
import time
from pathlib import Path
from urllib.parse import quote
import re
from threading import Thread


class TranslationService:
    """Serviço de tradução automática"""
    
    def __init__(self):
        self.cache = {}  # Cache para evitar traduzir o mesmo texto múltiplas vezes
        
    def detect_language(self, text):
        """Detecta se o texto está em inglês usando padrões comuns"""
        if not text or len(text.strip()) < 3:
            return "pt"
            
        text_lower = text.lower()
        
        # Palavras comuns em inglês acadêmico
        english_indicators = [
            'the', 'and', 'of', 'in', 'on', 'for', 'with', 'by', 'from', 'up', 'about', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among',
            'analysis', 'research', 'study', 'review', 'development', 'application', 'approach',
            'method', 'system', 'model', 'framework', 'theory', 'concept', 'investigation',
            'examination', 'assessment', 'evaluation', 'implementation', 'design', 'performance'
        ]
        
        # Palavras comuns em português
        portuguese_indicators = [
            'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'para', 'por',
            'com', 'sobre', 'entre', 'através', 'durante', 'antes', 'depois', 'acima', 'abaixo',
            'análise', 'pesquisa', 'estudo', 'revisão', 'desenvolvimento', 'aplicação', 'abordagem',
            'método', 'sistema', 'modelo', 'estrutura', 'teoria', 'conceito', 'investigação',
            'exame', 'avaliação', 'implementação', 'design', 'desempenho', 'uma', 'um', 'umas', 'uns'
        ]
        
        words = re.findall(r'\b\w+\b', text_lower)
        
        english_score = sum(1 for word in words if word in english_indicators)
        portuguese_score = sum(1 for word in words if word in portuguese_indicators)
        
        # Se houver mais indicadores em inglês, considera inglês
        if english_score > portuguese_score and english_score >= 2:
            return "en"
        else:
            return "pt"
    
    def translate_google_api_fallback(self, text, from_lang="en", to_lang="pt"):
        """Tradução usando API pública do Google Translate (método de fallback)"""
        try:
            # URL da API pública (não oficial)
            base_url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": from_lang,
                "tl": to_lang,
                "dt": "t",
                "q": text
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and len(result[0]) > 0:
                    translated_text = ''.join([item[0] for item in result[0] if item[0]])
                    return translated_text.strip()
                    
        except Exception as e:
            print(f"Erro na tradução via Google API: {e}")
            
        return None
    
    def translate_mymemory(self, text, from_lang="en", to_lang="pt"):
        """Tradução usando MyMemory API (gratuita)"""
        try:
            url = f"https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f'{from_lang}|{to_lang}'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'responseData' in result and 'translatedText' in result['responseData']:
                    translation = result['responseData']['translatedText']
                    # Verifica se a tradução é válida (não é erro)
                    if not translation.upper().startswith('PLEASE'):
                        return translation.strip()
                        
        except Exception as e:
            print(f"Erro na tradução via MyMemory: {e}")
            
        return None
    
    def translate_text(self, text):
        """Traduz texto do inglês para português"""
        if not text or text.strip() == "":
            return text
            
        # Verifica cache
        cache_key = text.lower().strip()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Detecta idioma
        if self.detect_language(text) != "en":
            # Se não é inglês, retorna o texto original
            self.cache[cache_key] = text
            return text
        
        # Tenta várias APIs de tradução
        translation = None
        
        # Primeira tentativa: MyMemory (mais confiável)
        translation = self.translate_mymemory(text)
        
        # Segunda tentativa: Google API (fallback)
        if not translation:
            time.sleep(0.5)  # Pausa para evitar rate limit
            translation = self.translate_google_api_fallback(text)
        
        # Se conseguiu traduzir, salva no cache
        if translation and translation.lower() != text.lower():
            self.cache[cache_key] = translation
            return translation
        else:
            # Se não conseguiu traduzir, salva o original no cache
            self.cache[cache_key] = text
            return text
    
    def get_cache_size(self):
        """Retorna o tamanho do cache de traduções"""
        return len(self.cache)


class ModernStyle:
    """Configurações de estilo moderno para a interface"""
    
    # Paleta de cores moderna
    COLORS = {
        'primary': '#2563eb',      # Azul moderno
        'primary_hover': '#1d4ed8', 
        'secondary': '#64748b',    # Cinza azulado
        'success': '#10b981',      # Verde
        'warning': '#f59e0b',      # Amarelo
        'danger': '#ef4444',       # Vermelho
        'bg_primary': '#ffffff',   # Branco
        'bg_secondary': '#f8fafc', # Cinza muito claro
        'text_primary': '#1e293b', # Cinza escuro
        'text_secondary': '#64748b', # Cinza médio
        'border': '#e2e8f0'        # Cinza claro
    }
    
    @staticmethod
    def apply_modern_style():
        """Aplica estilo moderno aos widgets ttk"""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Estilo para botões
        style.configure(
            'Modern.TButton',
            padding=(20, 10),
            font=('Segoe UI', 10),
            borderwidth=1,
            focuscolor='none'
        )
        
        style.map(
            'Modern.TButton',
            background=[
                ('active', ModernStyle.COLORS['primary_hover']),
                ('!active', ModernStyle.COLORS['primary'])
            ],
            foreground=[('active', 'white'), ('!active', 'white')],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')]
        )
        
        # Estilo para botão primário
        style.configure(
            'Primary.TButton',
            padding=(25, 12),
            font=('Segoe UI', 11, 'bold')
        )
        
        # Estilo para botão de tradução
        style.configure(
            'Translation.TButton',
            padding=(20, 10),
            font=('Segoe UI', 10),
            borderwidth=1
        )
        
        style.map(
            'Translation.TButton',
            background=[
                ('active', '#059669'),
                ('!active', '#10b981')
            ],
            foreground=[('active', 'white'), ('!active', 'white')]
        )
        
        # Estilo para labels
        style.configure(
            'Modern.TLabel',
            font=('Segoe UI', 10),
            foreground=ModernStyle.COLORS['text_primary']
        )
        
        # Estilo para título
        style.configure(
            'Title.TLabel',
            font=('Segoe UI', 18, 'bold'),
            foreground=ModernStyle.COLORS['primary']
        )
        
        # Estilo para entry
        style.configure(
            'Modern.TEntry',
            padding=(10, 8),
            font=('Segoe UI', 10),
            borderwidth=2
        )
        
        # Estilo para LabelFrame
        style.configure(
            'Modern.TLabelframe',
            borderwidth=2,
            relief='flat',
            labelmargins=(10, 0, 0, 0)
        )
        
        style.configure(
            'Modern.TLabelframe.Label',
            font=('Segoe UI', 11, 'bold'),
            foreground=ModernStyle.COLORS['primary']
        )
        
        # Estilo para checkbutton
        style.configure(
            'Modern.TCheckbutton',
            font=('Segoe UI', 10),
            foreground=ModernStyle.COLORS['text_primary']
        )


class ArticleAnalyzer:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.apply_modern_style()
        self.create_interface()
        
        # Inicializa serviço de tradução
        self.translator = TranslationService()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("Analisador de Artigos e Livros v2.1 - Com Tradução")
        self.root.geometry("950x750")
        self.root.minsize(850, 650)
        
        # Configurar ícone (se disponível)
        try:
            if hasattr(sys, '_MEIPASS'):
                # Executável PyInstaller
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                icon_path = 'icon.ico'
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Centralizar janela
        self.center_window()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Inicializa as variáveis da aplicação"""
        self.df = None
        self.all_titles = []
        self.translated_titles = []
        self.duplicates = []
        self.file_path = tk.StringVar()
        self.enable_translation = tk.BooleanVar(value=True)
        self.translation_progress = tk.StringVar(value="")
        
    def apply_modern_style(self):
        """Aplica o estilo moderno"""
        ModernStyle.apply_modern_style()
        self.root.configure(bg=ModernStyle.COLORS['bg_secondary'])
        
    def create_interface(self):
        """Cria a interface do usuário"""
        # Container principal com padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(3, weight=1)
        
        # Cabeçalho
        self.create_header(main_container)
        
        # Seção de seleção de arquivo
        self.create_file_selection(main_container)
        
        # Seção de configurações de tradução
        self.create_translation_options(main_container)
        
        # Área de resultados
        self.create_results_area(main_container)
        
        # Área de botões de exportação
        self.create_export_buttons(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Cria o cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 25))
        header_frame.columnconfigure(0, weight=1)
        
        # Título principal
        title_label = ttk.Label(
            header_frame,
            text="📚 Analisador de Artigos e Livros",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0)
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Análise profissional de listas acadêmicas em CSV com tradução automática",
            style='Modern.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
    def create_file_selection(self, parent):
        """Cria a seção de seleção de arquivo"""
        file_frame = ttk.LabelFrame(
            parent,
            text="📁 Selecionar Arquivo CSV",
            style='Modern.TLabelframe',
            padding=15
        )
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(1, weight=1)
        
        # Label
        ttk.Label(
            file_frame,
            text="Arquivo:",
            style='Modern.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Entry para caminho do arquivo
        self.file_entry = ttk.Entry(
            file_frame,
            textvariable=self.file_path,
            style='Modern.TEntry'
        )
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botão procurar
        browse_btn = ttk.Button(
            file_frame,
            text="📂 Procurar",
            command=self.browse_file,
            style='Modern.TButton'
        )
        browse_btn.grid(row=0, column=2)
        
        # Botão analisar
        analyze_btn = ttk.Button(
            file_frame,
            text="🔍 Analisar Arquivo",
            command=self.analyze_file,
            style='Primary.TButton'
        )
        analyze_btn.grid(row=1, column=0, columnspan=3, pady=(15, 0))
        
    def create_translation_options(self, parent):
        """Cria as opções de tradução"""
        translation_frame = ttk.LabelFrame(
            parent,
            text="🌐 Configurações de Tradução",
            style='Modern.TLabelframe',
            padding=15
        )
        translation_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        translation_frame.columnconfigure(1, weight=1)
        
        # Checkbox para habilitar tradução
        self.translation_checkbox = ttk.Checkbutton(
            translation_frame,
            text="Traduzir títulos em inglês automaticamente",
            variable=self.enable_translation,
            style='Modern.TCheckbutton'
        )
        self.translation_checkbox.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Label de progresso da tradução
        self.translation_progress_label = ttk.Label(
            translation_frame,
            textvariable=self.translation_progress,
            style='Modern.TLabel'
        )
        self.translation_progress_label.grid(row=1, column=0, sticky=tk.W)
        
        # Informação sobre a tradução
        info_label = ttk.Label(
            translation_frame,
            text="💡 Dica: Títulos detectados em inglês serão traduzidos para português e exibidos junto ao original",
            style='Modern.TLabel',
            foreground=ModernStyle.COLORS['text_secondary']
        )
        info_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
    def create_results_area(self, parent):
        """Cria a área de resultados"""
        results_frame = ttk.LabelFrame(
            parent,
            text="📊 Resultados da Análise",
            style='Modern.TLabelframe',
            padding=15
        )
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Text widget com scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.results_text = tk.Text(
            text_frame,
            font=('Consolas', 10),
            wrap=tk.WORD,
            bg='white',
            fg=ModernStyle.COLORS['text_primary'],
            relief='flat',
            borderwidth=2,
            padx=15,
            pady=15
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
    def create_export_buttons(self, parent):
        """Cria os botões de exportação"""
        export_frame = ttk.Frame(parent)
        export_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        export_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Botão exportar todos
        self.export_all_btn = ttk.Button(
            export_frame,
            text="📋 Exportar Lista Completa",
            command=self.export_all_titles,
            state=tk.DISABLED,
            style='Modern.TButton'
        )
        self.export_all_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        # Botão exportar com tradução
        self.export_translated_btn = ttk.Button(
            export_frame,
            text="🌐 Exportar com Traduções",
            command=self.export_with_translations,
            state=tk.DISABLED,
            style='Translation.TButton'
        )
        self.export_translated_btn.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Botão exportar duplicados
        self.export_duplicates_btn = ttk.Button(
            export_frame,
            text="🔍 Exportar Duplicados",
            command=self.export_duplicates,
            state=tk.DISABLED,
            style='Modern.TButton'
        )
        self.export_duplicates_btn.grid(row=0, column=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
    def create_status_bar(self, parent):
        """Cria a barra de status"""
        self.status_var = tk.StringVar(value="Pronto para análise")
        status_label = ttk.Label(
            parent,
            textvariable=self.status_var,
            style='Modern.TLabel',
            relief=tk.SUNKEN,
            padding=(10, 5)
        )
        status_label.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
    def update_status(self, message):
        """Atualiza a mensagem de status"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def update_translation_progress(self, message):
        """Atualiza o progresso da tradução"""
        self.translation_progress.set(message)
        self.root.update_idletasks()
        
    def browse_file(self):
        """Abre dialog para seleção de arquivo"""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo CSV",
            filetypes=[
                ("Arquivos CSV", "*.csv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if file_path:
            self.file_path.set(file_path)
            self.update_status(f"Arquivo selecionado: {Path(file_path).name}")
    
    def is_valid_academic_content(self, df):
        """Verifica se o CSV contém conteúdo acadêmico válido"""
        if df.empty:
            return False
            
        academic_keywords = [
            'title', 'titulo', 'título', 'article', 'artigo', 'book', 'livro',
            'paper', 'journal', 'author', 'autor', 'publication', 'publicação',
            'doi', 'isbn', 'volume', 'issue', 'year', 'ano', 'name', 'nome'
        ]
        
        columns_text = ' '.join(df.columns).lower()
        has_academic_columns = any(keyword in columns_text for keyword in academic_keywords)
        
        if not has_academic_columns:
            return False
            
        # Verifica se há dados válidos
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['title', 'titulo', 'título', 'nome', 'name']):
                sample_data = df[col].dropna().head(10)
                if len(sample_data) > 0:
                    avg_length = sample_data.str.len().mean()
                    if avg_length > 10:
                        return True
        
        return False
    
    def find_title_and_author_columns(self, df):
        """Identifica colunas de título e autor"""
        title_col = None
        author_col = None
        
        # Procura coluna de título
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in ['title', 'titulo', 'título', 'nome', 'name']):
                title_col = col
                break
        
        # Procura coluna de autor
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in ['author', 'autor', 'autores', 'authors']):
                author_col = col
                break
        
        return title_col, author_col
    
    def translate_titles_async(self, titles):
        """Traduz títulos em thread separada"""
        def translate_worker():
            translated = []
            total = len(titles)
            
            for i, title in enumerate(titles):
                if self.enable_translation.get():
                    # Extrai apenas o título (remove autor se existir)
                    title_only = title.split(" — ")[0] if " — " in title else title
                    
                    # Atualiza progresso
                    progress_msg = f"Traduzindo... {i+1}/{total} ({((i+1)/total)*100:.0f}%)"
                    self.root.after(0, lambda msg=progress_msg: self.update_translation_progress(msg))
                    
                    # Traduz o título
                    translated_title = self.translator.translate_text(title_only)
                    
                    # Se foi traduzido (diferente do original), adiciona a tradução
                    if (translated_title.lower() != title_only.lower() and 
                        self.translator.detect_language(title_only) == "en"):
                        
                        if " — " in title:
                            author_part = " — " + title.split(" — ")[1]
                            full_entry = f"{title_only}\n   🔄 {translated_title}{author_part}"
                        else:
                            full_entry = f"{title_only}\n   🔄 {translated_title}"
                        translated.append(full_entry)
                    else:
                        translated.append(title)
                else:
                    translated.append(title)
                    
                # Pequena pausa para não sobrecarregar as APIs
                time.sleep(0.1)
            
            # Atualiza a interface principal com os resultados
            self.root.after(0, lambda: self.finish_translation(translated))
            
        # Inicia a thread de tradução
        thread = Thread(target=translate_worker, daemon=True)
        thread.start()
    
    def finish_translation(self, translated_titles):
        """Finaliza o processo de tradução"""
        self.translated_titles = translated_titles
        self.update_translation_progress(f"✅ Tradução concluída! Cache: {self.translator.get_cache_size()} entradas")
        
        # Reexibe os resultados com as traduções
        self.display_results_with_translations()
        
        # Habilita o botão de exportação com tradução
        if self.translated_titles:
            self.export_translated_btn.config(state=tk.NORMAL)
    
    def analyze_file(self):
        """Analisa o arquivo CSV selecionado"""
        if not self.file_path.get():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV.")
            return
        
        file_path = self.file_path.get()
        if not os.path.exists(file_path):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return
        
        self.update_status("Analisando arquivo...")
        
        try:
            # Lê o arquivo CSV
            self.df = pd.read_csv(file_path, encoding='utf-8')
            
        except UnicodeDecodeError:
            try:
                # Tenta com encoding diferente
                self.df = pd.read_csv(file_path, encoding='latin1')
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler arquivo: {str(e)}")
                return
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar arquivo: {str(e)}")
            return
        
        # Valida conteúdo
        if not self.is_valid_academic_content(self.df):
            messagebox.showerror(
                "Arquivo Inválido", 
                "O arquivo não parece conter uma lista válida de artigos ou livros acadêmicos.\n\n"
                "Verifique se o arquivo possui colunas como 'title', 'autor', etc."
            )
            return
        
        # Identifica colunas
        title_col, author_col = self.find_title_and_author_columns(self.df)
        
        if not title_col:
            messagebox.showerror("Erro", "Não foi possível identificar uma coluna de títulos.")
            return
        
        # Processa dados
        self.process_data(title_col, author_col)
        
        # Habilita botões de exportação
        self.export_all_btn.config(state=tk.NORMAL)
        self.export_duplicates_btn.config(state=tk.NORMAL)
        
        # Inicia tradução se habilitada
        if self.enable_translation.get() and self.all_titles:
            self.update_translation_progress("Iniciando tradução...")
            self.translate_titles_async(self.all_titles)
        else:
            self.update_translation_progress("")
        
        self.update_status("Análise concluída com sucesso!")
        
    def process_data(self, title_col, author_col):
        """Processa os dados do CSV"""
        # Remove linhas vazias
        self.df = self.df.dropna(subset=[title_col])
        
        total_count = len(self.df)
        
        # Prepara lista completa
        self.all_titles = []
        for _, row in self.df.iterrows():
            title = str(row[title_col]).strip()
            if author_col and pd.notna(row[author_col]):
                author = str(row[author_col]).strip()
                self.all_titles.append(f"{title} — {author}")
            else:
                self.all_titles.append(title)
        
        # Identifica duplicados
        if author_col:
            # Combina título e autor para detecção de duplicados
            self.df['combined'] = (
                self.df[title_col].astype(str).str.strip() + " | " + 
                self.df[author_col].astype(str).str.strip()
            )
            duplicated_mask = self.df.duplicated(subset=['combined'], keep=False)
            duplicates_df = self.df[duplicated_mask]
            
            self.duplicates = []
            for _, row in duplicates_df.iterrows():
                title = str(row[title_col]).strip()
                author = str(row[author_col]).strip() if pd.notna(row[author_col]) else "Autor não informado"
                self.duplicates.append(f"{title} — {author}")
        else:
            duplicated_mask = self.df.duplicated(subset=[title_col], keep=False)
            duplicates_df = self.df[duplicated_mask]
            self.duplicates = [str(title).strip() for title in duplicates_df[title_col]]
        
        # Exibe resultados
        self.display_results(total_count, len(self.duplicates), title_col, author_col)
    
    def display_results(self, total_count, duplicate_count, title_col, author_col):
        """Exibe os resultados da análise"""
        self.results_text.delete(1.0, tk.END)
        
        # Cabeçalho estilizado
        result_text = "═" * 70 + "\n"
        result_text += "📊 ANÁLISE COMPLETA DE ARTIGOS E LIVROS\n"
        result_text += "═" * 70 + "\n\n"
        
        # Resumo executivo
        result_text += "📋 RESUMO EXECUTIVO\n"
        result_text += "─" * 40 + "\n"
        result_text += f"• Total de registros analisados: {total_count:,}\n"
        result_text += f"• Registros únicos: {total_count - duplicate_count:,}\n"
        result_text += f"• Duplicados encontrados: {duplicate_count:,}\n"
        
        if duplicate_count > 0:
            percentage = (duplicate_count / total_count) * 100
            result_text += f"• Taxa de duplicação: {percentage:.1f}%\n"
        
        result_text += f"• Coluna de títulos: '{title_col}'\n"
        if author_col:
            result_text += f"• Coluna de autores: '{author_col}'\n"
        
        # Informações de tradução
        if self.enable_translation.get():
            result_text += f"• Tradução automática: HABILITADA 🌐\n"
            result_text += f"• Cache de traduções: {self.translator.get_cache_size()} entradas\n"
        else:
            result_text += f"• Tradução automática: DESABILITADA\n"
        
        result_text += "\n" + "═" * 70 + "\n\n"
        
        # Lista completa
        result_text += "📚 LISTA COMPLETA DE TÍTULOS\n"
        result_text += "─" * 40 + "\n"
        
        for i, title in enumerate(self.all_titles, 1):
            result_text += f"{i:4d}. {title}\n"
        
        result_text += f"\n✅ Total listado: {len(self.all_titles):,} registros\n"
        
        if self.enable_translation.get():
            result_text += "\n💡 NOTA: Títulos em inglês serão traduzidos automaticamente\n"
            result_text += "    🔄 = Tradução para português\n"
        
        result_text += "\n"
        
        # Duplicados (se houver)
        if duplicate_count > 0:
            result_text += "🔍 REGISTROS DUPLICADOS IDENTIFICADOS\n"
            result_text += "─" * 40 + "\n"
            
            for i, duplicate in enumerate(self.duplicates, 1):
                result_text += f"{i:4d}. {duplicate}\n"
            
            result_text += f"\n⚠️  Total de duplicados: {len(self.duplicates):,} registros\n"
            result_text += "\n💡 RECOMENDAÇÃO: Revise os duplicados antes de prosseguir\n"
        else:
            result_text += "✅ NENHUM DUPLICADO ENCONTRADO\n"
            result_text += "─" * 40 + "\n"
            result_text += "Parabéns! Sua lista não contém registros duplicados.\n"
        
        result_text += "\n" + "═" * 70 + "\n"
        result_text += "📤 Use os botões abaixo para exportar os resultados\n"
        
        self.results_text.insert(1.0, result_text)
    
    def display_results_with_translations(self):
        """Exibe os resultados com as traduções incluídas"""
        self.results_text.delete(1.0, tk.END)
        
        # Cabeçalho estilizado
        result_text = "═" * 70 + "\n"
        result_text += "📊 ANÁLISE COMPLETA COM TRADUÇÕES\n"
        result_text += "═" * 70 + "\n\n"
        
        # Resumo executivo
        result_text += "📋 RESUMO EXECUTIVO\n"
        result_text += "─" * 40 + "\n"
        result_text += f"• Total de registros analisados: {len(self.all_titles):,}\n"
        result_text += f"• Registros únicos: {len(self.all_titles) - len(self.duplicates):,}\n"
        result_text += f"• Duplicados encontrados: {len(self.duplicates):,}\n"
        
        # Conta quantos títulos foram traduzidos
        translated_count = sum(1 for title in self.translated_titles if "🔄" in title)
        result_text += f"• Títulos traduzidos: {translated_count:,}\n"
        result_text += f"• Cache de traduções: {self.translator.get_cache_size()} entradas\n"
        
        if len(self.duplicates) > 0:
            percentage = (len(self.duplicates) / len(self.all_titles)) * 100
            result_text += f"• Taxa de duplicação: {percentage:.1f}%\n"
        
        result_text += "\n" + "═" * 70 + "\n\n"
        
        # Lista completa com traduções
        result_text += "📚 LISTA COMPLETA COM TRADUÇÕES\n"
        result_text += "─" * 40 + "\n"
        result_text += "🔄 = Tradução automática para português\n\n"
        
        for i, title in enumerate(self.translated_titles, 1):
            result_text += f"{i:4d}. {title}\n"
        
        result_text += f"\n✅ Total listado: {len(self.translated_titles):,} registros\n"
        result_text += f"✅ Traduzidos: {translated_count:,} títulos\n\n"
        
        # Duplicados (se houver)
        if len(self.duplicates) > 0:
            result_text += "🔍 REGISTROS DUPLICADOS IDENTIFICADOS\n"
            result_text += "─" * 40 + "\n"
            
            for i, duplicate in enumerate(self.duplicates, 1):
                result_text += f"{i:4d}. {duplicate}\n"
            
            result_text += f"\n⚠️  Total de duplicados: {len(self.duplicates):,} registros\n"
            result_text += "\n💡 RECOMENDAÇÃO: Revise os duplicados antes de prosseguir\n"
        else:
            result_text += "✅ NENHUM DUPLICADO ENCONTRADO\n"
            result_text += "─" * 40 + "\n"
            result_text += "Parabéns! Sua lista não contém registros duplicados.\n"
        
        result_text += "\n" + "═" * 70 + "\n"
        result_text += "📤 Use os botões abaixo para exportar os resultados\n"
        
        self.results_text.insert(1.0, result_text)
    
    def export_all_titles(self):
        """Exporta todos os títulos para CSV"""
        if not self.all_titles:
            messagebox.showwarning("Aviso", "Não há dados para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar lista completa",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if file_path:
            try:
                export_data = []
                for i, title in enumerate(self.all_titles, 1):
                    export_data.append({"Número": i, "Título Completo": title})
                
                # Adiciona resumo
                export_data.append({"Número": "", "Título Completo": ""})
                export_data.append({"Número": "RESUMO:", "Título Completo": f"Total de {len(self.all_titles)} registros"})
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo(
                    "Exportação Concluída", 
                    f"Lista completa exportada com sucesso!\n\n"
                    f"Arquivo: {Path(file_path).name}\n"
                    f"Total de registros: {len(self.all_titles)}"
                )
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar arquivo: {str(e)}")
    
    def export_with_translations(self):
        """Exporta lista com traduções para CSV"""
        if not self.translated_titles:
            messagebox.showwarning("Aviso", "Não há dados traduzidos para exportar. Execute a análise primeiro.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar lista com traduções",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if file_path:
            try:
                export_data = []
                translated_count = 0
                
                for i, title in enumerate(self.translated_titles, 1):
                    # Separa original e tradução se houver
                    if "🔄" in title:
                        translated_count += 1
                        lines = title.split("\n")
                        original = lines[0].strip()
                        translation = lines[1].replace("   🔄 ", "").strip()
                        
                        export_data.append({
                            "Número": i, 
                            "Título Original": original,
                            "Tradução (PT-BR)": translation,
                            "Status": "Traduzido"
                        })
                    else:
                        export_data.append({
                            "Número": i, 
                            "Título Original": title,
                            "Tradução (PT-BR)": "",
                            "Status": "Original em português"
                        })
                
                # Adiciona resumo
                export_data.append({
                    "Número": "", 
                    "Título Original": "",
                    "Tradução (PT-BR)": "",
                    "Status": ""
                })
                export_data.append({
                    "Número": "RESUMO:", 
                    "Título Original": f"Total: {len(self.translated_titles)} registros",
                    "Tradução (PT-BR)": f"Traduzidos: {translated_count}",
                    "Status": f"Cache: {self.translator.get_cache_size()} entradas"
                })
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo(
                    "Exportação Concluída", 
                    f"Lista com traduções exportada com sucesso!\n\n"
                    f"Arquivo: {Path(file_path).name}\n"
                    f"Total de registros: {len(self.translated_titles)}\n"
                    f"Traduzidos: {translated_count}"
                )
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar arquivo: {str(e)}")
    
    def export_duplicates(self):
        """Exporta apenas os duplicados para CSV"""
        if not self.duplicates:
            messagebox.showinfo("Informação", "Não há registros duplicados para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar lista de duplicados",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if file_path:
            try:
                export_data = []
                for i, duplicate in enumerate(self.duplicates, 1):
                    export_data.append({"Número": i, "Registro Duplicado": duplicate})
                
                # Adiciona resumo
                export_data.append({"Número": "", "Registro Duplicado": ""})
                export_data.append({"Número": "RESUMO:", "Registro Duplicado": f"Total de {len(self.duplicates)} duplicados"})
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo(
                    "Exportação Concluída", 
                    f"Lista de duplicados exportada com sucesso!\n\n"
                    f"Arquivo: {Path(file_path).name}\n"
                    f"Total de duplicados: {len(self.duplicates)}"
                )
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar arquivo: {str(e)}")


def main():
    """Função principal da aplicação"""
    try:
        root = tk.Tk()
        app = ArticleAnalyzer(root)
        root.mainloop()
    except Exception as e:
        # Log do erro para debug
        import traceback
        with open('error_log.txt', 'w') as f:
            f.write(f"Erro na aplicação: {e}\n")
            f.write(traceback.format_exc())
        
        # Mostra erro para o usuário
        try:
            messagebox.showerror("Erro Fatal", f"Erro inesperado: {e}")
        except:
            print(f"Erro fatal: {e}")


if __name__ == "__main__":
    main()