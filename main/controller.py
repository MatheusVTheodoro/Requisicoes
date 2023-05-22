import tkinter as tk
from view import ViewApp
from model import ModelApp



class ControllerApp:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.options = self.get_options()
        self.tree_opcoes = view.retorna_tree_op()
                 
    def get_options(self):
        return self.model.data
    
    def tabela_opcoes_data(self):
        for X in range (0,len(self.options['Data'])):
            self.tree_opcoes.insert("", tk.END,values=(self.options['MessageID'][X],self.options['Size'][X],self.options['Data'][X],self.options['Hora'][X],"Confirmado"))

       
if __name__ == "__main__":
    model = ModelApp()
    root = tk.Tk()
    controller = ControllerApp(model, ViewApp(root, None))
    view = ViewApp(root, controller)
    controller.view = view
    view.interface()
    root.mainloop()