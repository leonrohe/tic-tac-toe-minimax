import os

class board:
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (6, 4, 2)]

    def __init__(self, position):
        self.position = position

    def drawBoard(self):
        print("")
        for y in range(0, 3):
            line_str = ""
            for x in range(0, 3):
                ele = self.position[y*3+x]
                if(ele == 0): line_str+=" - "
                elif(ele == -1): line_str+=" X "
                else: line_str+=" O "
            print(line_str)

    def checkWin(self):
        for c in self.win_conditions:
            val = self.position[c[0]] + self.position[c[1]] + self.position[c[2]]
            if(val == 3 or val == -3):
                return True
    
    def availableMoves(self):
        moves = 0
        for e in self.position:
            if(e==0): moves+=1
        return moves
    
    def isBoardOver(self):
        if(self.checkWin() or self.availableMoves() == 0):
            return True
    
    def getChildBoards(self, player):
        children = []
        for i in range(0, len(self.position)):
            if(self.position[i]==0):
                temp = self.position[:]
                temp[i] = player
                children.append(board(temp))
        return children

    def rateBoard(self):
        eval = 0
        for c in self.win_conditions:
            playerAmount, botAmount = 0, 0
            for e in c:
                if(self.position[e] == 1): botAmount+=1
                if(self.position[e] == -1): playerAmount+=1

            if(playerAmount > 0 and playerAmount < 3 and botAmount > 0 and botAmount < 3):
                if(playerAmount+botAmount == 3):
                    continue

            if(playerAmount == 1): eval-=1
            elif(playerAmount == 2): eval-=10
            elif(playerAmount == 3): eval-=100

            if(botAmount == 1): eval+=1
            elif(botAmount == 2): eval+=10
            elif(botAmount == 3): eval+=100
        return eval

def minimax(board, maximizing):
    if(board.isBoardOver()):
        return board.rateBoard()

    if maximizing:
        maxEval = -1000000
        p_children = board.getChildBoards(1)
        for child in p_children:
            eval = minimax(child, False)
            maxEval = max(maxEval, eval)
        return maxEval 
    else:
        minEval = +1000000
        p_children = board.getChildBoards(-1)
        for child in p_children:
            eval = minimax(child, True)
            minEval = min(minEval, eval)
        return minEval

def getInput():
    global b
    print("")
    pInput = input("Wo soll das X platziert werden? (1-9)" + "\n")
    pInput = int(pInput)-1
    b.position[pInput] = -1

def genMove():
    global b
    b_children = b.getChildBoards(1)

    maximum, index = -1, 0
    possibilities = []
    for i in range(0, len(b_children)):
        eval = minimax(b_children[i], False)

        if(eval > maximum): maximum, index = eval, i
        
        if(eval == maximum): possibilities.append(b_children[i])   

    maximum, index = -1000000, 0
    for i in range(0, len(possibilities)):
        eval = possibilities[i].rateBoard()
        if(eval > maximum): maximum, index = eval, i

    b = possibilities[index]

def finishGame():
    global b
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (6, 4, 2)]

    print("")
    for c in win_conditions:
        val = b.position[c[0]] + b.position[c[1]] + b.position[c[2]]
        if(val == 3): print("Computer gewinnt!"); return 
        elif(val == -3): print("Spieler gewinnt!"); return
    print("Spiel endet mit einem Unentschieden")

start_position= [0, 0, 0,   # 0, 1, 2 
                0, 0, 0,    # 3, 4, 5
                0, 0, 0]    # 6, 7, 8

b = board(start_position)

while 1:
    if(b.isBoardOver()): break

    b.drawBoard()

    getInput()

    if(b.isBoardOver()): break

    genMove()

b.drawBoard()

finishGame()

os.system("pause")