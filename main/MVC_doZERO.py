import tkinter as tk
from tkinter import ttk
import re
import requests as req
from tkinter import PhotoImage
import firebirdsql



class ViewApp:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
    def interface(self):
        cor = {"verde" : "#A7C957","azul" : "#1D3557","azulClaro" : "#98c1d9","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
 
        img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        img_coliseu = img_coliseu.subsample(2, 2)
        frame_cabecario = tk.Frame(self.root,height=100,bg=cor["azul"],padx=10)
        frame_cabecario.pack(side="top", fill="x")
        frame_cabecario.columnconfigure(0, weight=1)
        frame_cabecario.columnconfigure(1, weight=4)
        frame_cabecario.columnconfigure(2, weight=1)
        frame_cabecario.rowconfigure(0, weight=1)

        lb_Logo = ttk.Label(frame_cabecario, image=img_coliseu,background=cor["azul"])
        
        
        lb_requisicoes = ttk.Label(frame_cabecario, text="Requisições",background=cor["azul"],foreground=cor["branco"]
                                        ,font=("Arial", 24,"bold"))
        

        #frame com as tabelas vizu e opcoes
        frame_tabelas = tk.Frame(self.root,bg=cor["vermelho"])
        frame_tabelas.pack(fill="both", expand=True, padx=10, pady=10)
        frame_tabelas.rowconfigure(0, weight=4)
        frame_tabelas.rowconfigure(1, weight=2)
        frame_tabelas.rowconfigure(2, weight=1)
        frame_tabelas.columnconfigure(0, weight=1)

        #frame com a tabela de opções (a de cima)
        frame_opcoes = tk.Frame(frame_tabelas,bg=cor["cinza"])
        
        
        

        #frame utilizado para posicionar a tabela de opções juntamente com seu scroll
        frame_tabela_opcoes = tk.Frame(frame_opcoes,bg=cor["azul"])
        

        #frame com a tabela de visualizar (a de baixo)
        frame_vizu = tk.Frame(frame_tabelas,bg=cor["cinza"])
        
        
        

        #frame utilizado para posicionar a tabela de visualizar juntamente com seu scroll
        frame_tabela_vizu = tk.Frame(frame_vizu,bg=cor["azul"])
        

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
        for X in range(0,5):
            if X % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "normal"
            tabela_opcoes.insert("", tk.END,values=(X,X,X,X,X),tags=(fundo))
            tabela_opcoes.tag_configure("branco", background=cor["branco"])

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

        btVizu = tk.Button(frame_opcoes,command=None,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])


        lb_Logo.grid(row=0,column=2)
        lb_requisicoes.grid(row=0,column=0)
        frame_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        frame_opcoes.grid_rowconfigure(0, weight=1)
        frame_opcoes.grid_columnconfigure(0, weight=1)
        frame_tabela_opcoes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        frame_vizu.grid(row=2, column=0, sticky='nsew')
        frame_vizu.grid_rowconfigure(0, weight=1)
        frame_vizu.grid_columnconfigure(0, weight=1)
        frame_tabela_vizu.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        
        
    def insert_values_tree(self, table, rows):
        for row in rows:
            table.insert("", "end", values=row)

class ModelApp:
    def __init__(self):
        self.dados = "select * from clientes"

    def conection(self):
        with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
            self.banco= arquivo.read()

        self.conection = firebirdsql.connect(
                        host='localhost',
                        database=self.banco,
                        user='SYSDBA',
                        password='masterkey',
                        port=3050,
                        charset='WIN1252')
        return(self.conection)
    
    def htmlResponseText(self,link):
        self.user='CampFacil'
        self.senha='dsffjyxtf4x'
        self.response = req.get(link, auth=(self.user,self.senha))
        return(self.response.text)
    
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

class ControllerApp:
    def __init__(self, model, view):
        self.model = model
        self.view = view
          
    def load_data(self):
        return self.model.data

    def get_data(self):
        return self.model.data

if __name__ == "__main__":
    model = ModelApp()
    root = tk.Tk()
    controller = ControllerApp(model, ViewApp(root, None))
    view = ViewApp(root, controller)
    controller.view = view
    view.interface()
    root.mainloop()