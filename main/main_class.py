import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cor = {"verde" : "#A7C957","azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
        self.geometry("800x600")
        self.config(bg=self.cor["branco"])
        self.state('zoomed')
        self.title("Requisições")
        self.iconbitmap(default='')

        self.banco = self.set_banco()
        self.button_created = True
        self.button_created2 = False
        self.pbVizu_created = False

    def set_banco(self):
        with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
            banco= arquivo.read()
        return banco

app = Application()
app.mainloop()