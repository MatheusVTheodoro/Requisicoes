import tkinter as tk
from tkinter import PhotoImage
#from tkinter import ttk
import ttkbootstrap as ttk
import requests as req
import re
import firebirdsql
from tkinter import messagebox
from data import Data

class Home(ttk.Window):
    def __init__(self):
        super().__init__()
        self.style.theme_use("flatly")
        self.title("Requisições")
        self.pedidos_screen()
        self.menuBar_open = False     
      
    def pedidos_screen(self):
        self.pedidos_create_widgets()
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
        self.btAdd = ttk.Button(self.success,command=None,text='Adicionar',bootstyle=("info"))

        self.btGerar = ttk.Button(self.success,command=None,text='Gerar',bootstyle=("info"))

        self.tree_pedidos = ttk.Treeview(self.danger, columns=("razao","fantasia", "nf","pedido","emissao","chave","valor","uf","cidade","cnpj"), show='headings')
        danger_columns = [
            ("razao","Razão",10),
            ("fantasia","Fantasia",10),
            ( "nf","NF",10),
            ("pedido","Pedido",10),
            ("emissao","Emissão",10),
            ("chave","Chave",10),
            ("valor","Valor",10),
            ("uf","UF",10),
            ("cidade","Cidade",10),
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
                                        text ="Requisições",
                                        bootstyle=("primary", 'inverse'),
                                        font=("Arial",24,"bold"))

        

        self.bt_navbar = ttk.Button(self.frame_cabecario,command=self.menubar_expandir,width=10,text='Opções',bootstyle=("info"))

        self.bt_navbar2 = ttk.Button(self.frame_lateral,command=self.pedidos_screen,width=10,text='pedidos',bootstyle=("info"))
        self.bt_navbar3 = ttk.Button(self.frame_lateral,command=None,width=10,text='Pedidos',bootstyle=("info"))
        self.bt_navbar4 = ttk.Button(self.frame_lateral,command=None,width=10,text='>>>',bootstyle=("primary"))
        self.bt_navbar5 = ttk.Button(self.frame_lateral,command=None,width=10,text='>>>',bootstyle=("primary"))
        self.bt_navbar6 = ttk.Button(self.frame_lateral,command=None,width=10,text='>>>',bootstyle=("primary"))
        self.bt_navbar7 = ttk.Button(self.frame_lateral,command=None,width=10,text='Logoff',bootstyle=("info"))

        
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

    def menubar_expandir(self): 
        if self.current_width < self.target_width:
            self.current_width += self.increment
            self.frame_lateral.config(width=self.current_width)
            self.after(10, self.menubar_expandir)
        else:
            self.bt_navbar2.grid(row=0, column=0)
            self.bt_navbar3.grid(row=1, column=0)
            self.bt_navbar4.grid(row=2, column=0)
            self.bt_navbar5.grid(row=3, column=0)
            self.bt_navbar6.grid(row=4, column=0)
            self.bt_navbar7.grid(row=5, column=0)
            self.menuBar_open = True

class Main_aplication():
    def __init__(self):
        self.Home = Home()
        self.Home.mainloop()

if __name__ == "__main__":
    Aplication = Main_aplication()
 