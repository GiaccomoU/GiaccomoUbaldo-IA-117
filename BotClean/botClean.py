#!/usr/bin/python

# Head ends here
def next_move(posr, posc, board):
    dirtyList = getDirtyPositions(board)
    next_move_aux(posr, posc, board, 1, dirtyList)

def next_move_aux(posr, posc, board, num, dirtyList):
    if num < 4:
        if (posr-num) >= 0 and board[posr-num][posc] == "d": # arriba
            for i in range(0, num):
                print("UP")
            print("CLEAN")
            board[posr-num][posc] = "-"
            dirtyList = cleanPosition(posr-num, posc, dirtyList)
            next_move_aux(posr-num, posc, board, 1, dirtyList)
        elif (posc + num) < len(board) and board[posr][posc+num] == "d": #derecha
            for i in range(0, num):
                print("RIGHT")
            print("CLEAN")
            board[posr][posc+num] = "-"
            dirtyList = cleanPosition(posr, posc+num, dirtyList)
            next_move_aux(posr, posc+num, board, 1, dirtyList)
        elif (posc - num) > 0  and board[posr][posc-num] == "d": #izquierda
            for i in range(0, num):
                print("LEFT")
            print("CLEAN")
            board[posr][posc-num] = "-"
            dirtyList = cleanPosition(posr, posc-num, dirtyList)
            next_move_aux(posr, posc-num, board, 1, dirtyList)
        elif posr+num <= 4 and board[posr+num][posc] == "d": #abajo
            for i in range(0, num):
                print("DOWN")
            print("CLEAN")
            board[posr+num][posc] = "-"
            dirtyList = cleanPosition(posr+num, posc, dirtyList)
            next_move_aux(posr+num, posc, board, 1, dirtyList)
        elif ((posr-num) >= 0) and ((posc + num) < len(board)) and board[posr-num][posc+num] == "d": # diagonal arriba derecha
            for i in range(0, num): 
                print("UP")
                print("RIGHT")
            print("CLEAN")
            board[posr-num][posc+num] = "-"
            dirtyList = cleanPosition(posr-num, posc+num, dirtyList)
            next_move_aux(posr-num, posc+num, board, 1, dirtyList)
        elif ((posr-num) >= 0) and ((posc - num) > 0) and board[posr-num][posc-num] == "d": # diagonal arriba izquierda
            for i in range(0, num):
                print("UP")
                print("LEFT")
            print("CLEAN")
            board[posr-num][posc-num] = "-"
            dirtyList = cleanPosition(posr-num, posc-num, dirtyList)
            next_move_aux(posr-num, posc-num, board, 1, dirtyList)
        elif (posr+num <= 4) and ((posc + num) < len(board)) and board[posr+num][posc+num] == "d": # diagonal abajo derecha
            for i in range(0, num):
                print("DOWN")
                print("RIGHT")
            print("CLEAN")
            board[posr+num][posc+num] = "-"
            dirtyList = cleanPosition(posr+num, posc+num, dirtyList)
            next_move_aux(posr+num, posc+num, board, 1, dirtyList)
        elif (posr+num <= 4) and ((posc - num) > 0) and board[posr+num][posc-num] == "d": # diagonal abajo izquierda
            for i in range(0, num): 
                print("DOWN")
                print("LEFT")
            print("CLEAN")
            board[posr+num][posc-num] = "-"
            dirtyList = cleanPosition(posr+num, posc-num, dirtyList)
            next_move_aux(posr+num, posc-num, board, 1, dirtyList)
        else:
            next_move_aux(posr, posc, board, num+1, dirtyList)
    else:
        if dirtyList != []:
            newPositions = getAdjustedPosition(posr, posc, dirtyList)
            newPosR = newPositions[0]
            newPosC = newPositions[1]
            board[newPosR][newPosC] = "-"
            dirtyList = cleanPosition(newPosR, newPosC, dirtyList)
            next_move_aux(newPosR, newPosC, board, 1, dirtyList)
            
            


def getAdjustedPosition(posr, posc, dirtyList):
    dirtyPosition = dirtyList[0]
    
    dirtyPosR = dirtyPosition[0]
    dirtyPosC = dirtyPosition[1]
    
    #rows = (posr + dirtyPosition[0])//2
    #cols = (posc + dirtyPosition[1])//2
    
    if dirtyPosR-posr < 0:
        for i in range(0, (posr-dirtyPosR)):
            print("UP")
    else:
        for i in range(0, (dirtyPosR-posr)):
            print("DOWN")
            
    if dirtyPosC-posc < 0:
        for i in range(0, (posc-dirtyPosC)):
            print("LEFT")
    else:
        for i in range(0, (dirtyPosC-posc)):
            print("RIGHT")
    
    print("CLEAN")
    
    return [dirtyPosR,dirtyPosC]
            
def cleanPosition(posr, posc, dirtyList):
    for i in range(0, len(dirtyList)):
        if dirtyList[i] == [posr, posc]:
            dirtyList.pop(i)
            break
    return dirtyList
            
        
def getDirtyPositions(board):
    dirtyList = []
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j] == "d":
                dirtyList.append([i,j])
    return dirtyList
    
    
# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
