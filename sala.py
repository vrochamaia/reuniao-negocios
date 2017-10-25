from threading import Thread
import threading


class Sala(Thread):

    lock = threading.Condition()

    def __init__(self):
        Thread.__init__(self)
        self.pessoas_na_sala = []
        self.pessoas_sairam_da_sala = []
        self.sala_esta_cheia = False
        self.sala_esta_fechada = False

    def run(self):
        print('Sala abriu')

    def inserir_pessoa_sala(self, pessoa):

        with self.lock:

            while self.sala_esta_cheia or self.sala_esta_fechada:
                print(pessoa.nome + ' dormiu pois nao conseguiu entrar na sala')
                self.lock.wait()
                print(pessoa.nome + ' foi acordada para entrar na sala')

            self.pessoas_na_sala.append(pessoa)

            # Pode ter no maximo 5 pessoas na sala
            if len(self.pessoas_na_sala) == 5:
                self.sala_esta_cheia = True

        return True

    def remover_pessoa_sala(self, pessoa):

        with self.lock:
            self.pessoas_sairam_da_sala.append(pessoa)
            self.pessoas_na_sala.remove(pessoa)

            print(pessoa.nome + ' saiu da sala')
            self.lock.notify()
            print(pessoa.nome + ' acordou uma das pessoas.')

            if self.sala_esta_cheia:
                self.sala_esta_cheia = False

    def fechar_sala(self):
        self.sala_esta_fechada = True
        print('Sala fechou')





