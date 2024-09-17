import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
from datetime import datetime

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda")

        # centralizar janela principal
        self.center_window(500, 300)
        
        # lista de tarefas
        self.tasks = []
        self.load_tasks()

        # elementos GUI
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # evento de duplo clique para abrir os detalhes da tarefa
        self.task_listbox.bind("<Double-Button-1>", self.show_task_details)

        self.add_button = tk.Button(root, text="Adicionar tarefa", command=self.open_add_task_window)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Deletar tarefa", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Salvar", command=self.save_tasks)
        self.save_button.pack(pady=5)

        self.update_task_list()
        self.delete_due_tasks()  # deleta tarefas automaticamente

    def center_window(self, width, height):
        # centraliza a janela com a largura e altura especificadas.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def open_add_task_window(self):
        # cria uma nova janela toplevel (popup)
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Adicionar nova tarefa")
        
        # Centralizar a janela de popup
        self.center_toplevel_window(add_task_window, 400, 200)

        # titulo da tarefa
        tk.Label(add_task_window, text="Tarefa:").grid(row=0, column=0, padx=10, pady=10)
        task_title_entry = tk.Entry(add_task_window, width=40)
        task_title_entry.grid(row=0, column=1, padx=10, pady=10)

        # descrição da tarefa
        tk.Label(add_task_window, text="Descrição:").grid(row=1, column=0, padx=10, pady=10)
        task_desc_entry = tk.Entry(add_task_window, width=40)
        task_desc_entry.grid(row=1, column=1, padx=10, pady=10)

        # data
        tk.Label(add_task_window, text="Data (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        task_due_date_entry = tk.Entry(add_task_window, width=40)
        task_due_date_entry.grid(row=2, column=1, padx=10, pady=10)

        # botão de adicionar 
        def save_task():
            # getters das informações
            title = task_title_entry.get()
            description = task_desc_entry.get()
            due_date = task_due_date_entry.get()

            # check campos vazios
            if not title or not description or not due_date:
                messagebox.showerror("Erro", "Todos os campos são necessários.")
                return
            
            # validar formato da data
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Data Inválida!", "Favor informar a data no seguinte formato: YYYY-MM-DD.")
                return
            
            # adicionar tarefa a lista
            task = {'title': title, 'description': description, 'due_date': due_date}
            self.tasks.append(task)
            self.update_task_list()
            
            # fechar o popup
            add_task_window.destroy()

        tk.Button(add_task_window, text="Adicionar tarefa", command=save_task).grid(row=3, column=1, pady=10)

    def center_toplevel_window(self, window, width, height):
        # centraliza janela Toplevel com a largura e altura especificadas
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f'{width}x{height}+{x}+{y}')

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks.pop(selected_index)
            messagebox.showinfo("Tarefa deletada", f"Tarefa '{task['title']}' deletada.")
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Erro", "Favor selecione uma tarefa para ser deletada.")

    def show_task_details(self, event):
        # abre uma janela popup com os detalhes da tarefa selecionada.
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_index]
            
            # criar janela popup para mostrar os detalhes
            details_window = tk.Toplevel(self.root)
            details_window.title("Detalhes da Tarefa")
            
            # centralizar janela popup
            self.center_toplevel_window(details_window, 400, 200)

            # exibir detalhes da tarefa
            tk.Label(details_window, text=f"{task['title']}").pack(pady=10)
            tk.Label(details_window, text=f"{task['description']}").pack(pady=10)
            tk.Label(details_window, text=f"{task['due_date']}").pack(pady=10)

        except IndexError:
            messagebox.showwarning("Erro", "Favor selecione uma tarefa para ver os detalhes.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = f"{task['title']} - Data: {task['due_date']}"
            self.task_listbox.insert(tk.END, display_text)

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)
        messagebox.showinfo("Ok.", "Tarefas foram salvas em tasks.json.")

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def delete_due_tasks(self):
        # deleta tarefas vencidas
        today = datetime.now().date()
        due_tasks = [task for task in self.tasks if datetime.strptime(task['due_date'], '%Y-%m-%d').date() < today]

        for task in due_tasks:
            self.tasks.remove(task)
            messagebox.showinfo("Tarefa expirada", f"Tarefa '{task['title']}' com vencimento {task['due_date']} foi removida.")
        
        self.update_task_list()

# main app
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
