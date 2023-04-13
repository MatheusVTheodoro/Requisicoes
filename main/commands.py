import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


def select_file():
    global filename
    filetypes = (
        ('MBX files', '*.mbx'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
def read_mbx():
    global filename
    global texto
    with open(filename, 'r') as f:
        texto = f.readlines()
        arquivo = texto[1]
        tam = 8
        peca = arquivo[0:0+tam]
        codCliente = arquivo[tam:tam+6]
        tam=tam+6
        nPedido = arquivo[tam:tam+6]
        tam=tam+6
        quantidade = arquivo[tam:tam+5]
        tam=tam+5
        dataArquivo = arquivo[tam:tam+8]
        tam=tam+8
        codFornecedor = arquivo[tam:tam+9]
        tam=tam+9
        tipoDSODSC = arquivo[tam:tam+1]
        tam = tam+1
        NPedidoGMSAP = arquivo[tam:tam+9]
        tam=tam+9
        hora = arquivo[tam:tam+6]
        tam=tam+6
        linhaDoPedido = arquivo[tam:tam+5]

        
    
    print(f"peca: {peca}\ncodCliente: {codCliente}\nnPedido: {nPedido}\nquantidade: {quantidade}\ndataArquivo: {dataArquivo}\ncodFornecedor: {codFornecedor}\ntipoDSODSC: {tipoDSODSC}\nNPedidoGMSAP: {NPedidoGMSAP}\nhora: {hora}\nlinhaDoPedido: {linhaDoPedido}")
      