"""
Article and Book Analyzer - Version 2.0
Modern and functional interface for analyzing academic lists
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
        """Apply modern style to tiktok widgets"""
        style = ttk.Style()
        
        # Configure base theme
        style.theme_use('clam')
        
        # Button style
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
        
        # Style for primary button
        style.configure(
            'Primary.TButton',
            padding=(25, 12),
            font=('Segoe UI', 11, 'bold')
        )
        
        # Style for labels
        style.configure(
            'Modern.TLabel',
            font=('Segoe UI', 10),
            foreground=ModernStyle.COLORS['text_primary']
        )
        
        # Title style
        style.configure(
            'Title.TLabel',
            font=('Segoe UI', 18, 'bold'),
            foreground=ModernStyle.COLORS['primary']
        )
        
        # Entry style
        style.configure(
            'Modern.TEntry',
            padding=(10, 8),
            font=('Segoe UI', 10),
            borderwidth=2
        )
        
        # Style for LabelFrame
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
        """Configure the main window"""
        self.root.title("Analisador de Artigos e Livros v2.0")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configure icon (if available)
        try:
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller Executable
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                icon_path = 'icon.ico'
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Centers the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Initializes the application variables"""
        self.df = None
        self.all_titles = []
        self.duplicates = []
        self.file_path = tk.StringVar()
        
    def apply_modern_style(self):
        """Apply the modern style"""
        ModernStyle.apply_modern_style()
        self.root.configure(bg=ModernStyle.COLORS['bg_secondary'])
        
    def create_interface(self):
        """Creates the user interface"""
        # Main container with padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header
        self.create_header(main_container)
        
        # File selection section
        self.create_file_selection(main_container)
        
        # Results area
        self.create_results_area(main_container)
        
        # Export buttons area
        self.create_export_buttons(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Creates the application header"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        header_frame.columnconfigure(0, weight=1)
        
        # Main title
        title_label = ttk.Label(
            header_frame,
            text="📚 Article and Book Analyzer",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0)
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Professional analysis of academic lists in CSV format",
            style='Modern.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
    def create_file_selection(self, parent):
        """Creates the file selection section"""
        file_frame = ttk.LabelFrame(
            parent,
            text="📁 Select CSV File",
            style='Modern.TLabelframe',
            padding=15
        )
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        # Label
        ttk.Label(
            file_frame,
            text="File:",
            style='Modern.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Entry for file path
        self.file_entry = ttk.Entry(
            file_frame,
            textvariable=self.file_path,
            style='Modern.TEntry'
        )
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Search button
        browse_btn = ttk.Button(
            file_frame,
            text="📂 Search",
            command=self.browse_file,
            style='Modern.TButton'
        )
        browse_btn.grid(row=0, column=2)
        
        # Analyze button
        analyze_btn = ttk.Button(
            file_frame,
            text="🔍 Analyze File",
            command=self.analyze_file,
            style='Primary.TButton'
        )
        analyze_btn.grid(row=1, column=0, columnspan=3, pady=(15, 0))
        
    def create_results_area(self, parent):
        """Creates the results area"""
        results_frame = ttk.LabelFrame(
            parent,
            text="📊 Analysis Results",
            style='Modern.TLabelframe',
            padding=15
        )
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
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
        """Creates the export buttons"""
        export_frame = ttk.Frame(parent)
        export_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        export_frame.columnconfigure((0, 1), weight=1)
        
        # Export all button
        self.export_all_btn = ttk.Button(
            export_frame,
            text="📋 Export Complete List",
            command=self.export_all_titles,
            state=tk.DISABLED,
            style='Modern.TButton'
        )
        self.export_all_btn.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        # Export Duplicates Button
        self.export_duplicates_btn = ttk.Button(
            export_frame,
            text="🔍 Export Duplicates",
            command=self.export_duplicates,
            state=tk.DISABLED,
            style='Modern.TButton'
        )
        self.export_duplicates_btn.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
    def create_status_bar(self, parent):
        """Creates the status bar"""
        self.status_var = tk.StringVar(value="Ready for analysis")
        status_label = ttk.Label(
            parent,
            textvariable=self.status_var,
            style='Modern.TLabel',
            relief=tk.SUNKEN,
            padding=(10, 5)
        )
        status_label.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
    def update_status(self, message):
        """Updates the status message"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def browse_file(self):
        """Opens dialog for file selection"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[
                ("Arquivos CSV", "*.csv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if file_path:
            self.file_path.set(file_path)
            self.update_status(f"Arquivo selecionado: {Path(file_path).name}")
    
    def is_valid_academic_content(self, df):
        """Checks if the CSV contains valid academic content"""
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
            
        # Checks for valid data
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['title', 'titulo', 'título', 'nome', 'name']):
                sample_data = df[col].dropna().head(10)
                if len(sample_data) > 0:
                    avg_length = sample_data.str.len().mean()
                    if avg_length > 10:
                        return True
        
        return False
    
    def find_title_and_author_columns(self, df):
        """Identifies title and author columns"""
        title_col = None
        author_col = None
        
        # Search for title column
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in ['title', 'titulo', 'título', 'nome', 'name']):
                title_col = col
                break
        
        # Search for author column
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in ['author', 'autor', 'autores', 'authors']):
                author_col = col
                break
        
        return title_col, author_col
    
    def analyze_file(self):
        """Parses the selected CSV file"""
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a CSV file.")
            return
        
        file_path = self.file_path.get()
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found.")
            return
        
        self.update_status("Analyzing file...")
        
        try:
            # Reads the CSV file
            self.df = pd.read_csv(file_path, encoding='utf-8')
            
        except UnicodeDecodeError:
            try:
                # Try with different encoding
                self.df = pd.read_csv(file_path, encoding='latin1')
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {str(e)}")
            return
        
        # Validates content
        if not self.is_valid_academic_content(self.df):
            messagebox.showerror(
                "Invalid File", 
                "The file does not appear to contain a valid list of academic articles or books.\n\n"
                "Check if the file has columns like 'title', 'autor', etc."
            )
            return
        
        # Identifies columns
        title_col, author_col = self.find_title_and_author_columns(self.df)
        
        if not title_col:
            messagebox.showerror("Error", "Unable to identify a heading column.")
            return
        
        # Processes data
        self.process_data(title_col, author_col)
        
        # Enables export buttons
        self.export_all_btn.config(state=tk.NORMAL)
        self.export_duplicates_btn.config(state=tk.NORMAL)
        
        self.update_status("Analysis completed successfully!")
        
    def process_data(self, title_col, author_col):
        """Processes CSV data"""
        # Remove empty lines
        self.df = self.df.dropna(subset=[title_col])
        
        total_count = len(self.df)
        
        # Prepare a complete list
        self.all_titles = []
        for _, row in self.df.iterrows():
            title = str(row[title_col]).strip()
            if author_col and pd.notna(row[author_col]):
                author = str(row[author_col]).strip()
                self.all_titles.append(f"{title} — {author}")
            else:
                self.all_titles.append(title)
        
        # Identifies duplicates
        if author_col:
            # Combine title and author for duplicate detection
            self.df['combined'] = (
                self.df[title_col].astype(str).str.strip() + " | " + 
                self.df[author_col].astype(str).str.strip()
            )
            duplicated_mask = self.df.duplicated(subset=['combined'], keep=False)
            duplicates_df = self.df[duplicated_mask]
            
            self.duplicates = []
            for _, row in duplicates_df.iterrows():
                title = str(row[title_col]).strip()
                author = str(row[author_col]).strip() if pd.notna(row[author_col]) else "Author not informed"
                self.duplicates.append(f"{title} — {author}")
        else:
            duplicated_mask = self.df.duplicated(subset=[title_col], keep=False)
            duplicates_df = self.df[duplicated_mask]
            self.duplicates = [str(title).strip() for title in duplicates_df[title_col]]
        
        # Displays results
        self.display_results(total_count, len(self.duplicates), title_col, author_col)
    
    def display_results(self, total_count, duplicate_count, title_col, author_col):
        """Displays the analysis results"""
        self.results_text.delete(1.0, tk.END)
        
        # Stylized header
        result_text = "═" * 70 + "\n"
        result_text += "📊 COMPLETE ANALYSIS OF ARTICLES AND BOOKS\n"
        result_text += "═" * 70 + "\n\n"
        
        # Executive summary
        result_text += "📋 EXECUTIVE SUMMARY\n"
        result_text += "─" * 40 + "\n"
        result_text += f"• Total records analyzed: {total_count:,}\n"
        result_text += f"• Unique records: {total_count - duplicate_count:,}\n"
        result_text += f"• Duplicates found: {duplicate_count:,}\n"
        
        if duplicate_count > 0:
            percentage = (duplicate_count / total_count) * 100
            result_text += f"• Doubling rate: {percentage:.1f}%\n"
        
        result_text += f"• Title column: '{title_col}'\n"
        if author_col:
            result_text += f"• Authors column: '{author_col}'\n"
        
        result_text += "\n" + "═" * 70 + "\n\n"
        
        # Complete list
        result_text += "📚 COMPLETE LIST OF TITLES\n"
        result_text += "─" * 40 + "\n"
        
        for i, title in enumerate(self.all_titles, 1):
            result_text += f"{i:4d}. {title}\n"
        
        result_text += f"\n✅ Total listed: {len(self.all_titles):,} records\n\n"
        
        # Duplicados (se houver)
        if duplicate_count > 0:
            result_text += "🔍 DUPLICATE RECORDS IDENTIFIED\n"
            result_text += "─" * 40 + "\n"
            
            for i, duplicate in enumerate(self.duplicates, 1):
                result_text += f"{i:4d}. {duplicate}\n"
            
            result_text += f"\n⚠️  Total duplicates: {len(self.duplicates):,} records\n"
            result_text += "\n💡 RECOMMENDATION: Review duplicates before proceeding\n"
        else:
            result_text += "✅ NO DUPLICATE FOUND\n"
            result_text += "─" * 40 + "\n"
            result_text += "Congratulations! Your list contains no duplicate records..\n"
        
        result_text += "\n" + "═" * 70 + "\n"
        result_text += "📤 Use the buttons below to export the results\n"
        
        self.results_text.insert(1.0, result_text)
    
    def export_all_titles(self):
        """Export all titles to CSV"""
        if not self.all_titles:
            messagebox.showwarning("Warning!", "There is no data to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save full list",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if file_path:
            try:
                export_data = []
                for i, title in enumerate(self.all_titles, 1):
                    export_data.append({"Number": i, "Full Title": title})
                
                # Add summary
                export_data.append({"Number": "", "Full Title": ""})
                export_data.append({"Number": "SUMMARY:", "Full Title": f"Total of {len(self.all_titles)} records"})
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo(
                    "Export Completed", 
                    f"Complete list exported successfully!\n\n"
                    f"File: {Path(file_path).name}\n"
                    f"Total records: {len(self.all_titles)}"
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting file: {str(e)}")
    
    def export_duplicates(self):
        """Export only duplicates to CSV"""
        if not self.duplicates:
            messagebox.showinfo("Information", "There are no duplicate records to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save duplicate list",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if file_path:
            try:
                export_data = []
                for i, duplicate in enumerate(self.duplicates, 1):
                    export_data.append({"Number": i, "Duplicate Registration": duplicate})
                
                # Add summary
                export_data.append({"Number": "", "Duplicate Registration": ""})
                export_data.append({"Number": "SUMMARY:", "Duplicate Registration": f"Total of {len(self.duplicates)} duplicates"})
                
                df_export = pd.DataFrame(export_data)
                df_export.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo(
                    "Export Completed", 
                    f"Duplicate list exported successfully!\n\n"
                    f"File: {Path(file_path).name}\n"
                    f"Total duplicates: {len(self.duplicates)}"
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting file: {str(e)}")


def main():
    """Main function of the application"""
    try:
        root = tk.Tk()
        app = ArticleAnalyzer(root)
        root.mainloop()
    except Exception as e:
        # Error log for debugging
        import traceback
        with open('error_log.txt', 'w') as f:
            f.write(f"Application error: {e}\n")
            f.write(traceback.format_exc())
        
        # Show error to user
        try:
            messagebox.showerror("Fatal Error", f"Unexpected error: {e}")
        except:
            print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()