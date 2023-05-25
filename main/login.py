import tkinter as tk

# Dicionário com os usuários correspondentes aos IDs
usuarios = {
    "1": "SILENUS",
    "456": "usuario2",
    "789": "usuario3"
}

def preencher_usuario(event=None):
    # Função para preencher o campo "Usuário" com base no ID digitado
    id_digitado = id_entry.get()

    # Verificar se o ID está presente no dicionário
    if id_digitado in usuarios:
        usuario_entry.configure(state='normal')  # Habilitar o campo "Usuário" para escrita
        usuario_entry.delete(0, tk.END)  # Limpar o campo "Usuário"
        usuario_entry.insert(0, usuarios[id_digitado])  # Preencher com o valor correspondente
        usuario_entry.configure(state='readonly')  # Bloquear o campo "Usuário" para escrita novamente
        senha_entry.focus()  # Mover o foco para o campo "Senha"

def confirmar_login(event=None):
    # Função para confirmar o login
    id_digitado = id_entry.get()
    usuario_digitado = usuario_entry.get()
    senha_digitada = senha_entry.get()

    # Lógica para realizar o login com os valores digitados
    # Exemplo: Verificar se o ID, Usuário e Senha são válidos

    # Exibir resultado do login
    resultado_label.config(text=f"ID: {id_digitado}\nUsuário: {usuario_digitado}\nSenha: {senha_digitada}")

# Criar a janela de login
root = tk.Tk()
root.title("Tela de Login")

# Criar os widgets da tela
id_label = tk.Label(root, text="ID:")
id_entry = tk.Entry(root)
id_entry.bind("<Return>", preencher_usuario)  # Chamar a função preencher_usuario ao pressionar Enter no campo ID

usuario_label = tk.Label(root, text="Usuário:")
usuario_entry = tk.Entry(root, state='readonly')  # Configurar o campo "Usuário" como somente leitura

senha_label = tk.Label(root, text="Senha:")
senha_entry = tk.Entry(root, show="*")
senha_entry.bind("<Return>", confirmar_login)  # Chamar a função confirmar_login ao pressionar Enter no campo Senha

login_button = tk.Button(root, text="Fazer Login", command=confirmar_login)

resultado_label = tk.Label(root, text="")

# Posicionar os widgets na tela
id_label.grid(row=0, column=0, sticky=tk.E)
id_entry.grid(row=0, column=1)

usuario_label.grid(row=1, column=0, sticky=tk.E)
usuario_entry.grid(row=1, column=1)

senha_label.grid(row=2, column=0, sticky=tk.E)
senha_entry.grid(row=2, column=1)

login_button.grid(row=3, column=0, columnspan=2)

resultado_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
