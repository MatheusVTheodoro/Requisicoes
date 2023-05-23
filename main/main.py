import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
    banco= arquivo.read()
    
def select(con,query):
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchall()
    cur.close()
    return resultado

def execute(con,query):
    cur = con.cursor()
    cur.execute(query)
    cur.close()
    
def htmlResponseText(link):
    user='CampFacil'
    senha='dsffjyxtf4x'
    response = req.get(link, auth=(user,senha))
    return(response.text)

def opcoes():
    html=htmlResponseText("https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get")
    MessageId=[]
    Data=[]
    Hora=[]
    Size=[]
    
    X = re.findall("&nbsp;[0-9]+&nbsp",html)
    for v in X:
        message = re.sub("&nbsp;","",v)
        Size.append(re.sub("&nbsp","",message))

    X = re.findall("<td><tt>&nbsp;........&nbsp;",html)
    for v in X:
        message = re.sub("<td><tt>&nbsp;","",v)
        MessageId.append(re.sub("&nbsp;","",message))
    
    X = re.findall("<nobr>&nbsp;........",html)
    for v in X:
        dia = re.sub("<nobr>&nbsp;","",v)
        Data.append(dia)
    
    X = re.findall("&nbsp;.....:..",html)
    for v in X:
        hora = re.sub("&nbsp;","",v)
        Hora.append(hora)

    return {'MessageID':MessageId,'Data':Data,'Hora':Hora, 'Size' :Size}

def trataPedescoTxt(link):
    global tabela_vizu,root,pbVizu,banco,messageId_clicked,importavel
    importavel = True
    procedures=[]
    texto = htmlResponseText(link)
    texto = re.findall("98.............................................................",texto)
    maximum=len(texto) 
    pbVizu['maximum'] = maximum
    con = firebirdsql.connect(
    host='localhost',
    database=banco,
    user='SYSDBA',
    password='masterkey',
    port=3050,
    charset='WIN1252')

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

        query=(f"select NOME_FANTASIA from clientes where clientes.DOC_EX = '{codCliente}'")
        cliente=select(con,query)
        query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
        produto=select(con,query)
        
        if(produto==[]):
            produto='Produto não vinculado'
            importavel = False
        else:
            produto=produto[0]
            produto=str(produto)
            produto = produto[2:-3]

        if(cliente==[]):
            cliente='Codigo de cliente não vinculado'
            importavel = False
        else:
            cliente=cliente[0]
            cliente=str(cliente)
            cliente = cliente[2:-3]

        procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{messageId_clicked}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
        procedures.append(procedure)
        if index % 2 == 0 :
            fundo = "branco"
        else:
            fundo = "verde"
        
        tabela_vizu.insert("", tk.END,values=(codCliente,cliente,produto,peca,quantidade),tags=(fundo))
        tabela_vizu.tag_configure("branco", background=cor["branco"])
        pbVizu['value'] = index+1
        root.update()
    con.close()
    pbVizu.destroy()    
    return {'procedures':procedures}

def item_clicked(event):
    global button_created2,btVizu,btEnvia
    tabela_vizu.delete(*tabela_vizu.get_children())
    if button_created:
        btEnvia.destroy()
    if button_created2:
        btVizu.destroy()
        btVizu = tk.Button(frame_opcoes,command=visualiza,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    else:
        btVizu = tk.Button(frame_opcoes,command=visualiza,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        button_created2 = True
   
def visualiza():
    global button_created,btEnvia,btVizu,pbVizu,messageId_clicked,importavel
    btVizu.destroy()
    pbVizu = ttk.Progressbar(frame_opcoes, mode='determinate')
    pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    tabela_vizu.delete(*tabela_vizu.get_children())
    item = tabela_opcoes.selection()[0]
    messageId_clicked = tabela_opcoes.item(item, "values")[0]
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={messageId_clicked}")
    pedidos = trataPedescoTxt(linkView)

    def importar():
        global banco,importavel
        con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252')
        con.begin()
        for value in pedidos['procedures']:
            execute(con,value)    
        con.commit()
        con.close()
        con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252')
        lista_importados = select(con,"select pedido from requisicoes ")
        con.close()
        lista_importados = [' '.join(map(str, tupla)) for tupla in lista_importados]
        tabela_opcoes.delete(*tabela_opcoes.get_children())
        for X in range (0,len(options['Data'])):
    
            if X % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "normal"
            if  options['MessageID'][X] in lista_importados:
                fundo = "verde"  
            tabela_opcoes.insert("", tk.END,values=(options['MessageID'][X],options['Size'][X],options['Data'][X],options['Hora'][X],"Confirmado"),tags=(fundo))
        tabela_opcoes.tag_configure("branco", background=cor["branco"])
        tabela_opcoes.tag_configure("verde", background=cor["verde"])
        btEnvia.destroy()
        root.update()
        
   
    
    if importavel:
        if button_created:
            btEnvia.destroy()
            btEnvia = tk.Button(frame_opcoes,command=importar,text='Importar',bg=cor["azul"], fg=cor["branco"])
            btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        else:
            btEnvia = tk.Button(frame_opcoes,command=importar,text='Importar',bg=cor["azul"], fg=cor["branco"])
            btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            button_created = True
    
    else:
        print('erro')

options=opcoes()

con = firebirdsql.connect(
    host='localhost',
    database=banco,
    user='SYSDBA',
    password='masterkey',
    port=3050,
    charset='WIN1252')
lista_importados = select(con,"select pedido from requisicoes ")
con.close()

cor = {"verde" : "#A7C957","azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}

button_created = True
button_created2 = False
pbVizu_created = False
importavel = True

root = tk.Tk()
root.geometry("800x600")
root.config(bg=cor["branco"])
root.state('zoomed')
root.title("Requisições")
root.iconbitmap(default='')

img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
img_coliseu = img_coliseu.subsample(2, 2)

frame_cabecario = tk.Frame(root,height=100,bg=cor["azul"],padx=10)
frame_cabecario.pack(side="top", fill="x")
frame_cabecario.columnconfigure(0, weight=1)
frame_cabecario.columnconfigure(1, weight=4)
frame_cabecario.columnconfigure(2, weight=1)
frame_cabecario.rowconfigure(0, weight=1)

lb_Logo = ttk.Label(frame_cabecario, image=img_coliseu,background=cor["azul"])
lb_Logo.grid(row=0,column=2)

lb_requisicoes = ttk.Label(frame_cabecario, text="Requisições",background=cor["azul"],foreground=cor["branco"]
                   ,font=("Arial", 24,"bold"))
lb_requisicoes.grid(row=0,column=0)

#frame com as tabelas vizu e opcoes
frame_tabelas = tk.Frame(root,bg=cor["vermelho"])
frame_tabelas.pack(fill="both", expand=True, padx=10, pady=10)
frame_tabelas.rowconfigure(0, weight=4)
frame_tabelas.rowconfigure(1, weight=2)
frame_tabelas.rowconfigure(2, weight=1)
frame_tabelas.columnconfigure(0, weight=1)

#frame com a tabela de opções (a de cima)
frame_opcoes = tk.Frame(frame_tabelas,bg=cor["cinza"])
frame_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
frame_opcoes.grid_rowconfigure(0, weight=1)
frame_opcoes.grid_columnconfigure(0, weight=1)

#frame utilizado para posicionar a tabela de opções juntamente com seu scroll
frame_tabela_opcoes = tk.Frame(frame_opcoes,bg=cor["azul"])
frame_tabela_opcoes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

#frame com a tabela de visualizar (a de baixo)
frame_vizu = tk.Frame(frame_tabelas,bg=cor["cinza"])
frame_vizu.grid(row=2, column=0, sticky='nsew')
frame_vizu.grid_rowconfigure(0, weight=1)
frame_vizu.grid_columnconfigure(0, weight=1)

#frame utilizado para posicionar a tabela de visualizar juntamente com seu scroll
frame_tabela_vizu = tk.Frame(frame_vizu,bg=cor["azul"])
frame_tabela_vizu.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

#configurações da tabela de opções
tabela_opcoes = ttk.Treeview(frame_tabela_opcoes, columns=("Message Id","Size", "Data","Hora"), show='headings')
tabela_opcoes.column("Message Id", anchor="center")
tabela_opcoes.column("Size", anchor="center")
tabela_opcoes.column("Data", anchor="center")
tabela_opcoes.column("Hora", anchor="center")
tabela_opcoes.heading("Message Id", text="Message Id")
tabela_opcoes.heading("Size", text="Size")
tabela_opcoes.heading("Data", text="Data")
tabela_opcoes.heading("Hora", text="Hora")
lista_importados=list(lista_importados)


lista_importados = [' '.join(map(str, tupla)) for tupla in lista_importados]

for X in range (0,len(options['Data'])):
    
    if X % 2 == 0 :
        fundo = "branco"
    else:
        fundo = "normal"
    if  options['MessageID'][X] in lista_importados:
        fundo = "verde"  
    tabela_opcoes.insert("", tk.END,values=(options['MessageID'][X],options['Size'][X],options['Data'][X],options['Hora'][X],"Confirmado"),tags=(fundo))
tabela_opcoes.tag_configure("branco", background=cor["branco"])
tabela_opcoes.tag_configure("verde", background=cor["verde"])
tabela_opcoes.bind("<ButtonRelease-1>", item_clicked)
scrollY_opcoes = ttk.Scrollbar(frame_tabela_opcoes, orient="vertical", command=tabela_opcoes.yview)
scrollY_opcoes.pack(side="right", fill="y")
tabela_opcoes.configure(yscrollcommand=scrollY_opcoes.set)
tabela_opcoes.pack(fill="both", expand=True,pady=5,padx=2)

#configurações da tabela de vizualisar
tabela_vizu = ttk.Treeview(frame_tabela_vizu, columns=("codCliente","cliente","produto","referencia","quantidade"), show='headings')
tabela_vizu.column("codCliente", anchor="center")
tabela_vizu.column("cliente", anchor="center")
tabela_vizu.column("produto", anchor="center")
tabela_vizu.column("referencia", anchor="center")
tabela_vizu.column("quantidade", anchor="center")
tabela_vizu.heading("codCliente", text="Cód.Cliente")
tabela_vizu.heading("cliente", text="Cliente")
tabela_vizu.heading("produto", text="Produto")
tabela_vizu.heading("referencia", text="Ref.")
tabela_vizu.heading("quantidade", text="Uni.")
scrollY_vizu = ttk.Scrollbar(frame_tabela_vizu, orient="vertical", command=tabela_vizu.yview)
scrollY_vizu.pack(side="right", fill="y")
tabela_vizu.configure(yscrollcommand=scrollY_vizu.set)
tabela_vizu.pack(fill="both", expand=True,pady=5,padx=2)

btEnvia = tk.Button(frame_opcoes,text='Importar',bg=cor["azul"], fg=cor["branco"])

pbVizu = ttk.Progressbar(frame_opcoes, mode='determinate')

btVizu = tk.Button(frame_opcoes,command=visualiza,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

root.mainloop()



