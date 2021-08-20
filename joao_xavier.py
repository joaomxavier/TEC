# Trabalho final TEC
# Disciplina: Teoria da Computação
# Aluno: João Marcelo Specki Xavier
# Professora: Karina Roggia
import os

# Função que lê o arquivo de entrada
def lendo_arquivo(nome):
    entrada = list()
    ref_arquivo = open(caminho_arquivo + "\\" + nome, "r")
    for linha in ref_arquivo:
        valores = linha.split()
        if valores[0] == "0":  # Eu troco o estado inicial por 'iniciaprocessamento'
            valores[0] = "iniciaProcessamento"
        if valores[4] == "0":
            valores[4] = "iniciaProcessamento"
        entrada.append(valores)
    ref_arquivo.close()
    return entrada


caminho_arquivo = os.path.dirname(os.path.realpath(__file__))  # Caminho do arquivo
arquivo_entrada = lendo_arquivo("exemplo.in")
cont = 0  # Contador de estados auxiliares (no caso de movimentos estacionários)
alfabeto_fita = ["0", "1", "_"]
lista_tratada = list()

print('PRINTANDO ARQUIVO DE ENTRADA')
for transicao in arquivo_entrada:
    print(transicao)

# Como novo símbolo de branco, utilizei o '$'
# <current state> <current symbol> <new symbol> <direction> <new state>
for transicao in arquivo_entrada:
    if transicao[3] == "*":  # Caso a gente tenha um movimento estacionário
        novo_estado = transicao[4]
        # Primeiro fazendo uma transição para a direita
        transicao[3] = "r"
        transicao[4] = "qaux" + str(cont)
        # Inserindo movimento a direita
        if transicao[2] == "_":
            lista_tratada.append([transicao[0], transicao[1], "$", transicao[3], transicao[4]])
            branco = True
        else:
            lista_tratada.append(transicao)
        for simbolo in alfabeto_fita:
            # Inserindo |Γ| movimentos à esquerda
            if simbolo == "_":
                lista_tratada.append(["qaux" + str(cont), simbolo, "$", "l", novo_estado])
                branco = True
            else:
                lista_tratada.append(["qaux" + str(cont), simbolo, simbolo, "l", novo_estado])
        cont = cont + 1
    elif transicao[1] != "_" and transicao[2] == "_":  # Escrevo branco, mas nao leio
        transicao[2] = "$"
        lista_tratada.append([transicao[0], transicao[1], "$", transicao[3], transicao[4]])
        branco = True
    elif transicao[1] == "_" and transicao[2] == "_":  # Lê e escreve branco
        lista_tratada.append([transicao[0], "_", "$", transicao[3], transicao[4]])
        lista_tratada.append([transicao[0], "$", "$", transicao[3], transicao[4]])
        branco = True
    else:
        lista_tratada.append(transicao)


# Caso escreva branco, é necessário adicionar, para cada transição que lê branco,
# uma transição que lê o 'novo' branco ($)
if branco:
    for transicao in lista_tratada:
        if transicao[1] == "_":
            lista_tratada.append([transicao[0], "$", transicao[2], transicao[3], transicao[4]])

# Essas transições são adicionados para simular o movimento "fique parado" no caso do
# cabeçote estar na célula mais a esquerda e fazer movimento à esquerda na máquina do Sipser
# E também adicionar o novo símbolo de branco ($) logo após o término da palavra de entrada.
# Antes de iniciar a simulação a máquina começa fazendo um movimento para esquerda e colocando o símbolo '#'
# (não pertencente ao alfabeto da fita), depois vai até o primeiro branco após a palavra de entrada
# e coloca o novo símbolo de branco ($), por fim, volta para o início da fita e inicia o processamento
lista_tratada.append(["0", "_", '$', "l", "primeiroSimbolo"])
lista_tratada.append(["0", "0", '0', "l", "primeiroSimbolo"])
lista_tratada.append(["0", "1", '1', "l", "primeiroSimbolo"])
lista_tratada.append(["primeiroSimbolo", "_", '#', "r", "indoFinal"])
lista_tratada.append(["indoFinal", "_", '$', "l", "indoInicio"])
lista_tratada.append(["indoFinal", "0", '0', "r", "indoFinal"])
lista_tratada.append(["indoFinal", "1", '1', "r", "indoFinal"])
lista_tratada.append(["indoInicio", "$", '$', "l", "indoInicio"])
lista_tratada.append(["indoInicio", "0", '0', "l", "indoInicio"])
lista_tratada.append(["indoInicio", "1", '1', "l", "indoInicio"])
lista_tratada.append(["indoInicio", "#", '#', "r", "iniciaProcessamento"])
lista_tratada.append(["*", "#", '#', "r", "*"])

# Tirando valores repetidos e ordenando a lista
traducao = [i for j, i in enumerate(lista_tratada) if i not in lista_tratada[:j]]
traducao = sorted(traducao)
print('PRINTANDO LISTA TRADUZIDA POS DE TIRAR REPETICAO')
for transicao in traducao:
    print(transicao)

file = open("arquivo.out", "w")
for transicao in traducao:
    file.write(
        ' '.join([transicao[0], transicao[1], transicao[2], transicao[3], transicao[4]+"\n"]))

