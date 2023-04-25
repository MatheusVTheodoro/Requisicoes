import tkinter as tk
from commands import *

root = tk.Tk()

# Crie uma lista de opções
options = opcoes()

# Crie um widget Listbox para exibir a lista
listbox = tk.Listbox(root)
for option in options:
    listbox.insert(tk.END, option)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Adicione uma barra de rolagem para o widget Listbox
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Adicione um comando para exibir a opção selecionada
def ConfirmPedesco():
    selection = listbox.get(listbox.curselection())
    link=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={selection}")
    texto = htmlResponseText(link)
    print(texto,type(texto))
    """print (type(texto))
    texto.pop(0)
    texto.pop(-1)
    for value in texto:
        tam = 8
        peca = value[0:0+tam]
        codCliente = value[tam:tam+6]
        tam=tam+6
        nPedido = value[tam:tam+6]
        tam=tam+6
        quantidade = value[tam:tam+5]
        tam=tam+5
        datavalue = value[tam:tam+8]
        tam=tam+8
        codFornecedor = value[tam:tam+9]
        tam=tam+9
        tipoDSODSC = value[tam:tam+1]
        tam = tam+1
        NPedidoGMSAP = value[tam:tam+9]
        tam=tam+9
        hora = value[tam:tam+6]
        tam=tam+6
        linhaDoPedido = value[tam:tam+5]
        print(f"execute procedure GERAR_REQUISICAO ('{codCliente}','{nPedido}','{NPedidoGMSAP}')")
        print(f"peca: {peca}\ncodCliente: {codCliente}\nnPedido: {nPedido}\nquantidade: {quantidade}\ndataArquivo: {datavalue}\ncodFornecedor: {codFornecedor}\ntipoDSODSC: {tipoDSODSC}\nNPedidoGMSAP: {NPedidoGMSAP}\nhora: {hora}\nlinhaDoPedido: {linhaDoPedido}")
"""
button = tk.Button(root, text="Executar comando", command=print_selection)
button.pack(side=tk.BOTTOM)

root.mainloop()