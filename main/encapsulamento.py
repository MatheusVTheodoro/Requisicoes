'''Neste exemplo, a classe Cofre possui atributos e métodos encapsulados. A senha e o conteúdo do cofre são atributos privados, indicados pelo uso de __ (dois underscores) como prefixo. Isso impede que eles sejam acessados diretamente fora da classe.

Os métodos abrir, guardar_conteudo, pegar_conteudo e fechar são responsáveis por interagir com o cofre. A função __verificar_senha é um método privado que verifica se a senha informada é correta.

Ao criar uma instância da classe Cofre (meu_cofre = Cofre()), você pode usar os métodos públicos para interagir com o cofre. Por exemplo, meu_cofre.abrir("1234") tenta abrir o cofre com a senha fornecida.

Lembre-se de que o encapsulamento permite controlar o acesso aos atributos e métodos de uma classe, evitando modificações indesejadas e garantindo que as ações corretas sejam executadas.




class Cofre:
    def __init__(self):
        self.__senha = "1234"  # Atributo privado
        self.__conteudo = None

    def __verificar_senha(self, senha):
        return senha == self.__senha
    # o trecho a cima compara a senha inserida na função com a senha do cofre
    # retornando um valor booleano

    def abrir(self, senha):
        # este if testa o retorno booleano da função __verificar_senha
        if self.__verificar_senha(senha):
            print("Cofre aberto.")
            return True
        else:
            print("Senha incorreta. Cofre permanece fechado.")
            return False

    def guardar_conteudo(self, senha, conteudo):
        #como a função abrir retorna um booleano utilizamos ela na condicional
        #assim se voce conseguir abrir o cofre com a senha voce guarda o conteudo.
        if self.abrir(senha):
            self.__conteudo = conteudo
            print("Conteúdo guardado com sucesso.")

    def pegar_conteudo(self, senha):
        if self.abrir(senha):
            if self.__conteudo:
                print(f"Conteúdo: {self.__conteudo}")
            else:
                print("O cofre está vazio.")

    def fechar(self):
        self.__conteudo = None
        print("Cofre fechado.")


# Exemplo de uso:

meu_cofre = Cofre()

meu_cofre.abrir("5678")  # Senha incorreta. Cofre permanece fechado.

meu_cofre.abrir("1234")  # Cofre aberto.

meu_cofre.guardar_conteudo("1234", "Objeto valioso")  # Conteúdo guardado com sucesso.

meu_cofre.pegar_conteudo("5678")  # Senha incorreta. Cofre permanece fechado.

meu_cofre.pegar_conteudo("1234")  # Conteúdo: Objeto valioso

meu_cofre.fechar()  # Cofre fechado.

'''



''' mesmo exemplo porem agora dividindo o exemplo em 2 class'''


'''class Autenticacao:
    def __init__(self, senha_correta):
        self.__senha_correta = senha_correta

    def verificar_senha(self, senha):
        return senha == self.__senha_correta


class Cofre:
    def __init__(self, senha_correta):
        self.__autenticacao = Autenticacao(senha_correta)
        self.__conteudo = None

    def abrir(self, senha):
        # note que aqui é acessado um método de outra class, a class Autenticação
        # para isso no metodo init é iniciada uma instancia privada da class Autenticação
        # e para acessar o metodo dessa instancia utilizamos o nome da instancia . o metodo que
        # ela herdou da class que foi seu molde.
        if self.__autenticacao.verificar_senha(senha):
            print("Cofre aberto.")
            return True
        else:
            print("Senha incorreta. Cofre permanece fechado.")
            return False

    def guardar_conteudo(self, senha, conteudo):
        if self.abrir(senha):
            self.__conteudo = conteudo
            print("Conteúdo guardado com sucesso.")

    def pegar_conteudo(self, senha):
        if self.abrir(senha):
            if self.__conteudo:
                print(f"Conteúdo: {self.__conteudo}")
            else:
                print("O cofre está vazio.")

    def fechar(self):
        self.__conteudo = None
        print("Cofre fechado.")


# Exemplo de uso:

senha_correta = "1234"

meu_cofre = Cofre(senha_correta)

meu_cofre.abrir("5678")  # Senha incorreta. Cofre permanece fechado.

meu_cofre.abrir("1234")  # Cofre aberto.

meu_cofre.guardar_conteudo("1234", "Objeto valioso")  # Conteúdo guardado com sucesso.

meu_cofre.pegar_conteudo("5678")  # Senha incorreta. Cofre permanece fechado.

meu_cofre.pegar_conteudo("1234")  # Conteúdo: Objeto valioso

meu_cofre.fechar()  # Cofre fechado.'''


'''adicionamos agora uma interface encapsulada numa class para substituir a parte exemplos de uso '''

class Autenticacao:
    def __init__(self, senha_correta):
        self.__senha_correta = senha_correta

    def verificar_senha(self, senha):
        return senha == self.__senha_correta


class Cofre:
    def __init__(self, senha_correta):
        self.__autenticacao = Autenticacao(senha_correta)
        self.__conteudo = None

    def abrir(self, senha):
        if self.__autenticacao.verificar_senha(senha):
            print("Cofre aberto.")
            return True
        else:
            print("Senha incorreta. Cofre permanece fechado.")
            return False

    def guardar_conteudo(self, senha, conteudo):
        if self.abrir(senha):
            self.__conteudo = conteudo
            print("Conteúdo guardado com sucesso.")

    def pegar_conteudo(self, senha):
        if self.abrir(senha):
            if self.__conteudo:
                print(f"Conteúdo: {self.__conteudo}")
            else:
                print("O cofre está vazio.")

    def fechar(self):
        self.__conteudo = None
        print("Cofre fechado.")


class InterfaceCofre:
    def __init__(self):
        self.__cofre = None

    def iniciar(self):
        senha_correta = input("Digite a senha correta para o cofre: ")
        self.__cofre = Cofre(senha_correta)
        self.menu()

    def menu(self):
        opcoes = """
        Menu do Cofre:
        1. Abrir cofre
        2. Guardar conteúdo
        3. Pegar conteúdo
        4. Fechar cofre
        5. Sair
        """

        while True:
            print(opcoes)
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                senha = input("Digite a senha: ")
                self.__cofre.abrir(senha)
            elif escolha == "2":
                senha = input("Digite a senha: ")
                conteudo = input("Digite o conteúdo a ser guardado: ")
                self.__cofre.guardar_conteudo(senha, conteudo)
            elif escolha == "3":
                senha = input("Digite a senha: ")
                self.__cofre.pegar_conteudo(senha)
            elif escolha == "4":
                self.__cofre.fechar()
            elif escolha == "5":
                break
            else:
                print("Opção inválida. Digite novamente.")


# Exemplo de uso:

interface = InterfaceCofre()
interface.iniciar()


