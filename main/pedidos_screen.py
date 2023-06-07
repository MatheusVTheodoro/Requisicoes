import tkinter as tk
from tkinter import PhotoImage
#from tkinter import ttk
import ttkbootstrap as ttk
import requests as req
import re
import firebirdsql
from tkinter import messagebox

class ScreenGerar(ttk.Window):
    def __init__(self):
        super().__init__()
        self.style.theme_use("flatly")
        self.title("Requisições")
        #self.home_create_widgets()
        #self.tree_opcoes_update()
        #self.home_configure_layout()
        self.gerar_screen()
        self.btVizu_created = False
        self.btEnvia_created = False
        self.importavel = True
        self.menuBar_open = False     
      
    def gerar_screen(self):
        self.home_create_widgets()
        self.home_configure_layout()

    def home_create_widgets(self):
        self.geometry("1280x720")
        self.resizable(width=True, height=True)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.frame_cabecario = ttk.Frame(self, height= 100, bootstyle="primary")
        self.frame_cabecario.columnconfigure(0, weight=1)
        self.frame_cabecario.columnconfigure(1, weight=8)
        self.frame_cabecario.columnconfigure(2, weight=2)
        self.frame_cabecario.columnconfigure(3, weight=1)
        self.frame_cabecario.rowconfigure(0, weight=1)
        
        self.frame_principal = ttk.Frame(self)
        self.frame_principal.rowconfigure(0, weight=4)
        self.frame_principal.rowconfigure(1, weight=2)
        self.frame_principal.rowconfigure(2, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        
        self.current_width = 0
        self.target_width = 100
        self.increment = 5

        self.frame_tree_opcoes = ttk.Frame(self.frame_principal,bootstyle="light")
        self.frame_tree_opcoes.grid_rowconfigure(0, weight=1)
        self.frame_tree_opcoes.grid_columnconfigure(0, weight=1)

        self.frame_treeScroll_opcoes = ttk.Frame(self.frame_tree_opcoes,bootstyle="primary")
        self.frame_lateral = ttk.Frame(self.frame_treeScroll_opcoes,bootstyle="primary")

        self.frame_tree_vizu = ttk.Frame(self.frame_principal,bootstyle="light")
        self.frame_tree_vizu.grid_rowconfigure(0, weight=1)
        self.frame_tree_vizu.grid_columnconfigure(0, weight=1)

        self.frame_treeScroll_vizu = ttk.Frame(self.frame_tree_vizu,bootstyle="primary")

        self.img_logoColiseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_logoColiseu = self.img_logoColiseu.subsample(2,2)

        self.lb_logoColiseu = ttk.Label(self.frame_cabecario,
                                        image = self.img_logoColiseu,
                                        bootstyle=("primary", 'inverse'))

        self.lb_requisicoes = ttk.Label(self.frame_cabecario,
                                        text ="Requisições",
                                        bootstyle=("primary", 'inverse'),
                                        font=("Arial",24,"bold"))

        self.btEnvia = ttk.Button(self.frame_tree_opcoes,command=None,text='Importar',bootstyle=("primary"))

        self.bt_navbar = ttk.Button(self.frame_cabecario,command=self.menubar_expandir,width=10,text='Opções',bootstyle=("info"))

        self.bt_navbar2 = ttk.Button(self.frame_lateral,command=self.gerar_screen,width=10,text='Home',bootstyle=("info"))
        self.bt_navbar3 = ttk.Button(self.frame_lateral,command=None,width=10,text='Pedidos',bootstyle=("info"))
        self.bt_navbar4 = ttk.Button(self.frame_lateral,command=None,width=10,text='>>>',bootstyle=("primary"))
        self.bt_navbar5 = ttk.Button(self.frame_lateral,command=None,width=10,text='>>>',bootstyle=("primary"))
        self.bt_navbar6 = ttk.Button(self.frame_lateral,command=None,width=10,text='>>>',bootstyle=("primary"))
        self.bt_navbar7 = ttk.Button(self.frame_lateral,command=None,width=10,text='Logoff',bootstyle=("info"))

        self.btVizu = ttk.Button(self.frame_tree_opcoes,command=None,text='Carregar Visualização',bootstyle=("primary"))

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
        self.bt_navbar.grid(row=0,column=0)
        self.frame_tree_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        self.frame_treeScroll_opcoes.grid(row=0, column=0, pady=10, sticky='nsew')
        self.frame_lateral.pack(side=ttk.LEFT, fill=ttk.BOTH)
        self.frame_tree_vizu.grid(row=0, column=1, sticky='nsew')
        self.frame_treeScroll_vizu.grid(row=0, column=0, pady=10, sticky='nsew')
        self.scrollY_opcoes.pack(side="right", fill="y")
        self.scrollY_vizu.pack(side="right", fill="y")
        self.tree_opcoes.pack(fill="both", expand=True,pady=10,padx=0)
        self.tree_vizu.pack(fill="both", expand=True,pady=10,padx=0)
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

    def item_clicked(self,event):
        self.tree_vizu.delete(*self.tree_vizu.get_children())

        if self.btEnvia_created:
            self.btVizu.destroy()

        if self.btVizu_created:
            self.btVizu.destroy()
            self.btVizu = ttk.Button(self.frame_tree_opcoes,command=self.visualiza,text='Carregar Visualização',bootstyle=("info"))
            self.btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        else:
            self.btVizu = ttk.Button(self.frame_tree_opcoes,command=self.visualiza,text='Carregar Visualização',bootstyle=("info"))
            self.btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
            self.btVizu_created = True
              
class Main_aplication():
    def __init__(self):
        self.Home = ScreenGerar()
        self.Home.mainloop()

if __name__ == "__main__":
    Aplication = Main_aplication()
