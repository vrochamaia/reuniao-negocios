from cartao_visita import CartaoVisita
from threading import Thread
import threading
import time


class Pessoa(Thread):

    lock = threading.Condition()

    tempo_entrada_sala = 0
    tempo_entrada_fila = 0
    tempo_total_na_sala = 0
    tempo_total_na_fila = 0

    def __init__(self, nome, sexo, sala):
        Thread.__init__(self)
        self.nome = nome
        self.sexo = sexo
        self.sala = sala
        self.cartao_pessoal = CartaoVisita(self)
        self.cartoes_recebidos = []

    def run(self):
        self.tempo_entrada_fila = time.time()
        if self.sala.inserir_pessoa_sala(self):
            self.tempo_total_na_fila = time.time() - self.tempo_entrada_fila
            print(self.nome + ' ('+self.sexo+') entrou na sala')
            self.tempo_entrada_sala = time.time()
            self.trocar_cartoes()

    def trocar_cartoes(self):
        print("Troca de cartoes iniciada pela pessoa "+self.nome)

        with self.lock:

            continuar_loop = True
            condicao_atendida = False

            while continuar_loop and not self.sala.sala_esta_fechada:

                for pessoa in self.sala.pessoas_na_sala:
                    if pessoa.cartao_pessoal not in self.cartoes_recebidos and pessoa != self:
                        self.cartoes_recebidos.append(pessoa.cartao_pessoal)
                        pessoa.cartoes_recebidos.append(self.cartao_pessoal)
                        time.sleep(2)
                        pessoa.lock.notify()

                        if self.condicoes_atentidas():
                            condicao_atendida = True
                            break

                if not condicao_atendida:
                    print(self.nome + " foi dormir porque não conseguiu os cartões necessários")
                    self.lock.wait()
                    print(self.nome + " foi acordada para continuar troca de cartões")

                    if self.condicoes_atentidas():
                        continuar_loop = False
                else:
                    continuar_loop = False

        self.sair_sala()

    def condicoes_atentidas(self):

        cartao_masculino = False
        cartao_feminino = False

        for cartao_visita in self.cartoes_recebidos:
            if cartao_visita.pessoa.sexo == "H":
                cartao_masculino = True
            if cartao_visita.pessoa.sexo == "M":
                cartao_feminino = True

        # verificar se ja tem 3 cartões e pelo menos um de cada sexo, se sim, sai da sala, se não, dorme
        if len(self.cartoes_recebidos) >= 3 and cartao_masculino and cartao_feminino:
            return True
        else:
            return False

    def sair_sala(self):
        if not self.sala.sala_esta_fechada:
            self.tempo_total_na_sala = round(time.time() - self.tempo_entrada_sala, 2)
            self.sala.remover_pessoa_sala(self)

    def relatorio(self):

        relatorio = ""

        for cartao in self.cartoes_recebidos:
            relatorio += 'Pessoa '+cartao.pessoa.nome+'('+cartao.pessoa.sexo+')\n'

        relatorio += 'Tempo total na sala: '+str(self.tempo_total_na_sala)+' segundos'

        return relatorio






