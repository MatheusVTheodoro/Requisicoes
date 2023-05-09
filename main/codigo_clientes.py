import pandas as pd

# leia a planilha do Excel
df = pd.read_excel('C:\REPOSITORIOS\COLISEU\ColiseuRequisicoes\main\LISTA_CLIENTES.xlsx')

# armazene os valores das duas colunas em listas
cod = df['Código'].tolist()
CNPJ = df['CNPJ Concessionária'].tolist()
with open("SQL_files\CLIENTESCOD.sql", "w") as arquivo:
    for i in range (0,len(cod)):
        update=(f"UPDATE ClIENTES SET DOC_EX = '{cod[i]}' WHERE CPF_CNPJ = '{CNPJ[i]}';")
        arquivo.write(update + "\n")
