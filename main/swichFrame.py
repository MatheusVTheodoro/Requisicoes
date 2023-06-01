import tkinter as tk

class Tela1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        self.button = tk.Button(self, text="Ir para a Tela 2", command=self.ir_para_tela2)
        self.button.pack()

    def ir_para_tela2(self):
        self.master.switch_frame(Tela2)

class Tela2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        self.button = tk.Button(self, text="Ir para a Tela 1", command=self.ir_para_tela1)
        self.button.pack()

    def ir_para_tela1(self):
        self.master.switch_frame(Tela1)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Exemplo de Redirecionamento entre Telas")
        self.geometry("300x200")

        self.current_frame = None
        self.switch_frame(Tela1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()