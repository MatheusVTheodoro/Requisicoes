from tkinter import filedialog
import os

# Definir o nome fixo do arquivo
nome_arquivo = "meu_arquivo.dat"

# Abrir a caixa de diálogo para selecionar um diretório
diretorio = filedialog.askdirectory()

# Verificar se um diretório foi selecionado
if diretorio:
    # Construir o caminho completo do arquivo
    caminho_completo = os.path.join(diretorio, nome_arquivo)
    print("Caminho completo do arquivo:", caminho_completo)

    # Aqui você pode adicionar o código para gerar o conteúdo do arquivo

    # Exemplo: Escrever conteúdo no arquivo
    conteudo = "Este é o conteúdo do arquivo que será salvo."
    with open(caminho_completo, "w") as arquivo:
        arquivo.write(conteudo)

    print("Arquivo salvo com sucesso!")
else:
    print("Nenhum diretório selecionado.")