import tkinter as tk

# Cria a janela principal
app = tk.Tk()

# Define uma cor para usar como fundo do frame canvas
canvas_bg = '#F0F0F0'

# Cria o frame canvas
nav_lateral_canvas = tk.Canvas(app, bg=canvas_bg, width=300, height=300)

# Cria o frame que será adicionado ao canvas
nav_lateral_frame = tk.Frame(nav_lateral_canvas, bg=canvas_bg, width=300, height=3000)

# Adiciona o frame ao canvas
nav_lateral_canvas.create_window((0, 0), window=nav_lateral_frame, anchor='nw')

# Cria uma barra de rolagem vertical
scrollbar = tk.Scrollbar(app, orient=tk.VERTICAL, command=nav_lateral_canvas.yview)

# Conecta a barra de rolagem ao canvas
nav_lateral_canvas.configure(yscrollcommand=scrollbar.set)

# Define a posição do frame canvas e da barra de rolagem
nav_lateral_canvas.place(x=-300, y=0)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Adiciona widgets ao frame
for i in range(50):
    tk.Label(nav_lateral_frame, text=f'Label {i}').pack()

# Inicia o loop principal do Tkinter
app.mainloop()