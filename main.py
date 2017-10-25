from pessoa import Pessoa
from sala import Sala
from random import randint
import time
import threading
import string
import os

pessoas_nomes = string.ascii_letters[0:20]
generos = ["M", "F"]
pessoas_criadas = []
pessoas_sairam_da_sala = []
quantidade_pessoas_geradas = 0

tempo_inicio_script = time.time()

# 2 minutos
TEMPO_MAXIMO_EXECUCAO = tempo_inicio_script + 60 * 2
QUANTIDADE_MAXIMA_PESSOAS = 20


# "Abrindo" a sala
sala = Sala()
sala.start()


def gerar_pessoas():

    global quantidade_pessoas_geradas

    if quantidade_pessoas_geradas != QUANTIDADE_MAXIMA_PESSOAS:
        inserir_pessoa_sala()
        quantidade_pessoas_geradas += 1
        threading.Timer(2, gerar_pessoas).start()


def inserir_pessoa_sala():
    pessoa = Pessoa(pessoas_nomes[len(pessoas_criadas)], generos[randint(0, 1)], sala)
    pessoas_criadas.append(pessoa)
    pessoa.start()

gerar_pessoas()


# Garante a execuçao do programa por 2 minutos
while True:
    if time.time() >= TEMPO_MAXIMO_EXECUCAO:

        # Pegar as pessoas que sairam e as que estao la dentro para fazer a listagem de cartoes que cada uma pegou
        # e dizer o tempo em que ela ficou na sala.
        # Exibir o tempo médio em que a pessoa fica na fila de entrada e o tempo médio dentro da sala

        sala.fechar_sala()
        print("--------------------------------||---------------- RESUMO -------------------||------------------------")

        tempo_total_na_sala = 0
        tempo_total_na_fila = 0

        for pessoa in sala.pessoas_sairam_da_sala:
            print('\nCartões recebidos pela pessoa '+pessoa.nome+':')
            print(pessoa.relatorio())
            tempo_total_na_sala += pessoa.tempo_total_na_sala
            tempo_total_na_fila += pessoa.tempo_total_na_fila

        quantidade_pessoas = len(sala.pessoas_sairam_da_sala)

        tempo_medio_na_sala = round(tempo_total_na_sala / quantidade_pessoas, 2)
        tempo_medio_na_fila = round(tempo_total_na_fila / quantidade_pessoas, 2)

        print("\nTempo médio de cada pessoa na sala: "+str(tempo_medio_na_sala)+" segundos")
        print("Tempo médio de espera na fila de entrada: "+str(tempo_medio_na_fila)+" segundos")
        os._exit(1)













