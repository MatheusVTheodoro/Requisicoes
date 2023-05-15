import requests as req
import re
import firebirdsql

global banco

with open('C:/COLISEU/Requisicoes/banco.txt', 'r') as arquivo:
    banco= arquivo.read()
    print(banco)

def select(query):
    global banco
    con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252'
    )
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchall()
    cur.close()
    con.close()
    return resultado

def execute(query):
    global banco
    con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252'
    )
    cur = con.cursor()
    cur.execute(query)
    cur.close()
    con.commit()
    con.close()

def htmlResponseText(link):
    user='CampFacil'
    senha='dsffjyxtf4x'
    response = req.get(link, auth=(user,senha))
    return(response.text)

def opcoes():
    global banco
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
opcoes()        
def trataPedescoTxt(link):
    clienteCol=[]
    produtoCol=[]
    produtoRefCol=[]
    quantidadeCol=[]
    codigoClienteCol=[]
    procedures=[]
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
        quantidade=int(quantidade)

        cliente=select((f"select NOME_FANTASIA from clientes where clientes.DOC_EX = '{codCliente}'"))
        produto=select((f"select descricao from produtos where produtos.codigo_fab = '{peca}'"))
        
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

        
        procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','{nPedido}','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
        procedures.append(procedure)
        clienteCol.append(cliente)
        codigoClienteCol.append(codCliente)
        produtoCol.append(produto)
        produtoRefCol.append(peca)
        quantidadeCol.append(quantidade)
        print(cliente)
    return {'procedures':procedures,'clienteCol':clienteCol,'codigoClienteCol':codigoClienteCol,'produtoCol':produtoCol,'produtoRefCol':produtoRefCol,'quantidadeCol':quantidadeCol,}



