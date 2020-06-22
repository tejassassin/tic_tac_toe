import threading
from threading import Thread, Lock

player = 'o'
opponent = 'x'
item = [-1,-1]
bestVal= -1000
data_lock = Lock()
moveVal = 0 
bestMove = [0,0]

def isMoveLeft(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j] == '_'):
                return True 
    return False
def evaluate(board):
    for row in range(len(board)):
        if(board[row][0] == board[row][1] and board[row][1] == board[row][2]):
            if(board[row][0] == player):
                return +10
            elif(board[row][0] == opponent):
                return -10
    for col in range(len(board)):
        if(board[0][col] == board[1][col] and board[1][col] == board[2][col]): 
            if(board[0][col] == player):
                return +10
            elif(board[0][col] == opponent):
                return -10
    if(board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        if(board[0][0]==player):
            return +10
        elif(board[0][0]==opponent):
            return -10
    if(board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if(board[0][2]==player):
            return +10
        elif(board[0][2]==opponent):
            return -10
    #in case of a draw  
    return 0
def minimax(board,depth,isMax):
    score = evaluate(board)
    # print(score," and ",depth)
#     print(score)
#     print(board)
#     print(isMax)
    if(score == 10):
        return score-depth
    elif(score == -10):
        return score+depth
    if(isMoveLeft(board) == False):
        return 0
    if(isMax):
        best = -1000
        for i in range(len(board)):
            for j in range(len(board[0])):
                if(board[i][j] == '_'):
                    board[i][j]=player ; 
                    # isMax = False
                    best = max(best,minimax(board,depth+1,not isMax))
                    board[i][j] = '_'
        return best
    else:
        best = 1000
        for i in range(len(board)):
            for j in range(len(board[0])):
                if(board[i][j] == '_'):
                    board[i][j] = opponent
                    best = min(best,minimax(board,depth+1,not isMax))
                    board[i][j] = '_'
        return best 

def finding(board,i,item):
    global bestVal
    for j in range(len(board[0])):
            if(board[i][j] == '_'):
                board[i][j] = player
                moveVal = minimax(board,0,False) 
                board[i][j] = '_' ; 
                with data_lock:
                    if(moveVal > bestVal):
                        # print(moveVal,"and the current best Val",bestVal)
                        item[0] = i
                        item[1] = j
                        bestVal = moveVal 
    print("tic-tac-toe.py",item,bestVal)
def findBestMove(board):
    global bestVal
    bestVal = -1000 
    item = [-1,-1]
    for i in range(len(board)):
        dummy_board = board
        t = threading.Thread(target=finding,args=(board,i,item))  
        t.start() 
    t.join()    
    return item

# board = [['x','_','_'],
#          ['_','_','_'],
#          ['_','_','_']]  
# bestMove = findBestMove(board)
# # board[][]
# print("l",board)
# # bestMove = findBestMove(board)
# # print("2",board)
# print("The optimal move is : ",bestMove[0],"and",bestMove[1] )