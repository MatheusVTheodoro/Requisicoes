import tkinter as tk

root = tk.Tk()

# Frame principal
frame_principal = tk.Frame(root)
frame_principal.grid(sticky='nsew')

# Frame 1
frame1 = tk.Frame(frame_principal, bg='red')
frame1.grid(row=0, column=0, sticky='nsew')

# Frame 2
frame2 = tk.Frame(frame_principal, bg='blue')
frame2.grid(row=1, column=0, sticky='nsew')

# Define o tamanho do Frame principal
frame_principal.grid_rowconfigure(0, weight=1)
frame_principal.grid_columnconfigure(0, weight=1)

root.mainloop()
