# very much based on : Trevor Payne https://www.youtube.com/watch?v=fInYh90YMJU&noredirect=1
from sys import maxsize
import numpy as np
import pickle

#my version

#it's alpha version of minimax algorithm solving balls game

#creating set with all nodes.actualboards to avoid permutatution on diff levelss
#pass i_playerNum to permute and spider2 to asure boards on -player are added as negative numbers
#pass set to spider2 and if there is intersection with permute(newbord) skip it

'''
for i in range (65536):
	if i%1000 == 0:
		print(i)
	secik.difference_update(permute(numboard(i)))
	secik.add(i)
	#returns 8548 unique boards (in less than 3 minutes)
'''



def createboard(n):
    return np.ones((n, n), dtype = bool)


def allmoves(board):
    #returns all possible moves (not boards!)

    #vertical
    listofallmoves = []
    for n in range (len(board)):
        for m in range (len(board)):
            for k in range (len(board)):
                if (m < (len(board)-k)): 
                    boardx = np.zeros((len(board), len(board)), dtype = bool)
                    boardx[n,m:(len(board)-k)] = True
                    listofallmoves.append(boardx)
        
    #horizontal
    for n in range (len(board)):
        for m in range (len(board)):
            for k in range (len(board)):
                if (m < (len(board)-k-1)): #-1 due to repeate ones
                    boardx = np.zeros((len(board), len(board)), dtype = bool)
                    boardx[m:len(board)-k,n] = True
                    listofallmoves.append(boardx)
    return listofallmoves


def moves(board):
    #returns all possible boards after creating legal move
    listofmoves = []
    #listofallmoves = allmoves(board) - moved to global var
    for move in listofallmoves:
        if (np.logical_and(board, move).any()):
            posibleBoard = np.logical_xor(np.logical_and(board, move), board)       
            for m in listofmoves:
                #if arrays are equal:
                if not(np.logical_xor(m, posibleBoard).any()):
                    break
            else:    
                listofmoves.append(posibleBoard)
    return listofmoves

def spider(board):
    #returns all possible moves (not boards!)
    #to make a move use logical AND on board and move

    #vertical
    listofallmoves = []
    for n in range (len(board)):
        for m in range (len(board)):
            if board[n,m] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k)):
                        if board[n,(len(board)-k-1)] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[n,m:(len(board)-k)] = False
                            listofallmoves.append(boardx)
    
    #horizontal
    for n in range (len(board)):
        for m in range (len(board)):
            if board[m,n] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k-1)): #-1 due to repeate ones
                        if board[(len(board)-k-1),n] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[m:len(board)-k,n] = False
                            listofallmoves.append(boardx)
    return listofallmoves

def spider2(board):
    #returns all boards after making moves, witout permutation
    #boards are represented by numbers

    #vertical
    setboards = set()
    for n in range (len(board)):
        for m in range (len(board)):
            if board[n,m] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k)):
                        if board[n,(len(board)-k-1)] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[n,m:(len(board)-k)] = False
                            setboards.difference_update(permute(np.logical_and(board, boardx)))
                            setboards.add(boardnum(np.logical_and(board, boardx)))
    
    #horizontal
    for n in range (len(board)):
        for m in range (len(board)):
            if board[m,n] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k-1)): #-1 due to repeate ones
                        if board[(len(board)-k-1),n] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[m:len(board)-k,n] = False
                            setboards.difference_update(permute(np.logical_and(board, boardx)))
                            setboards.add(boardnum(np.logical_and(board, boardx)))
    return setboards

def permute(board):
    #this turns board into set of its permutation
    listpermutation = set()
    for i in range(4):
        board = np.rot90(board)
        listpermutation.add(boardnum(board))
        listpermutation.add(boardnum(np.flip(board,0)))
        listpermutation.add(boardnum(np.flip(board,1)))                     
    return listpermutation

    
def boardnum(board):
    k = len(board)
    num = 0
    i=1
                               
    for n in range (k):
        for m in range (k):
            if board[n,m] == False:
                num = num+i
            i=i*2
    return num
                               
def numboard(num):
    board = createboard(n)
    ind = 2**(n**2-1)
    while ind >= 1:
        if num // ind > 0:
            i = 0
            for x in range (n):
                for y in range (n):
                    if i == np.log2(ind):
                        board[x,y] = False
                    i = i + 1
        num=num%ind
        ind = ind / 2
    return board
            

    

    
class Node(object):
    def __init__(self, i_depth, i_playerNum, actualBoard, i_value = 0):
        self.i_depth = i_depth
        self.i_playerNum = i_playerNum
        self.actualBoard = actualBoard
        self.i_value = self.iswin(actualBoard)
        self.children = []
        self.createChildren()


    def createChildren(self):
        if self.i_depth < 0:
            return
        '''ver 1 
        for new_board in moves(self.actualBoard):
            self.children.append(Node(self.i_depth - 1, -self.i_playerNum, new_board, self.iswin(new_board)))
        '''
        
        setofboards = spider2(self.actualBoard)
        while len(setofboards) > 0:
            new_board = numboard(setofboards.pop())
            self.children.append(Node(self.i_depth - 1, -self.i_playerNum, new_board, self.iswin(new_board)))

        '''
        for move in spider(self.actualBoard):
            new_board = np.logical_and(self.actualBoard, move)
            self.children.append(Node(self.i_depth - 1, -self.i_playerNum, new_board, self.iswin(new_board)))
        '''   
    def iswin(self, board):
        if np.sum(board) == 1:
            return maxsize * -self.i_playerNum
        elif np.sum(board) == 0:
            return maxsize * self.i_playerNum
        return 0


def minimax(node, i_depth, i_playerNum):
    if (i_depth == 0) or (abs(node.i_value) == maxsize):
        return node.i_value
    #we start with worst value
    i_bestValue = maxsize * -i_playerNum

    for child in node.children:
        i_val = minimax(child, i_depth - 1, -i_playerNum)
        
        #check if current value is closer to bestvalue than last the best found value
        if abs(maxsize * i_playerNum - i_val) < abs(maxsize * i_playerNum - i_bestValue):
            i_bestValue = i_val
            

    ##debug
    #print(str(i_depth*i_playerNum)+" + " + str(i_bestValue))
    return i_bestValue


def winCheck(board, i_playerNum):
    i_sum = np.sum(board)
    if i_sum <= 1:

        print("*" * 30)
        print("final board:")
        drawBoard(board)
        print("*" * 30)
        if i_playerNum > 0:
            if i_sum == 0:
                print("\t You lose you crossed out last ball")
            else:
                print("\t You win comp  must cross out last ball")
        else:
            if i_sum == 0:
                print("\t You win.. there are no balls left.")
            else:
                print("\t You loose you must cross out last ball!")
        print("*" * 30)
        return 0
    return 1

def drawBoard(board):
    n = len(board)
    for x in range (n):
        for y in range (n):
            if board[x,y]: print('O',end=' ')
            else: print('X',end=' ')
        print('')

        
#function role is to obtain move from user!
def getMove(n):    
    Move = np.zeros((n, n), dtype = bool)
    '''
    print('pattern:')
    if n == 4:
        print(' 0  1  2  3')
        print(' 4  5  6  7')
        print(' 8  9 10 11')
        print('12 13 14 15')
    elif n == 3:
        print('0 1 2')
        print('3 4 5 ')
        print('6 7 8')
    elif n == 2:
        print('0 1')
        print('2 3')
    print('chose ball to cross out when finish type x or enter')
    '''
    while 1:
        choice = input()
        if choice == 'x' or choice == '': break
        i = 0
        for x in range (n):
            for y in range (n):
                if i == int(choice):
                    Move[x,y] = 1
                i = i + 1
    for legalMove in allmoves(Move):
        #if arrays are equal
        if not(np.logical_xor(legalMove, Move).any()):
            return Move

    print ('illegal move')
    return 0

def generateTree():
    with open('tree2.bin','wb') as output:
        root =  Node(i_depth, i_curPlayer, b1)
        pickle.dump(root, output, -1)
    return 1
def loadTree():
    with open('tree2.bin','rb') as input:
        root = pickle.load(input)
    return root
        
if __name__ == '__main__':

    #size of board
    n=4

    #default depth
    i_depth = 5

    
    #1 = human, -1 = comp
    i_curPlayer = -1
    
    b1 = createboard(n)
    listofallmoves = allmoves(b1)
    
    print("INSTRUCTIONS : cross out any balls in row or column. who cross out last ball loses.")
    print('board:')
    drawBoard(b1)
    print('pattern:')
    if n == 4:
        print(' 0  1  2  3')
        print(' 4  5  6  7')
        print(' 8  9 10 11')
        print('12 13 14 15')
    elif n == 3:
        print('0 1 2')
        print('3 4 5 ')
        print('6 7 8')
    elif n == 2:
        print('0 1')
        print('2 3')
    print('chose ball to cross out when finish type x or enter')
    while np.sum(b1) > 1:
        #break
        if i_curPlayer < 0:
            print("Comp is thinking...")
            node = Node(i_depth, i_curPlayer, b1)
            
            #default bestChoice ahould be ranodmized, maybe in next version
            bestChoice = node.children[0].actualBoard

            #we start with worst possible value
            i_bestValue = -i_curPlayer * maxsize
            for child in node.children:
                i_val = minimax(child, i_depth, -i_curPlayer)
                if abs(i_curPlayer * maxsize - i_val) < abs(i_curPlayer * maxsize - i_bestValue):
                    i_bestValue = i_val
                    bestChoice = child.actualBoard
            print("Comp plays: ")
            drawBoard(bestChoice)
            print ("\tEvaluation: " + str(i_bestValue))
            b1 = bestChoice
            i_curPlayer *= -1 
        if i_curPlayer > 0:
            print("board:")
            drawBoard(b1)
            print("your turn:")
            i_choice = getMove(n)
            b1 = np.logical_xor(np.logical_and(i_choice, b1), b1)
            print("You play:")
            drawBoard(b1)
            i_curPlayer *= -1
    winCheck(b1, -i_curPlayer)
        


