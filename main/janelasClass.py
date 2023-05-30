import tkinter as tk

#tk.Tk = main         tk.toplevel = secundarias

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Janela Principal")

        self.btn_open_second_window = tk.Button(self, text="Abrir Segunda Janela", command=self.open_second_window)
        self.btn_open_second_window.pack(pady=10)

    def open_second_window(self):
        self.withdraw()  # Esconder a janela principal
        self.second_window = SecondWindow(self)

class SecondWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Segunda Janela")

        self.btn_return_to_main = tk.Button(self, text="Voltar para a Janela Principal", command=self.return_to_main)
        self.btn_return_to_main.pack(pady=10)

    def return_to_main(self):
        self.destroy()  # Fechar a janela atual
        self.main_window.deiconify()  # Exibir novamente a janela principal

class ThirdWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Terceira Janela")

        self.btn_return_to_main = tk.Button(self, text="Voltar para a Janela Principal", command=self.return_to_main)
        self.btn_return_to_main.pack(pady=10)

    def return_to_main(self):
        self.destroy()  # Fechar a janela atual
        self.main_window.deiconify()  # Exibir novamente a janela principal

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
