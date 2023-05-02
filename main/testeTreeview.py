import tkinter as tk
from tkinter import ttk

# Cria a janela principal do tkinter
root = tk.Tk()
root.title("TreeView Exemplo")

# Cria a Treeview
treeview = ttk.Treeview(root)
treeview.pack(side="left", fill="both", expand=True)

# Adiciona algumas colunas
treeview["columns"] = ("nome", "idade")
treeview.column("#0", width=100, minwidth=100, stretch=tk.NO)
treeview.column("nome", width=100, minwidth=100, stretch=tk.NO)
treeview.column("idade", width=100, minwidth=100, stretch=tk.NO)

# Define os cabeçalhos das colunas
treeview.heading("#0", text="ID", anchor=tk.W)
treeview.heading("nome", text="Nome", anchor=tk.W)
treeview.heading("idade", text="Idade", anchor=tk.W)

# Adiciona alguns itens à Treeview
treeview.insert("", "end", text="001", values=("João", "30"))
treeview.insert("", "end", text="002", values=("Maria", "25"))
treeview.insert("", "end", text="003", values=("Pedro", "40"))

# Cria um Label para exibir o valor selecionado
label = tk.Label(root, text="")
label.pack()

# Define a função de clique da Treeview
def item_clicked(event):
    item = treeview.selection()[0]
    value = treeview.item(item, "values")[0]
    label.config(text=value)

# Associa a função de clique à Treeview
treeview.bind("<ButtonRelease-1>", item_clicked)

# Inicia o loop principal do tkinter
root.mainloop()