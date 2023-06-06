import tkinter as tk
from ttkbootstrap import ttk

class Tela2(ttk.Window):
    def __init__(self):
        super().__init__()
        
        self.geometry("300x200")
        self.title("Tela 2")
        
        self.label = ttk.Label(self, text="Tela 2")
        self.label.pack()

class Home(ttk.Window):
    def __init__(self):
        super().__init__()
        
        self.geometry("300x200")
        self.title("Tela Home")
        
        self.label = ttk.Label(self, text="Tela Home")
        self.label.pack()
        
        self.button = ttk.Button(self, text="Acessar Tela 2", command=self.show_tela2)
        self.button.pack()
    
    def show_tela2(self):
        self.destroy()  # Fecha a tela Home
        tela2 = Tela2()
        tela2.mainloop()

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        self.title("Tela Principal")
        
        self.home = Home()
        self.home.mainloop()

app = TelaPrincipal()
app.mainloop()
