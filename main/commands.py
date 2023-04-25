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
    X = re.findall("<td><tt>&nbsp;........&nbsp;",html)
    for v in X:
        message = re.sub("<td><tt>&nbsp;","",v)
        MessageId.append(re.sub("&nbsp;","",message))
    return MessageId

   #print(f"execute procedure GERAR_REQUISICAO ('{codCliente}','{nPedido}','{NPedidoGMSAP}')")
   #print(f"peca: {peca}\ncodCliente: {codCliente}\nnPedido: {nPedido}\nquantidade: {quantidade}\ndataArquivo: {datavalue}\ncodFornecedor: {codFornecedor}\ntipoDSODSC: {tipoDSODSC}\nNPedidoGMSAP: {NPedidoGMSAP}\nhora: {hora}\nlinhaDoPedido: {linhaDoPedido}")
      