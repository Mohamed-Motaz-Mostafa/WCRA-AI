import ImageProcessing.ImageHelpers.ImageHelpers as im
import numpy as np
import cv2
import AI.AiHelpers.AiHelpers as ai

def print_board(newBoard):
    print("UC")
    for i in range(8):
        print(newBoard.UC[i])
    print(".C")
    for i in range(8):
        print(newBoard.C[i])



class Board:    
    def __init__(self ,playerColor):
        if playerColor == 'B':

            self.C =[
                ["r", "n", "b", "q", "k", "b", "n", "r"],
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                ["R", "N", "B", "Q", "K", "B", "N", "R"]]
            
            self.UC=[
                ["B", "B", "B", "B", "B", "B", "B", "B"],
                ["B", "B", "B", "B", "B", "B", "B", "B"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["W", "W", "W", "W", "W", "W", "W", "W"],
                ["W", "W", "W", "W", "W", "W", "W", "W"],
            ]


            self.RanksForUpdate = ['8', '7', '6', '5', '4', '3', '2', '1']
            self.FilesForUpdate = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        else :
            self.C =[
                ["R", "N", "B", "K", "Q", "B", "N", "R"],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],        
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                ["r", "n", "b", "k", "q", "b", "n", "r"]
                ]
            
            self.UC=[
                ["W", "W", "W", "W", "W", "W", "W", "W"],
                ["W", "W", "W", "W", "W", "W", "W", "W"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["B", "B", "B", "B", "B", "B", "B", "B"],
                ["B", "B", "B", "B", "B", "B", "B", "B"]]




            
            
            self.RanksForUpdate = ['1', '2', '3', '4', '5', '6', '7', '8']
            self.FilesForUpdate = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        
    def setUC(self,uc):
        self.UC=uc





    def UpdateBoardForCassiling( self ,side, UpdateFor) :
        if side =='KS':
            move = 'h'+str(self.RanksForUpdate[0])+'f'+str(self.RanksForUpdate[0])
            self.updateBoard ( move, UpdateFor)
        else :
            move = 'a'+str(self.RanksForUpdate[0])+'d'+str(self.RanksForUpdate[0])
            self.updateBoard (  move, UpdateFor)



    def updateBoard ( self, move, UpdateFor):
        
        NewRank = self.RanksForUpdate.index(move[3])
        NewFile = self.FilesForUpdate.index(move[2])
        OldRank = self.RanksForUpdate.index(move[1])
        OldFile = self.FilesForUpdate.index(move[0])
        self.UC [ NewRank ][ NewFile ] = UpdateFor
        self.UC [ OldRank ][ OldFile ] = '1'
        self.C [NewRank][NewFile] = self.C [ OldRank ][ OldFile ]
        self.C [OldRank][OldFile] = '1'
        print('board after update by' , move,': ')
        #print(Files)
        print_board(self)

def makeNewBoard(newBoard):
    colorDict = {0:'1', 1:'W', 2:'B'}
    tempBoard = im.captureAiSequence()
    board = []
    for i in range(64):
        tempSq = tempBoard[i]
        board.append(cv2.resize(tempSq, (190,190)))
    board = np.array(board)
    board = np.reshape(board, (8,8,190,190,3))
    for i in range(8):
        for j in range(8):
            newBoard.UC[i][j] = colorDict[ai.runAiModel(board[i][j])]
   # print('the new board: ')
    #print_board(newBoard)
    return newBoard.UC


def Castiling(newBoard, prevBoard,move, playerColor = 'B'):
    if playerColor == 'B':
        A = (prevBoard.UC[0][6] == '1' and prevBoard.UC[0][5] == '1')
        B = (newBoard.UC[0][6] == 'B' and newBoard.UC[0][5] == 'B')

        C = (prevBoard.UC[0][2] == '1' and prevBoard.UC[0][3] == '1')
        D = (newBoard.UC[0][3] == 'B' and newBoard.UC[0][3] == 'B')

        if (A and B) or (C and D) :
            newBoard.UpdateBoardForCassiling('KS' if (A and B) else 'QS','B')
            move = 'e8g8' if (A and B) else 'e8c8'
        return move

    else :
        
        A = (prevBoard.UC[0][1] == '1' and prevBoard.UC[0][2] == '1')
        B = (newBoard.UC[0][1] == 'W' and newBoard.UC[0][2] == 'W')

        C = (prevBoard.UC[0][4] == '1' and prevBoard.UC[0][5] == '1')
        D = (newBoard.UC[0][4] == 'W' and newBoard.UC[0][5] == 'W')
        print ('conditions : =============>  ',A,B,C,D)

        if (A and B) or (C and D) :
            newBoard.UpdateBoardForCassiling('KS' if (A and B) else 'QS','W')
            move ='e1g1' if (A and B) else 'e1c1'
        return move


def compareBoards( newBoard, prevBoard, playerColor = 'B') :

    
    playerRow = 0

    # Print the unclassified board . Good tool to see if the color recognition is working as intended .
    # for q in newBoard .UC:
    # print (q)

    print_board ( newBoard)
    print('*********************************************')
    print_board(prevBoard)
    for i in range (0 ,8) :
        for j in range (0 ,8) :
            #If a square now holds a piece it didn't before , this is where a piece has moved .
            if newBoard.UC[i][j] == playerColor and prevBoard.UC[i][j] != playerColor:
                NewRank = newBoard.RanksForUpdate [i]
                NewFile = newBoard.FilesForUpdate [j]

            #If a square now does ’t hold a piece and it previously did , this is where a piece has moved from.
            if newBoard.UC[i][j] != playerColor and prevBoard.UC[i][j] == playerColor:
                OldRank = newBoard.RanksForUpdate [i]
                OldFile = newBoard.FilesForUpdate [j]

    move = OldFile+OldRank+ NewFile+NewRank

    # if (prevBoard.C[OldRank][OldFile] == ('p' if playerColor == 'B' else 'P')) and NewRank == newBoard.RanksForUpdate [7]:
    #     print('***************promotion move*********************')
    #     move = move + '=q'




    # check if its a king move , did he castles or not ?
    move=Castiling(newBoard, prevBoard,move, playerColor)
    

    newBoard.updateBoard( move, playerColor)


    return newBoard , move 



if __name__ == "__main__":
    import numpy as np
    import sys
    sys.path.insert(0,'../../AI')
    import AiHelpers as ai

    sys.path.insert(0,'../../ImageProcessing/ChessBoard')
    import ImageHelpers as im