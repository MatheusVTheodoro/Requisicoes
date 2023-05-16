from view import *
import model as model

app = None

def trataPedescoTxt(link):
    procedures=[]
    texto = model.htmlResponseText(link)
    texto = re.findall("98.............................................................",texto)
    maximum=len(texto) 
    app.pbVizu['maximum'] = maximum
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
        cliente=model.select(con,query)
        query=(f"select descricao from produtos where produtos.codigo_fab = '{peca}'")
        produto=model.select(con,query)
        
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

        procedure=(f"execute procedure GERAR_REQUISICAO('{codCliente}','','{int(NPedidoGMSAP)}','{peca}',{quantidade});")
        procedures.append(procedure)
        if index % 2 == 0 :
            fundo = "branco"
        else:
            fundo = "verde"
        
        app.tabela_vizu.insert("", tk.END,values=(codCliente,cliente,produto,peca,quantidade),tags=(fundo))
        app.pbVizu['value'] = index+1
        app.root.update()
    con.close()
    app.pbVizu.destroy()    
    return {'procedures':procedures}

def visualiza():
    options=model.opcoes()
    app.btVizu.destroy()
    pbVizu = ttk.Progressbar(app.frame_opcoes, mode='determinate')
    pbVizu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    app.tabela_vizu.delete(*app.tabela_vizu.get_children())
    item = app.tabela_opcoes.selection()[0]
    messageId_clicked = app.tabela_opcoes.item(item, "values")[0]
    linkView=(f"https://messaging.covisint.com/invoke/HTTPConnector.Mailbox/get?action=msg_view&id={messageId_clicked}")
    pedidos = trataPedescoTxt(linkView)

    def importar():
        global banco
        con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252')
        con.begin()
        for value in pedidos['procedures']:
            model.execute(con,value)    
        con.commit()
        con.close()
        con = firebirdsql.connect(
        host='localhost',
        database=banco,
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='WIN1252')
        lista_importados = model.select(con,"select pedido from requisicoes ")
        con.close()
        lista_importados = [' '.join(map(str, tupla)) for tupla in lista_importados]
        app.tabela_opcoes.delete(*app.tabela_opcoes.get_children())
        for X in range (0,len(options['Data'])):
    
            if X % 2 == 0 :
                fundo = "branco"
            else:
                fundo = "normal"
            if  options['MessageID'][X] in lista_importados:
                fundo = "verde"  
            app.tabela_opcoes.insert("", tk.END,values=(options['MessageID'][X],options['Size'][X],options['Data'][X],options['Hora'][X],"Confirmado"),tags=(fundo))
        app.tabela_opcoes.tag_configure("branco", background=app.cor["branco"])
        app.tabela_opcoes.tag_configure("verde", background=app.cor["verde"])
        app.btEnvia.destroy()
        app.root.update()

def item_clicked(event):
    app.tabela_vizu.delete(*app.tabela_vizu.get_children())
    if app.button_created:
        app.btEnvia.destroy()
    if button_created2:
        btVizu.destroy()
        btVizu = tk.Button(app.frame_opcoes,command=visualiza,text='Carregar Visualização',bg=app.cor["azul"], fg=app.cor["branco"])
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    else:
        btVizu = tk.Button(app.frame_opcoes,command=visualiza,text='Carregar Visualização',bg=app.cor["azul"], fg=app.cor["branco"])
        btVizu.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        button_created2 = True

if __name__ == "__main__":
    # ao determinar app como Interface() eu basicamente trago minha classe interface completa
    # podendo ser acessada assim como feito abaixo em app.root.mainloop()
    # que acessa o parametro root para iniciar minha janela 
    app = Interface()
    app.tabelaOpcoes.bind("<ButtonRelease-1>", item_clicked)
    
    app.root.mainloop()