import tkinter as tk
from tkinter import ttk

class AppView:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()

        self.input_entry = tk.Entry(self.root)
        self.input_entry.pack()

        self.add_button = tk.Button(self.root, text="Adicionar", command=self.adicionar_dado)
        self.add_button.pack()

        self.treeview = ttk.Treeview(self.root)
        self.treeview.pack()

        self.atualizar_treeview()

    def atualizar_treeview(self):
        self.treeview.delete(*self.treeview.get_children())  # Limpa a TreeView

        dados = self.controller.obter_dados()
        for dado in dados:
            self.treeview.insert("", "end", values=dado)

    def adicionar_dado(self):
        dado = self.input_entry.get()
        if dado:
            self.controller.adicionar_dado(dado)
            self.input_entry.delete(0, tk.END)
            self.atualizar_treeview()

    def executar(self):
        self.root.mainloop()


class DadosModel:
    def __init__(self):
        self.dados = []  # Dados que serão exibidos na TreeView

    def obter_dados(self):
        # Retorna os dados a serem exibidos
        return self.dados

    def adicionar_dado(self, dado):
        # Adiciona um dado à lista
        self.dados.append(dado)


class AppController:
    def __init__(self):
        self.model = DadosModel()
        self.view = AppView(self)

    def obter_dados(self):
        return self.model.obter_dados()

    def adicionar_dado(self, dado):
        self.model.adicionar_dado(dado)
        self.view.atualizar_treeview()

    def executar(self):
        self.view.executar()


# Uso do controlador
if __name__ == "__main__":
    controller = AppController()
    controller.executar()