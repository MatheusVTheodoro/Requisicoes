import tkinter as tk
from tkinter import PhotoImage
#from tkinter import ttk
import ttkbootstrap as ttk
import requests as req
import re
import firebirdsql
from tkinter import messagebox
from data import Data
from tkinter import filedialog

class Home(ttk.Window):
    def __init__(self):
        super().__init__()
        self.Data = Data()
        self.banco = self.Data.get_banco()
        self.options = self.Data.treeOpcoesData()
        self.pedidosNf = self.Data.pedidosNfeData()
        self.lista_importados = self.Data.get_lista_importados()
        self.style.theme_use("flatly")
        self.title("Requisições")
        #self.home_create_widgets()
        #self.tree_opcoes_update()
        #self.home_configure_layout()
        self.usuarios = {
            "1": "SILENUS",
            "123": "usuario1",
            "456": "usuario2",
            "789": "usuario3"
        }
        self.login_screen()
        self.btVizu_created = False
        self.btEnvia_created = False
        self.importavel = True
        self.menuBar_open = False     
      


    def tree_pedidosNf_update(self):
        self.pedidosNf = self.Data.pedidosNfeData()
        for X in range (0,len(self.pedidosNf)):
            '''
            config de status --- pode ser util depois
            if  self.options['MessageID'][X] in self.lista_importados:
                fundo = "verde"
            else:
                fundo ="normal"
            '''
            pedido=self.pedidosNf[X]    
            self.tree_pedidos.insert("", tk.END,values=(pedido['nome'],pedido['nome_fantasia'],pedido['nf'],pedido['pedido'],pedido['chave'],pedido['valor'],pedido['cnpj']))
            
        



    def tree_opcoes_update(self):
        self.lista_importados = self.Data.get_lista_importados()
        for X in range (0,len(self.options['Data'])):
            if  self.options['MessageID'][X] in self.lista_importados:
                fundo = "verde"
            else:
                fundo ="normal"  
            self.tree_opcoes.insert("", tk.END,values=(self.options['MessageID'][X],self.options['Size'][X],self.options['Data'][X],self.options['Hora'][X],"Confirmado"),tags=(fundo))
        self.tree_opcoes.bind("<ButtonRelease-1>", self.item_clicked)

    def add_pedidoNf(self):
        item = self.tree_pedidos.selection()
        pedido = self.tree_pedidos.item(item, "values")[3]
        nf = self.tree_pedidos.item(item, "values")[2]
        valor = self.tree_pedidos.item(item, "values")[5]
        cnpj = self.tree_pedidos.item(item, "values")[6]
        self.tree_adicionados.insert("", tk.END,values=(pedido,nf,valor,cnpj))

    def gerar_arquivo(self):
        arquivo = filedialog.asksaveasfile(defaultextension=".txt")
        
        if arquivo is None:
            return
        
        frase = """HEADERNFFORN20230411114705.DAT                                                                                                     98553852A57001DD010300000601900190350667103032023C018531291000020000000299746000044962000020983000020983000000000        00010     """
        arquivo.write(frase)
        arquivo.close()
        
        print("Frase gravada no arquivo:", arquivo.name)




    def visualiza(self):
        self.btVizu.destroy()
        self.tree_vizu.delete(*self.tree_vizu.get_children())
        item = self.tree_opcoes.selection()[0]
        self.messageId_clicked = self.tree_opcoes.item(item, "values")[0]
        self.linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={self.messageId_clicked}")
        self.pedidos = self.consultarPedido(self.linkView)
        
        if self.importavel:
            if self.btEnvia_created:
                self.btEnvia.destroy()
                self.btEnvia = ttk.Button(self.frame_tree_opcoes,command=self.importar,text='Importar',bootstyle=("info"))
                self.btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            else:
                self.btEnvia = ttk.Button(self.frame_tree_opcoes,command=self.importar,text='Importar',bootstyle=("info"))
                self.btEnvia.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
                self.btEnvia_created = True 
        else:
            self.btEnvia.destroy()
            self.btEnvia_created = False   
    
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
            self.Data.execute(con,value)    
        con.commit()
        con.close()
        self.tree_opcoes.delete(*self.tree_opcoes.get_children())
        self.tree_opcoes_update()
        self.btEnvia.destroy()
        self.update()

    def consultarPedido(self,link):
        self.importavel = True
        procedures=[]
        texto = self.Data.htmlResponseText(link)
        texto = re.findall("98.............................................................",texto)
        maximum=len(texto) 
        

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
            listtupla=self.Data.select(query)
            query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
            produto=self.Data.select(query)
            
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
            
            self.tree_vizu.insert("", tk.END,values=(codCliente,nome,nome_fantasia,cidade,uf,produto,peca,quantidade),tags=(fundo))
            self.tree_vizu.tag_configure("vermelho", background="#E63946")
            
            self.update()

            
        return {'procedures':procedures}


   
    '''@@@@@@ Telas do app @@@@@@@'''

    def login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.config(bg="white")
        self.state('normal')
        largura_janela = 420  # Largura da janela em pixels
        altura_janela = 300  # Altura da janela em pixels
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.resizable(width=False, height=False)
        self.title("Requisições")
        self.img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_coliseu = self.img_coliseu.subsample(2, 2)
        self.frame_login = ttk.Frame(self,bootstyle="primary")
        self.frame_login_campos = ttk.Frame(self,padding=(0,20))
        self.frame_login_campos_azul = ttk.Frame(self.frame_login_campos,bootstyle=("primary"),padding=(0,0))
        self.lb_Logo = ttk.Label(self.frame_login, image=self.img_coliseu, bootstyle=("primary","inverse"))
        self.id_label = ttk.Label(self.frame_login_campos_azul, text="ID:",font=("Arial", 12,"bold"),bootstyle=("primary","inverse"))
        self.id_entry = ttk.Entry(self.frame_login_campos_azul)
        self.id_entry.bind("<Return>", self.preencher_usuario)
        self.usuario_label = ttk.Label(self.frame_login_campos_azul, text="Usuário:",font=("Arial", 12,"bold"),bootstyle=("primary","inverse"))
        self.usuario_entry = ttk.Entry(self.frame_login_campos_azul, state='readonly')  
        self.label_senha = ttk.Label(self.frame_login_campos_azul, text="Senha:",font=("Arial", 12,"bold"),bootstyle=("primary","inverse"))
        self.senha = ttk.Entry(self.frame_login_campos_azul, show="*")
        self.botao_entrar = ttk.Button(self.frame_login_campos_azul, text="Entrar", command=self.fazer_login,bootstyle=("info"))
        self.senha.bind("<Key>", self.verificar_tecla)
        self.lb_requisi = ttk.Label(self.frame_login,text="Requisições",font=("Arial", 24,"bold"),bootstyle=("primary","inverse"))

        self.frame_login.pack(side="top", fill="x")
        self.frame_login_campos.pack(fill="both", expand=True)
        self.lb_requisi.grid(row=0,column=1,padx=5,pady=5)
        self.lb_Logo.grid(row=0,column=0,padx=5,pady=5)
        self.frame_login_campos_azul.pack(fill="both", expand=True)

        self.frame_login_campos_azul.rowconfigure(0, weight=1)
        self.frame_login_campos_azul.rowconfigure(1, weight=1)
        self.frame_login_campos_azul.rowconfigure(2, weight=1)
        self.frame_login_campos_azul.rowconfigure(3, weight=1)
        self.frame_login_campos_azul.rowconfigure(4, weight=1)
        self.frame_login_campos_azul.columnconfigure(0, weight=5)
        self.frame_login_campos_azul.columnconfigure(1, weight=1)
        self.frame_login_campos_azul.columnconfigure(2, weight=4)
        self.frame_login_campos_azul.columnconfigure(3, weight=1)

        self.id_label.grid(row=1, column=0)
        self.id_entry.grid(row=1, column=1)
        self.usuario_label.grid(row=2, column=0)
        self.usuario_entry.grid(row=2, column=1)
        self.label_senha.grid(row=3, column=0)
        self.senha.grid(row=3, column=1)
        self.botao_entrar.grid(row=4,column=1,pady=10)

    def pedidos_screen(self):
        self.pedidos_create_widgets()
        self.tree_pedidosNf_update()
        self.pedidos_configure_layout()

    def pedidos_create_widgets(self):
        self.geometry("1280x720")
        self.resizable(width=True, height=True)
        self.frame_cabecario = ttk.Frame(self, height= 100, bootstyle="primary")
        self.frame_cabecario.columnconfigure(0, weight=1)
        self.frame_cabecario.columnconfigure(1, weight=8)
        self.frame_cabecario.columnconfigure(2, weight=2)
        self.frame_cabecario.columnconfigure(3, weight=1)
        self.frame_cabecario.rowconfigure(0, weight=1)

        self.frame_principal = ttk.Frame(self) #este frame é utilizado apenas para receber organizar outros 2
        self.frame_principal.grid_columnconfigure(0, weight=3)
        self.frame_principal.grid_columnconfigure(1, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.danger_all = ttk.Frame(self.frame_principal)
        self.danger = ttk.Frame(self.danger_all)
        self.success_all = ttk.Frame(self.frame_principal)
        self.success = ttk.Frame(self.success_all)
        

        self.frame_lateral = ttk.Frame(self.danger,bootstyle="primary")
        self.danger_all.grid(row=0, column=0, sticky='nsew')
        self.danger.pack(side='left', fill='both', expand=True)
        self.success_all.grid(row=0, column=1, sticky='nsew')
        self.success.pack(side='left', fill='both', expand=True)
        self.btAdd = ttk.Button(self.success,command=self.add_pedidoNf,text='Adicionar',bootstyle=("info"))

        self.btGerar = ttk.Button(self.success,command=self.gerar_arquivo,text='Gerar',bootstyle=("info"))

        self.tree_pedidos = ttk.Treeview(self.danger, columns=("razao","fantasia", "nf","pedido","chave","valor","cnpj"), show='headings')
        danger_columns = [
            ("razao","Razão",10),
            ("fantasia","Fantasia",10),
            ( "nf","NF",10),
            ("pedido","Pedido",10),
            ("chave","Chave",10),
            ("valor","Valor",10),
            ("cnpj","CNPJ",10)
        ]

        for col in danger_columns:
            self.tree_pedidos.column(col[0], anchor="center", width=col[2])
            self.tree_pedidos.heading(col[0],text=col[1])

        self.tree_adicionados = ttk.Treeview(self.success, columns=("pedido","nf","valor","cnpj"), show='headings')
        success_columns = [
            ("pedido","Pedido",10),
            ( "nf","NF",10),
            ("valor","Valor",10),
            ("cnpj","CNPJ",10)
        ]
        for col in success_columns:
            self.tree_adicionados.column(col[0], anchor="center", width=col[2])
            self.tree_adicionados.heading(col[0],text=col[1])

        self.current_width = 0
        self.target_width = 100
        self.increment = 5



        self.img_logoColiseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_logoColiseu = self.img_logoColiseu.subsample(2,2)

        self.lb_logoColiseu = ttk.Label(self.frame_cabecario,
                                        image = self.img_logoColiseu,
                                        bootstyle=("primary", 'inverse'))

        self.lb_requisicoes = ttk.Label(self.frame_cabecario,
                                        text ="Gerar Arquivos",
                                        bootstyle=("primary", 'inverse'),
                                        font=("Arial",24,"bold"))

        

        self.bt_navbar = ttk.Button(self.frame_cabecario,command=self.menubar_expandir,width=10,text='Opções',bootstyle=("info"))

        self.bt_navbar2 = ttk.Button(self.frame_lateral,command=self.home_screen,width=10,text='Importar',bootstyle=("info"))
        self.bt_navbar3 = ttk.Button(self.frame_lateral,command=self.pedidos_screen,width=10,text='Gerar',bootstyle=("info"))
        self.bt_navbar7 = ttk.Button(self.frame_lateral,command=self.login_screen,width=10,text='Logoff',bootstyle=("info"))

    def pedidos_configure_layout(self):
        self.frame_cabecario.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.frame_principal.grid(row=1, column=1, sticky="nsew")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight= 1)

        self.bt_navbar.grid(row=0,column=0)



        self.frame_lateral.pack(side=ttk.LEFT, fill=ttk.BOTH)
        self.tree_pedidos.pack(fill="both", expand=True,pady=0,padx=0)
        self.btAdd.pack(fill="both",pady=5,padx=2)
        self.tree_adicionados.pack(fill="both", expand=True,pady=0,padx=2)
        self.btGerar.pack(fill="both",pady=5,padx=2)
        self.lb_requisicoes.grid(row=0,column=1)
        self.lb_logoColiseu.grid(row=0,column=2)

    def home_screen(self):
        self.home_create_widgets()
        self.tree_opcoes_update()
        self.home_configure_layout()

    def home_create_widgets(self):
        self.geometry("1280x720")
        self.resizable(width=True, height=True)
        self.frame_cabecario = ttk.Frame(self, height= 100, bootstyle="primary")
        self.frame_cabecario.columnconfigure(0, weight=1)
        self.frame_cabecario.columnconfigure(1, weight=8)
        self.frame_cabecario.columnconfigure(2, weight=2)
        self.frame_cabecario.columnconfigure(3, weight=1)
        self.frame_cabecario.rowconfigure(0, weight=1)
        
        self.frame_principal = ttk.Frame(self) #este frame é utilizado apenas para receber organizar outros 2
        self.frame_principal.rowconfigure(0, weight=4)
        self.frame_principal.rowconfigure(1, weight=2)
        self.frame_principal.rowconfigure(2, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        
        self.current_width = 0
        self.target_width = 100
        self.increment = 5

        self.frame_tree_opcoes = ttk.Frame(self.frame_principal)
        self.frame_tree_opcoes.grid_rowconfigure(0, weight=1)
        self.frame_tree_opcoes.grid_columnconfigure(0, weight=1)

        self.frame_treeScroll_opcoes = ttk.Frame(self.frame_tree_opcoes,bootstyle="primary")
        self.frame_lateral = ttk.Frame(self.frame_treeScroll_opcoes,bootstyle="primary")

        self.frame_tree_vizu = ttk.Frame(self.frame_principal)
        self.frame_tree_vizu.grid_rowconfigure(0, weight=1)
        self.frame_tree_vizu.grid_columnconfigure(0, weight=1)

        self.frame_treeScroll_vizu = ttk.Frame(self.frame_tree_vizu,bootstyle="primary")

        self.img_logoColiseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_logoColiseu = self.img_logoColiseu.subsample(2,2)

        self.lb_logoColiseu = ttk.Label(self.frame_cabecario,
                                        image = self.img_logoColiseu,
                                        bootstyle=("primary", 'inverse'))

        self.lb_requisicoes = ttk.Label(self.frame_cabecario,
                                        text ="Importar Requisições",
                                        bootstyle=("primary", 'inverse'),
                                        font=("Arial",24,"bold"))

        self.btEnvia = ttk.Button(self.frame_tree_opcoes,command=self.importar,text='Importar',bootstyle=("primary"))

        self.bt_navbar = ttk.Button(self.frame_cabecario,command=self.menubar_expandir,width=10,text='Opções',bootstyle=("info"))

        self.bt_navbar2 = ttk.Button(self.frame_lateral,command=self.home_screen,width=10,text='Importar',bootstyle=("info"))
        self.bt_navbar3 = ttk.Button(self.frame_lateral,command=self.pedidos_screen,width=10,text='Gerar',bootstyle=("info"))
        self.bt_navbar7 = ttk.Button(self.frame_lateral,command=self.login_screen,width=10,text='Logoff',bootstyle=("info"))

        self.btVizu = ttk.Button(self.frame_tree_opcoes,command=self.visualiza,text='Carregar Visualização',bootstyle=("primary"))

        self.tree_opcoes = ttk.Treeview(self.frame_treeScroll_opcoes, columns=("Message Id","Size", "Data","Hora"), show='headings')
        self.tree_opcoes.column("Message Id", anchor="center")
        self.tree_opcoes.column("Size", anchor="center")
        self.tree_opcoes.column("Data", anchor="center")
        self.tree_opcoes.column("Hora", anchor="center")
        self.tree_opcoes.heading("Message Id", text="Message Id")
        self.tree_opcoes.heading("Size", text="Size")
        self.tree_opcoes.heading("Data", text="Data")
        self.tree_opcoes.heading("Hora", text="Hora")
        self.scrollY_opcoes = ttk.Scrollbar(self.frame_treeScroll_opcoes, orient="vertical", command=self.tree_opcoes.yview)
        self.tree_opcoes.configure(yscrollcommand=self.scrollY_opcoes.set)
        self.tree_opcoes.tag_configure("verde", background="#A7C957")     
        
        columns = [
            ("codCliente", "Código", 1),
            ("nome", "Nome", 200),
            ("nome_fantasia", "Nome Fantasia", 100),
            ("cidade", "Cidade", 100),
            ("uf", "UF", 1),
            ("produto", "Produto", 200),
            ("referencia", "Código de Fab.", 1),
            ("quantidade", "Unid.", 1)
        ]

        self.tree_vizu = ttk.Treeview(self.frame_treeScroll_vizu, columns=[col[0] for col in columns], show='headings')
        self.scrollY_vizu = ttk.Scrollbar(self.frame_treeScroll_vizu, orient="vertical", command=self.tree_vizu.yview)
        self.tree_vizu.configure(yscrollcommand=self.scrollY_vizu.set)

        for col in columns:
            self.tree_vizu.column(col[0], anchor="center", width=col[2])
            self.tree_vizu.heading(col[0], text=col[1])
        
    def home_configure_layout(self):
        self.frame_cabecario.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.frame_principal.grid(row=1, column=1, sticky="nsew")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.bt_navbar.grid(row=0,column=0)

        self.frame_tree_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        self.frame_treeScroll_opcoes.grid(row=0, column=0, pady=5, sticky='nsew')
        self.frame_lateral.pack(side=ttk.LEFT, fill=ttk.BOTH)
        self.frame_tree_vizu.grid(row=2, column=0, sticky='nsew')
        self.frame_treeScroll_vizu.grid(row=0, column=0, pady=5, sticky='nsew')
        self.scrollY_opcoes.pack(side="right", fill="y")
        self.scrollY_vizu.pack(side="right", fill="y")
        self.tree_opcoes.pack(fill="both", expand=True,pady=0,padx=0)
        self.tree_vizu.pack(fill="both", expand=True,pady=0,padx=0)
        self.lb_requisicoes.grid(row=0,column=1)
        self.lb_logoColiseu.grid(row=0,column=2)
    
    '''@@@@@@@@@@@@@@@@@@@@@@@@@@@'''

    '''@@ Telas Widgets Funções @@'''    
    
    def menubar_expandir(self):
        if self.current_width < self.target_width:
            self.current_width += self.increment
            self.frame_lateral.config(width=self.current_width)
            self.after(10, self.menubar_expandir)
        else:
            self.bt_navbar2.grid(row=0, column=0,padx=2,pady=5)
            self.bt_navbar3.grid(row=1, column=0,padx=2,pady=5)
            self.bt_navbar7.grid(row=5, column=0,padx=2,pady=50)
            self.menuBar_open = True
    
    def preencher_usuario(self,event=None):
        # Função para preencher o campo "Usuário" com base no ID digitado
        id_digitado = self.id_entry.get()

        # Verificar se o ID está presente no dicionário
        if id_digitado in self.usuarios:
            self.usuario_entry.configure(state='normal')  # Habilitar o campo "Usuário" para escrita
            self.usuario_entry.delete(0, ttk.END)  # Limpar o campo "Usuário"
            self.usuario_entry.insert(0, self.usuarios[id_digitado])  # Preencher com o valor correspondente
            self.usuario_entry.configure(state='readonly')  # Bloquear o campo "Usuário" para escrita novamente
            self.senha.focus()  # Mover o foco para o campo "Senha"

    def fazer_login(self):
        senha_digitada = self.senha.get()
        if senha_digitada == "62728292":
            for widget in self.winfo_children():
                widget.destroy()
            self.home_screen()
        
        else:
            messagebox.showerror("Login", "Senha incorreta!")
    
    def verificar_tecla(self,event):
        if event.keycode == 13:
            self.fazer_login()

    def item_clicked(self,event):
        self.tree_vizu.delete(*self.tree_vizu.get_children())

        if self.btEnvia_created:
            self.btVizu.destroy()

        if self.btVizu_created:
            self.btVizu.destroy()
            self.btVizu = ttk.Button(self.frame_tree_opcoes,command=self.visualiza,text='Carregar Visualização',bootstyle=("info"))
            self.btVizu.grid(row=2, column=0, padx=2, pady=2, sticky='ew')

        else:
            self.btVizu = ttk.Button(self.frame_tree_opcoes,command=self.visualiza,text='Carregar Visualização',bootstyle=("info"))
            self.btVizu.grid(row=2, column=0, padx=2, pady=2, sticky='ew')
            self.btVizu_created = True

    '''@@@@@@@@@@@@@@@@@@@@@@@@@@@''' 



class Main_aplication():
    def __init__(self):
        self.Home = Home()
        self.Home.mainloop()

if __name__ == "__main__":
    Aplication = Main_aplication()
 