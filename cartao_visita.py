class CartaoVisita:
    def __init__(self, pessoa):
        self.mensagem = "Cartao de negócios da pessoa "+pessoa.nome+" "+pessoa.sexo
        self.pessoa = pessoa
