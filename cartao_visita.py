class CartaoVisita:
    def __init__(self, pessoa):
        self.mensagem = "Cartao de negocios da pessoa "+pessoa.nome+" "+pessoa.sexo
        self.pessoa = pessoa
