def getSucesoresValidos(posicion, tablero):
    sucesores = []
    
    if posicion[0] != 0 and tablero[posicion[0]-1][posicion[1]] != "%": # ARRIBA
        sucesores.append([posicion[0]-1, posicion[1]])
    if posicion[1] != 0 and tablero[posicion[0]][posicion[1]-1] != "%": # IZQUIERDA
        sucesores.append([posicion[0], posicion[1]-1])
    if posicion[0] != len(tablero)-1 and tablero[posicion[0]+1][posicion[1]] != "%": # ABAJO
        sucesores.append([posicion[0]+1, posicion[1]])
    if posicion[1] != len(tablero[0])-1 and tablero[posicion[0]][posicion[1]+1] != "%": # DERECHA
        sucesores.append([posicion[0], posicion[1]+1]) 
    return sucesores

def distanciaEntreNodos(nodoA, nodoB):
    #|r1 - r | + |c1 - c|
    distancia = abs(nodoA[0] - nodoB[0]) + abs(nodoA[1] - nodoB[1])
    return distancia

def getNodoMenosCostoso(origen, destino, lista):
    minCosto = 9999999999999
    indiceNodo = -1
    for i in range(0, len(lista)):
        G = distanciaEntreNodos(origen, [lista[i][0], lista[i][1]]) + 1
        H = distanciaEntreNodos([lista[i][0], lista[i][1]], destino)
        F = G + H
        if F < minCosto:
            indiceNodo = i     
    return lista[indiceNodo]

def estaEnLista(posicion, lista):
    for i in lista:
        if posicion[0] == i[0] and posicion[1] == i[1]:
            return True
    return False 
       
def getListaDeReemplazo(nodo, lista): #Verifica si el costo es menor para reemplazarlo y devuelve la lista nueva
    nuevaLista = []
    for i in lista:
        if nodo[0] == i[0] and nodo[1] == i[1]:
            if(i[2] < nodo[2]):
                nuevaLista.append([nodo[0], nodo[1], i[2]])
            else:
                nuevaLista.append(i)
        else:
            nuevaLista.append(i)
    return nuevaLista
       
    
posPacMan = input().split(" ")
posComida = input().split(" ")
dimensiones = input().split(" ")

filas = int(dimensiones[0])
columnas = int(dimensiones[1])

tablero = []

for i in range(0, columnas):
    tablero.append(input())

abiertos = []
cerrados = []

origen = [int(posPacMan[0]), int(posPacMan[1])]
destino = [int(posComida[0]), int(posComida[1])]

abiertos.append(origen + [0]) # [R, C, costo]
encontrado = False

#print(getNodoMenosCostoso(origen, destino, [[34,35,35],[35,34,34]]))
distancia = 0
camino = ""

while(abiertos != [] and not encontrado):
    nodoActual = getNodoMenosCostoso(origen, destino, abiertos)
    abiertos.remove(nodoActual)
    sucesores = getSucesoresValidos(nodoActual, tablero)
    #print(str(nodoActual[0]) + " " + str(nodoActual[1]))
    for sucesor in sucesores:
        if sucesor == destino:
            encontrado = True
            break
            
        sucesorG = distanciaEntreNodos(origen, nodoActual) + 1
        sucesorH = distanciaEntreNodos(nodoActual, destino)
        sucesorF = sucesorG + sucesorH
        
        sucesor += [sucesorF]
        
        if not estaEnLista(sucesor, cerrados):
            abiertos = getListaDeReemplazo(sucesor, abiertos)
            abiertos.append(sucesor)
            
    cerrados.append(nodoActual)
    camino += str(nodoActual[0]) + " " + str(nodoActual[1]) + "\n"
    distancia += 1

print(distancia)
print(camino)

