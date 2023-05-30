import tkinter as tk
from tkinter import simpledialog

class Autenticacao:
    def __init__(self, senha_correta):
        self.__senha_correta = senha_correta

    def verificar_senha(self, senha):
        return senha == self.__senha_correta


class Cofre:
    def __init__(self, senha_correta):
        self.__autenticacao = Autenticacao(senha_correta)
        self.__conteudo = None

    def abrir(self, senha):
        if self.__autenticacao.verificar_senha(senha):
            return True
        else:
            return False

    def guardar_conteudo(self, senha, conteudo):
        if self.abrir(senha):
            self.__conteudo = conteudo

    def pegar_conteudo(self, senha):
        if self.abrir(senha):
            return self.__conteudo
        else:
            return None

    def fechar(self):
        self.__conteudo = None


class InterfaceCofre:
    def __init__(self):
        self.__cofre = None
        self.__root = tk.Tk()
        self.__root.title("Cofre")

        self.__label_senha = tk.Label(self.__root, text="Senha:")
        self.__label_senha.pack()

        self.__entry_senha = tk.Entry(self.__root, show="*")
        self.__entry_senha.pack()

        self.__button_abrir = tk.Button(self.__root, text="Abrir Cofre", command=self.abrir_cofre)
        self.__button_abrir.pack()

        self.__button_guardar = tk.Button(self.__root, text="Guardar Conteúdo", command=self.guardar_conteudo)
        self.__button_guardar.pack()

        self.__button_pegar = tk.Button(self.__root, text="Pegar Conteúdo", command=self.pegar_conteudo)
        self.__button_pegar.pack()

        self.__button_fechar = tk.Button(self.__root, text="Fechar Cofre", command=self.fechar_cofre)
        self.__button_fechar.pack()

    def abrir_cofre(self):
        senha = self.__entry_senha.get()
        if self.__cofre.abrir(senha):
            tk.messagebox.showinfo("Cofre", "Cofre aberto.")
        else:
            tk.messagebox.showwarning("Cofre", "Senha incorreta. Cofre permanece fechado.")

    def guardar_conteudo(self):
        senha = self.__entry_senha.get()
        conteudo = tk.simpledialog.askstring("Cofre", "Digite o conteúdo a ser guardado:")
        self.__cofre.guardar_conteudo(senha, conteudo)
        tk.messagebox.showinfo("Cofre", "Conteúdo guardado com sucesso.")

    def pegar_conteudo(self):
        senha = self.__entry_senha.get()
        conteudo = self.__cofre.pegar_conteudo(senha)
        if conteudo:
            tk.messagebox.showinfo("Cofre", f"Conteúdo: {conteudo}")
        else:
            tk.messagebox.showwarning("Cofre", "Senha incorreta ou o cofre está vazio.")

    def fechar_cofre(self):
        self.__cofre.fechar()
        tk.messagebox.showinfo("Cofre", "Cofre fechado.")

    def iniciar(self):
        senha_correta = tk.simpledialog.askstring("Cofre", "Digite a senha correta para o cofre:")
        self.__cofre = Cofre(senha_correta)
        self.__root.mainloop()


# Exemplo de uso:

interface = InterfaceCofre()
interface.iniciar()
       
