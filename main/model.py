import requests as req
import re
import firebirdsql
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

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
