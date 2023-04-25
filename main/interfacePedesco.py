import tkinter as tk
from commands import *

root = tk.Tk()
options = opcoes()
listbox = tk.Listbox(root)
for option in options:
    listbox.insert(tk.END, option)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Adicione uma barra de rolagem para o widget Listbox
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Adicione um comando para exibir a opção selecionada
def ConfirmPedesco():
    selection = listbox.get(listbox.curselection())
    link=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={selection}")
    trataPedescoTxt(link)
button = tk.Button(root, text="Executar comando", command=ConfirmPedesco)
button.pack(side=tk.BOTTOM)

root.mainloop()