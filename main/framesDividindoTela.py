import tkinter as tk

# Cria a janela principal
janela = tk.Tk()

# Define o tamanho da janela
largura = janela.winfo_screenwidth()
altura = janela.winfo_screenheight()
janela.geometry(f"{largura}x{altura}")

# Cria o frame vermelho
frame_red = tk.Frame(janela, bg="red")
frame_red.pack(fill=tk.BOTH, expand=True)

# Cria o frame azul
frame_blue = tk.Frame(frame_red, bg="blue",width=100)
frame_blue.pack(side=tk.LEFT, fill=tk.BOTH)

# Cria o frame verde
frame_green = tk.Frame(janela, bg="green")
frame_green.pack(fill=tk.BOTH, expand=True)

# Exibe a janela
janela.mainloop()
