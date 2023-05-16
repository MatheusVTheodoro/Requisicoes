import tkinter as tk
import tkinter.ttk as ttk
from model import Model
from view import View
from controller import Controller

if __name__ == '__main__':
    root = tk.Tk()
    model = Model()
    controller = Controller(model)
    view = View(root, controller)
    controller.update_country_tv()
    root.mainloop()
