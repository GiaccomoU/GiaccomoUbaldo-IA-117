#!/usr/bin/python
def displayPathtoPrincess(n,grid):
    if grid[0][0] == "p": 
        print(upLeftCorner(n, grid))
    elif grid[0][n-1] == "p":
        print(upRightCorner(n, grid))
    elif grid[n-1][0] == "p":
        print(downLeftCorner(n, grid))
    elif grid[n-1][n-1] == "p":
        print(downRightCorner(n, grid))
    else:
        print("ERROR: MISSING PRINCESS")

def upLeftCorner(n, grid):
    respuesta = ""
    avance = n//2
    for i in range(0,avance):
        respuesta += "LEFT\n"
    for i in range(0,avance):
        respuesta += "UP\n"
    return respuesta
    
def upRightCorner(n, grid):
    respuesta = ""
    avance = n//2
    for i in range(0,avance):
        respuesta += "RIGHT\n"
    for i in range(0,avance):
        respuesta += "UP\n"
    return respuesta

def downLeftCorner(n, grid):
    respuesta = ""
    avance = n//2
    for i in range(0,avance):
        respuesta += "LEFT\n"
    for i in range(0,avance):
        respuesta += "DOWN\n"
    return respuesta

def downRightCorner(n, grid):
    respuesta = ""
    avance = n//2
    for i in range(0,avance):
        respuesta += "RIGHT\n"
    for i in range(0,avance):
        respuesta += "DOWN\n"
    return respuesta
        
     
#print all the moves here
m = int(input())
grid = [[]] 
for i in range(0, m): 
    grid.append(input().strip())
    
#print(grid)

grid = grid[1:]

#print(grid)

displayPathtoPrincess(m,grid)


