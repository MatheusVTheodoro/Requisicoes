import tkinter as tk
from tkinter import filedialog
import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
import requests as req
import re
import firebirdsql
from tkinter import messagebox







def get_banco():
    with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
        banco= arquivo.read()
    return banco

def select(query):
    banco = get_banco()
    con = firebirdsql.connect(
            host='localhost',
            database=banco,
            user='SYSDBA',
            password='masterkey',
            port=3050,
            charset='WIN1252')
        

    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchall()
    cur.close()
    return resultado



def salvar_arquivo():
    arquivo = filedialog.asksaveasfile(defaultextension=".txt")
    
    if arquivo is None:
        return
    
    frase = """HEADERNFFORN20230209101828.DAT                                                                                                     
    98553852L57001PREVMB00000471000190350667119012023C018474319000030000000439728000065960000030781000030781000000000        00010     
"""
    arquivo.write(frase)
    arquivo.close()
    
    print("Frase gravada no arquivo:", arquivo.name)


def get_pedidos_nfe():
    query=("""select clientes.nome,clientes.nome_fantasia,pedidos.nota_fiscal,pedidos.pedido,pedidos.chave_nfe,pedidos.valor_pedido
    from pedidos
    join clientes on pedidos.id_cliente = clientes.id_cliente
    where pedidos.id_requisicao is not null and (pedidos.nota_fiscal != 0 )""")
    
    listtupla=select(query)
    listPedidos=[]
    for i in range (0,len(listtupla)):
        tupla=listtupla[i]
        nome = tupla[0]
        nome_fantasia = tupla[1]
        pedido = tupla[2]
        nf = tupla[3]
        chave = tupla[4]
        valor = tupla[5]
        listPedidos.append({'nome':nome,
                                'nome_fantasia':nome_fantasia,
                                'pedido':pedido,
                                'nf' :nf,
                                'chave' :chave,
                                'valor' :valor})

    return listPedidos

    def treeOpcoesData():
        MessageId=[]
        Data=[]
        Hora=[]
        Size=[]
        
        X = re.findall("&nbsp;[0-9]+&nbsp",html)
        for v in X:
            message = re.sub("&nbsp;","",v)
            Size.append(re.sub("&nbsp","",message))

        X = re.findall("<td><tt>&nbsp;........&nbsp;",html)
        for v in X:
            message = re.sub("<td><tt>&nbsp;","",v)
            MessageId.append(re.sub("&nbsp;","",message))
        
        X = re.findall("<nobr>&nbsp;........",html)
        for v in X:
            dia = re.sub("<nobr>&nbsp;","",v)
            Data.append(dia)
        
        X = re.findall("&nbsp;.....:..",html)
        for v in X:
            hora = re.sub("&nbsp;","",v)
            Hora.append(hora)

        return {'MessageID':MessageId,'Data':Data,'Hora':Hora, 'Size' :Size}













janela = tk.Tk()


botao = tk.Button(janela, text="Selecionar Local", command=get_pedidos_nfe)
botao.pack()


janela.mainloop()
