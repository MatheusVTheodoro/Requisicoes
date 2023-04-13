import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from commands import * 


root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file   
)
open_button.pack()

read_button = ttk.Button(
    root,
    text='ler arquivo',
    command=read_mbx   
    )
    

read_button.pack()

root.mainloop()

