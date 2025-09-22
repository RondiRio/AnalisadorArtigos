"""
Analisador de Artigos e Livros - Versão 2.0
Interface moderna e funcional para análise de listas acadêmicas
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import sys
from pathlib import Path


class ModernStyle:
    """Modern style settings for the interface"""
    
    # Modern color palette
    COLORS = {
        'primary': '#2563eb',      # Modern blue
        'primary_hover': '#1d4ed8', 
        'secondary': '#64748b',    # Bluish gray
        'success': '#10b981',      # Green
        'warning': '#f59e0b',      # Yellow
        'danger': '#ef4444',       # Red
        'bg_primary': '#ffffff',   # White
        'bg_secondary': '#f8fafc', # Very light gray
        'text_primary': '#1e293b', # Dark gray
        'text_secondary': '#64748b', # Medium gray
        'border': '#e2e8f0'        # Light gray
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


class ArticleAnalyzer:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.apply_modern_style()
        self.create_interface()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("Analisador de Artigos e Livros v2.0")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
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
        self.duplicates = []
        self.file_path = tk.StringVar()
        
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
        main_container.rowconfigure(2, weight=1)
        
        # Cabeçalho
        self.create_header(main_container)
        
        # Seção de seleção de arquivo
        self.create_file_selection(main_container)
        
        # Área de resultados
        self.create_results_area(main_container)
        
        # Área de botões de exportação
        self.create_export_buttons(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Cria o cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
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
            text="Análise profissional de listas acadêmicas em formato CSV",
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
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
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
        
    def create_results_area(self, parent):
        """Cria a área de resultados"""
        results_frame = ttk.LabelFrame(
            parent,
            text="📊 Resultados da Análise",
            style='Modern.TLabelframe',
            padding=15
        )
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
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
        export_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        export_frame.columnconfigure((0, 1), weight=1)
        
        # Botão exportar todos
        self.export_all_btn = ttk.Button(
            export_frame,
            text="📋 Exportar Lista Completa",
            command=self.export_all_titles,
            state=tk.DISABLED,
            style='Modern.TButton'
        )
        self.export_all_btn.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        # Botão exportar duplicados
        self.export_duplicates_btn = ttk.Button(
            export_frame,
            text="🔍 Exportar Duplicados",
            command=self.export_duplicates,
            state=tk.DISABLED,
            style='Modern.TButton'
        )
        self.export_duplicates_btn.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
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
        status_label.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
    def update_status(self, message):
        """Atualiza a mensagem de status"""
        self.status_var.set(message)
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
        
        result_text += "\n" + "═" * 70 + "\n\n"
        
        # Lista completa
        result_text += "📚 LISTA COMPLETA DE TÍTULOS\n"
        result_text += "─" * 40 + "\n"
        
        for i, title in enumerate(self.all_titles, 1):
            result_text += f"{i:4d}. {title}\n"
        
        result_text += f"\n✅ Total listado: {len(self.all_titles):,} registros\n\n"
        
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