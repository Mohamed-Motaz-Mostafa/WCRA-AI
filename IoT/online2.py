import AI.AiHelpers.AiHelpers as ai
import ImageProcessing.ImageHelpers as im
import Sound.SoundHelper.SoundHelper as Sound
import ChessEngine.ChessHelpers.ChessHelpers as chess
import ChessEngine.WCRAchessEngine.ChessEngine as eng
import Embedded.i2c as em
import Embedded.ArduinoCom as rc
import chess as C
import online as ol
import time

time_limit = 3 

def print_board(newBoard):
    print('new board 🥲
    for i in range(8):
        print(newBoard.C[i])

#Sound.playSound('Call_Me_Ziko_Melody4Arab.Com.mp3',0.4)
prevBoard = chess.Board()
newBoard = chess.Board()
#newBoard, move = chess.compareBoards(newBoard, prevBoard, 'W')
#print('move: ',move)
board = C.Board()
color = ''




while(color != "1" and color != "2"):
    em.writedata("0000x")
    color = rc.getArdunioResponse()
    print("your color is" + color)

if color == '2':
    print('start the game')
    while not board.is_game_over() :
        newBoard.setUC(chess.makeNewBoard(newBoard))
        newBoard, HumanMove = chess.compareBoards(newBoard, prevBoard, 'W')
        prevBoard.updateBoard(HumanMove,'W')
        print_board(newBoard)
        print('Your move is : ',HumanMove)
        ol.data(HumanMove)

        armMove=ol.get_move()
         print ("armMove is:",armMove)
         em.writeData(armMove)
elif color == '1':
    print("the engine is thinking....") 
    while not board.is_game_over():
        firstTurn = True
        armMove=ol.get_move()
         print ("armMove is:",armMove)
        em.writeData(armMove)
        print('Make your move : ')

        newBoard.setUC(chess.makeNewBoard(newBoard))
        newBoard, HumanMove = chess.compareBoards(newBoard, prevBoard, 'B')
        prevBoard.updateBoard(str(HumanMove),'B')
        print_board(newBoard)
        print('Your move is : ',HumanMove)
            ol.data(HumanMove)
        firstTurn = False
else:
    print("SOMETHING WENTWRONG")




game=eng.board_to_game(board)
print(game)