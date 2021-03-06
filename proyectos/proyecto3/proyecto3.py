from random import randint
from random import uniform
import numpy
import time

class Cliente:
    def __init__(self, posicionActual, vivienda, trabajo, horaTrabajo, tiempoTrabajo=0.4):
        self.posicionActual = posicionActual
        self.vivienda = vivienda
        self.trabajo = trabajo
        self.horaTrabajo = horaTrabajo #porcentaje
        self.tiempoTrabajo = tiempoTrabajo #porcentaje
        self.destino = None

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
    def __init__(self, posicionActual, simboloLibre, simboloOcupado='O', tiempoCongestionado=0):
        self.posicionActual = posicionActual
        self.simboloActual = simboloLibre
        self.simboloLibre = simboloLibre
        self.simboloOcupado = simboloOcupado
        #self.estaEnCongestionamiento = estaEnCongestionamiento
        self.tiempoCongestionado = tiempoCongestionado
        self.clienteActual = None
        self.caminoActual = None
        self.caminoRecorrido = [] # Lista de explorados para evitar repetir caminos

    def tieneCliente(self):
        if self.clienteActual == None:
            return False
        else: 
            return True

    def dejarCliente(self):
        cliente = self.clienteActual
        cliente.posicionActual = cliente.destino.posicion
        cliente.destino = None
        self.clienteActual = None
        self.caminoActual = None
        self.simboloActual = self.simboloLibre

class Espacio:
    def __init__(self, cantidadDeCarros, tiempoCongestionamiento, posicion):
        self.posicion = posicion
        self.cantidadDeCarros = cantidadDeCarros
        self.tiempoCongestionamiento = tiempoCongestionamiento

    def setCongestionamiento(self):
        if self.cantidadDeCarros == 0 or self.cantidadDeCarros == 1:
            self.tiempoCongestionamiento = 0
        else:
            self.tiempoCongestionamiento = self.cantidadDeCarros

    def noHayCongestionamiento(self):
        if self.tiempoCongestionamiento == 0:
            return True
        else:
            return False

class Tiempo:
    def __init__(self, duracionDia, rangoIda, rangoVuelta, velocidadAnimacion):
        self.duracionDia = duracionDia
        self.rangoIda = rangoIda
        self.rangoVuelta = rangoVuelta
        self.velocidadAnimacion = velocidadAnimacion

    def getInicioSalidaAlTrabajo(self):
        return self.rangoIda[0] * self.duracionDia

    def getFinSalidaAlTrabajo(self):
        return self.rangoIda[1] * self.duracionDia

    def getInicioSalidaDelTrabajo(self):
        return self.rangoVuelta[0] * self.duracionDia

    def getFinSalidaDelTrabajo(self):
        return self.rangoVuelta[1] * self.duracionDia

class Ciudad:
    def __init__(self, mapa, taxis, personas, edificiosTrabajo, edificiosVivienda, espacios, tiempo, tiempoMapaCongestionamiento, redNeuronal):
        self.mapa = mapa
        self.taxis = taxis
        self.personas = personas
        self.edificiosTrabajo = edificiosTrabajo
        self.edificiosVivienda = edificiosVivienda
        self.tiempo = tiempo
        self.espacios = espacios
        self.diasPasados = 0
        self.mapasHechos = 0
        self.tiempoMapaCongestionamiento = tiempoMapaCongestionamiento
        self.redNeuronal = redNeuronal

    def sacarClienteAfuera(self, persona):
        posicionesDisponibles = getPosicionesAceraEdificio(persona.posicionActual)
        posElegida = posicionesDisponibles[randint(0, len(posicionesDisponibles)-1)]
        self.mapa[posElegida[0]][posElegida[1]] = "o"
        persona.posicionActual = posElegida

    def sacarClientesATrabajar(self, hora):
        duracionDia = self.tiempo.duracionDia
        for persona in self.personas:
            horaDeTrabajo = persona.horaTrabajo*duracionDia
            if  horaDeTrabajo <= hora and esEdificio(persona.posicionActual, self.mapa):
                self.sacarClienteAfuera(persona)
        #imprimirTablero(ciudad.mapa)

    def sacarClientesDeTrabajar(self, hora):
        duracionDia = self.tiempo.duracionDia
        for persona in self.personas:
            horaDeSalida = persona.horaTrabajo*duracionDia + persona.tiempoTrabajo*duracionDia
            if  horaDeSalida <= hora and esEdificio(persona.posicionActual, self.mapa):
                self.sacarClienteAfuera(persona)
        #imprimirTablero(ciudad.mapa)

    def moverTaxis(self):
        for taxi in self.taxis:
            posTaxi = taxi.posicionActual
            espacio = self.getEspacioPorPosicion(posTaxi)
            if taxi.tiempoCongestionado == 0:
                if taxi.tieneCliente():
                    if taxi.caminoActual == []: #Llego a su destino, solo queda su parada
                        taxi.dejarCliente()
                    else:
                        self.moverTaxiAPosicion(taxi, taxi.caminoActual[0])
                        taxi.caminoActual = taxi.caminoActual[1:]

                else:
                    if self.mapa[posTaxi[0] - 1][posTaxi[1]] == 'o':
                        cliente = self.getClientePorPosicion([posTaxi[0] - 1, posTaxi[1]])
                        self.recogerCliente(taxi, cliente)

                    elif self.mapa[posTaxi[0]][posTaxi[1] + 1] == 'o':
                        cliente = self.getClientePorPosicion([posTaxi[0], posTaxi[1] + 1])
                        self.recogerCliente(taxi, cliente)

                    elif self.mapa[posTaxi[0] + 1][posTaxi[1]] == 'o':
                        cliente = self.getClientePorPosicion([posTaxi[0] + 1, posTaxi[1]])
                        self.recogerCliente(taxi, cliente)

                    elif self.mapa[posTaxi[0]][posTaxi[1] - 1] == 'o':
                        cliente = self.getClientePorPosicion([posTaxi[0], posTaxi[1] - 1])
                        self.recogerCliente(taxi, cliente)
                    else:
                        eleccion = getEleccion(self.redNeuronal.query(convertirEntrada(self.mapa)))
                        print("ELECCION: " + eleccion)

                        if eleccion == "ARRIBA":
                            self.moverTaxiAPosicion(taxi, [taxi.posicionActual[0]-1, taxi.posicionActual[1]])
                        elif eleccion == "DERECHA":
                            self.moverTaxiAPosicion(taxi, [taxi.posicionActual[0], taxi.posicionActual[1]+1])
                        elif eleccion == "ABAJO":
                            self.moverTaxiAPosicion(taxi, [taxi.posicionActual[0]+1, taxi.posicionActual[1]])
                        else:
                            self.moverTaxiAPosicion(taxi, [taxi.posicionActual[0], taxi.posicionActual[1]-1])
                        #self.moverTaxiAPosicion(taxi, posicionNueva)
            else:
                taxi.tiempoCongestionado -= 1

    def moverTaxiAPosicion(self, taxi, posicionNueva):  #HAY QUE IMPRIMIR EL TABLERO, LEYENDO POSICIONES, DESPUES DE MOVER TAXIS PARA QUE TAXIS QUE SE ATRAVIESEN NO SE BORREN ENTRE SI
        posVieja = taxi.posicionActual
        self.mapa[posVieja[0]][posVieja[1]] = " "  
        self.mapa[posicionNueva[0]][posicionNueva[1]] = taxi.simboloActual
        taxi.posicionActual = posicionNueva

        if taxi.tieneCliente():
            taxi.clienteActual.posicionActual = posicionNueva

    def recogerCliente(self, taxi, cliente):
        clienteEnCasa = cliente.estaEnCasa
        self.mapa[cliente.posicionActual[0]][cliente.posicionActual[1]] = '-'
        cliente.posicionActual = taxi.posicionActual
        taxi.simboloActual = taxi.simboloOcupado
        taxi.clienteActual = cliente

        if clienteEnCasa:
            cliente.destino = cliente.trabajo
            posLlegada = getPosicionMasCercana(taxi.posicionActual, getPosicionesParqueoEdificio(cliente.trabajo.posicion))
        else:
            cliente.destino = cliente.vivienda
            posLlegada = getPosicionMasCercana(taxi.posicionActual, getPosicionesParqueoEdificio(cliente.vivienda.posicion))

        taxi.caminoActual = rutaMasCorta(self.mapa, taxi.posicionActual, posLlegada)

    def getClientePorPosicion(self, posicionCliente):
        for persona in self.personas:
             if persona.posicionActual == posicionCliente:
                return persona
        print("No se encontró al cliente con la posición: " + str(posicionCliente))
        return None

    def getEspacioPorPosicion(self, posicionEspacio):
        for espacio in self.espacios:
             if espacio.posicion == posicionEspacio:
                return espacio
        print("No se encontró el espacio con la posición: " + str(posicionEspacio))
        return None

    def refrescarTablero(self):
        for espacio in self.espacios:
            self.mapa[espacio.posicion[0]][espacio.posicion[1]] == ' '
            espacio.cantidadDeCarros = 0
            '''
            if not espacio.noHayCongestionamiento():
                espacio.tiempoCongestionamiento -= 1
                print("espacio: " + str(espacio.posicion) + " con tiempo restante: " + str(espacio.tiempoCongestionamiento))
            '''
        for persona in self.personas:
            if persona.posicionActual != persona.vivienda.posicion and persona.posicionActual != persona.trabajo.posicion:
                self.mapa[persona.posicionActual[0]][persona.posicionActual[1]] == 'o'
        for taxi in self.taxis:
            espacio = self.getEspacioPorPosicion(taxi.posicionActual)
            espacio.cantidadDeCarros = espacio.cantidadDeCarros + 1
            #espacio.setCongestionamiento()
            self.mapa[taxi.posicionActual[0]][taxi.posicionActual[1]] = taxi.simboloActual

    def ajustarCongestionamiento(self):
        for espacio in self.espacios:
            if espacio.cantidadDeCarros >= 2:
                listaTaxis = self.getTaxisEnPosicion(espacio.posicion)
                for taxi in listaTaxis:
                    if taxi.tiempoCongestionado == 0:
                        taxi.tiempoCongestionado = espacio.cantidadDeCarros
                    else:
                        taxi.tiempoCongestionado -= 1

    def getTaxisEnPosicion(self, posicion):
        taxisEnPosicion = []
        for taxi in self.taxis:
            if taxi.posicionActual == posicion:
                taxisEnPosicion.append(taxi)
        return taxisEnPosicion
        
    def getTiempoConcurrido(self, tiempoTranscurrido):
        segundosTotales = self.diasPasados*self.tiempo.duracionDia + tiempoTranscurrido
        minutos = segundosTotales // 60
        segundos = segundosTotales % 60
        return str(int(minutos)) + ":" + str(int(segundos))

    def generarMapaDeCongestionamiento(self, nombreArchivo, tiempoTranscurrido):
        for espacio in self.espacios:
            if espacio.cantidadDeCarros == 0:
                self.mapa[espacio.posicion[0]][espacio.posicion[1]] = " "
            else:
                self.mapa[espacio.posicion[0]][espacio.posicion[1]] = str(espacio.cantidadDeCarros)
 
        file = open(nombreArchivo,"w") 
        file.write(self.getTiempoConcurrido(tiempoTranscurrido) + str("\n"))
        impresion = ""
        for i in range(0, len(self.mapa)):
            for j in range(0, len(self.mapa[i])):
                impresion += self.mapa[i][j]
            impresion += "\n"
        file.write(impresion)

        file.close() 
        self.refrescarTablero()

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

class RedNeuronal:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        
        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc 
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate
        
        # activation function is the sigmoid function
        self.activation_function = lambda x: 1/(1+numpy.exp(-x))

    
    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        
        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors) 
        
        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))
        
        pass

    
    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        
        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

#####################################################################################

def definirRedNeuronal(n):
    training_data_file = open("targetsTraining.csv", 'r')
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    target_data_file = open("targetsDirecciones.txt", 'r')
    target_data_list = target_data_file.readlines()
    target_data_file.close()

    # train the neural network
    all_targets = []
    for record in target_data_list:
        # split the record by the ',' commas
        all_targets.append(record.split(','))
        # scale and shift the inputs

    targets = (numpy.asfarray(all_targets))
    print("TARGETS")
    print(targets)

    all_inputs = []
    for record in training_data_list:
        # split the record by the ',' commas
        all_inputs.append(record.split(','))
        # scale and shift the inputs

    inputs = (numpy.asfarray(all_inputs) / 255.0 * 0.99) + 0.01


    n.train(inputs, targets)


def convertirEntrada(entrada):
    entradaNum = []
        
    for linea in entrada:
        for caracter in linea:
            if caracter == (" "):
                entradaNum.append(127)
            elif caracter == ("-"):
                entradaNum.append(0)
            elif caracter == ("_"):
                entradaNum.append(0)
            elif caracter == ("|"):
                entradaNum.append(0)
            elif caracter == ("\n"):
                entradaNum.append(0)
            elif caracter == ("T"):
                entradaNum.append(255)
            else:
                print("ERRORRRRRR")

    entradaNum = (numpy.asfarray(entradaNum) / 255.0 * 0.99) + 0.01
    return entradaNum


def getEleccion(resultado):
    if max(resultado) == resultado[0]:
        return "ARRIBA"
    elif max(resultado) == resultado[1]:
        return "DERECHA"
    elif max(resultado) == resultado[2]:
        return "ABAJO"
    else:
        return "IZQUIERDA"



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
    #print("Recibi pos inicial " + str(posInicial) + " y pos destino " + str(posDestino))
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


def getPosicionesVisitables(posicion, ciudad):
    posVisitables = []
    fila = posicion[0]
    columna = posicion[1]
    if ciudad.mapa[fila-1][columna] not in "_-|o*+/": #Arriba
        posVisitables.append([fila-1,columna])
    if ciudad.mapa[fila][columna+1] not in "_-|o*+/": #Derecha
        posVisitables.append([fila,columna+1])
    if ciudad.mapa[fila+1][columna] not in "_-|o*+/": #Abajo
        posVisitables.append([fila+1,columna])
    if ciudad.mapa[fila][columna-1] not in "_-|o*+/": #Izquierda
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

def getPosicionMasCercana(posicion, listaPosiciones):
    distanciaMin = 999999
    posCercana = [-1, -1]
    for pos in listaPosiciones:
        distEntrePosiciones = distanciaEntrePosiciones(pos, posicion)
        if distEntrePosiciones < distanciaMin:
            distanciaMin = distEntrePosiciones
            posCercana = pos
    return posCercana

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

def getPosicionesParqueoEdificio(posEdificio):
    posiciones = []
    posiciones.append([posEdificio[0] - 2, posEdificio[1] - 1])
    posiciones.append([posEdificio[0] - 2, posEdificio[1]])
    posiciones.append([posEdificio[0] - 2, posEdificio[1] + 1])
    posiciones.append([posEdificio[0] + 2, posEdificio[1] - 1])
    posiciones.append([posEdificio[0] + 2, posEdificio[1]])
    posiciones.append([posEdificio[0] + 2, posEdificio[1] + 1])
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

def cargarCliente(posCliente, taxi, ciudad):
    ciudad.mapa[posCliente[0]][posCliente[1]] = '-'
    cliente = ciudad.getClientePorPosicion(posCliente)
    destino = ajustarPosicionLlegada(taxi.posicionActual, cliente.getDestino())
    taxi.caminoActual = rutaMasCorta(ciudad.mapa, taxi.posicionActual, destino)

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

def crearCiudad(tablero, archivoConfiguracion, redNeuronal):
    taxis = []
    personas = []
    viviendas = []
    trabajos = []
    espacios = []

    rangoIda = getRangoIda(archivoConfiguracion)
    velocidadAnimacion = getVelocidadAnimacion(archivoConfiguracion)
    tiempoTrabajo = getTiempoTrabajo(archivoConfiguracion)
    duracionDia = getDuracionDia(archivoConfiguracion)
    rangoVuelta = getRangoVuelta(archivoConfiguracion)
    tiempoMapaCongestionamiento = getTiempoMapaCongestionamiento(archivoConfiguracion)

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
                        taxis.append(Taxi(posActual, tablero[i][j]))
                        espacios.append(Espacio(1, 0, posActual))

    for vivienda in viviendas:
        for i in range(0, vivienda.cantidadHabitantes):
            trabajoAleatorio = trabajos[randint(0, len(trabajos)-1)]
            horaDeEntradaAleatoria = uniform(rangoIda[0], rangoIda[1])
            nuevoCliente = Cliente(vivienda.posicion, vivienda, trabajoAleatorio, horaDeEntradaAleatoria, tiempoTrabajo)
            print(nuevoCliente.horaTrabajo)
            personas.append(nuevoCliente) 

    tiempoAUsar = Tiempo(duracionDia, rangoIda, rangoVuelta, velocidadAnimacion)
    nuevaCiudad = Ciudad(tablero, taxis, personas, trabajos, viviendas, espacios, tiempoAUsar, tiempoMapaCongestionamiento, redNeuronal)
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
    impresion = ""
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero[i])):
            impresion += tablero[i][j]
        impresion += "\n"
    print(impresion)

#######################################################################################

def getRangoIda(nombreArchivo):
    with open(nombreArchivo) as f:
        for line in f:
            line = line.split("=")
            if line[0] == "RangoIda":
                rango = line[1][1:].split("]")[0].split(",")
                return [float(rango[0]), float(rango[1])]

def getVelocidadAnimacion(nombreArchivo):
    with open(nombreArchivo) as f:
        for line in f:
            line = line.split("=")
            if line[0] == "VelocidadAnimacion":
                return float(line[1])    

def getTiempoTrabajo(nombreArchivo):
    with open(nombreArchivo) as f:
        for line in f:
            line = line.split("=")
            if line[0] == "TiempoTrabajo":
                return float(line[1])    

def getTiempoMapaCongestionamiento(nombreArchivo):
    with open(nombreArchivo) as f:
        for line in f:
            line = line.split("=")
            if line[0] == "TiempoMapaCongestionamiento":
                return float(line[1])   

def getDuracionDia(nombreArchivo):
    with open(nombreArchivo) as f:
        for line in f:
            line = line.split("=")
            if line[0] == "DuracionDia":
                return float(line[1])    

def getRangoVuelta(nombreArchivo):
    with open(nombreArchivo) as f:
        for line in f:
            line = line.split("=")
            if line[0] == "RangoVuelta":
                rango = line[1][1:].split("]")[0].split(",")
                return [float(rango[0]), float(rango[1])]

#######################################################################################

def getPosicionesAceraEdificio(posEdificio):
    posiciones = []
    posiciones.append([posEdificio[0] - 1, posEdificio[1] - 1])
    posiciones.append([posEdificio[0] - 1, posEdificio[1]])
    posiciones.append([posEdificio[0] - 1, posEdificio[1] + 1])
    posiciones.append([posEdificio[0] + 1, posEdificio[1] - 1])
    posiciones.append([posEdificio[0] + 1, posEdificio[1]])
    posiciones.append([posEdificio[0] + 1, posEdificio[1] + 1])
    return posiciones

def simularDia(ciudad):
    
    inicioSalidaAlTrabajo = ciudad.tiempo.getInicioSalidaAlTrabajo() #120 * 0.2 = 24
    finSalidaAlTrabajo = ciudad.tiempo.getFinSalidaAlTrabajo() #120 * 0.3 = 36

    inicioSalidaDelTrabajo = ciudad.tiempo.getInicioSalidaDelTrabajo() 
    finSalidaDelTrabajo = ciudad.tiempo.getFinSalidaDelTrabajo() 

    duracionDia = ciudad.tiempo.duracionDia # 120
    
    tiempoActual = 0
    tiempo = time.time() #comienzo 0

    while tiempoActual < duracionDia:
        if int(tiempoActual) % ciudad.tiempoMapaCongestionamiento == 0:
     	   ciudad.generarMapaDeCongestionamiento("mapaCongestionamiento" + str(ciudad.mapasHechos) + ".txt", tiempoActual)
     	   ciudad.mapasHechos += 1
    
        while tiempoActual >= inicioSalidaAlTrabajo and tiempoActual < finSalidaAlTrabajo:
            ciudad.sacarClientesATrabajar(tiempoActual)
            imprimirTablero(ciudad.mapa)
            tiempoActual = time.time() - tiempo
            time.sleep(ciudad.tiempo.velocidadAnimacion)
            ciudad.moverTaxis()
            ciudad.refrescarTablero()

        while tiempoActual >= inicioSalidaDelTrabajo and tiempoActual < finSalidaDelTrabajo:
            ciudad.sacarClientesDeTrabajar(tiempoActual)
            imprimirTablero(ciudad.mapa)
            tiempoActual = time.time() - tiempo
            time.sleep(ciudad.tiempo.velocidadAnimacion)
            ciudad.moverTaxis()
            ciudad.refrescarTablero()

        ciudad.moverTaxis()
        ciudad.refrescarTablero()
        ciudad.ajustarCongestionamiento()
        tiempoActual = time.time() - tiempo
        time.sleep(ciudad.tiempo.velocidadAnimacion)
        imprimirTablero(ciudad.mapa)

def main():


    redNeuronal = RedNeuronal(736,200,4,0.1)
    definirRedNeuronal(redNeuronal)


    tablero = getTablero()
    ciudad = crearCiudad(tablero, "ajustesTaxi.txt", redNeuronal) # HACER QUE ESTOS PARAMETROS SEAN TOMADOS DESDE ARCHIVO DE CONFIGURACION
    imprimirTablero(ciudad.mapa)

    while True:
        simularDia(ciudad)
        ciudad.diasPasados += 1

main()
