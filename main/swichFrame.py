import tkinter as tk
from tkinter import ttk

class Tela2(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pack()
        self.label = ttk.Label(self, text="Tela 2")
        self.label.pack()

class Home(ttk.Frame):
    def __init__(self, parent, show_tela2):
        super().__init__(parent)
        
        self.pack()
        self.label = ttk.Label(self, text="Tela Home")
        self.label.pack()
        
        self.button = ttk.Button(self, text="Acessar Tela 2", command=show_tela2)
        self.button.pack()

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        self.title("Tela Principal")
        
        self.home = Home(self, self.show_tela2)
        self.home.pack()
    
    def show_tela2(self):
        self.home.pack_forget()  # Esconde a tela Home
        self.tela2 = Tela2(self)
        self.tela2.pack()

app = TelaPrincipal()
app.mainloop()