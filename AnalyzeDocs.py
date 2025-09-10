import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pandas as pd
import os
import re

class ArticleAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Artigos e Livros")
        self.root.geometry("800x600")
        
        # Variáveis
        self.df = None
        self.all_titles = []
        self.duplicates = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Analisador de Artigos e Livros", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de arquivo
        ttk.Label(main_frame, text="Arquivo CSV:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(main_frame, textvariable=self.file_path_var, width=50)
        self.file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        
        browse_button = ttk.Button(main_frame, text="Procurar", command=self.browse_file)
        browse_button.grid(row=1, column=2, pady=5)
        
        # Botão de análise
        analyze_button = ttk.Button(main_frame, text="Analisar Arquivo", 
                                   command=self.analyze_file, style="Accent.TButton")
        analyze_button.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para botões de export
        export_frame = ttk.Frame(main_frame)
        export_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.export_all_button = ttk.Button(export_frame, text="Exportar Todos os Títulos", 
                                           command=self.export_all_titles, state="disabled")
        self.export_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_duplicates_button = ttk.Button(export_frame, text="Exportar Duplicados", 
                                                  command=self.export_duplicates, state="disabled")
        self.export_duplicates_button.pack(side=tk.LEFT)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def is_valid_academic_content(self, df):
        """
        Verifica se o CSV contém uma lista válida de artigos/livros acadêmicos
        """
        # Palavras-chave que indicam conteúdo acadêmico
        academic_keywords = [
            'title', 'titulo', 'título', 'article', 'artigo', 'book', 'livro',
            'paper', 'journal', 'author', 'autor', 'publication', 'publicação',
            'doi', 'isbn', 'volume', 'issue', 'year', 'ano', 'publisher', 'editora'
        ]
        
        # Verifica se há colunas com nomes relacionados a conteúdo acadêmico
        columns = [col.lower() for col in df.columns]
        has_academic_columns = any(keyword in ' '.join(columns) for keyword in academic_keywords)
        
        if not has_academic_columns:
            return False
        
        # Verifica se há pelo menos uma coluna que parece conter títulos
        title_columns = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['title', 'titulo', 'título', 'nome', 'name']):
                title_columns.append(col)
        
        if not title_columns:
            return False
        
        # Verifica se os dados nas colunas de título parecem ser títulos válidos
        for col in title_columns:
            sample_data = df[col].dropna().head(10)
            if len(sample_data) == 0:
                continue
            
            # Verifica se os textos têm tamanho razoável para títulos
            avg_length = sample_data.str.len().mean()
            if avg_length > 10:  # Títulos geralmente têm mais de 10 caracteres
                return True
        
        return False
    
    def find_title_and_author_columns(self, df):
        """
        Identifica as colunas de título e autor no DataFrame
        """
        title_col = None
        author_col = None
        
        # Procura coluna de título
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['title', 'titulo', 'título', 'nome']):
                title_col = col
                break
        
        # Procura coluna de autor
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['author', 'autor', 'autores', 'authors']):
                author_col = col
                break
        
        return title_col, author_col
    
    def analyze_file(self):
        if not self.file_path_var.get():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV.")
            return
        
        try:
            # Lê o arquivo CSV
            self.df = pd.read_csv(self.file_path_var.get())
            
            # Verifica se é um arquivo válido
            if not self.is_valid_academic_content(self.df):
                messagebox.showerror("Arquivo inválido", 
                                   "Arquivo inválido, inclua uma lista de artigos, livros ou algo similar.")
                return
            
            # Identifica colunas de título e autor
            title_col, author_col = self.find_title_and_author_columns(self.df)
            
            if not title_col:
                messagebox.showerror("Erro", "Não foi possível identificar uma coluna de títulos.")
                return
            
            # Limpa dados
            self.df = self.df.dropna(subset=[title_col])
            
            # Primeira contagem - todos os títulos
            total_count = len(self.df)
            
            # Prepara lista de todos os títulos
            if author_col:
                self.all_titles = []
                for _, row in self.df.iterrows():
                    title = str(row[title_col]).strip()
                    author = str(row[author_col]).strip() if pd.notna(row[author_col]) else "Autor não informado"
                    self.all_titles.append(f"{title} - {author}")
            else:
                self.all_titles = [str(title).strip() for title in self.df[title_col]]
            
            # Identifica duplicados (títulos e autores exatamente iguais)
            if author_col:
                # Cria uma coluna combinada para identificar duplicados
                self.df['title_author'] = self.df[title_col].astype(str) + " | " + self.df[author_col].astype(str)
                duplicated_mask = self.df.duplicated(subset=['title_author'], keep=False)
                duplicates_df = self.df[duplicated_mask].copy()
                
                # Prepara lista de duplicados
                self.duplicates = []
                for _, row in duplicates_df.iterrows():
                    title = str(row[title_col]).strip()
                    author = str(row[author_col]).strip() if pd.notna(row[author_col]) else "Autor não informado"
                    self.duplicates.append(f"{title} - {author}")
            else:
                duplicated_mask = self.df.duplicated(subset=[title_col], keep=False)
                duplicates_df = self.df[duplicated_mask]
                self.duplicates = [str(title).strip() for title in duplicates_df[title_col]]
            
            duplicate_count = len(self.duplicates)
            
            # Exibe resultados
            self.display_results(total_count, duplicate_count, title_col, author_col)
            
            # Habilita botões de exportação
            self.export_all_button.config(state="normal")
            self.export_duplicates_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar o arquivo: {str(e)}")
    
    def display_results(self, total_count, duplicate_count, title_col, author_col):
        """
        Exibe os resultados na área de texto
        """
        self.results_text.delete(1.0, tk.END)
        
        # Cabeçalho
        result_text = "="*60 + "\n"
        result_text += "RESULTADOS DA ANÁLISE\n"
        result_text += "="*60 + "\n\n"
        
        # Primeira contagem
        result_text += f"📊 CONTAGEM TOTAL: {total_count} títulos encontrados\n\n"
        
        # Lista todos os títulos
        result_text += "📚 LISTA DE TODOS OS TÍTULOS:\n"
        result_text += "-"*40 + "\n"
        for i, title in enumerate(self.all_titles, 1):
            result_text += f"{i:3d}. {title}\n"
        
        result_text += f"\nTotal de títulos listados: {len(self.all_titles)}\n\n"
        
        # Segunda contagem (duplicados)
        if duplicate_count > 0:
            result_text += f"🔍 CONTAGEM DE DUPLICADOS: {duplicate_count} títulos duplicados encontrados\n\n"
            result_text += "📋 LISTA DE TÍTULOS DUPLICADOS:\n"
            result_text += "-"*40 + "\n"
            for i, duplicate in enumerate(self.duplicates, 1):
                result_text += f"{i:3d}. {duplicate}\n"
            
            result_text += f"\nTotal de títulos duplicados: {len(self.duplicates)}\n"
        else:
            result_text += "✅ Nenhum título duplicado encontrado!\n"
        
        self.results_text.insert(1.0, result_text)
    
    def export_all_titles(self):
        """
        Exporta todos os títulos para um arquivo CSV
        """
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
                # Cria DataFrame com todos os títulos
                export_data = []
                for i, title in enumerate(self.all_titles, 1):
                    export_data.append({"Número": i, "Título": title})
                
                # Adiciona linha com o total
                export_data.append({"Número": "", "Título": f"TOTAL DE TÍTULOS: {len(self.all_titles)}"})
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo("Sucesso", f"Lista completa exportada com sucesso!\nArquivo: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar arquivo: {str(e)}")
    
    def export_duplicates(self):
        """
        Exporta apenas os títulos duplicados para um arquivo CSV
        """
        if not self.duplicates:
            messagebox.showinfo("Info", "Não há títulos duplicados para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar lista de duplicados",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if file_path:
            try:
                # Cria DataFrame com títulos duplicados
                export_data = []
                for i, duplicate in enumerate(self.duplicates, 1):
                    export_data.append({"Número": i, "Título Duplicado": duplicate})
                
                # Adiciona linha com o total
                export_data.append({"Número": "", "Título Duplicado": f"TOTAL DE DUPLICADOS: {len(self.duplicates)}"})
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo("Sucesso", f"Lista de duplicados exportada com sucesso!\nArquivo: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar arquivo: {str(e)}")

def main():
    root = tk.Tk()
    app = ArticleAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()