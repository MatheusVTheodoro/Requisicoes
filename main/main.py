import tkinter as tk
from tkinter import ttk
from commands import *
from tkinter import PhotoImage

button_created = False
button_created2 = False
pbVizu_created = False

def trataPedescoTxt(link):
    global tvVizu,root,pbVizu
    procedures=[]
    texto = htmlResponseText(link)
    texto = re.findall("98.............................................................",texto)
    maximum=len(texto) 
    pbVizu['maximum'] = maximum
    for index,value in enumerate(texto):
        tam = 8
        peca = value[0:0+tam]
        codCliente = value[tam:tam+6]
        tam=tam+6
        nPedido = value[tam:tam+6]
        tam=tam+6
        quantidade = value[tam:tam+5]
        tam=tam+5
        datavalue = value[tam:tam+8]
        tam=tam+8
        codFornecedor = value[tam:tam+9]
        tam=tam+9
        tipoDSODSC = value[tam:tam+1]
        tam = tam+1
        NPedidoGMSAP = value[tam:tam+9]
        tam=tam+9
        hora = value[tam:tam+6]
        tam=tam+6
        linhaDoPedido = value[tam:tam+5]
        quantidade=int(quantidade)

        cliente=select((f"select NOME_FANTASIA from clientes where clientes.DOC_EX = '{codCliente}'"))
        produto=select((f"select descricao from produtos where produtos.codigo_fab = '{peca}'"))
        
        if(produto==[]):
            produto='Produto não vinculado'
        else:
            produto=produto[0]
            produto=str(produto)
            produto = produto[2:-3]
        
        
        if(cliente==[]):
            cliente='Codigo de cliente não vinculado'

        else:
            cliente=cliente[0]
            cliente=str(cliente)
            cliente = cliente[2:-3]

        
        procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{nPedido}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
        procedures.append(procedure)
        tvVizu.insert("", tk.END,values=(codCliente,cliente,produto,peca,quantidade))
        pbVizu['value'] = index+1
        root.update()
        
    return {'procedures':procedures}

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

# Configura o gerenciador de layout grid para ajustar os widgets de forma responsiva
frameTvTop.grid_rowconfigure(0, weight=1)
frameTvTop.grid_columnconfigure(0, weight=1)

frameTvBot = tk.Frame(frameCom2Tv,bg=cor["azul"])
frameTvBot.grid(row=2, column=0, sticky='nsew')

frame_tv = ttk.Frame(frameTvTop)
frame_tv.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


treeview = ttk.Treeview(frame_tv, columns=("Message Id","Size", "Data","Hora","Status"), show='headings')

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


tvVizu = ttk.Treeview(frameTvBot, columns=("codCliente","cliente","produto","referencia","quantidade"), show='headings')
tvVizu.column("codCliente", anchor="center")
tvVizu.column("cliente", anchor="center")
tvVizu.column("produto", anchor="center")
tvVizu.column("referencia", anchor="center")
tvVizu.column("quantidade", anchor="center")
tvVizu.heading("codCliente", text="Cód.Cliente")
tvVizu.heading("cliente", text="Cliente")
tvVizu.heading("produto", text="Produto")
tvVizu.heading("referencia", text="Ref.")
tvVizu.heading("quantidade", text="Uni.")

btEnvia = tk.Button(frameTvTop,text='Importar')



def item_clicked(event):
    global button_created2,btVizu,btEnvia
    
    if button_created:
        btEnvia.destroy()
    if button_created2:
        btVizu.destroy()
        btVizu = tk.Button(frameTvTop,command=visualiza,text='Carregar Visualização')
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    else:
        btVizu = tk.Button(frameTvTop,command=visualiza,text='Carregar Visualização')
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        button_created2 = True
   
def visualiza():
    global button_created,btEnvia,btVizu
    btVizu.destroy()

    

    tvVizu.delete(*tvVizu.get_children())
    item = treeview.selection()[0]
    value = treeview.item(item, "values")[0]
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={value}")
    pedidos = trataPedescoTxt(linkView)

    def enviar():
        for value in pedidos['procedures']:
            execute(value)
     
    if button_created:
        btEnvia.destroy()
        btEnvia = tk.Button(frameTvTop,command=enviar,text='Importar')
        btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    else:
        btEnvia = tk.Button(frameTvTop,command=enviar,text='Importar')
        btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        button_created = True
    

treeview.bind("<ButtonRelease-1>", item_clicked)


scrollY = ttk.Scrollbar(frame_tv, orient="vertical", command=treeview.yview)
scrollY.pack(side="right", fill="y")


scrollY2 = ttk.Scrollbar(frameTvBot, orient="vertical", command=tvVizu.yview)
scrollY2.pack(side="right", fill="y")


treeview.configure(yscrollcommand=scrollY.set)
tvVizu.configure(yscrollcommand=scrollY2.set)
treeview.pack(fill="both", expand=True)
tvVizu.pack(fill="both", expand=True,padx=10,pady=10)

pbVizu = ttk.Progressbar(frameTvTop, mode='determinate')
pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')



root.mainloop()


