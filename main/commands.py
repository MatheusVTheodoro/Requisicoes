import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import requests as req
import re

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

    return {'MessageID':MessageId,'Data':Data,'Hora':Hora}
    
    
def trataPedescoTxt(link):
    pecaLT=[]
    codClienteLT=[]
    nPedidoLT=[]
    quantidadeLT=[]
    codFornecedorLT=[]
    procedureLT=[]
    texto = htmlResponseText(link)
    texto = re.findall("98.............................................................",texto)
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
        procrdure=(f"execute procedure('{codCliente}','{nPedido}','{NPedidoGMSAP}','{peca}',{quantidade})")
        procedureLT.append(procrdure)
        pecaLT.append(peca)
        codClienteLT.append(codCliente)
        nPedidoLT.append(nPedido)
        quantidadeLT.append(quantidade)
        codFornecedorLT.append(codFornecedor)
        
    return {'procedure':procedureLT,'peca':pecaLT,'codCliente':codClienteLT,'nPedido':nPedidoLT,'quantidade':quantidadeLT,'codFornecedor':codFornecedorLT}




