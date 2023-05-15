import tkinter as tk
from tkinter import ttk

def insert_values():
    values = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']  # Lista de valores a serem inseridos
    total_values = len(values)  # Total de valores na lista

    progress_bar['maximum'] = total_values  # Define o valor máximo da ProgressBar

    for index, value in enumerate(values):
        tree.insert('', 'end', text=value)  # Insere o valor no TreeView
        progress_bar['value'] = index + 1  # Atualiza o valor da ProgressBar
        root.update()  # Atualiza a janela
        root.after(500)  # Pausa de 500 milissegundos (0,5 segundos)

# Cria a janela principal
root = tk.Tk()
root.title("Exemplo de ProgressBar com TreeView e Scrollbar")

# Cria um frame para conter a TreeView
frame_tv = ttk.Frame(root)
frame_tv.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Cria uma TreeView
tree = ttk.Treeview(frame_tv)
tree.pack(side='left', fill='both', expand=True)

# Cria uma Scrollbar vertical
scrollY = ttk.Scrollbar(frame_tv, orient="vertical", command=tree.yview)
scrollY.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollY.set)

# Cria uma barra de progresso
progress_bar = ttk.Progressbar(root, mode='determinate')
progress_bar.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

# Cria um botão para iniciar a inserção dos valores
insert_button = tk.Button(root, text="Inserir Valores", command=insert_values)
insert_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

# Configura o redimensionamento responsivo dos widgets
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Executa o loop principal da janela
root.mainloop()
