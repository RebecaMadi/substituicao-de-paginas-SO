#REBECA MADI OLIVEIRA
#FORMATO DE ENTRADA: python3 paginacao.py arquivo.txt
import sys

# Tamanho da memória 
memoria_size = 8000

# Inicializa a memória como vazia
memoria = []
memoria2 = []
memoria3 = []

def inicia(m):
    for i in range(memoria_size):
        m.append((-1,-1))

def iniciaZeros(m):
    for i in range(memoria_size):
        m.append((0,0))

# Função que implementa o FIFO
def fifo(page_references):
    page_faults = 0
    pos = 0
    for reference in page_references:
        if reference not in memoria:
            page_faults += 1
            if pos == memoria_size:
                frame_to_replace = 0
                pos = 1
            else:
                frame_to_replace = pos
                pos += 1
            memoria[frame_to_replace] = reference
    return page_faults

# Função que implementa o LRU (Least Recently Used)
def lru(page_references):
    #Se não ta na fila de usadas então insere, se ta traz pra frente
    page_faults = 0
    time_stamp = 0
    tam = 0
    last_used = []
    for reference in page_references:
        if reference not in memoria2:
            page_faults += 1
            if(tam == memoria_size):
                time_stamp = last_used[len(last_used)-1]
                last_used.pop()
            else:
                time_stamp = tam
                tam +=1
            memoria2[time_stamp] = reference
            last_used.insert(0, time_stamp)
        else:
            index = memoria2.index(reference, 0)
            if index in last_used:
                i = last_used.index(index)
                last_used.pop(i)
            last_used.insert(0, index)
            #print(last_used)
    return page_faults

# Função que implementa o Segunda Chance (ou Relógio)
def segunda_chance(page_references):
    page_faults = 0
    hand = 0
    reference_bit  = []
    iniciaZeros(reference_bit)
    for reference in page_references:
        if reference not in memoria3:
            page_faults += 1
            while True:
                if reference_bit[hand] == (0,0):
                    memoria3[hand] = reference
                    reference_bit[hand] = (1,1)
                    break
                else:
                    reference_bit[hand] = (0,0)
                hand = (hand + 1) % memoria_size
    return page_faults

#inicia a string de referencia
size_references = 0
string_referencia = []

#Abre o arquivo e preenche a string de referência
nome = sys.argv[1]
print(nome)
file = open(nome, "r")
text = file.read()
word = ""
processo = -1
pagina = -1
for char in text:
    if char == ';':
        size_references += 1
        pagina = int(word)
        string_referencia.append((processo, pagina))
        word = ""
    if char == ',':
        processo = int(word)
        word = ""
    if char != ';':
        if char != ',':
            word += char

#Inicia a memoria
inicia(memoria)
if(string_referencia[size_references-1]==(0,0)):
        string_referencia.pop(size_references-1)

# Executa e exibe o número de page faults para FIFO
page_faults_fifo = fifo(string_referencia)
print(f"Page Faults FIFO: {page_faults_fifo}")

# Reinicializa a memória
inicia(memoria2)

# Executa e exibe o número de page faults para LRU
page_faults_lru = lru(string_referencia)
print(f"Page Faults LRU: {page_faults_lru}")

# Reinicializa a memória
inicia(memoria3)

# Executa e exibe o número de page faults para Segunda Chance
page_faults_segunda_chance = segunda_chance(string_referencia)
print(f"Page Faults Relogio: {page_faults_segunda_chance}")
