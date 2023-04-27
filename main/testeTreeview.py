import tkinter as tk
from tkinter import ttk

# Cria uma janela
root = tk.Tk()

# Define o tamanho da janela
root.geometry("500x500")

# Cria uma Treeview
tree = ttk.Treeview(root)

# Define as colunas da Treeview
tree["columns"] = ("Nome", "Idade")

# Define o nome das colunas
tree.heading("#0", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Idade", text="Idade")

# Adiciona alguns dados
for i in range(10):
    tree.insert("", tk.END,values=(str(i),"Pessoa " + str(i), str(i*10)))

# Cria um scrollbar vertical
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)

# Define o scrollbar na Treeview
tree.configure(yscrollcommand=scrollbar.set)

# Posiciona a Treeview no centro da tela
tree.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Posiciona o scrollbar ao lado direito da Treeview
scrollbar.place(relx=0.99, rely=0.5, anchor=tk.E)

# Inicia a janela
root.mainloop()