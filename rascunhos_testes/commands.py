import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from main import *

with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
    banco= arquivo.read()

def select(con,query):
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchall()
    cur.close()
    return resultado

def execute(con,query):
    cur = con.cursor()
    cur.execute(query)
    cur.close()

def htmlResponseText(link):
    user='CampFacil'
    senha='dsffjyxtf4x'
    response = req.get(link, auth=(user,senha))
    return(response.text)

def opcoes():
    html=htmlResponseText("https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get")
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

def trataPedescoTxt(link):
    global tabela_vizu,root,pbVizu,banco,messageId_clicked
    
    procedures=[]
    texto = htmlResponseText(link)
    texto = re.findall("98.............................................................",texto)
    maximum=len(texto) 
    pbVizu['maximum'] = maximum
    con = firebirdsql.connect(
    host='localhost',
    database=banco,
    user='SYSDBA',
    password='masterkey',
    port=3050,
    charset='WIN1252')

    for index,value in enumerate(texto):
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
        quantidade=int(quantidade)

        query=(f"select NOME_FANTASIA from clientes where clientes.DOC_EX = '{codCliente}'")
        cliente=select(con,query)
        query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
        produto=select(con,query)
        
        if(produto==[]):
            produto='Produto não vinculado'
        else:
            produto=produto[0]
            produto=str(produto)
            produto = produto[2:-3]

        if(cliente==[]):
            cliente='Codigo de cliente não vinculado'
        else:
            cliente=cliente[0]
            cliente=str(cliente)
            cliente = cliente[2:-3]

        procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{messageId_clicked}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
        procedures.append(procedure)
        if index % 2 == 0 :
            fundo = "branco"
        else:
            fundo = "verde"
        
        tabela_vizu.insert("", tk.END,values=(codCliente,cliente,produto,peca,quantidade),tags=(fundo))
        tabela_vizu.tag_configure("branco", background=cor["branco"])
        pbVizu['value'] = index+1
        root.update()
    con.close()
    pbVizu.destroy()    
    return {'procedures':procedures}

def item_clicked(event):
    tabela_vizu.delete(*tabela_vizu.get_children())
    if button_created:
        btEnvia.destroy()
    if button_created2:
        btVizu.destroy()
        btVizu = tk.Button(frame_opcoes,command=visualiza,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    else:
        btVizu = tk.Button(frame_opcoes,command=visualiza,text='Carregar Visualização',bg=cor["azul"], fg=cor["branco"])
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        button_created2 = True






















