import requests as req
import re
import firebirdsql



class ModelApp:
    def __init__(self):
        self.data = self.opcoes()
      
    def conection(self):
        with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
            banco= arquivo.read()

        self.conection = firebirdsql.connect(
                        host='localhost',
                        database=banco,
                        user='SYSDBA',
                        password='masterkey',
                        port=3050,
                        charset='WIN1252')
        return(self.conection)
    
    def htmlResponseText(self,link):
        user='CampFacil'
        senha='dsffjyxtf4x'
        self.response = req.get(link, auth=(user,senha))
        return(self.response.text)
    
    def opcoes(self):
        html=self.htmlResponseText("https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get")
        MessageId=[]
        Data=[]
        Hora=[]
        Size=[]
        dados=[]
        
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
   
    def minha_outra_funcao(self):
        dados = self.opcoes()
        self.controller.model.add_data(dados['MessageID'], dados['Data'], dados['Hora'], dados['Size'])
