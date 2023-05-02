import tkinter as tk
from tkinter import ttk
#import ttkbootstrap as ttk
from commands import *
options=opcoes()
cor = {"azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
root = tk.Tk()
root.geometry("800x600")
root.config(bg=cor["branco"])
root.state('zoomed')

frameTop = tk.Frame(root,height=100,bg=cor["azul"],padx=10)
frameTop.pack(side="top", fill="x")
frameTv = tk.Frame(root,bg=cor["azulClaro"])
frameTv.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)
frameBot = tk.Frame(frameTv,height=300,bg=cor["cinza"],padx=10)
frameBot.pack(side="bottom", fill="x")

label = tk.Label(frameBot, text="")
label.pack()


treeview = ttk.Treeview(frameTv, columns=("Message Id", "Data","Hora","Status"), show='headings')

treeview.heading("Message Id", text="Message Id")
treeview.heading("Data", text="Data")
treeview.heading("Hora", text="Hora")
treeview.heading("Status", text="Status")


for X in range (0,len(options['Data'])):
    treeview.insert("", tk.END,values=(options['MessageID'][X],options['Data'][X],options['Hora'][X],"Confirmado"))

print(type(options))

def item_clicked(event):
    item = treeview.selection()[0]
    value = treeview.item(item, "values")[0]
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={value}")
    label_text = trataPedescoTxt(linkView)
    label.config(text=label_text)

treeview.bind("<ButtonRelease-1>", item_clicked)

scrollY = ttk.Scrollbar(frameTv, orient="vertical", command=treeview.yview)
scrollY.pack(side="right", fill="y")

treeview.configure(yscrollcommand=scrollY.set)
treeview.pack(fill="both", expand=True,padx=10,pady=10)

root.mainloop()