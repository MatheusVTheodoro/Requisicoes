import tkinter as tk
from tkinter import filedialog
from data import Data

def salvar_arquivo():
    # Abrir a janela de diálogo para seleção do local de salvamento
    arquivo = filedialog.asksaveasfile(defaultextension=".txt")
    
    if arquivo is None:
        # Nenhum arquivo selecionado
        return
    
    # Obter o texto a ser salvo
    frase = "Esta é uma frase de exemplo."
    
    # Escrever a frase no arquivo
    arquivo.write(frase)
    arquivo.close()
    
    print("Frase gravada no arquivo:", arquivo.name)


def get_pedidos_nfe():
    Data = Data()
    query=("""select clientes.nome,clientes.nome_fantasia,pedidos.nota_fiscal,pedidos.pedido,pedidos.chave_nfe,pedidos.valor_pedido
from pedidos
join clientes on pedidos.id_cliente = clientes.id_cliente
where pedidos.id_requisicao is not null and (pedidos.nota_fiscal != 0 )""")
    
    listtupla=Data.select(query)

    print(listtupla)


janela = tk.Tk()


botao = tk.Button(janela, text="Selecionar Local", command=get_pedidos_nfe)
botao.pack()


janela.mainloop()
