import tkinter as tk
from tkinter import ttk
#import ttkbootstrap as ttk
from commands import *
from PIL import Image, ImageTk
from tkinter import PhotoImage

options=opcoes()
cor = {"azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}





root = tk.Tk()
root.geometry("800x600")
root.config(bg=cor["branco"])
root.state('zoomed')
root.title("Requisições")
root.iconbitmap(default='')
img_coliseu =PhotoImage(file="C:/REPOSITORIOS/COLISEU/ColiseuRequisicoes/main/assets/COLISEUsFundo.png")
img_coliseu = img_coliseu.subsample(2, 2)



frameTop = tk.Frame(root,height=100,bg=cor["azul"],padx=10)
frameTop.pack(side="top", fill="x")
labelLogo = ttk.Label(frameTop, image=img_coliseu,background=cor["azul"])
labelLogo.grid(row=0,column=2)

lb_req = ttk.Label(frameTop, text="Requisições",background=cor["azul"],foreground=cor["branco"]
                   ,font=("Arial", 24,"bold"))
lb_req.grid(row=0,column=0)


frameTop.columnconfigure(0, weight=1)
frameTop.columnconfigure(1, weight=4)
frameTop.columnconfigure(2, weight=1)
frameTop.rowconfigure(0, weight=1)





frameCom2Tv = tk.Frame(root,bg=cor["vermelho"])
frameCom2Tv.pack(fill="both", expand=True, padx=10, pady=10)

frameTvTop = tk.Frame(frameCom2Tv,bg=cor["cinza"])
frameTvTop.grid(row=0, column=0, sticky='nsew', rowspan=2)

frameTvBot = tk.Frame(frameCom2Tv,bg=cor["azul"])
frameTvBot.grid(row=2, column=0, sticky='nsew')

frameCom2Tv.rowconfigure(0, weight=4)
frameCom2Tv.rowconfigure(1, weight=2)
frameCom2Tv.rowconfigure(2, weight=1)
frameCom2Tv.columnconfigure(0, weight=1)

treeview = ttk.Treeview(frameTvTop, columns=("Message Id", "Data","Hora","Status"), show='headings')
treeviewVizu = ttk.Treeview(frameTvBot, columns=("peca","codCliente","nPedido","quantidade","codFornecedor"), show='headings')

treeview.heading("Message Id", text="Message Id")
treeview.heading("Data", text="Data")
treeview.heading("Hora", text="Hora")
treeview.heading("Status", text="Status")

treeviewVizu.heading("peca", text="peca")
treeviewVizu.heading("codCliente", text="codCliente")
treeviewVizu.heading("nPedido", text="nPedido")
treeviewVizu.heading("quantidade", text="quantidade")
treeviewVizu.heading("codFornecedor", text="codFornecedor")

for X in range (0,len(options['Data'])):
    treeview.insert("", tk.END,values=(options['MessageID'][X],options['Data'][X],options['Hora'][X],"Confirmado"))



def item_clicked(event):
    treeviewVizu.delete(*treeviewVizu.get_children())
    item = treeview.selection()[0]
    value = treeview.item(item, "values")[0]
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={value}")
    pedidos = trataPedescoTxt(linkView)
    for i in range (0,len(pedidos['peca'])):
        treeviewVizu.insert("", tk.END,values=(pedidos['procedure'][i],pedidos['codCliente'][i],pedidos['nPedido'][i],pedidos['quantidade'][i],pedidos['codFornecedor'][i]))
    
    

treeview.bind("<ButtonRelease-1>", item_clicked)

scrollY = ttk.Scrollbar(frameTvTop, orient="vertical", command=treeview.yview)
scrollY2 = ttk.Scrollbar(frameTvBot, orient="vertical", command=treeviewVizu.yview)
scrollY.pack(side="right", fill="y")
scrollY2.pack(side="right", fill="y")

treeview.configure(yscrollcommand=scrollY.set)
treeviewVizu.configure(yscrollcommand=scrollY2.set)
treeview.pack(fill="both", expand=True,padx=10,pady=10)
treeviewVizu.pack(fill="both", expand=True,padx=10,pady=10)

root.mainloop()