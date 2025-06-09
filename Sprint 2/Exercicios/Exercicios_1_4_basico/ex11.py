'''
Exercícios Parte 1
Escreva uma função que recebe como parâmetro uma lista e retorna 3 listas: a lista recebida 
dividida em 3 partes iguais. Teste sua implementação com a lista abaixo

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
'''

def divide_em_tres_partes(lista):

    tamanho = len(lista)
    parte = tamanho // 3
    
    parte1 = lista[:parte]
    parte2 = lista[parte:2*parte]
    parte3 = lista[2*parte:]
    
    return parte1, parte2, parte3


lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

p1, p2, p3 = divide_em_tres_partes(lista)

print(p1, p2, p3)
