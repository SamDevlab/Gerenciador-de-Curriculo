import os
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- CONFIGURAÇÕES ---
DB_FILE = "resume_history.json"
STORAGE_DIR = "resume_backups"
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.md'}

class ResumeManager:
    def __init__(self):
        # Garante que a pasta de storage existe
        self.storage_dir = Path(STORAGE_DIR)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Garante que o arquivo JSON existe
        self.db_file = Path(DB_FILE)
        if not self.db_file.exists():
            self._save_db([])

    def _load_db(self) -> List[Dict]:
        """Carrega o histórico do JSON."""
        try:
            with self.db_file.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_db(self, data: List[Dict]) -> None:
        """Salva o histórico no JSON."""
        with self.db_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _validate_file(self, file_path: str) -> bool:
        """Valida se o arquivo existe e tem extensão permitida."""
        path = Path(file_path)
        if not path.exists():
            print(f"❌ Erro: O arquivo '{file_path}' não foi encontrado.")
            return False
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            print(f"❌ Erro: Extensão '{path.suffix}' não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}")
            return False
        return True

    def add_version(self, file_path: str, tag: str, note: str) -> None:
        """Salva uma nova versão do currículo."""
        if not self._validate_file(file_path):
            return

        history = self._load_db()
        
        # --- CORREÇÃO DE ID ---
        # Pega o maior ID atual, ou 0 se a lista estiver vazia
        last_id = max([item['id'] for item in history], default=0)
        new_id = last_id + 1
        # ----------------------

        # Gerar timestamp e nome único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_path = Path(file_path)
        original_name = original_path.name
        extension = original_path.suffix
        
        # Nome do arquivo no backup: 20260101_120000_Senior_Python.pdf
        safe_tag = tag.replace(" ", "_")
        new_filename = f"{timestamp}_{safe_tag}{extension}"
        destination = self.storage_dir / new_filename

        # Copiar o arquivo
        try:
            shutil.copy2(file_path, destination)
            
            # Criar registro
            record = {
                "id": new_id,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tag": tag,
                "note": note,
                "original_name": original_name,
                "backup_path": str(destination)
            }
            
            history.append(record)
            self._save_db(history)
            
            print(f"✅ Sucesso! Versão salva (ID: {new_id}) como: {new_filename}")
            print(f"📝 Nota: {note}")
            
        except Exception as e:
            print(f"❌ Erro ao copiar arquivo: {e}")

    def list_versions(self) -> None:
        """Lista todas as versões salvas."""
        history = self._load_db()
        
        if not history:
            print("📭 Nenhum histórico encontrado.")
            return

        print(f"\n{'ID':<5} | {'DATA':<18} | {'TAG':<15} | {'NOTA'}")
        print("-" * 75)
        
        # Ordena por ID decrescente (mais recente primeiro) para facilitar visualização
        for item in sorted(history, key=lambda x: x['id'], reverse=True):
            # Trunca a nota se for muito longa
            note = (item['note'][:30] + '..') if len(item['note']) > 30 else item['note']
            print(f"{item['id']:<5} | {item['date']:<18} | {item['tag']:<15} | {note}")
        print("\n")

    def restore_version(self, version_id: int, output_path: Optional[str] = None) -> None:
        """Recupera uma versão antiga."""
        history = self._load_db()
        record = next((item for item in history if item["id"] == version_id), None)

        if not record:
            print(f"❌ ID {version_id} não encontrado.")
            return

        src = Path(record["backup_path"])
        
        if not src.exists():
            print(f"❌ Erro Crítico: O arquivo de backup '{src}' não foi encontrado no disco.")
            return

        # Se o usuário não definiu nome de saída, usa o original + prefixo
        if not output_path:
            output_path = f"RESTORED_{record['original_name']}"

        output = Path(output_path)
        
        # Confirmação se o arquivo já existe na pasta atual
        if output.exists():
            response = input(f"⚠️  O arquivo '{output_path}' já existe aqui. Substituir? (s/n): ").strip().lower()
            if response not in ['s', 'sim', 'y', 'yes']:
                print("❌ Operação cancelada.")
                return

        try:
            shutil.copy2(src, output)
            print(f"✅ Versão {version_id} restaurada com sucesso para: {output_path}")
        except Exception as e:
            print(f"❌ Erro ao restaurar: {e}")

    def delete_version(self, version_id: int) -> None:
        """Remove uma versão do histórico e o arquivo de backup."""
        history = self._load_db()
        record = next((item for item in history if item["id"] == version_id), None)

        if not record:
            print(f"❌ ID {version_id} não encontrado.")
            return

        # Confirmação
        print(f"🗑️  Você vai deletar a versão do dia {record['date']} com tag '{record['tag']}'.")
        response = input(f"⚠️  Tem certeza? (s/n): ").strip().lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("❌ Operação cancelada.")
            return

        try:
            # Remove o arquivo de backup
            backup_path = Path(record["backup_path"])
            if backup_path.exists():
                backup_path.unlink()
                print("Arquivo físico deletado.")
            else:
                print("Aviso: Arquivo físico não encontrado, removendo apenas do registro.")
            
            # Remove do histórico
            history = [item for item in history if item["id"] != version_id]
            self._save_db(history)
            
            print(f"✅ Versão {version_id} removida do banco de dados.")
        except Exception as e:
            print(f"❌ Erro ao deletar: {e}")

class ResumeGUI:
    def __init__(self, manager):
        self.manager = manager
        # Inicialização padrão do Tkinter sem DragAndDrop
        self.root = tk.Tk()
        self.root.title("Gerenciador de Versões de Currículo")
        self.root.geometry("500x400")
        
        # Variáveis
        self.file_path = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_label = ttk.Label(self.root, text="📄 Gerenciador de Versões de Currículo", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Área de seleção
        frame = ttk.Frame(self.root, relief="groove", borderwidth=2)
        frame.pack(pady=10, padx=20, fill="x")
        
        # Texto atualizado
        select_text = "Clique aqui para selecionar seu currículo"
        select_label = ttk.Label(frame, text=select_text, background="#f0f0f0", padding=20)
        select_label.pack(fill="x")
        # Bind apenas para clique
        select_label.bind("<Button-1>", self.select_file)
        
        # Campo para mostrar arquivo selecionado
        file_entry = ttk.Entry(self.root, textvariable=self.file_path, state="readonly")
        file_entry.pack(pady=5, padx=20, fill="x")
        
        # Campo Tag
        ttk.Label(self.root, text="Tag:").pack(anchor="w", padx=20)
        self.tag_entry = ttk.Entry(self.root)
        self.tag_entry.pack(pady=5, padx=20, fill="x")
        self.tag_entry.insert(0, "Ex: Senior, Google, Estagio")
        
        # Campo Nota
        ttk.Label(self.root, text="Nota (opcional):").pack(anchor="w", padx=20)
        self.note_entry = ttk.Entry(self.root)
        self.note_entry.pack(pady=5, padx=20, fill="x")
        
        # Botão Adicionar
        add_button = ttk.Button(self.root, text="➕ Adicionar Versão", command=self.add_version)
        add_button.pack(pady=20)
        
        # Botão Listar
        list_button = ttk.Button(self.root, text="📋 Listar Histórico", command=self.list_versions)
        list_button.pack(pady=5)
    
    def select_file(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Selecione seu currículo",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
    
    def add_version(self):
        file_path = self.file_path.get()
        tag = self.tag_entry.get().strip()
        note = self.note_entry.get().strip()
        
        if not file_path:
            messagebox.showerror("Erro", "Selecione um arquivo primeiro!")
            return
        
        if not tag or tag == "Ex: Senior, Google, Estagio":
            messagebox.showerror("Erro", "Digite uma tag válida!")
            return
        
        try:
            self.manager.add_version(file_path, tag, note)
            messagebox.showinfo("Sucesso", "Versão adicionada com sucesso!")
            # Limpar campos
            self.file_path.set("")
            self.tag_entry.delete(0, tk.END)
            self.note_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar versão: {e}")
    
    def list_versions(self):
        # Criar nova janela para mostrar o histórico
        list_window = tk.Toplevel(self.root)
        list_window.title("Histórico de Versões")
        list_window.geometry("600x400")
        
        text = tk.Text(list_window, wrap="word")
        text.pack(fill="both", expand=True)
        
        # Capturar output do list_versions
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        self.manager.list_versions()
        
        sys.stdout = old_stdout
        text.insert("1.0", buffer.getvalue())
        text.config(state="disabled")
    
    def run(self):
        self.root.mainloop()

# --- LÓGICA DO CLI ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerenciador de Versões de Currículo")
    
    # IMPORTANTE: required=False permite rodar sem argumentos
    subparsers = parser.add_subparsers(dest="command", required=False)

    # Comando: add
    cmd_add = subparsers.add_parser("add", help="Adicionar nova versão")
    cmd_add.add_argument("file", help="Caminho do arquivo do currículo")
    cmd_add.add_argument("-t", "--tag", required=True, help="Tag (Ex: Google, Senior)")
    cmd_add.add_argument("-n", "--note", default="", help="Nota opcional")

    # Comando: list
    cmd_list = subparsers.add_parser("list", help="Listar histórico")

    # Comando: restore
    cmd_restore = subparsers.add_parser("restore", help="Recuperar versão")
    cmd_restore.add_argument("id", type=int, help="ID da versão")
    cmd_restore.add_argument("-o", "--output", help="Nome do arquivo de saída")

    # Comando: delete
    cmd_delete = subparsers.add_parser("delete", help="Deletar versão")
    cmd_delete.add_argument("id", type=int, help="ID da versão")

    # Comando: gui
    cmd_gui = subparsers.add_parser("gui", help="Abrir interface gráfica")

    args = parser.parse_args()
    manager = ResumeManager()

    # SE NENHUM COMANDO FOR PASSADO (ou for explicitamente 'gui'), ABRE A JANELA
    if args.command is None or args.command == "gui":
        print("🖥️  Iniciando interface gráfica...")
        gui = ResumeGUI(manager)
        gui.run()
    
    # Outros comandos do terminal
    elif args.command == "add":
        manager.add_version(args.file, args.tag, args.note)
    elif args.command == "list":
        manager.list_versions()
    elif args.command == "restore":
        manager.restore_version(args.id, args.output)
    elif args.command == "delete":
        manager.delete_version(args.id)