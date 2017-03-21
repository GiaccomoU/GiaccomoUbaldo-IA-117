posicionPacMan = input().split(" ")
posicionComida = input().split(" ")
dimensionesTablero = input().split(" ")

rPacMan = int(posicionPacMan[0])
cPacMan = int(posicionPacMan[1])

rComida = int(posicionComida[0])
cComida = int(posicionComida[1])

rows = int(dimensionesTablero[0])
cols = int(dimensionesTablero[1])

############################

def getTablero():
    tablero = []
    for i in range(0, rows):
        fila = input()
        nuevaFila = []
        for j in range(0, cols):
            nuevaFila.append(fila[j])
        tablero.append(nuevaFila)
    return tablero

def getVecinosNoExplorados(posicion, explorados, tablero):
    vecinos = []
    #arriba
    if(posicion[0] != 0 and tablero[posicion[0]-1][posicion[1]] != '%'):
        if [posicion[0]-1,posicion[1]] not in explorados:
            vecinos.append([posicion[0]-1,posicion[1]])

    #izquierda
    if(posicion[1] != 0 and tablero[posicion[0]][posicion[1]-1] != '%'):
        if [posicion[0],posicion[1]-1] not in explorados:
            vecinos.append([posicion[0],posicion[1]-1])
    #derecha
    if((posicion[1] < len(tablero[0])-1) and tablero[posicion[0]][posicion[1]+1] != '%'):
        if [posicion[0],posicion[1]+1] not in explorados:
            vecinos.append([posicion[0],posicion[1]+1])
    
    #abajo
    if((posicion[0] < len(tablero)-1) and tablero[posicion[0]+1][posicion[1]] != '%'):
        if [posicion[0]+1,posicion[1]] not in explorados:
            vecinos.append([posicion[0]+1,posicion[1]])
    return vecinos

############################

tablero = getTablero()

explorados = []
pila = []


#explorados.append([rPacMan, cPacMan])
pila.append([rPacMan, cPacMan])
posActual = pila[len(pila)-1]


while(tablero[posActual[0]][posActual[1]] != "." or len(pila) == 0):
    posActual = pila[len(pila)-1]
    pila.pop()
    explorados.append(posActual)
    vecinosDisponibles = getVecinosNoExplorados(posActual, explorados, tablero)
    for i in range(0, len(vecinosDisponibles)):
        pila.append(vecinosDisponibles[i])

print(len(explorados))

for i in explorados:
    print(str(i[0]) + " " + str(i[1]))
    
print(len(explorados)-1)
for i in explorados:
    print(str(i[0]) + " " + str(i[1]))