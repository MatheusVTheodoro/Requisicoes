import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from commands import * 

root = tk.Tk()
options = opcoes()
listbox = tk.Listbox(root)
for option in options:
    listbox.insert(tk.END, option)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

def confirmaPedido():
    for widget in root.winfo_children():
        if widget.winfo_class() == 'Label':
            widget.destroy()
    selection = listbox.get(listbox.curselection())
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={selection}")
    label_text = trataPedescoTxt(linkView)
    for values in label_text:
        label = tk.Label(root, text=values, fg="black")
        label.pack()

btConfirm = tk.Button(root, text="Executar comando", command=confirmaPedido)
btConfirm.pack(side=tk.BOTTOM)

root.mainloop()
