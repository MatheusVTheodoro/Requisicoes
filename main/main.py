import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox


root = tk.Tk()

class Aplication():
    def __init__(self):
        self.cor = {"verde" : "#A7C957","azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#ced4da","vermelho" : "#E63946", "cinza" : "#8D99AE"}
        with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
            self.banco= arquivo.read()
        self.options = self.tabelaOpcoesData()
        self.root = root
        con = firebirdsql.connect(
            host='localhost',
            database=self.banco,
            user='SYSDBA',
            password='masterkey',
            port=3050,
            charset='WIN1252')
        self.lista_importados = self.select(con,"select pedido from requisicoes ")
        self.lista_importados = [' '.join(map(str, tupla)) for tupla in self.lista_importados]
        self.button_created = True
        self.button_created2 = False
        self.pbVizu_created = False
        self.importavel = True
        self.usuarios = {
            "1": "SILENUS",
            "123": "usuario1",
            "456": "usuario2",
            "789": "usuario3"
        }
        self.telalogin()
        root.mainloop() 
    
    def telalogin(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(bg=self.cor["branco"])
        largura_janela = 500  # Largura da janela em pixels
        altura_janela = 300  # Altura da janela em pixels
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.root.resizable(width=False, height=False)

        self.img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_coliseu = self.img_coliseu.subsample(2, 2)
        self.frame_login = tk.Frame(self.root,bg=self.cor["azul"])
        self.frame_login.pack(fill="both", expand=True)
        self.lb_Logo = ttk.Label(self.frame_login, image=self.img_coliseu,background=self.cor["azul"])
        self.lb_Logo.grid(row=0,column=0)
        self.id_label = tk.Label(self.frame_login, text="ID:")
        self.id_entry = tk.Entry(self.frame_login)
        self.id_entry.bind("<Return>", self.preencher_usuario)
        self.usuario_label = tk.Label(self.frame_login, text="Usuário:")
        self.usuario_entry = tk.Entry(self.frame_login, state='readonly')  
        self.label_senha = tk.Label(self.frame_login, text="Senha:")

        self.senha = tk.Entry(self.frame_login, show="*")
        
        self.botao_entrar = tk.Button(self.frame_login, text="Entrar", command=self.fazer_login)
        
        self.senha.bind("<Key>", self.verificar_tecla)

        self.id_label.grid(row=0, column=0, sticky=tk.E)
        self.id_entry.grid(row=0, column=1)
        self.usuario_label.grid(row=1, column=0, sticky=tk.E)
        self.usuario_entry.grid(row=1, column=1)
        self.label_senha.grid(row=2, column=0)
        self.senha.grid(row=2, column=1)
        self.botao_entrar.grid(row=1, column=0, columnspan=2, pady=10)

    def preencher_usuario(self,event=None):
        # Função para preencher o campo "Usuário" com base no ID digitado
        id_digitado = self.id_entry.get()

        # Verificar se o ID está presente no dicionário
        if id_digitado in self.usuarios:
            self.usuario_entry.configure(state='normal')  # Habilitar o campo "Usuário" para escrita
            self.usuario_entry.delete(0, tk.END)  # Limpar o campo "Usuário"
            self.usuario_entry.insert(0, self.usuarios[id_digitado])  # Preencher com o valor correspondente
            self.usuario_entry.configure(state='readonly')  # Bloquear o campo "Usuário" para escrita novamente
            self.senha.focus()  # Mover o foco para o campo "Senha"

    def fazer_login(self):
        senha_digitada = self.senha.get()
        if senha_digitada == "62728292":
            for widget in self.root.winfo_children():
                widget.destroy()
            self.telaInicial()
        else:
            messagebox.showerror("Login", "Senha incorreta!")
    
    def verificar_tecla(self,event):
        if event.keycode == 13:
            self.fazer_login()

    def telaInicial(self):
        self.root.geometry("800x600")
        self.root.config(bg=self.cor["branco"])
        self.root.resizable(width=True, height=True)
        self.root.state('zoomed')
        self.root.title("Requisições")
        self.img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_coliseu = self.img_coliseu.subsample(2, 2)
        self.frame_cabecario = tk.Frame(root,height=100,bg=self.cor["azul"],padx=10)
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
        self.frame_tabelas = tk.Frame(root,bg=self.cor["vermelho"])
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
        self.tabela_vizu = ttk.Treeview(self.frame_tabela_vizu, columns=("codCliente","nome","nome_fantasia","cidade","uf","produto","referencia","quantidade"), show='headings')
        self.tabela_vizu.column("codCliente", anchor="center",width=1)
        self.tabela_vizu.column("nome", anchor="center",width=200)
        self.tabela_vizu.column("nome_fantasia", anchor="center",width=100)
        self.tabela_vizu.column("cidade", anchor="center",width=100)
        self.tabela_vizu.column("uf", anchor="center",width=1)
        self.tabela_vizu.column("produto", anchor="center",width=200)
        self.tabela_vizu.column("referencia", anchor="center",width=1)
        self.tabela_vizu.column("quantidade", anchor="center",width=1)
        self.tabela_vizu.heading("codCliente", text="Código")
        self.tabela_vizu.heading("nome", text="Nome")
        self.tabela_vizu.heading("nome_fantasia", text="Nome Fantasia")
        self.tabela_vizu.heading("cidade", text="Cidade")
        self.tabela_vizu.heading("uf", text="UF")
        self.tabela_vizu.heading("produto", text="Produto")
        self.tabela_vizu.heading("referencia", text="Código de Fab.")
        self.tabela_vizu.heading("quantidade", text="Unid.")
        self.scrollY_vizu = ttk.Scrollbar(self.frame_tabela_vizu, orient="vertical", command=self.tabela_vizu.yview)
        self.scrollY_vizu.pack(side="right", fill="y")
        self.tabela_vizu.configure(yscrollcommand=self.scrollY_vizu.set)
        self.tabela_vizu.pack(fill="both", expand=True,pady=5,padx=2)

        self.btEnvia = tk.Button(self.frame_opcoes,text='Importar',bg=self.cor["azul"], fg=self.cor["branco"])

        self.pbVizu = ttk.Progressbar(self.frame_opcoes, mode='determinate')

        self.btVizu = tk.Button(self.frame_opcoes,command=self.visualiza,text='Carregar Visualização',bg=self.cor["azul"], fg=self.cor["branco"])

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

    def tabelaOpcoesData(self):
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

    def htmlResponseText(self,link):
        user='CampFacil'
        senha='dsffjyxtf4x'
        response = req.get(link, auth=(user,senha))
        return(response.text)

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

    def consultarPedido(self,link):
        self.importavel = True
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
            clientedados=[]
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

            query=(f"select NOME,NOME_FANTASIA,cidade, uf from clientes JOIN regioes ON clientes.id_regiao = regioes.id_regiao where clientes.DOC_EX = '{codCliente}'")
            listtupla=self.select(con,query)
            query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
            produto=self.select(con,query)
            
            if(self.messageId_clicked in self.lista_importados):
                self.importavel = False
            if(produto==[]):
                produto='CÓDIGO DE FABRICA NÃO VINCULADO'
                self.importavel = False
            else:
                produto=produto[0]
                produto=str(produto)
                produto = produto[2:-3]

            if(listtupla==[]):
                nome = 'CODIGO DE CLIENTE NÃO VINCULADO'
                nome_fantasia = 'CODIGO DE CLIENTE NÃO VINCULADO'
                cidade = 'CODIGO DE CLIENTE NÃO VINCULADO'
                uf = 'CODIGO DE CLIENTE NÃO VINCULADO'
                self.importavel = False
            else:
                tupla=listtupla[0]
                nome = tupla[0]
                nome_fantasia = tupla[1]
                cidade = tupla[2]
                uf = tupla[3]

            procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{self.messageId_clicked}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
            procedures.append(procedure)
            
            if (nome =='CODIGO DE CLIENTE NÃO VINCULADO')or(produto =='CÓDIGO DE FABRICA NÃO VINCULADO'):
                fundo = "vermelho"
            elif (index % 2 == 0) :
                fundo = "branco"
            else:
                fundo="verde"
            
            self.tabela_vizu.insert("", tk.END,values=(codCliente,nome,nome_fantasia,cidade,uf,produto,peca,quantidade),tags=(fundo))
            self.tabela_vizu.tag_configure("branco", background=self.cor["branco"])
            self.tabela_vizu.tag_configure("vermelho", background=self.cor["vermelho"])
            self.pbVizu['value'] = index+1
            root.update()
        con.close()
        self.pbVizu.destroy()    
        return {'procedures':procedures}

    def visualiza(self):
        self.btVizu.destroy()
        self.pbVizu = ttk.Progressbar(self.frame_opcoes, mode='determinate')
        self.pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.tabela_vizu.delete(*self.tabela_vizu.get_children())
        item = self.tabela_opcoes.selection()[0]
        self.messageId_clicked = self.tabela_opcoes.item(item, "values")[0]
        self.linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={self.messageId_clicked}")
        self.pedidos = self.consultarPedido(self.linkView)
        
        if self.importavel:
            if self.button_created:
                self.btEnvia.destroy()
                self.btEnvia = tk.Button(self.frame_opcoes,command=self.importar,text='Importar',bg=self.cor["azul"], fg=self.cor["branco"])
                self.btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            else:
                self.btEnvia = tk.Button(self.frame_opcoes,command=self.importar,text='Importar',bg=self.cor["azul"], fg=self.cor["branco"])
                self.btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
                self.button_created = True
        
        else:
            print('error')

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
        self.tabela_opcoes.delete(*self.tabela_opcoes.get_children())
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

Aplication()
