from tkinter import *
from random import randint
from threading import Thread
import time
import os

class Cliente:

    def __init__(self, posicion, destino):
        self.posicion = posicion
        self.destino = destino

class Nodo:
    def __init__(self, posicion, parent=None, g=None):
        self.posicion = posicion
        self.g = g
        self.f = None
        self.parent = parent

def mostrarPanel():
    global tablero
    top = Tk()
    top.geometry("100x80")
    #L1 = Label(top, text="Instrucción: ")
    #L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=TOP)
    B3 = Button(top, text="Ejecutar", command=lambda: ejecutar(E1.get()))
    B3.place(x=40, y=40)
    top.mainloop()

def ejecutar(comando):
    if type(comando) == str:
        comando = comando.split(" ")
        if comando[0] == "clientes": # CLIENTES N
            cantidad = int(comando[1])
            agregarClientesAleatorios(cantidad)
        if comando[0] == "cliente": # CLIENTE CUADRA DESTINO
            nombreOrigen = comando[1]
            nombreDestino = comando[2]
            agregarClienteNuevo(nombreOrigen, nombreDestino)
        if comando[0] == "pasear": # PASEAR
            t3 = Thread(target=pasear)
            t3.daemon = True
            t3.start()
        if comando[0] == "parar": # PARAR
            dejarDePasear()
        if comando[0] == "parquear": # PARQUEAR CUADRA
            cuadra = comando[1]
            t2 = Thread(target=parquear, args=[getPosicion(cuadra)])
            t2.daemon = True
            t2.start()
        if comando[0] == "mostrar":
            if comando[1] == "on":
                activarMostrarRecorrido()
            elif comando[1] == "off":
                desactivarMostrarRecorrido()
                borrarRecorrido()
                imprimirTablero(getPosicion(simboloTaxi))
        if comando[0] == "ruta":
            if comando[1] == "on":
                activarMostrarRuta()
            elif comando[1] == "off":
                desactivarMostrarRuta()
                borrarRuta()
                imprimirTablero(getPosicion(simboloTaxi))
        if comando[0] == "animar":
            cambiarVelocidad(int(comando[1]))
        if comando[0] == "buscar":
            t4 = Thread(target=buscarTodosLosClientes)
            t4.daemon = True
            t4.start()

def getTablero():
    with open("entrada.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x for x in content]
    tab = llenarEspacios(content)
    if tab == None:
        print("ERROR DE ENTRADA: Solo puede haber un taxi (Con símbolo T)")
    else:
        return tab
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
    contadorTaxis = 0
    for i in range(0, len(tablero)):
        term = False
        linea = list(tablero[i])
        for j in range(0, len(linea)):
            if contadorTaxis > 1:
                return None
            if tablero[i][j] == 'T':
                contadorTaxis += 1
            if term == True:
                linea[j] = ' '
            if(tablero[i][j] == '\n'):
                linea[j] = ' '
                term = True
        tablero[i] = linea
    return tablero

def getPosicion(nombre):
    global tablero
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

def getPosicionesVisitables(posicion):
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
                tablero[i][j] = simboloTaxi
                print(simboloTaxi, end='')
            else:
                if tablero[i][j] == simboloTaxi:
                    print(' ', end='')
                    tablero[i][j] = ' '
                else:
                    print(tablero[i][j], end='')
        print("\n",end='')

def imprimirTableroConCamino(posicion):
    clear = lambda: os.system('cls')
    clear()
    global tablero
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero[i])):
            if i == posicion[0] and j == posicion[1]:
                tablero[i][j] = simboloTaxi
                print(simboloTaxi, end='')
            else:
                if tablero[i][j] == simboloTaxi:
                    print('*', end='')
                    tablero[i][j] = '*'
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

def activarMostrarRecorrido():
    global mostrarCaminoRecorrido
    mostrarCaminoRecorrido = True

def desactivarMostrarRecorrido():
    global mostrarCaminoRecorrido
    mostrarCaminoRecorrido = False

def activarMostrarRuta():
    global mostrarRuta
    mostrarRuta = True

def desactivarMostrarRuta():
    global mostrarRuta
    mostrarRuta = False

def pasear():
    global tablero
    borrarRuta()
    borrarRecorrido()
    explorados = []

    elegido = getPosicion(simboloTaxi)
    global seguirPaseando
    seguirPaseando = True

    while seguirPaseando:
        posActual = elegido
        explorados.append(posActual)
        time.sleep(velocidadAnimacion/1000)
        imprimirTablero(posActual)
        vecinos = getPosicionesVisitables(posActual)
        if todosLosVecinosExplorados(vecinos, explorados):
            del explorados[:]

        elegido = vecinos[randint(0,len(vecinos)-1)]
        while(elegido in explorados):
            elegido = vecinos[randint(0, len(vecinos) - 1)]

def dejarDeBuscar():
    global seguirBuscando
    seguirBuscando = False

def buscarTodosLosClientes():
    global seguirBuscando
    seguirBuscando = True

    while seguirBuscando or len(listaClientes) == 0:
        buscarClientes()

def buscarClientes():
    global tablero
    explorados = []
    elegido = getPosicion(simboloTaxi)
    while seguirBuscando:
        posActual = elegido
        if tablero[posActual[0]-1][posActual[1]] == 'o':
            dejarDePasear()
            posCliente = [posActual[0]-1,posActual[1]]
            llevarClienteADestino(posCliente)
            #seguirBuscando = False
            break

        elif tablero[posActual[0]][posActual[1]+1] == 'o':
            dejarDePasear()
            posCliente = [posActual[0],posActual[1]+1]
            llevarClienteADestino(posCliente)
            #seguirBuscando = False
            break

        elif tablero[posActual[0]+1][posActual[1]] == 'o':
            dejarDePasear()
            posCliente = [posActual[0]+1,posActual[1]]
            llevarClienteADestino(posCliente)
            #seguirBuscando = False
            break

        elif tablero[posActual[0]][posActual[1]-1] == 'o':
            dejarDePasear()
            posCliente = [posActual[0],posActual[1]-1]
            llevarClienteADestino(posCliente)
            #seguirBuscando = False
            break

        explorados.append(posActual)
        time.sleep(velocidadAnimacion / 1000)
        imprimirTablero(posActual)
        vecinos = getPosicionesVisitables(posActual)
        if todosLosVecinosExplorados(vecinos, explorados):
            del explorados[:]

        elegido = vecinos[randint(0, len(vecinos) - 1)]
        while (elegido in explorados):
            elegido = vecinos[randint(0, len(vecinos) - 1)]

def getDestinoCliente(posicionCliente):
    for cliente in listaClientes:
        if cliente.posicion == posicionCliente:
            return cliente.destino

def getPosicionManzana(posCuadra):
    if tablero[posCuadra[0]][posCuadra[1] + 1] in "o-":
        if tablero[posCuadra[0]][posCuadra[1] + 2] in "o-":
            if tablero[posCuadra[0] + 1][posCuadra[1] + 2] == '|':
                return [posCuadra[0] + 1,posCuadra[1] + 1]
            else:
                return [posCuadra[0] - 1, posCuadra[1] + 1]
        else:
            if tablero[posCuadra[0] + 1][posCuadra[1] + 1] == '|':
                return [posCuadra[0] + 1,posCuadra[1]]
            else:
                return [posCuadra[0] - 1,posCuadra[1]]
    else:
        if tablero[posCuadra[0]+1][posCuadra[1]] in "|":
            return [posCuadra[0] + 1,posCuadra[1] - 1]
        else:
            return [posCuadra[0] - 1,posCuadra[1] - 1]

def actualizarSimboloTaxi():
    global simboloTaxi
    global tablero
    for i in range(0, len(tablero)-1):
        for j in range(0, len(tablero[i])-1):
            if tablero[i][j] == simboloTaxiOcupado:
                tablero[i][j] = simboloTaxiLibre
                break
            if tablero[i][j] == simboloTaxiLibre:
                tablero[i][j] = simboloTaxiOcupado
                break
    #print("El nuevo simbolo del taxi es: " + simboloTaxi)

def eliminarCliente(posicion, destino):
    global listaClientes
    global seguirBuscando
    if len(listaClientes) == 1:
        seguirBuscando = False
    for i in range(0, len(listaClientes)):
        if listaClientes[i].posicion == posicion:
            del listaClientes[i]
            break


def llevarClienteADestino(posicionCliente):
    global tablero
    global estaDejandoCliente
    global simboloTaxi
    simboloTaxi = simboloTaxiOcupado
    actualizarSimboloTaxi()
    estaDejandoCliente = True
    tablero[posicionCliente[0]][posicionCliente[1]] = '-'
    imprimirTablero(getPosicion(simboloTaxi))
    destinoCliente = getDestinoCliente(posicionCliente)
    print("El destino del cliente es: " + str(destinoCliente))
    parquear(destinoCliente)
    dejarCliente(destinoCliente)
    eliminarCliente(posicionCliente, destinoCliente)

def detener():
    global detenerse
    detenerse = True

def getPosicionesDeClientesPosibles():
    listaPosiciones = []
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero[i])):
            #print(tablero[i][j])
            if tablero[i][j] == '-':
                listaPosiciones.append([i, j])
    return listaPosiciones

def agregarClienteATablero(cliente):
    global tablero
    posicion = cliente.posicion
    #print(posicion)
    tablero[posicion[0]][posicion[1]] = 'o'

def agregarClientesAleatorios(cantidad):
    global listaClientes
    posPosibles = getPosicionesDeClientesPosibles()
    for i in range(0, cantidad):
        posicionCliente = [-1,-1]
        destino = [-1, -1]
        while(posicionCliente == destino):
            posicionCliente = posPosibles[randint(0, len(posPosibles)-1)]
            destino = posPosibles[randint(0, len(posPosibles)-1)]
        cliente = Cliente(posicionCliente, destino)
        listaClientes.append(cliente)
        agregarClienteATablero(cliente)

    imprimirTablero(getPosicion(simboloTaxi))

def getUbicacionesPosiblesEnCuadra(nombreCuadra):
    global tablero
    posicion = getPosicion(nombreCuadra)
    listaUbicaciones = []
    listaUbicaciones.append([posicion[0] - 1, posicion[1] - 1])
    listaUbicaciones.append([posicion[0] - 1, posicion[1]])
    listaUbicaciones.append([posicion[0] - 1, posicion[1] + 1])
    listaUbicaciones.append([posicion[0] + 1, posicion[1] - 1])
    listaUbicaciones.append([posicion[0] + 1, posicion[1]])
    listaUbicaciones.append([posicion[0] + 1, posicion[1] + 1])
    return listaUbicaciones

def agregarClienteNuevo(nombreCuadra, nombreDestino):
    ubicacionesPosibles = getUbicacionesPosiblesEnCuadra(nombreCuadra)
    ubicacionExacta = ubicacionesPosibles[randint(0,len(ubicacionesPosibles)-1)]

    destinosPosibles = getUbicacionesPosiblesEnCuadra(nombreDestino)
    destinoExacto = destinosPosibles[randint(0, len(destinosPosibles) - 1)]

    cliente = Cliente(ubicacionExacta, destinoExacto)
    global listaClientes
    listaClientes.append(cliente)
    agregarClienteATablero(cliente)
    imprimirTablero(getPosicion('T7'))

def distanciaEntrePosiciones(posA, posB):
    distancia = abs(posA[0]-posB[0]) + abs(posA[1]-posB[1])
    return distancia

def eliminarNodo(nodoAEliminar, lista):
    for i in range(0, len(lista)-1):
        if lista[i].posicion == nodoAEliminar.posicion:
            del lista[i]
    return lista

def getNodoMenosCostoso(lista):
    nodoMenosCostoso = None
    costo = 999999
    for nodo in lista:
        if nodo.f < costo:
            nodoMenosCostoso = nodo
            costo = nodo.f
    return nodoMenosCostoso

def nodoEstaEnLista(nodo, lista):
    for i in lista:
        if i.posicion == nodo.posicion:
            return True
    return False

def getNodoEnLista(nodo, lista):
    for i in lista:
        if i.posicion == nodo.posicion:
            return i
    print("NO SE ENCONTRÓ EL NODO")

def getNodosVecinos(nodo):
    posVisitables = []
    fila = nodo.posicion[0]
    columna = nodo.posicion[1]
    #print([fila,columna])
    if tablero[fila-1][columna] not in "_-|o*+/": #Arriba
        posVisitables.append(Nodo([fila-1,columna], nodo, nodo.g + 1))
    if tablero[fila][columna+1] not in "_-|o*+/": #Derecha
        posVisitables.append(Nodo([fila,columna+1], nodo, nodo.g + 1))
    if tablero[fila+1][columna] not in "_-|o*+/": #Abajo
        posVisitables.append(Nodo([fila+1,columna], nodo, nodo.g + 1))
    if tablero[fila][columna-1] not in "_-|o*+/": #Izquierda
        posVisitables.append(Nodo([fila,columna-1], nodo, nodo.g + 1))
    return posVisitables

def construirCamino(nodo):
    camino = [nodo.posicion]
    while nodo.parent != None:
        nodo = nodo.parent
        camino.append(nodo.posicion)
    return camino

def borrarRuta():
    global tablero
    for i in range(0, len(tablero) - 1):
        for j in range(0, len(tablero[i]) - 1):
            if tablero[i][j] == '+':
                tablero[i][j] = ' '

def borrarRecorrido():
    global tablero
    for i in range(0, len(tablero) - 1):
        for j in range(0, len(tablero[i]) - 1):
            if tablero[i][j] == '*':
                tablero[i][j] = ' '

def dibujarRuta(camino):
    global tablero
    posTaxi = getPosicion(simboloTaxi)
    llego = False
    for i in range(0,len(camino)-1):
        if llego:
            tablero[camino[i][0]][camino[i][1]] = '+'
        if  camino[i] == posTaxi:
            llego = True

def moverseAPosicion(posDestino): #A*
    start = Nodo(getPosicion(simboloTaxi))
    open = [start]
    closed = []
    start.g = 0
    start.f = start.g + distanciaEntrePosiciones(start.posicion, posDestino)
    while open != []:
        current = getNodoMenosCostoso(open)
        if current.posicion == posDestino:
            return construirCamino(current)
        open = eliminarNodo(current, open)
        closed.append(current)
        vecinos = getNodosVecinos(current)
        for vecino in vecinos:
            if not nodoEstaEnLista(vecino, closed):
                vecino.f = vecino.g + distanciaEntrePosiciones(vecino.posicion, posDestino)
                if not nodoEstaEnLista(vecino, open):
                    open.append(vecino)
                else:
                    openVecino = getNodoEnLista(vecino, open)
                    if vecino.g < openVecino.g:
                        openVecino.g = vecino.g
                        openVecino.parent = vecino.parent
    return False

def getPosicionFrenteADestino(destino):
    if tablero[destino[0]][destino[1] + 1] in "o-":
        if tablero[destino[0]][destino[1] + 2] in "o-":
            if tablero[destino[0] + 1][destino[1] + 2] == '|':
                return [destino[0] - 1,destino[1]]
            else:
                return [destino[0] + 1, destino[1]]
        else:
            if tablero[destino[0] + 1][destino[1] + 1] == '|':
                return [destino[0] - 1, destino[1]]
            else:
                return [destino[0] + 1, destino[1]]
    else:
        if tablero[destino[0]+1][destino[1]] in "|":
            return [destino[0] - 1, destino[1]]
        else:
            return [destino[0] + 1, destino[1]]

def parquear(posCuadra):
    global detenerse
    global tablero
    global estaDejandoCliente
    detenerse = False
    borrarRuta()
    borrarRecorrido()
    dejarDePasear()
    posicionActual = getPosicion(simboloTaxi)
    destino = posCuadra
    if estaDejandoCliente:
        #ENTONCES posCuadra es la ubicación exacta donde el cliente quiere llegar
        destino = getPosicionFrenteADestino(destino)
        estaDejandoCliente = False
    else:
        # ENTONCES posCuadra es la ubicación de la manzana en sí
        destinoArriba = [destino[0]-2, destino[1]]
        destinoAbajo = [destino[0]+2, destino[1]]
        distanciaArriba = distanciaEntrePosiciones(posicionActual, destinoArriba)
        distanciaAbajo = distanciaEntrePosiciones(posicionActual, destinoAbajo)
        if distanciaAbajo > distanciaArriba:
            destino = destinoArriba
        else:
            destino = destinoAbajo
    caminoMasCorto = list(reversed(moverseAPosicion(destino)))
    #print(caminoMasCorto)
    for posicion in caminoMasCorto:
        time.sleep(velocidadAnimacion/1000)
        if(detenerse):
            break
        if(mostrarRuta):
            dibujarRuta(caminoMasCorto)
        else:
            borrarRuta()

        if(mostrarCaminoRecorrido):
            imprimirTableroConCamino(posicion)
        else:
            borrarRecorrido()
            imprimirTablero(posicion)

def dejarCliente(posCuadra): #Alternativa de pasear
    global simboloTaxi
    tablero[posCuadra[0]][posCuadra[1]] = '☻'
    imprimirTablero(getPosicion(simboloTaxi))
    time.sleep(1.5)
    simboloTaxi = simboloTaxiLibre
    actualizarSimboloTaxi()
    tablero[posCuadra[0]][posCuadra[1]] = '-'
    imprimirTablero(getPosicion(simboloTaxi))

def getClientesOriginales():
    listaPosiciones = []
    for i in range(0, len(tablero)-1):
        for j in range(0, len(tablero[i])):
            if tablero[i][j] == 'o':
                listaPosiciones.append([i, j])
    return listaPosiciones

def asignarDestinosAClientes():
    global listaClientes
    posicionesClientes = getClientesOriginales()
    posPosibles = getPosicionesDeClientesPosibles()
    for posCliente in posicionesClientes:
        destino = posCliente
        while (posCliente == destino):
            destino = posPosibles[randint(0, len(posPosibles) - 1)]
        cliente = Cliente(posCliente, destino)
        listaClientes.append(cliente)
        #agregarClienteATablero(cliente)

def cambiarVelocidad(velocidad):
    global detenerse
    global velocidadAnimacion
    global seguirBuscando

    if velocidad == 0:
        dejarDePasear()
        desactivarMostrarRecorrido()
        desactivarMostrarRuta()
        detenerse = True
        dejarDeBuscar()
        imprimirTablero(getPosicion(simboloTaxi))
    else:
        detenerse = False
        velocidadAnimacion = velocidad

def main():
    global tablero
    global listaClientes
    global mostrarCaminoRecorrido
    global mostrarRuta
    global velocidadAnimacion
    global detenerse
    global estaDejandoCliente
    global simboloTaxi
    global simboloTaxiLibre
    global simboloTaxiOcupado

    simboloTaxiOcupado = '♥'
    simboloTaxiLibre = 'T'
    simboloTaxi = simboloTaxiLibre

    estaDejandoCliente = False
    detenerse = False
    velocidadAnimacion = 500
    mostrarCaminoRecorrido = False
    mostrarRuta = False
    listaClientes = []
    tablero = getTablero()
    if tablero != None:
        asignarDestinosAClientes()
        mostrarPanel()

main()
