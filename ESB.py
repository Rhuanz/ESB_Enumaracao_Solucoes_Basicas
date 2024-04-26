"""
* Programa: Enumeração de soluções básicas
* Autor(es): Rhuan Gabriel, Ana Paula Kendall
* Data de Criação: 15/05/2021
* Última alteração: 01/06/2021
* Descrição Geral: Modelagem genérica de enumeração e soluções básicas para problemas na forma padrão, programa apresentado como parte
da segunda nota da disciplina Pesquisa Operacional.
"""

import numpy as np
from itertools import combinations

print("Olá!\n"
      "Para resolver seu problema de enumeração de soluções básicas\n"
      "escreva os dados num arquivo .txt no fomato a seguir:")

print("3 2 #3 variaveis e 2 restricoes\n"
      "5 10 8 #coeficientes das variaveis na funcao objetivo\n"
      "3 5 2 60 #restricao 1\n"
      "4 4 4 72 #restricao 2\n")

print("Depois, verifique se o arquivo esta no diretorio 'Problemas_Alvo' e digite o nome do arquivo\n")

#organizando nome do arquivo
arq = input("Digite o nome do arquivo: ")
arq = arq+".txt"

#lendo os dados do arquivo
ref_arquivo = open("Problemas_Alvo/"+arq, "r")

probC = []

for line in ref_arquivo:
    probC.append(line)

ref_arquivo.close()

#removendo as quebras de linha e espaços em branco

for i in range(0, len(probC)):
    probC[i] = probC[i].rstrip("\n")
    probC[i] = probC[i].split()

#distribuindo valores recebidos

qVarss = int(probC[0][0]) #qVarss -> Quantidade de variáveis

qRes = int(probC[0][1]) #qRes -> Quantidade de restrições

coefZ = [] #coefZ -> Coeficiente das variáveis da função Z

for i in range(0, len(probC[1])):

    coefZ.append(int(probC[1][i]))

#Declaração de matriz de restriçoes
restr = [[[]for i in range(0)] for j in range(qRes)] #restr -> Restrições

#Preenchendo matriz de restrições
for i in range(2, qRes+2):
    for j in range(0, len(probC[i])):
        restr[i-2].append(int(probC[i][j]))

#Separando resultados das restrições
b = []   #b -> matriz com o lado direito das restricoes
for i in range(len(restr)):
    b.append(restr[i][len(restr[i])-1])         #pega somente o ultimo elemento de restr
b = np.array(b)                                 #transformando em objeto np.array para ser utilizável

#Criando matriz de coeficientes das variáveis

A = [[[]for i in range(0)] for j in range(qRes)]
for i in range(len(restr)):
    for j in range(len(restr[i])-1):
        A[i].append(restr[i][j])



#============= 2: Passando para a forma padrao ===========================================================

mi = np.eye(len(A)) #mi -> matriz identidade
mi = mi * -1                                    #as variaveis de sobra tem coef negativos (por causa do >=)

for i in range(len(A)):
    qVarss = qVarss + 1                         #add uma variavel de sobra p/ cada restricao
    coefZ.append(0)                             #add o coef 0 para cada variável de sobra na função objetivo (Z)
    A[i].extend(mi[i])                          #add matriz identidade nas restricoes (valor de cada variavel nova)

    
#============= 3: Resolvendo ==============================================================================

solutions = []

#Criando matriz transposta com vetores coeficientes de cada variável
At = np.array(A)                                #Declarando At -> matriz transposta de A
At = At.T                                       #Calculando transposta de A
At = np.array(At).tolist()                      #transforma de np.array para lista para ficar mais facil de manipular


for i in range(len(At)):                        #adicionando o indice da variavel correspondente a cada vetor
    At[i].append(i+1)

#criando combinacoes com os vetores de coeficientes das variáveis
combinacoes = combinations(At, qRes)
comb = []                                       #comb = combinacoes feitas com as colunas de A (linhas de At)
for i in combinacoes:
    comb.append(i)

#resolvendo (XB = invB * b):
for i in range(len(comb)):
    
    m = comb[i]                                 #m -> Matriz de cada combinação gerada
    Bt = []                                     #Bt -> B transposta
    x = []                                      #x -> indice da variavel
    for i in range(len(m)):
        Bt.append(m[i][:-1])                    #adiciona o vetor sem o indice da var
        x.append(m[i][-1])                      #aponta o indice da variável da combinação atual

    B = np.array(Bt)                            #B = matriz com as bases (colunas de A)
    B = B.T                                     #desfaz a transposicao das colunas de A
    B = np.array(B).tolist()                    #transforma de np.array para lista normal
        
    if (np.linalg.det(B) != 0):                 #se o determinante nao for zero, ou seja, se for uma base
            
        iB = np.linalg.inv(B)                   #iB -> matriz inversa de B
        XB = np.dot(iB, b)

        for i in range(len(XB)):                
            print(f"x{x[i]} = {XB[i]}")

#aplicando o resultado na funcao objetivo(Z):
        resultZ = 0                             #resultZ -> Resultados de Z
        for i in range(len(XB)):
            resultZ += XB[i] * coefZ[x[i]-1]    #Multiplicando a variável pelo coeficiente correspondente

        print("Solucao = ", resultZ)

#============= 4: Enumerando os resultados ==============================================================================

#Xb, x e Z ja sao exibidos anteriormente

#Definindo solução como viável ou inviável
        viable = True
        for i in XB:
            if (i < 0):                         #Inviavel caso contenha alguma variável negativa
                viable = False
                print("É uma solucao inviavel \n\n")
                break
        if (viable == True):                    #Viável caso todas as variáveis sejam positivas
            print("É uma solucao viavel \n\n")
            solutions.append(resultZ)

#============= 5: indicando a solucao otima ==============================================================================

solutions = np.array(solutions)

print(f"Solucoes viaveis: {len(solutions)}")

if len(solutions) != 0:
    optimum = np.max(solutions)                     #seleciona a solucao de valor mais alto
    qOptimum = 0                                    #qOptimum -> Quantidade de soluções ótimas

    for i in solutions:
        if i == optimum:
            qOptimum += 1

    print(f"Solucao otima: {optimum}\nQuantidade de solucoes otimas: {qOptimum}\n")                    
