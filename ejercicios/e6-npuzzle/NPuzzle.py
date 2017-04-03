import copy


class Node:
    def __init__(self, tablero):
        self.tablero = tablero
        self.parent = None
        self.H = 0
        self.G = 0

    def setParent(self, pParent):
        self.parent = pParent

    def move_cost(self, other):
        return 1


def leerTablero():
    largo = int(input())
    tablero = []
    for i in range(0, largo):
        fila = []
        for j in range(0, largo):
            fila.append(int(input()))
        tablero.append(fila)

    print(tablero)
    return tablero


def getCostoTotal(nodo):
    largo = len(nodo.tablero)
    costoTotal = 0

    for i in range(0, largo):
        for j in range(0, largo):
            posicionActual = [i, j]
            posicionDeseada = getPosicionDeseada(largo, nodo.tablero[i][j])
            costoTotal += getDistanciaEntrePosiciones(posicionActual, posicionDeseada)
    return costoTotal


def getPosicionDeseada(largo, numero):
    fila = (numero) // largo
    columna = (numero) % largo
    return [fila, columna]


def getDistanciaEntrePosiciones(pos1, pos2):
    distancia = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    return distancia


def getIndiceDeNodoMenosCostoso(listaDeNodos):
    indice = -99
    costoMenor = 9999
    for i in range(0, len(listaDeNodos)):
        costoActual = getCostoTotal(listaDeNodos[i])
        if costoActual < costoMenor:
            costoMenor = costoActual
            indice = i
    return i


def getPosicionCero(tablero):
    largo = len(tablero)
    for i in range(0, largo):
        for j in range(0, largo):
            if tablero[i][j] == 0:
                return [i, j]
    print("No se encontró cero.")
    return [-1, -1]


def getPosiblesMovimientos(tablero):
    nodosVecinos = []
    posicionCero = getPosicionCero(tablero)

    if posicionCero[0] > 0:  # Arriba
        tabArriba = copy.deepcopy(tablero)
        numPasado = tablero[posicionCero[0] - 1][posicionCero[1]]
        tabArriba[posicionCero[0] - 1][posicionCero[1]] = 0
        tabArriba[posicionCero[0]][posicionCero[1]] = numPasado
        # print("Arriba: " + str(tabArriba))
        nodosVecinos.append(Node(tabArriba))

    if posicionCero[1] < (len(tablero) - 1):  # Derecha
        tabDerecha = copy.deepcopy(tablero)
        numPasado = tabDerecha[posicionCero[0]][posicionCero[1] + 1]
        tabDerecha[posicionCero[0]][posicionCero[1] + 1] = 0
        tabDerecha[posicionCero[0]][posicionCero[1]] = numPasado
        # print("Derecha: " + str(tabDerecha))
        nodosVecinos.append(Node(tabDerecha))

    if posicionCero[0] < (len(tablero) - 1):  # Abajo
        tabAbajo = copy.deepcopy(tablero)
        numPasado = tabAbajo[posicionCero[0] + 1][posicionCero[1]]
        tabAbajo[posicionCero[0] + 1][posicionCero[1]] = 0
        tabAbajo[posicionCero[0]][posicionCero[1]] = numPasado
        # print("Abajo: " + str(tabAbajo))
        nodosVecinos.append(Node(tabAbajo))

    if posicionCero[1] > 0:  # Izquierda
        tabIzquierda = copy.deepcopy(tablero)
        numPasado = tablero[posicionCero[0]][posicionCero[1] - 1]
        tabIzquierda[posicionCero[0]][posicionCero[1] - 1] = 0
        tabIzquierda[posicionCero[0]][posicionCero[1]] = numPasado
        # print("Izquierda: " + str(tabIzquierda))
        nodosVecinos.append(Node(tabIzquierda))

    return nodosVecinos


def getIndiceNodoAntiguo(nodoGemelo, abiertos):
    for i in range(0, len(abiertos)):
        if abiertos[i].tablero == nodoGemelo.tablero:
            return i
    print("No se encontro nodo con tablero igual")
    return -99


def nodoEstaEnLista(nodo, lista):
    for i in range(0, len(lista)):
        if lista[i].tablero == nodo.tablero:
            return True
    return False


def estimarPath(primerNodo):
    abiertos = [primerNodo]
    cerrados = []

    while (abiertos != []):
        indice = getIndiceDeNodoMenosCostoso(abiertos)
        nodoActual = abiertos[indice]

        costoEnEsteMomento = getCostoTotal(nodoActual)
        print(costoEnEsteMomento)

        if (costoEnEsteMomento == 0):
            break

        cerrados.append(abiertos[indice])
        del abiertos[indice]

        nodosProbables = getPosiblesMovimientos(nodoActual.tablero)
        # print("***")
        for nodoVecino in nodosProbables:
            # print(nodoVecino.tablero)
            if not nodoEstaEnLista(nodoVecino, cerrados):
                if not nodoEstaEnLista(nodoVecino, abiertos):
                    nodoVecino.setParent(nodoActual)
                    nodoVecino.G = nodoVecino.parent.G + 1
                    nodoVecino.H = getCostoTotal(nodoVecino)
                    abiertos.append(nodoVecino)
                else:
                    indiceNodoAntiguo = getIndiceNodoAntiguo(nodoVecino, abiertos)
                    FAntiguo = abiertos[indiceNodoAntiguo].H + abiertos[indiceNodoAntiguo].G
                    FNuevo = nodoVecino.H + nodoVecino.G
                    if FNuevo < FAntiguo:
                        nodoVecino.setParent(nodoActual)
                        nodoVecino.G = nodoVecino.parent.G + 1
                        nodoVecino.H = getCostoTotal(nodoVecino)
                        abiertos[indiceNodoAntiguo] = nodoVecino


tablero = leerTablero()
nodoInicial = Node(tablero)
estimarPath(nodoInicial)
