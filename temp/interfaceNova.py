from tkinter import *
from tkinter import ttk
bt_move = False
cor = {"azul" : "#1D3557","azulClaro" : "#457B9D","branco" : "#F1FAEE","vermelho" : "#E63946", "cinza" : "#8D99AE"}
root = Tk()
root.geometry('400x400')

mainPainel = PanedWindow(bg="red")
# Cria um frame acima do TreeView
top_frame1 = Frame(root, bg='blue', height=40)
top_frame1.grid(row=0, column=0, sticky='nsew')#sticky como 'nsew' para que eles sejam expandidos em todas as direções e ocupem todo o espaço disponível.

bt_abre = Button(top_frame1,text="---\n---",fg=cor["branco"],bg=cor["azul"],padx=20,bd=0,
                       activebackground=cor["azul"],command=None)
bt_abre.place(x=10,y=10)

nav_lateral= Frame(root,bg=cor["azulClaro"],height=3000)
nav_lateral.place(x= -300,y=0)
# Cria outro frame acima do TreeView
top_frame2 = Frame(root, bg='green', height=100)
top_frame2.grid(row=1, column=0, sticky='nsew')

# Cria o TreeView com duas colunas
treeview = tTreeview(root, columns=('Name', 'Age'))

# Define o cabeçalho das colunas
treeview.heading('#0', text='ID')
treeview.heading('Name', text='Name')
treeview.heading('Age', text='Age')

# Define a largura das colunas
treeview.column('#0', width=50)
treeview.column('Name', width=150)
treeview.column('Age', width=50)

# Adiciona alguns itens à árvore
treeview.insert('', '0', 'item1', text='1', values=('John', 25))
treeview.insert('', '1', 'item2', text='2', values=('Sarah', 32))
treeview.insert('', 'end', 'item3', text='3', values=('Bob', 18))

# Define um estilo para os itens da árvore
style = tStyle()
style.configure('Treeview', font=('Arial', 12))

# Define a cor de fundo para os itens pares
treeview.tag_configure('even', background='#e8e8e8')

# Adiciona tags aos itens pares
treeview.item('item2', tags=('even',))

# Adiciona o TreeView aos frames acima
treeview.grid(row=2, column=0, sticky='nsew')
#top_frame1.grid_propagate(False)
#top_frame2.grid_propagate(False)

# Cria um frame abaixo do TreeView
bottom_frame = Frame(root)
bottom_frame.grid(row=3, column=0, sticky='nsew')

# Adiciona um botão ao frame abaixo
button = tButton(bottom_frame, text='Click me!')
button.pack(side=LEFT, padx=5, pady=5)

# Define o espaçamento das linhas e colunas da grade
root.rowconfigure(0, weight=1, minsize=30)
root.rowconfigure(1, weight=1, minsize=30)
root.rowconfigure(2, weight=1, minsize=300)
root.rowconfigure(3, weight=1, minsize=50)
root.columnconfigure(0, weight=1, minsize=400)

root.mainloop()