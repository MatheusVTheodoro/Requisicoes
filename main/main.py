import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

def main():

    #dicionario de cores do app
    cor = {
    "verde": "#A7C957",
    "azul": "#1D3557",
    "azulClaro": "#457B9D",
    "branco": "#F1FAEE",
    "vermelho": "#E63946",
    "cinza": "#8D99AE"
    }

    #main frame
    root = tk.Tk()
    root.geometry("800x600")
    root.config(bg=cor["branco"])
    root.state('zoomed')
    root.title("")
    root.iconbitmap(default='')

    #status inicial dos botões
    button_created = True
    button_created2 = False
    pbVizu_created = False

    #imagem logo da coliseu 
    img_coliseu =PhotoImage(file="C:/COLISEU/REQUISICOES/assets/COLISEUsFundo.png")
    img_coliseu = img_coliseu.subsample(2, 2)

    #frame superior onde fica o cabeçario com logo e titulo
    frame_cabecario = tk.Frame(root,height=100,bg=cor["azul"],padx=10)
    frame_cabecario.pack(side="top", fill="x")
    frame_cabecario.columnconfigure(0, weight=1)
    frame_cabecario.columnconfigure(1, weight=4)
    frame_cabecario.columnconfigure(2, weight=1)
    frame_cabecario.rowconfigure(0, weight=1)

    #label criado para posicionar a logo
    lb_Logo = ttk.Label(frame_cabecario, image=img_coliseu,background=cor["azul"])
    lb_Logo.grid(row=0,column=2)

    #titulo da aplicação no cabeçario
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

    #configurações da tabela de opcoes
    tabela_opcoes.tag_configure("branco", background=cor["branco"])
    tabela_opcoes.tag_configure("verde", background=cor["verde"])
    #tabela_opcoes.bind("<ButtonRelease-1>", item_clicked)
    scrollY_opcoes = ttk.Scrollbar(frame_tabela_opcoes, orient="vertical", command=tabela_opcoes.yview)
    scrollY_opcoes.pack(side="right", fill="y")
    tabela_opcoes.configure(yscrollcommand=scrollY_opcoes.set)
    tabela_opcoes.pack(fill="both", expand=True,pady=5,padx=2)



    btEnvia = tk.Button(frame_opcoes,text='Importar',bg=cor["azul"], fg=cor["branco"])

    pbVizu = ttk.Progressbar(frame_opcoes, mode='determinate')

    btVizu = tk.Button(frame_opcoes,command=None,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
    btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    root.mainloop()






























if __name__ == "__main__":
    main()