import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage


class App:
    def __init__(self,root):
        self.root = root
        with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
            self.banco= arquivo.read()
        self.options=self.opcoes()

    def select(self,con,query):
        cur = con.cursor()
        cur.execute(query)
        resultado = cur.fetchall()
        cur.close()
        return resultado

    def execute(self,con,query):
        cur = con.cursor()
        cur.execute(query)
        cur.close()
        
    def htmlResponseText(self,link):
        user='CampFacil'
        senha='dsffjyxtf4x'
        response = req.get(link, auth=(user,senha))
        return(response.text)

    def opcoes(self):
        html=self.htmlResponseText("https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get")
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

    def trataPedescoTxt(self,link):
        procedures=[]
        texto = self.htmlResponseText(link)
        texto = re.findall("98.............................................................",texto)
        maximum=len(texto) 
        self.pbVizu['maximum'] = maximum
        con = firebirdsql.connect(
        host='localhost',
        database=self.banco,
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
            cliente=self.select(con,query)
            query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
            produto=self.select(con,query)
            
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

            procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{self.messageId_clicked}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
            procedures.append(procedure)
            if index % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "verde"
            
            self.tabela_vizu.insert("", tk.END,values=(codCliente,cliente,produto,peca,quantidade),tags=(fundo))
            self.tabela_vizu.tag_configure("branco", background=self.cor["branco"])
            self.pbVizu['value'] = index+1
            self.root.update()
        con.close()
        self.pbVizu.destroy()    
        return {'procedures':procedures}

    def item_clicked(self,event):
        self.tabela_vizu.delete(*self.tabela_vizu.get_children())
        if self.button_created:
            self.btEnvia.destroy()
        if self.button_created2:
            self.btVizu.destroy()
            self.btVizu = tk.Button(self.frame_opcoes,command=self.visualiza,text='Carregar Visualização',bg=self.cor["azul"], fg=self.cor["branco"])
            self.btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        else:
            self.btVizu = tk.Button(self.frame_opcoes,command=self.visualiza,text='Carregar Visualização',bg=self.cor["azul"], fg=self.cor["branco"])
            self.btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            self.button_created2 = True
    
    def visualiza(self):
        self.btVizu.destroy()
        self.pbVizu = ttk.Progressbar(self.frame_opcoes, mode='determinate')
        self.pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.tabela_vizu.delete(*self.tabela_vizu.get_children())
        item = self.tabela_opcoes.selection()[0]
        self.messageId_clicked = self.tabela_opcoes.item(item, "values")[0]
        linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={self.messageId_clicked}")
        self.pedidos = self.trataPedescoTxt(linkView)

    def importar(self):
        con = firebirdsql.connect(
        host='localhost',
        database=self.banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252')
        con.begin()
        for value in self.pedidos['procedures']:
            self.execute(con,value)    
        con.commit()
        con.close()
        con = firebirdsql.connect(
        host='localhost',
        database=self.banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252')
        self.lista_importados = self.select(con,"select pedido from requisicoes ")
        con.close()
        self.lista_importados = [' '.join(map(str, tupla)) for tupla in self.lista_importados]
        self.tabela_opcoes.delete(*self.tabela_opcoes.get_children())
        for X in range (0,len(self.options['Data'])):
        
            if X % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "normal"
            if  self.options['MessageID'][X] in self.lista_importados:
                fundo = "verde"  
            self.tabela_opcoes.insert("", tk.END,values=(self.options['MessageID'][X],self.options['Size'][X],self.options['Data'][X],self.options['Hora'][X],"Confirmado"),tags=(fundo))
        self.tabela_opcoes.tag_configure("branco", background=self.cor["branco"])
        self.tabela_opcoes.tag_configure("verde", background=self.cor["verde"])
        self.btEnvia.destroy()
        self.root.update()
            
            
        

        if self.button_created:
            self.btEnvia.destroy()
            self.btEnvia = tk.Button(self.frame_opcoes,command=self.importar,text='Importar',bg=self.cor["azul"], fg=self.cor["branco"])
            self.btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        else:
            self.btEnvia = tk.Button(self.frame_opcoes,command=self.importar,text='Importar',bg=self.cor["azul"], fg=self.cor["branco"])
            self.btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            self.button_created = True

    def interface(self):
        self.cor = {"verde" : "#A7C957","azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
        
        self.button_created = True
        self.button_created2 = False
        self.pbVizu_created = False

        self.root.geometry("800x600")
        self.root.config(bg=self.cor["branco"])
        self.root.state('zoomed')
        self.root.title("Requisições")
        self.root.iconbitmap(default='')
        

        self.img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_coliseu = self.img_coliseu.subsample(2, 2)

        self.frame_cabecario = tk.Frame(self.root,height=100,bg=self.cor["azul"],padx=10)
        self.frame_cabecario.pack(side="top", fill="x")
        self.frame_cabecario.columnconfigure(0, weight=1)
        self.frame_cabecario.columnconfigure(1, weight=4)
        self.frame_cabecario.columnconfigure(2, weight=1)
        self.frame_cabecario.rowconfigure(0, weight=1)

        self.lb_Logo = ttk.Label(self.frame_cabecario, image=self.img_coliseu,background=self.cor["azul"])
        self.lb_Logo.grid(row=0,column=2)

        self.lb_requisicoes = ttk.Label(self.frame_cabecario, text="Requisições",background=self.cor["azul"],foreground=self.cor["branco"],font=("Arial", 24,"bold"))
        self.lb_requisicoes.grid(row=0,column=0)

        #frame com as tabelas vizu e opcoes
        self.frame_tabelas = tk.Frame(self.root,bg=self.cor["vermelho"])
        self.frame_tabelas.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame_tabelas.rowconfigure(0, weight=4)
        self.frame_tabelas.rowconfigure(1, weight=2)
        self.frame_tabelas.rowconfigure(2, weight=1)
        self.frame_tabelas.columnconfigure(0, weight=1)

        #frame com a tabela de opções (a de cima)
        self.frame_opcoes = tk.Frame(self.frame_tabelas,bg=self.cor["cinza"])
        self.frame_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        self.frame_opcoes.grid_rowconfigure(0, weight=1)
        self.frame_opcoes.grid_columnconfigure(0, weight=1)

        #frame utilizado para posicionar a tabela de opções juntamente com seu scroll
        self.frame_tabela_opcoes = tk.Frame(self.frame_opcoes,bg=self.cor["azul"])
        self.frame_tabela_opcoes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        #frame com a tabela de visualizar (a de baixo)
        self.frame_vizu = tk.Frame(self.frame_tabelas,bg=self.cor["cinza"])
        self.frame_vizu.grid(row=2, column=0, sticky='nsew')
        self.frame_vizu.grid_rowconfigure(0, weight=1)
        self.frame_vizu.grid_columnconfigure(0, weight=1)

        #frame utilizado para posicionar a tabela de visualizar juntamente com seu scroll
        self.frame_tabela_vizu = tk.Frame(self.frame_vizu,bg=self.cor["azul"])
        self.frame_tabela_vizu.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        #configurações da tabela de opções
        self.tabela_opcoes = ttk.Treeview(self.frame_tabela_opcoes, columns=("Message Id","Size", "Data","Hora"), show='headings')
        self.tabela_opcoes.column("Message Id", anchor="center")
        self.tabela_opcoes.column("Size", anchor="center")
        self.tabela_opcoes.column("Data", anchor="center")
        self.tabela_opcoes.column("Hora", anchor="center")
        self.tabela_opcoes.heading("Message Id", text="Message Id")
        self.tabela_opcoes.heading("Size", text="Size")
        self.tabela_opcoes.heading("Data", text="Data")
        self.tabela_opcoes.heading("Hora", text="Hora")





        con = firebirdsql.connect(
            host='localhost',
            database=self.banco,
            user='SYSDBA',
            password='masterkey',
            port=3050,
            charset='WIN1252')
        self.lista_importados = self.select(con,"select pedido from requisicoes ")
        con.close()






        self.lista_importados=list(self.lista_importados)


        self.lista_importados = [' '.join(map(str, tupla)) for tupla in self.lista_importados]

        for X in range (0,len(self.options['Data'])):
            
            if X % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "normal"
            if  self.options['MessageID'][X] in self.lista_importados:
                fundo = "verde"  
            self.tabela_opcoes.insert("", tk.END,values=(self.options['MessageID'][X],self.options['Size'][X],self.options['Data'][X],self.options['Hora'][X],"Confirmado"),tags=(fundo))
        self.tabela_opcoes.tag_configure("branco", background=self.cor["branco"])
        self.tabela_opcoes.tag_configure("verde", background=self.cor["verde"])
        self.tabela_opcoes.bind("<ButtonRelease-1>", self.item_clicked)
        self.scrollY_opcoes = ttk.Scrollbar(self.frame_tabela_opcoes, orient="vertical", command=self.tabela_opcoes.yview)
        self.scrollY_opcoes.pack(side="right", fill="y")
        self.tabela_opcoes.configure(yscrollcommand=self.scrollY_opcoes.set)
        self.tabela_opcoes.pack(fill="both", expand=True,pady=5,padx=2)

        #configurações da tabela de vizualisar
        self.tabela_vizu = ttk.Treeview(self.frame_tabela_vizu, columns=("codCliente","cliente","produto","referencia","quantidade"), show='headings')
        self.tabela_vizu.column("codCliente", anchor="center")
        self.tabela_vizu.column("cliente", anchor="center")
        self.tabela_vizu.column("produto", anchor="center")
        self.tabela_vizu.column("referencia", anchor="center")
        self.tabela_vizu.column("quantidade", anchor="center")
        self.tabela_vizu.heading("codCliente", text="Cód.Cliente")
        self.tabela_vizu.heading("cliente", text="Cliente")
        self.tabela_vizu.heading("produto", text="Produto")
        self.tabela_vizu.heading("referencia", text="Ref.")
        self.tabela_vizu.heading("quantidade", text="Uni.")
        self.scrollY_vizu = ttk.Scrollbar(self.frame_tabela_vizu, orient="vertical", command=self.tabela_vizu.yview)
        self.scrollY_vizu.pack(side="right", fill="y")
        self.tabela_vizu.configure(yscrollcommand=self.scrollY_vizu.set)
        self.tabela_vizu.pack(fill="both", expand=True,pady=5,padx=2)

        self.btEnvia = tk.Button(self.frame_opcoes,text='Importar',bg=self.cor["azul"], fg=self.cor["branco"])

        self.pbVizu = ttk.Progressbar(self.frame_opcoes, mode='determinate')

        self.btVizu = tk.Button(self.frame_opcoes,command=self.visualiza,text='Carregar Visualização',bg=self.cor["azul"], fg=self.cor["branco"])
        #self.btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')














if __name__ == "__main__":
    root = tk.Tk()
    program = App(root)
    program.interface()
    root.mainloop()