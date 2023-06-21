import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
import requests as req
import re
import firebirdsql
from tkinter import messagebox


class Data:
    def __init__(self):
        self.banco = self.get_banco()
        self.con = firebirdsql.connect(
            host='localhost',
            database=self.banco,
            user='SYSDBA',
            password='masterkey',
            port=3050,
            charset='WIN1252')
        
    def teste(self):
        query=("""select OBS from requisicoes where requisicoes.id_requisicao = 54""")
        
        listtupla=self.select(query)
        print(listtupla)


    def get_banco(self):
        with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
            self.banco= arquivo.read()   
        return self.banco     

    def select(self,query):
        cur = self.con.cursor()
        cur.execute(query)
        resultado = cur.fetchall()
        cur.close()
        return resultado

    def execute(self,con,query):
        cur = con.cursor()
        cur.execute(query)
        cur.close()

    def htmlResponseText(self,link):
        user='CampFacil'
        senha='dsffjyxtf4x'
        response = req.get(link, auth=(user,senha))
        return(response.text)
    
    def treeOpcoesData(self):
        html=self.htmlResponseText("https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get")
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

    def pedidosNfeData(self):
        query=("""select clientes.nome,clientes.nome_fantasia,pedidos.nota_fiscal,pedidos.pedido,pedidos.chave_nfe,pedidos.valor_pedido,clientes.cpf_cnpj
        from pedidos
        join clientes on pedidos.id_cliente = clientes.id_cliente
        where pedidos.id_requisicao is not null and (pedidos.nota_fiscal != 0 )""")
        
        listtupla=self.select(query)
        listPedidos=[]
        for i in range (0,len(listtupla)):
            tupla=listtupla[i]
            nome = tupla[0]
            nome_fantasia = tupla[1]
            pedido = tupla[2]
            nf = tupla[3]
            chave = tupla[4]
            valor = tupla[5]
            cnpj = tupla[6]
            listPedidos.append({'nome':nome,
                                    'nome_fantasia':nome_fantasia,
                                    'pedido':pedido,
                                    'nf' :nf,
                                    'chave' :chave,
                                    'valor' :valor,
                                    'cnpj' :cnpj})

        return listPedidos

    def get_lista_importados(self):
        self.lista_importados = self.select("select pedido from requisicoes ")
        self.lista_importados = [' '.join(map(str, tupla)) for tupla in self.lista_importados]
        return self.lista_importados

class Main_aplication():
    def __init__(self):
        self.Data = Data()
        self.Data.teste()

if __name__ == "__main__":
    Aplication = Main_aplication()