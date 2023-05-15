import tkinter as tk
from tkinter import ttk
from commands import *
from tkinter import PhotoImage
button_created = False
button_created2 = False
options=opcoes()
cor = {"azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}

root = tk.Tk()
root.geometry("800x600")
root.config(bg=cor["branco"])
root.state('zoomed')
root.title("Requisições")
root.iconbitmap(default='')
img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
img_coliseu = img_coliseu.subsample(2, 2)

frameTop = tk.Frame(root,height=100,bg=cor["azul"],padx=10)
frameTop.pack(side="top", fill="x")
frameTop.columnconfigure(0, weight=1)
frameTop.columnconfigure(1, weight=4)
frameTop.columnconfigure(2, weight=1)
frameTop.rowconfigure(0, weight=1)

labelLogo = ttk.Label(frameTop, image=img_coliseu,background=cor["azul"])
labelLogo.grid(row=0,column=2)

lb_req = ttk.Label(frameTop, text="Requisições",background=cor["azul"],foreground=cor["branco"]
                   ,font=("Arial", 24,"bold"))
lb_req.grid(row=0,column=0)



frameCom2Tv = tk.Frame(root,bg=cor["vermelho"])
frameCom2Tv.pack(fill="both", expand=True, padx=10, pady=10)
frameCom2Tv.rowconfigure(0, weight=4)
frameCom2Tv.rowconfigure(1, weight=2)
frameCom2Tv.rowconfigure(2, weight=1)
frameCom2Tv.columnconfigure(0, weight=1)

frameTvTop = tk.Frame(frameCom2Tv,bg=cor["cinza"])
frameTvTop.grid(row=0, column=0, sticky='nsew', rowspan=2)

frameTvBot = tk.Frame(frameCom2Tv,bg=cor["azul"])
frameTvBot.grid(row=2, column=0, sticky='nsew')




treeview = ttk.Treeview(frameTvTop, columns=("Message Id","Size", "Data","Hora","Status"), show='headings')

treeview.column("Message Id", anchor="center")
treeview.column("Size", anchor="center")
treeview.column("Data", anchor="center")
treeview.column("Hora", anchor="center")
treeview.column("Status", anchor="center")

treeview.heading("Message Id", text="Message Id")
treeview.heading("Size", text="Size")
treeview.heading("Data", text="Data")
treeview.heading("Hora", text="Hora")
treeview.heading("Status", text="Status")



for X in range (0,len(options['Data'])):
    treeview.insert("", tk.END,values=(options['MessageID'][X],options['Size'][X],options['Data'][X],options['Hora'][X],"Confirmado"))


treeviewVizu = ttk.Treeview(frameTvBot, columns=("codCliente","cliente","produto","referencia","quantidade"), show='headings')
treeviewVizu.column("codCliente", anchor="center")
treeviewVizu.column("cliente", anchor="center")
treeviewVizu.column("produto", anchor="center")
treeviewVizu.column("referencia", anchor="center")
treeviewVizu.column("quantidade", anchor="center")
treeviewVizu.heading("codCliente", text="Cód.Cliente")
treeviewVizu.heading("cliente", text="Cliente")
treeviewVizu.heading("produto", text="Produto")
treeviewVizu.heading("referencia", text="Ref.")
treeviewVizu.heading("quantidade", text="Uni.")

btEnvia = tk.Button(frameTvTop,text='Importar')

def item_clicked(event):
    global button_created2,btVizu,btEnvia
    if button_created:
        btEnvia.destroy()
    if button_created2:
        btVizu.destroy()
        btVizu = tk.Button(frameTvTop,command=visualiza,text='Carregar Visualização')
        btVizu.pack(fill='x',padx=10,pady=10)
    else:
        btVizu = tk.Button(frameTvTop,command=visualiza,text='Carregar Visualização')
        btVizu.pack(fill='x',padx=10,pady=10)
        button_created2 = True


def visualiza():
    global button_created,btEnvia,btVizu
    btVizu.destroy()
    treeviewVizu.delete(*treeviewVizu.get_children())
    item = treeview.selection()[0]
    value = treeview.item(item, "values")[0]
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={value}")
    pedidos = trataPedescoTxt(linkView)
    for i in range (0,len(pedidos['codigoClienteCol'])):
        treeviewVizu.insert("", tk.END,values=(pedidos['codigoClienteCol'][i],pedidos['clienteCol'][i],pedidos['produtoCol'][i],pedidos['produtoRefCol'][i],pedidos['quantidadeCol'][i]))
    def enviar():
        for value in pedidos['procedures']:
            execute(value)
     
    if button_created:
        btEnvia.destroy()
        btEnvia = tk.Button(frameTvTop,command=enviar,text='Importar')
        btEnvia.pack(fill='x',padx=10,pady=10)
    else:
        btEnvia = tk.Button(frameTvTop,command=enviar,text='Importar')
        btEnvia.pack(fill='x',padx=10,pady=10)
        button_created = True
    

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


