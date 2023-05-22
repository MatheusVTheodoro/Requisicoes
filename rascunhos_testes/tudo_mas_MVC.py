import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import firebirdsql
import re
import requests as req


class ManipulaDados():
    with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
        banco= arquivo.read()

    con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252') 
                                                                                                             
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
        html=ManipulaDados.htmlResponseText("https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get")
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
        global tabela_vizu,root,pbVizu,banco,messageId_clicked
        
        procedures=[]
        texto = ManipulaDados.htmlResponseText(link)
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
            cliente=ManipulaDados.select(con,query)
            query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
            produto=ManipulaDados.select(con,query)
            
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

            procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{messageId_clicked}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
            procedures.append(procedure)
        con.close()
        pbVizu.destroy()    
        return {'procedures':procedures}

class ViewInterface():
    def __init__(self, controller):
        self.controller = controller
        cor = {"verde" : "#ADC178","azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
        
        root = tk.Tk()
        root.geometry("800x600")
        root.config(bg=cor["branco"])
        root.state('zoomed')
        root.title("Requisições")
        root.iconbitmap(default='')

        imgColiseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        imgColiseu = imgColiseu.subsample(2, 2)
        frameCabecario = tk.Frame(root,height=100,bg=cor["azul"],padx=10)
        frameCabecario.columnconfigure(0, weight=1)
        frameCabecario.columnconfigure(1, weight=4)
        frameCabecario.columnconfigure(2, weight=1)
        frameCabecario.rowconfigure(0, weight=1)
        frameTabelas = tk.Frame(root,bg=cor["vermelho"])
        frameTabelas.rowconfigure(0, weight=4)
        frameTabelas.rowconfigure(1, weight=2)
        frameTabelas.rowconfigure(2, weight=1)
        frameTabelas.columnconfigure(0, weight=1)
        frameOpcoes = tk.Frame(frameTabelas,bg=cor["cinza"])
        frameTabelaOpcoes = tk.Frame(frameOpcoes,bg=cor["azul"])
        frameVisu = tk.Frame(frameTabelas,bg=cor["cinza"])
        frameTabelaVisu = tk.Frame(frameVisu,bg=cor["azul"])
        tabelaOpcoes = ttk.Treeview(frameTabelaOpcoes, columns=("Message Id","Size", "Data","Hora"), show='headings')
        tabelaOpcoes.column("Message Id", anchor="center")
        tabelaOpcoes.column("Size", anchor="center")
        tabelaOpcoes.column("Data", anchor="center")
        tabelaOpcoes.column("Hora", anchor="center")
        tabelaOpcoes.heading("Message Id", text="Message Id")
        tabelaOpcoes.heading("Size", text="Size")
        tabelaOpcoes.heading("Data", text="Data")
        tabelaOpcoes.heading("Hora", text="Hora")
        tabelaOpcoes.tag_configure("branco", background=cor["branco"])
        tabelaOpcoes.tag_configure("verde", background=cor["verde"])
        tabelaVisu = ttk.Treeview(frameTabelaVisu, columns=("codCliente","cliente","produto","referencia","quantidade"), show='headings')
        tabelaVisu.column("codCliente", anchor="center")
        tabelaVisu.column("cliente", anchor="center")
        tabelaVisu.column("produto", anchor="center")
        tabelaVisu.column("referencia", anchor="center")
        tabelaVisu.column("quantidade", anchor="center")
        tabelaVisu.heading("codCliente", text="Cód.Cliente")
        tabelaVisu.heading("cliente", text="Cliente")
        tabelaVisu.heading("produto", text="Produto")
        tabelaVisu.heading("referencia", text="Ref.")
        tabelaVisu.heading("quantidade", text="Uni.")
        scrollY_opcoes = ttk.Scrollbar(frameTabelaOpcoes, orient="vertical", command=tabelaOpcoes.yview)
        tabelaOpcoes.configure(yscrollcommand=scrollY_opcoes.set)
        scrollY_vizu = ttk.Scrollbar(frameTabelaVisu, orient="vertical", command=tabelaVisu.yview)
        tabelaVisu.configure(yscrollcommand=scrollY_vizu.set)
        pbVizu = ttk.Progressbar(frameOpcoes, mode='determinate')
        btVizu = tk.Button(frameOpcoes,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
        btEnvia = tk.Button(frameOpcoes,text='Importar',bg=cor["azul"], fg=cor["branco"])
        lbLogo = ttk.Label(frameCabecario, image=imgColiseu,background=cor["azul"])
        lbRequisicoes = ttk.Label(frameCabecario, text="Requisições",background=cor["azul"],foreground=cor["branco"],font=("Arial", 24,"bold"))

        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        lbLogo.grid(row=0,column=2)
        lbRequisicoes.grid(row=0,column=0)
        frameOpcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        frameOpcoes.grid_rowconfigure(0, weight=1)
        frameOpcoes.grid_columnconfigure(0, weight=1)
        frameTabelaOpcoes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        frameVisu.grid(row=2, column=0, sticky='nsew')
        frameVisu.grid_rowconfigure(0, weight=1)
        frameVisu.grid_columnconfigure(0, weight=1)
        frameTabelaVisu.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        frameCabecario.pack(side="top", fill="x")
        frameTabelas.pack(fill="both", expand=True, padx=10, pady=10)
        scrollY_opcoes.pack(side="right", fill="y")
        tabelaOpcoes.pack(fill="both", expand=True,pady=5,padx=2)
        scrollY_vizu.pack(side="right", fill="y")
        tabelaVisu.pack(fill="both", expand=True,pady=5,padx=2)

    def executar(self):
        self.root.mainloop()

class Controlador:
    def trataPedescoTxt(link):
        procedures=[]
        texto = ManipulaDados.htmlResponseText(link)
        texto = re.findall("98.............................................................",texto)
        maximum=len(texto) 
        app.pbVizu['maximum'] = maximum
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
            cliente=ManipulaDados.select(con,query)
            query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
            produto=ManipulaDados.select(con,query)
            
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

            procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
            procedures.append(procedure)
            if index % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "verde"
            
            app.tabela_vizu.insert("", tk.END,values=(codCliente,cliente,produto,peca,quantidade),tags=(fundo))
            app.pbVizu['value'] = index+1
            app.root.update()
        con.close()
        app.pbVizu.destroy()    
        return {'procedures':procedures}

    def visualiza():
        options=ManipulaDados.opcoes()
        app.btVizu.destroy()
        pbVizu = ttk.Progressbar(app.frame_opcoes, mode='determinate')
        pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        app.tabela_vizu.delete(*app.tabela_vizu.get_children())
        item = app.tabela_opcoes.selection()[0]
        messageId_clicked = app.tabela_opcoes.item(item, "values")[0]
        linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={messageId_clicked}")
        pedidos = Controlador.trataPedescoTxt(linkView)

        def importar():
            global banco
            con = firebirdsql.connect(
            host='localhost',
            database=banco,
            user='SYSDBA',
            password='masterkey',
            port=3050,
            charset='WIN1252')
            con.begin()
            for value in pedidos['procedures']:
                ManipulaDados.execute(con,value)    
            con.commit()
            con.close()
            con = firebirdsql.connect(
            host='localhost',
            database=banco,
            user='SYSDBA',
            password='masterkey',
            port=3050,
            charset='WIN1252')
            lista_importados = ManipulaDados.select(con,"select pedido from requisicoes ")
            con.close()
            lista_importados = [' '.join(map(str, tupla)) for tupla in lista_importados]
            app.tabela_opcoes.delete(*app.tabela_opcoes.get_children())
            for X in range (0,len(options['Data'])):
        
                if X % 2 == 0 :
                    fundo = "branco"
                else:
                    fundo = "normal"
                if  options['MessageID'][X] in lista_importados:
                    fundo = "verde"  
                app.tabela_opcoes.insert("", tk.END,values=(options['MessageID'][X],options['Size'][X],options['Data'][X],options['Hora'][X],"Confirmado"),tags=(fundo))
            app.tabela_opcoes.tag_configure("branco", background=app.cor["branco"])
            app.tabela_opcoes.tag_configure("verde", background=app.cor["verde"])
            app.btEnvia.destroy()
            app.root.update()

    def item_clicked(event):
        app.tabela_vizu.delete(*app.tabela_vizu.get_children())
        if app.button_created:
            app.btEnvia.destroy()
        if button_created2:
            btVizu.destroy()
            btVizu = tk.Button(app.frame_opcoes,command=Controlador.visualiza,text='Carregar Visualização',bg=app.cor["azul"], fg=app.cor["branco"])
            btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        else:
            btVizu = tk.Button(app.frame_opcoes,command=Controlador.visualiza,text='Carregar Visualização',bg=app.cor["azul"], fg=app.cor["branco"])
            btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            button_created2 = True
    
    def executar(self):
        self.view.executar()



        
if __name__ == "__main__":
    # ao determinar app como ViewInterface() eu basicamente trago minha classe Viewinterface completa
    # podendo ser acessada assim como feito abaixo em app.root.mainloop()
    # que acessa o parametro root para iniciar minha janela 
    app = ViewInterface()
        
    app.tabelaOpcoes.bind("<ButtonRelease-1>", Controlador.item_clicked)

    app.root.mainloop()
