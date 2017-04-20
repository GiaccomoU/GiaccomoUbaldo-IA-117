from tkinter import *
from random import randint
from threading import Thread
import time
import os

class Cliente:

    def __init__(self, posicion, destino):
        self.posicion = posicion
        self.destino = destino



def mostrarPanel():
    global tablero
    top = Tk()
    top.geometry("300x300")
    #L1 = Label(top, text="Instrucción: ")
    #L1.pack(side=LEFT)
    #E1 = Entry(top, bd=5)
    #E1.pack(side=RIGHT)
    B1 = Button(top, text="Pasear", command= lambda: mandar(1))
    B1.place(x=80, y=80)
    B2 = Button(top, text="Dejar de Pasear", command=dejarDePasear)
    B2.place(x=50, y=50)
    top.mainloop()

def getTablero():
    with open("entrada.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x for x in content]
    return llenarEspacios(content)
    #return content

def insertarEntre(lista, elementos, pos):
    nuevaLista = []
    for i in range(0, len(lista)):
        nuevaLista.append(lista[i])
        if i == pos:
            for elemento in elementos:
                nuevaLista.append(elemento)
    return nuevaLista

def getIntermedios(posA, posB):
    if posA == posB or sonVecinos(posA, posB):
        return []
    else:
        listaIntermedios = []
        if posA[0] < posB[0]:
            contador = posA[0]
            while contador < posB[0]:
                contador += 1
                listaIntermedios.append([contador, posA[1]])
        if posA[0] > posB[0]:
            contador = posB[0]
            while contador < posA[0]:
                contador += 1
                listaIntermedios.append([contador, posB[1]])
        if posA[1] < posB[1]:
            contador = posA[1]
            while contador < posB[1]:
                contador += 1
                listaIntermedios.append([posA[0], contador])
        if posA[1] > posB[1]:
            contador = posB[1]
            while contador < posA[1]:
                contador += 1
                listaIntermedios.append([posB[0], contador])

        if not sonVecinos(listaIntermedios[0], posA):
            listaIntermedios = list(reversed(listaIntermedios))
            return listaIntermedios[1:]
        else:
            return listaIntermedios[:-1]

def generarTrayecto(listaDePosiciones):
    if len(listaDePosiciones) <= 1:
        return listaDePosiciones
    else:
        i = 0
        j = 1
        while(j < len(listaDePosiciones)):
            if not sonVecinos(listaDePosiciones[i], listaDePosiciones[j]):
                listaDeIntermedios = getIntermedios(listaDePosiciones[i], listaDePosiciones[j])
                listaDePosiciones = insertarEntre(listaDePosiciones, listaDeIntermedios, i)
            i += 1
            j += 1
        return listaDePosiciones

def llenarEspacios(tablero):
    for i in range(0, len(tablero)):
        term = False
        #print("wat")
        linea = list(tablero[i])
        for j in range(0, len(linea)):
            #print("khe")
            if term == True:
                linea[j] = '*'
            if(tablero[i][j] == '\n'):
                linea[j] = '*'
                term = True
        tablero[i] = linea
    return tablero

def getPosicion(nombre, tablero):
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero[i])):
            if tablero[i][j] == nombre:
                return [i, j]
    return [-1,-1]

def sonVecinos(posA, posB):
    if posA == posB:
        return False
    if abs(posA[0]-posB[0]) <= 1 and abs(posA[1]-posB[1]) <= 1:
        return True
    else:
        return False

def getPosicionesVisitables(tablero, posicion):
    posVisitables = []
    fila = posicion[0]
    columna = posicion[1]
    if tablero[fila-1][columna] not in "_-|o*+/": #Arriba
        posVisitables.append([fila-1,columna])
    if tablero[fila][columna+1] not in "_-|o*+/": #Derecha
        posVisitables.append([fila,columna+1])
    if tablero[fila+1][columna] not in "_-|o*+/": #Abajo
        posVisitables.append([fila+1,columna])
    if tablero[fila][columna-1] not in "_-|o*+/": #Izquierda
        posVisitables.append([fila,columna-1])

    #print(posVisitables)
    return posVisitables

def imprimirTablero(posicion):
    clear = lambda: os.system('cls')
    clear()
    global tablero
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero[i])):
            if i == posicion[0] and j == posicion[1]:
                tablero[i][j] = 'T'
                print('T', end='')
            else:
                if tablero[i][j] == 'T': #Si es el taxi
                    print(' ', end='')
                    tablero[i][j] = ' '
                else:
                    print(tablero[i][j], end='')
        print("\n",end='')

def todosLosVecinosExplorados(vecinos, explorados):
    for i in vecinos:
        if i not in explorados:
            return False
    return True

def dejarDePasear():
    global seguirPaseando
    seguirPaseando = False

def mandar(opcion):
    if opcion == 1:
        t2 = Thread(target=pasear)
        t2.daemon = True
        t2.start()

def pasear():
    global tablero
    explorados = []

    elegido = getPosicion('T', tablero)
    global seguirPaseando
    seguirPaseando = True

    while seguirPaseando:
        posActual = elegido
        explorados.append(posActual)
        time.sleep(0.5)
        imprimirTablero(posActual)
        global posTaxi
        posTaxi = posActual

        vecinos = getPosicionesVisitables(tablero, posActual)
        if todosLosVecinosExplorados(vecinos, explorados):
            del explorados[:]

        elegido = vecinos[randint(0,len(vecinos)-1)]
        while(elegido in explorados):
            elegido = vecinos[randint(0, len(vecinos) - 1)]


'''
def agregarClientesAleatorios(cantidad):
    for i in range(0, cantidad):
        posicion = [randint(), randint()]
        while(tablero[posicion[0]][posicion[1]] == 'o'):
            random =

'''
global tablero
tablero = getTablero()
mostrarPanel()
