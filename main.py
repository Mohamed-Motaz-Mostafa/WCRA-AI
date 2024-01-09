import AI.AiHelpers.AiHelpers as ai
import ImageProcessing.ImageHelpers as im
#import Sound.SoundHelper.SoundHelper as Sound
import ChessEngine.ChessHelpers.ChessHelpers as chess
import ChessEngine.WCRAchessEngine.ChessEngine as eng
#import Embedded.i2c as em
import Embedded.ArduinoCom as rc
import chess as C   
import time
import IoT.online as ol
import serial

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)


time_limit = 3 

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()




def print_board(newBoard):
	print('new board :')
	for i in range(8):
		print(newBoard.C[i])

#Sound.playSound('Call_Me_Ziko_Melody4Arab.Com.mp3',0.4)

#newBoard, move = chess.compareBoards(newBoard, prevBoard, 'W')
#print('move: ',move)
board = C.Board()
color = '1'
mode = '2'
modes = ['online', 'offline']
difficulties =['easy', 'hard']
# while(mode != "1" and mode != "2"):
# 	ser.write("0000o".encode('utf-8'))
# 	mode = rc.getArduinoResponse()
# 	print("you are playing " + modes[int(mode)-1])

# if mode == '2':
# 	difficulty = rc.getArduinoResponse()
# 	print("you are playing " + difficulties[int(difficulty)-1])
# 	if difficulty == '2' :
# 		engine = eng.SetupEngine9()

# while(color != "1" and color != "2"):
# 	ser.write("0000x".encode('utf-8'))
# 	color = rc.getArduinoResponse()
# 	print("your color is" + color)










if mode=='2':
		
	if color == '2':

		print('start the game')
		prevBoard = chess.Board('W')
		newBoard = chess.Board('W')
		while not board.is_game_over() :
			print ( "Make your move and press the Button ")
			while True:
				input_state = GPIO.input(18)
				if input_state == False :
					break
			
			print('Button pressed')
			newBoard.setUC(chess.makeNewBoard(newBoard))
			newBoard, HumanMove = chess.compareBoards(newBoard, prevBoard, 'W')
			prevBoard.updateBoard(HumanMove,'W')
			print_board(newBoard)
			print('Your move is : ',HumanMove)
			eng.MakeMove(board,HumanMove)	
			allMoves = board.legal_moves
			print("the engine is thinking.....")
			AiMove , armMove  = eng.findBestMove(board,allMoves)
			print('this is armMove: ',armMove)
			newBoard.updateBoard( str(AiMove) , 'B')
			prevBoard.updateBoard(str(AiMove),'B')
			eng.MakeMove(board , AiMove )
			print(board)
			print('AI Move : ',AiMove)
			ser.write(armMove.encode('utf-8'))
			print('Make your move : ')
			#time.sleep(5)
			print('10 secand lift.......')
			#time.sleep(5)
		game=eng.board_to_game(board)
		print(game)

	elif color == '1':
		prevBoard = chess.Board('B')
		newBoard = chess.Board('B')
		print("the engine is thinking....") 
		while not board.is_game_over():
			firstTurn = True
			allMoves = board.legal_moves
			AiMove , armMove = eng.findBestMove(board,allMoves)
			print('this is armMove: ',armMove)
			newBoard.updateBoard( str(AiMove) , 'w')
			prevBoard.updateBoard(str(AiMove),'w')
			eng.MakeMove(board , AiMove )
			print(board)
			print('AI Move : ',AiMove)
			ser.write(armMove.encode('utf-8'))
			line= ser.readline().decode('utf-8').rstrip()
			while(line == ""):
				line= ser.readline().decode('utf-8').rstrip()
			print(line)
			#time.sleep(16)
			print('Make your move : ')
			#time.sleep(3)
			print('30 secand lift.......')
			#time.sleep(3)
			print ( "Make your move and press the Button ")
			while True:
				input_state = GPIO.input(18)
				if input_state ==False:
				    break
			print('Button pressed')
			newBoard.setUC(chess.makeNewBoard(newBoard))
			newBoard, HumanMove = chess.compareBoards(newBoard, prevBoard, 'B')
			prevBoard.updateBoard(str(HumanMove),'B')
			print_board(newBoard)
			print('Your move is : ',HumanMove)
			eng.MakeMove(board,HumanMove)
			firstTurn = False
		game=eng.board_to_game(board)
		print(game)

	else:
		print("SOMETHING WENTWRONG")
elif mode=='1' :
	print('you are on online mode ')
	prevBoard = chess.Board('B')
	newBoard = chess.Board('B')
	client = ol.SetUp()
	DBmoves,DBmovesToPrint = ol.AcessDB(client)
	HM='b2b6'
	onlineMove=ol.ReadLastMove(HM)
	while not board.is_game_over() :
		print('reding......')
		onlineMove=ol.ReadLastMove(HM)
		#ser.write(onlineMove.encode('utf-8'))
		eng.MakeMove(board,onlineMove)
		#print ( "Make your move and press the Button ")
		HM = input("Make your move: ")
		# newBoard.updateBoard( str(onlineMove) , 'w')
		# prevBoard.updateBoard(str(onlineMove),'w')
		# while True:
		# 	input_state = GPIO.input(18)
		# 	if input_state ==False:
		# 	    break
		# newBoard.setUC(chess.makeNewBoard(newBoard))
		# newBoard, HumanMove = chess.compareBoards(newBoard, prevBoard, 'B')
		# prevBoard.updateBoard(str(onlineMove),'B')
		eng.MakeMove(board,HM)

		print_board(board)
		print('Your move is : ',HM)
		ol.AddNewMove(HM,DBmoves)





		onlineMove=onlineMove[3]









else:
	print("SOMETHING WENTWRONG")



































'''

import AI.AiHelpers.AiHelpers as ai
import ImageProcessing.ImageHelpers as im
import Sound.SoundHelper.SoundHelper as Sound
import ChessEngine.ChessHelpers.ChessHelpers as chess
import ChessEngine.WCRAchessEngine.ChessEngine as eng
import chess as C
import time

def print_board(newBoard):
	print('new board :')
	for i in range(8):
		print(newBoard.C[i])


#Sound.playSound('Call_Me_Ziko_Melody4Arab.Com.mp3',0.4)

prevBoard = chess.Board()
newBoard = chess.Board()


#newBoard, move = chess.compareBoards(newBoard, prevBoard, 'W')



#print('move: ',move)

board = C.Board()

while not board.is_game_over() :
	newBoard.setUC(chess.makeNewBoard(newBoard))
	newBoard, HumanMove = chess.compareBoards(newBoard, prevBoard, 'W')
	prevBoard.updateBoard(str(HumanMove),'W')
	print_board(newBoard)
	print('Your move is : ',HumanMove)
	eng.MakeMove(board,HumanMove)
	allMoves = board.legal_moves
	AiMove = eng.findBestMove(board,allMoves)
	newBoard.updateBoard( str(AiMove) , 'B')
	prevBoard.updateBoard(str(AiMove),'B')
	eng.MakeMove(board , AiMove )
	print(board)
	print('AI Move : ',AiMove)
	print('Make your move : ')
	time.sleep(20)
	print('10 secand lift.......')
	time.sleep(10)

game=eng.board_to_game(board)
print(game)
'''