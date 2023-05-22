import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage


class ViewApp:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
    def retorna_tree_op(self):
        return self.tree_opcoes    
        
    def load_options(self):
        opcoes = self.controller.get_options()
        print(opcoes)




    def interface(self):
        #Cores da Home da interface
        cor = {"verde" : "#A7C957","azul" : "#1D3557","azulClaro" : "#98c1d9","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
        '''
        ---IMAGENS---
        '''
        #Logo Coliseu
        img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        img_coliseu = img_coliseu.subsample(2, 2)
        '''
        ---FRAMES---
        '''
        #frame com o cabeçario
        frame_cabecario = tk.Frame(self.root,height=100,bg=cor["azul"],padx=10)
        frame_cabecario.columnconfigure(0, weight=1)
        frame_cabecario.columnconfigure(1, weight=4)
        frame_cabecario.columnconfigure(2, weight=1)
        frame_cabecario.rowconfigure(0, weight=1)
        #frame com as trees vizu e opcoes
        frame_trees = tk.Frame(self.root,bg=cor["vermelho"])
        frame_trees.rowconfigure(0, weight=4)
        frame_trees.rowconfigure(1, weight=2)
        frame_trees.rowconfigure(2, weight=1)
        frame_trees.columnconfigure(0, weight=1)
        #frame com a tree de opções (a de cima)
        frame_opcoes = tk.Frame(frame_trees,bg=cor["cinza"])
        #frame utilizado para posicionar a tree de opções juntamente com seu scroll
        frame_tree_opcoes = tk.Frame(frame_opcoes,bg=cor["azul"])
        #frame com a tree de visualizar (a de baixo)
        frame_vizu = tk.Frame(frame_trees,bg=cor["cinza"])
        #frame utilizado para posicionar a tree de visualizar juntamente com seu scroll
        frame_tree_vizu = tk.Frame(frame_vizu,bg=cor["azul"])
        #configurações da tree de opções
        '''
        ---LABELS---
        '''
        lb_Logo = ttk.Label(frame_cabecario, image=img_coliseu,background=cor["azul"])
        lb_requisicoes = ttk.Label(frame_cabecario, text="Requisições",background=cor["azul"],foreground=cor["branco"],font=("Arial", 24,"bold"))
  
        
        '''
        ---TREEVIEWS---
        '''
        columns_tree_opcoes = ("Message Id", "Size", "Data","Hora")
        self.tree_opcoes = ttk.Treeview(frame_tree_opcoes, columns=columns_tree_opcoes, show='headings')
        self.tree_opcoes.column("Message Id", anchor="center")
        self.tree_opcoes.column("Size", anchor="center")
        self.tree_opcoes.column("Data", anchor="center")
        self.tree_opcoes.column("Hora", anchor="center")
        self.tree_opcoes.heading("Message Id", text="Message Id")
        self.tree_opcoes.heading("Size", text="Size")
        self.tree_opcoes.heading("Data", text="Data")
        self.tree_opcoes.heading("Hora", text="Hora")


        #configurações da tree de vizualisar
        tree_vizu = ttk.Treeview(frame_tree_vizu, columns=("codCliente","cliente","produto","referencia","quantidade"), show='headings')
        tree_vizu.column("codCliente", anchor="center")
        tree_vizu.column("cliente", anchor="center")
        tree_vizu.column("produto", anchor="center")
        tree_vizu.column("referencia", anchor="center")
        tree_vizu.column("quantidade", anchor="center")
        tree_vizu.heading("codCliente", text="Cód.Cliente")
        tree_vizu.heading("cliente", text="Cliente")
        tree_vizu.heading("produto", text="Produto")
        tree_vizu.heading("referencia", text="Ref.")
        tree_vizu.heading("quantidade", text="Uni.")

        '''
        ---TREEVIEWS_COOLOR_CONFIG_E_INSERÇÂO---
        ---***MUDAR_PARA_FUNÇÂO_SEPARADA***---
        ''' 
        

        '''
        ---BUTTONS---
        '''
        btEnvia = tk.Button(frame_opcoes,text='Importar',bg=cor["azul"], fg=cor["branco"])
        pbVizu = ttk.Progressbar(frame_opcoes, mode='determinate')
        btVizu = tk.Button(frame_opcoes,command=None,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])

        '''
        #################################################################
        -----------------------------------------------------------------
        ----------------POSICIONANDO_WIDGETS-----------------------------
        -----------------------------------------------------------------
        #################################################################
        '''
        lb_Logo.grid(row=0,column=2)
        lb_requisicoes.grid(row=0,column=0)
        frame_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        frame_opcoes.grid_rowconfigure(0, weight=1)
        frame_opcoes.grid_columnconfigure(0, weight=1)
        frame_tree_opcoes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        frame_vizu.grid(row=2, column=0, sticky='nsew')
        frame_vizu.grid_rowconfigure(0, weight=1)
        frame_vizu.grid_columnconfigure(0, weight=1)
        frame_tree_vizu.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        frame_cabecario.pack(side="top", fill="x")
        frame_trees.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_opcoes.pack(fill="both", expand=True,pady=5,padx=2)
        tree_vizu.pack(fill="both", expand=True,pady=5,padx=2)
        

