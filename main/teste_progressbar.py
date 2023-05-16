from tkinter import ttk
from tkinter import *

root = ttk.Tk()
# criar a Treeview
tree = ttk.Treeview(root)
tree.pack()

# adicionar uma coluna
tree["columns"] = ("col1", "col2")

# adicionar alguns dados
tree.insert("", "end", text="linha 1", values=("valor 1", "valor 2"))
tree.insert("", "end", text="linha 2", values=("valor 3", "valor 4"))

# definir uma tag com a cor desejada
tree.tag_configure("cor_desejada", background="red")

# aplicar a tag à célula específica
tree.item("linha 1", tags=("cor_desejada",))
root.mainloop()