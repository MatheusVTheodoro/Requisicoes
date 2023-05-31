import tkinter as tk
from tkinter import PhotoImage
#from tkinter import ttk
import ttkbootstrap as ttk

cor = {
    "verde": "#A7C957",
    "azul": "#1D3557",
    "azulClaro": "#457B9D",
    "branco": "#ced4da",
    "vermelho": "#E63946",
    "cinza": "#8D99AE"
}

class Home(ttk.Window):
    def __init__(self):
        super().__init__()
        self.style.theme_use("newtheme")
        self.title("Requisições")
        self.geometry("800x600")
        self.config(bg=cor["branco"])
        self.resizable(width=True, height=True)
        self.state('zoomed')
        self.create_widgets()
        self.configure_layout()
        
    
    def create_widgets(self):
        self.frame_cabecario = ttk.Frame(self, height= 100, bootstyle="primary")
        self.frame_cabecario.columnconfigure(0, weight=1)
        self.frame_cabecario.columnconfigure(1, weight=4)
        self.frame_cabecario.columnconfigure(2, weight=1)
        self.frame_cabecario.rowconfigure(0, weight=1)
        

        self.frame_principal = tk.Frame(self,bg=cor["vermelho"])
        self.frame_principal.rowconfigure(0, weight=4)
        self.frame_principal.rowconfigure(1, weight=2)
        self.frame_principal.rowconfigure(2, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        self.frame_tree_opcoes = tk.Frame(self.frame_principal,bg=cor["cinza"])
        self.frame_tree_opcoes.grid_rowconfigure(0, weight=1)
        self.frame_tree_opcoes.grid_columnconfigure(0, weight=1)

        self.frame_treeScroll_opcoes = tk.Frame(self.frame_tree_opcoes,bg=cor["azul"])
        
        self.frame_tree_vizu = tk.Frame(self.frame_principal,bg=cor["cinza"])
        self.frame_tree_vizu.grid_rowconfigure(0, weight=1)
        self.frame_tree_vizu.grid_columnconfigure(0, weight=1)

        self.frame_treeScroll_vizu = tk.Frame(self.frame_tree_vizu,bg=cor["azul"])

        self.img_logoColiseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
        self.img_logoColiseu = self.img_logoColiseu.subsample(2,2)

        self.lb_logoColiseu = ttk.Label(self.frame_cabecario,
                                         image = self.img_logoColiseu,
                                           background= cor["azul"])

        self.lb_requisicoes = ttk.Label(self.frame_cabecario,
                                        text ="Requisições",
                                        background=cor["azul"],
                                        foreground=cor["branco"],
                                        font=("Arial",24,"bold"))

        self.btEnvia = tk.Button(self.frame_principal,text='Importar',bg=cor["azul"], fg=cor["branco"])

        self.pbVizu = ttk.Progressbar(self.frame_principal, mode='determinate')

        self.btVizu = tk.Button(self.frame_principal,command=None,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])

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
        
    def configure_layout(self):
        self.frame_cabecario.pack(side="top", fill="x")
        self.frame_principal.pack(fill="both", expand=True)
        self.frame_tree_opcoes.grid(row=0, column=0, sticky='nsew', rowspan=2)
        self.frame_treeScroll_opcoes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frame_tree_vizu.grid(row=2, column=0, sticky='nsew')
        self.frame_treeScroll_vizu.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.scrollY_opcoes.pack(side="right", fill="y")
        self.scrollY_vizu.pack(side="right", fill="y")
        self.tree_opcoes.pack(fill="both", expand=True,pady=5,padx=2)
        self.tree_vizu.pack(fill="both", expand=True,pady=5,padx=2)
        self.lb_requisicoes.grid(row=0,column=0)
        self.lb_logoColiseu.grid(row=0,column=2)



if __name__ == "__main__":
    janela_home = Home()
    janela_home.mainloop()