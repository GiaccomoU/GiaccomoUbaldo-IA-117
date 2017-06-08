from random import randint
from random import uniform
import time

class Cliente:
    def __init__(self, posicionActual, vivienda, trabajo, horaTrabajo=uniform(0.2, 0.35)):
        self.vivienda = vivienda
        self.trabajo = trabajo
        self.horaTrabajo = horaTrabajo #porcentaje
        self.posicionActual = posicionActual

    def estaEnElTrabajo(self):
        if self.posicionActual == [self.trabajo[0] - 1, self.trabajo[1] - 1]:
            return True
        elif self.posicionActual == [self.trabajo[0] - 1, self.trabajo[1]]:
            return True
        elif self.posicionActual == [self.trabajo[0] - 1, self.trabajo[1] + 1]:
            return True
        elif self.posicionActual == [self.trabajo[0] + 1, self.trabajo[1] - 1]:
            return True
        elif self.posicionActual == [self.trabajo[0] + 1, self.trabajo[1]]:
            return True
        elif self.posicionActual == [self.trabajo[0] + 1, self.trabajo[1] + 1]:
            return True
        else:
            return False

    def estaEnCasa(self):
        if self.posicionActual == [self.vivienda[0] - 1, self.vivienda[1] - 1]:
            return True
        elif self.posicionActual == [self.vivienda[0] - 1, self.vivienda[1]]:
            return True
        elif self.posicionActual == [self.vivienda[0] - 1, self.vivienda[1] + 1]:
            return True
        elif self.posicionActual == [self.vivienda[0] + 1, self.vivienda[1] - 1]:
            return True
        elif self.posicionActual == [self.vivienda[0] + 1, self.vivienda[1]]:
            return True
        elif self.posicionActual == [self.vivienda[0] + 1, self.vivienda[1] + 1]:
            return True
        else:
            return False

    def getDestino(self):
        if self.estaEnElTrabajo():
            return self.vivienda
        else:
            return self.trabajo

class Taxi:
    def __init__(self, posicionActual, tieneCliente, simbolo):
        self.posicionActual = posicionActual
        self.tieneCliente = tieneCliente
        self.simbolo = simbolo
        self.caminoActual = None
        self.caminoRecorrido = [] # Lista de explorados para evitar repetir caminos

class Espacio:
    def __init__(self, cantidadDeCarros, congestionamiento, posicion):
        self.posicion = posicion
        self.cantidadDeCarros = cantidadDeCarros
        self.congestionamiento = congestionamiento

class Tiempo:
    def __init__(self, duracionDia, rangoIda, rangoVuelta):
        self.duracionDia = duracionDia
        self.rangoIda = rangoIda
        self.rangoVuelta = rangoVuelta

    def getHoraSalidaAlTrabajo(self):
        return self.rangoIda[0] * self.duracionDia

class Ciudad:
    def __init__(self, mapa, taxis, personas, edificiosTrabajo, edificiosVivienda, espacios, tiempo=Tiempo(120, [0.2, 0.3], [0.7, 0.8])):
        self.mapa = mapa
        self.taxis = taxis
        self.personas = personas
        self.edificiosTrabajo = edificiosTrabajo
        self.edificiosVivienda = edificiosVivienda
        self.tiempo = tiempo
        self.espacios = espacios

    def getClientePorPosicion(self, posicion):
        for cliente in self.personas:
            if cliente.posicionActual == posicion:
                return cliente
        print("No se encontró al cliente con esa posición.")
        return None #No se encontró

class Edificio:
    def __init__(self, posicion):
        self.posicion = posicion
        #self.cantidadHabitantes = cantidadHabitantes
        #self.tipo = tipo #VIVIENDA O TRABAJO

class EdificioVivienda(Edificio):
    def __init__(self, posicion, cantidadHabitantes):
        super(EdificioVivienda, self).__init__(posicion)
        self.cantidadHabitantes = cantidadHabitantes

class EdificioTrabajo(Edificio):
    def __init__(self, posicion):
        super(EdificioTrabajo, self).__init__(posicion)

class Nodo:
    def __init__(self, posicion, parent=None, g=None):
        self.posicion = posicion
        self.g = g
        self.f = None
        self.parent = parent

#####################################################################################

def getNodoMenosCostoso(listaDeNodos):
    nodoMenosCostoso = None
    costo = 999999
    for nodo in listaDeNodos:
        if nodo.f < costo:
            nodoMenosCostoso = nodo
            costo = nodo.f
    return nodoMenosCostoso

def eliminarNodo(nodoAEliminar, lista):
    for i in range(0, len(lista)-1):
        if lista[i].posicion == nodoAEliminar.posicion:
            del lista[i]
    return lista

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

def construirCamino(nodo):
    camino = [nodo.posicion]
    while nodo.parent != None:
        nodo = nodo.parent
        camino.append(nodo.posicion)
    return list(reversed(camino))

def getNodosVecinos(nodo, mapa):
    posVisitables = []
    fila = nodo.posicion[0]
    columna = nodo.posicion[1]
    #print([fila,columna])
    if mapa[fila-1][columna] not in "_-|o*+/": #Arriba
        posVisitables.append(Nodo([fila-1,columna], nodo, nodo.g + 1))
    if mapa[fila][columna+1] not in "_-|o*+/": #Derecha
        posVisitables.append(Nodo([fila,columna+1], nodo, nodo.g + 1))
    if mapa[fila+1][columna] not in "_-|o*+/": #Abajo
        posVisitables.append(Nodo([fila+1,columna], nodo, nodo.g + 1))
    if mapa[fila][columna-1] not in "_-|o*+/": #Izquierda
        posVisitables.append(Nodo([fila,columna-1], nodo, nodo.g + 1))
    return posVisitables

##########################################################################################

def rutaMasCorta(mapa, posInicial, posDestino): #A*
    start = Nodo(posInicial)
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
        vecinos = getNodosVecinos(current, mapa)
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

def getPosicionesVisitables(posicion, mapa):
    posVisitables = []
    fila = posicion[0]
    columna = posicion[1]
    if mapa[fila-1][columna] not in "_-|o*+/T": #Arriba
        posVisitables.append([fila-1,columna])
    if mapa[fila][columna+1] not in "_-|o*+/T": #Derecha
        posVisitables.append([fila,columna+1])
    if mapa[fila+1][columna] not in "_-|o*+/T": #Abajo
        posVisitables.append([fila+1,columna])
    if mapa[fila][columna-1] not in "_-|o*+/T": #Izquierda
        posVisitables.append([fila,columna-1])
    return posVisitables

def distanciaEntrePosiciones(posA, posB):
    distancia = abs(posA[0]-posB[0]) + abs(posA[1]-posB[1])
    return distancia

def listaEsSubconjunto(listaContenida, listaContenedora):
    for i in listaContenida:
        if i not in listaContenedora:
            return False
    return True

#####################################################################################

def getPosicionesEdificio(posEdificio):
    posiciones = []
    posiciones.append([posEdificio[0] - 1, posEdificio[1] - 1])
    posiciones.append([posEdificio[0] - 1, posEdificio[1]])
    posiciones.append([posEdificio[0] - 1, posEdificio[1] + 1])
    posiciones.append([posEdificio[0] + 1, posEdificio[1] - 1])
    posiciones.append([posEdificio[0] + 1, posEdificio[1]])
    posiciones.append([posEdificio[0] + 1, posEdificio[1] + 1])
    return posiciones

def getPosicionesLibres(ciudad):
    listaPosiciones = []
    for espacio in ciudad.espacios:
        if espacio.cantidadDeCarros == 0:
            listaPosiciones.append(espacio)
    return listaPosiciones

def ajustarPosicionLlegada(posInicial, posEdificio):
    distanciaMasCorta = 999999
    posicionMasCercana = [-1,-1]
    posicionesDisponibles = getPosicionesEdificio(posEdificio)

    for posicionDisponible in posicionesDisponibles:
        distanciaEvaluada = distanciaEntrePosiciones(posInicial, posicionDisponible)
        if distanciaEvaluada < distanciaMasCorta:
            distanciaMasCorta = distanciaEvaluada
            posicionMasCercana = posicionDisponible
    return posicionMasCercana

def moverTaxis(ciudad):
    for taxi in ciudad.taxis:
        if taxi.caminoActual == None:
            seguirBuscando(taxi, ciudad)
        elif taxi.caminoActual == []:
            taxi.caminoActual = None
            seguirBuscando(taxi, ciudad)
        else:
            taxi.posicionActual = taxi.caminoActual[0]
            taxi.caminoActual = taxi.caminoActual[1:]

def cargarCliente(posCliente, taxi, ciudad):
    ciudad.mapa[posCliente[0]][posCliente[1]] = '-'
    cliente = ciudad.getClientePorPosicion(posCliente)
    destino = ajustarPosicionLlegada(taxi.posicionActual, cliente.getDestino())
    taxi.caminoActual = rutaMasCorta(ciudad.mapa, taxi.posicionActual, destino)

def seguirBuscando(taxi, ciudad):
    posActual = taxi.posicionActual
    if ciudad.mapa[posActual[0] - 1][posActual[1]] == 'o':
        posCliente = [posActual[0] - 1, posActual[1]]
        cargarCliente(posCliente, taxi, ciudad)

    elif ciudad.mapa[posActual[0]][posActual[1] + 1] == 'o':
        posCliente = [posActual[0], posActual[1] + 1]
        cargarCliente(posCliente, taxi, ciudad)

    elif ciudad.mapa[posActual[0] + 1][posActual[1]] == 'o':
        posCliente = [posActual[0] + 1, posActual[1]]
        cargarCliente(posCliente, taxi, ciudad)

    elif ciudad.mapa[posActual[0]][posActual[1] - 1] == 'o':
        posCliente = [posActual[0], posActual[1] - 1]
        cargarCliente(posCliente, taxi, ciudad)

    if taxi.caminoActual == None:
        taxi.caminoRecorrido.append(posActual)
        vecinos = getPosicionesVisitables(posActual)
        if listaEsSubconjunto(vecinos, taxi.caminoRecorrido):
            del taxi.caminoRecorrido[:]

        elegido = vecinos[randint(0, len(vecinos) - 1)]
        while (elegido in taxi.caminoRecorrido):
            elegido = vecinos[randint(0, len(vecinos) - 1)]
        taxi.posicionActual = elegido

def agregarTaxis(numeroDeTaxis, ciudad, simbolo): #agregar taxis aleetorios
    espaciosDisponibles = getPosicionesLibres(ciudad)
    for i in range(0, numeroDeTaxis):
        if espaciosDisponibles == []:
            break
        indiceAleatorio = randint(0,len(espaciosDisponibles)-1)
        espacioLibre = espaciosDisponibles[indiceAleatorio]
        del espaciosDisponibles[indiceAleatorio]
        taxiNuevo = Taxi(espacioLibre.posicion, False, simbolo)
        ciudad.taxis.append(taxiNuevo)
        ciudad.mapa[espacioLibre.posicion[0]][espacioLibre.posicion[1]] = simbolo

def tieneCallesArriba(posicion, tablero):
    if tablero[posicion[0] - 1][posicion[1] - 1] in "o-":
        if tablero[posicion[0] - 1][posicion[1]] in "o-":
            if tablero[posicion[0] - 1][posicion[1] + 1] in "o-":
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def tieneCallesAbajo(posicion, tablero):
    if tablero[posicion[0] + 1][posicion[1] - 1] in "o-":
        if tablero[posicion[0] + 1][posicion[1]] in "o-":
            if tablero[posicion[0] + 1][posicion[1] + 1] in "o-":
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def tieneParedes(posicion, tablero):
    if tablero[posicion[0]][posicion[1] - 1] == "|":
        if tablero[posicion[0]][posicion[1] + 1] == "|":
            return True
        else:
            return False
    else:
        return False

def esEdificio(posicion, tablero):
    esValida = tieneCallesAbajo(posicion, tablero) and tieneCallesArriba(posicion, tablero)
    esValida = esValida and tieneParedes(posicion, tablero)
    if esValida:
        return True
    else:
        return False

def esObstaculo(posicion, tablero):
    if tablero[posicion[0]][posicion[1]] in "-|_o":
        return True
    else:
        return False

def crearCiudad(tablero):
    taxis = []
    personas = []
    viviendas = []
    trabajos = []
    espacios = []

    for i in range(0, len(tablero)-1):
        for j in range(0, len(tablero[i])-1):
            posActual = [i,j]
            if esEdificio(posActual, tablero):
                if tablero[i][j] == " ":
                    trabajos.append(EdificioTrabajo(posActual))
                else: 
                    try:
                        cantidadDeHabitantes = int(tablero[i][j])
                        if cantidadDeHabitantes == 0:
                            trabajos.append(EdificioTrabajo(posActual))
                        elif cantidadDeHabitantes > 0 and cantidadDeHabitantes < 10:
                            viviendas.append(EdificioVivienda(posActual, cantidadDeHabitantes))
                        else:
                            print("ERROR: CANTIDAD DE HABITANTES INVÁLIDA")
                            return -1
                    except:
                        print("ERROR: CARACTER DE CANTIDAD DE HABITANTES INVALIDA")
                        cantidadDeHabitantes = -1
            else:
                if not esObstaculo(posActual, tablero):
                    if tablero[i][j] == " ":
                        espacios.append(Espacio(0, 0, posActual))
                    else:
                        taxis.append(Taxi(posActual, False, tablero[i][j]))
                        espacios.append(Espacio(1, 0, posActual))

    for vivienda in viviendas:
        for i in range(0, vivienda.cantidadHabitantes):
            trabajoAleatorio = trabajos[randint(0, len(trabajos)-1)]
            personas.append(Cliente(vivienda.posicion, vivienda, trabajoAleatorio)) #HACER SUBCLASES VIVIENDA Y TRABAJO 

    nuevaCiudad = Ciudad(tablero, taxis, personas, trabajos, viviendas, espacios)
    return nuevaCiudad


#######################################################################################

def llenarEspacios(tablero):
    for i in range(0, len(tablero)):
        term = False
        linea = list(tablero[i])
        for j in range(0, len(linea)):
            if(tablero[i][j] == '\n'):
                linea[j] = ' '
        tablero[i] = linea
    return tablero

def getTablero():
    with open("entrada.txt") as f:
        content = f.readlines()
    content = [x for x in content]
    tab = llenarEspacios(content)
    if tab == None:
        print("ERROR DE ENTRADA: Solo puede haber un taxi (Con símbolo T)")
    else:
        return tab

def imprimirTablero(tablero):
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero[i])):
            print(tablero[i][j], end='')
        print("\n", end='')

def iniciarSimulacion(ciudad):
    tiempoActual = ciudad.tiempo.getHoraSalidaAlTrabajo()
    tiempo = time.time() #comienzo

    while tiempoActual >= ciudad.tiempo.rangoIda[0] and tiempoActual <= ciudad.tiempo.rangoIda[1]:
        print("Hola mundo")
        tiempoActual = time.time() - tiempo

def main():
    tablero = getTablero()
    ciudad = crearCiudad(tablero)
    imprimirTablero(ciudad.mapa)
    iniciarSimulacion(ciudad)

    '''
        if tablero != None:
        asignarDestinosAClientes()
        imprimirTablero(getPosicion(simboloTaxi))
        mostrarPanel()
    '''

main()

