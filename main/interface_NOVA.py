import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from commands import *
# cores da interface
cor = {"azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
#botão de opções (sidebar lateral)
bt_move = False
#carregando opções da treeview
options=opcoes()
#inicio do app
app = tk.Tk()
app.title("Coliseu Requisições")
app.config(bg=cor["branco"])
app.state('zoomed')
#frame_tree = tk.Frame(app, bg=cor["cinza"],width=1500,height=900,)
#frame_tree.place(x=0,y=300)


#tabela (tree view)
tree = ttk.Treeview(app,columns= ("Message Id", "Action","Type","Size","Created On"), show='headings')
tree.heading("Message Id", text="Message Id")
tree.heading("Action", text="Action")
tree.heading("Type", text="Type")
tree.heading("Size", text="Size")
tree.heading("Created On", text="Created On")
#inserção de dados na treeview
for option in options:
    tree.insert("", tk.END,values=(option,"Action","Type","Size","Created On"))
    

tree.grid(row=3, column=0, sticky='nsew')

def confirmaPedido():
    for widget in app.winfo_children():
        if widget.winfo_class() == 'Label':
            widget.destroy()
    selection = listbox.get(listbox.curselection())
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={selection}")
    label_text = trataPedescoTxt(linkView)
    for values in label_text:
        label = tk.Label(app, text=values, fg="black")
        label.pack()

btConfirm = tk.Button(app, text="Executar comando", command=confirmaPedido)
btConfirm.grid(row=4, column=0, sticky='nsew')

top_frame = tk.Frame(app, bg=cor['azul'])
top_frame.grid(row=0, column=0, sticky='nsew')

y=80

#opcao = ["JAVA","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#","PYTHON","C","C#"]
configs = ["BANCO DE DADOS","info2","info3","info4"]
for i in range(len(configs)):
    tk.Button(nav_lateral,text=configs[i],font="ExtraCondensed 15",bg=cor["azulClaro"]
              ,fg=cor["branco"],activebackground=cor["azul"],bd=0,command=None).place(x=25,y=y)
    y+=40

fechar_btn= tk.Button(nav_lateral, bg=cor["azul"],text="---\n---",fg=cor["branco"],
                      activebackground=cor["azul"],bd=0,command=Fecha)
fechar_btn.place(x=250,y=10)


app.mainloop()