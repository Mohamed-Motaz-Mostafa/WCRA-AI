from __future__ import division
from __future__ import print_function
from ctypes import *
import numpy
import collections
import chess.pgn
import chess
import chess.engine


CHECKMATE = 10000
STALEMATE = 0
global DEPTH
DEPTH = 3
global C
global WhiteToMove
C=0
WhiteToMove = True


# load NNUE shared library
nnue = cdll.LoadLibrary("/home/pi/Grad-Project/ChessEngine/WCRAchessEngine/nnue+stockfish/libnnueprobe.so")

# load NNUE weights file
nnue.nnue_init(b"/home/pi/Grad-Project/ChessEngine/WCRAchessEngine/nnue+stockfish/nn-c3ca321c51c9.nnue")
#nnue.nnue_init(b'nn-6877cd24400e.nnue')

def MakeMove(game_state,Move):
   global WhiteToMove 
   WhiteToMove = not WhiteToMove
   game_state.push_san(str(Move))

def UndoMove (game_state):
   global WhiteToMove 
   WhiteToMove = not WhiteToMove
   game_state.pop()


def scoreBoard(state):
   global WhiteToMove

   if state.is_checkmate():

      #print (' >>>>>>>>>>>>>>>>>>>CHECKMATE<<<<<<<<<<<<<<<<<<<')
      return (CHECKMATE-10) * (-1 if WhiteToMove else 1)
     
    
   elif state.is_stalemate():
      return 0
    
    # case draw
   elif state.can_claim_draw():
      return 0
        
    # case in insufficient material
   elif state.is_insufficient_material():
      return 0
    
   # get NNUE evaluation score
   score = nnue.nnue_evaluate_fen(bytes(state.fen(), encoding='utf-8'))
   # use static evaluation score
   return score


def findBestMove(game_state, valid_moves,WhiteToMove=True):
   '''
   get's the best move using NegaMax algorithm in a certain depth
   '''
   global next_move ,C
   next_move = None
   #random.shuffle(valid_moves)
   C=0
   valid_moves= SortingMoves(valid_moves)
   evalscore=findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE ,WhiteToMove)
   #print("defrant bord poss :",C ,'selected score', evalscore)
   if 'x' in next_move :
      arm =  'c'
   elif '=' in next_move :
      arm =  'p'
   else:
      arm = 'm'

   armMove = str(game_state.parse_san(next_move))
   armMove = armMove + arm
   next_move=game_state.parse_san(next_move)
   print ( 'next_move :', next_move )

   return next_move,armMove


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta ,WhiteMove):
   global next_move , C
  # global WhiteToMove
   global DEPTH
   C=C+1
   if (depth == 0) or (game_state.is_game_over()) :
      #print('the score at depth = 0: ',scoreBoard(game_state ))
      return scoreBoard(game_state ) 
   # move ordering - implement later //TODO
   max_score = - CHECKMATE
   for move in valid_moves:

      MakeMove(game_state,move) # push a move to game_state ( board )
      #game_state.push_san(str(move))

      next_moves = game_state.legal_moves # create all poseepols replays for obonent
      #next_moves = SortingMoves(next_moves)
      score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha , WhiteMove) # recall the function to create tree search
      if score > max_score:
         max_score = score
         #print('depth;>>>>>>>>>>>>>>>>>>>>>',depth)
         if depth == DEPTH:
            #print( "This is the chosen  move for now >>>>> depth == DEPTH >>>>>>", move)
            #print ('Score for parants :>>>', score)
            next_move = move
      UndoMove(game_state)
      #game_state.pop()   

      if max_score > alpha:
         alpha = max_score
      if alpha >= beta:
         break
   return max_score



def SortingMoves (valid_moves):
   '''
   this function sorts chess valed moves in a possession by getting algebraic notation from Chess.lagelMoves first then order the moves.
   if checkmate move is in valed moves return that move 
   else 
   let cheeks and captures and pawn moves examend first to speed up search.
   '''
   LM3=chess.LegalMoveGenerator.__iter__(valid_moves)
   LM3=chess.LegalMoveGenerator.__repr__(valid_moves)
   s= LM3.index('(')
   f= LM3.index(')')
   m=[]
   mate=[]
   LM3=LM3[s:f]
   LM3=LM3.replace('(', '')
   LM3=LM3.replace(')', '')
   LM3=LM3.replace(',', '')
   #print('replaceed:',LM3)
   LM3=LM3.split()
   for s in LM3:
      if '#' in s: # checkmate move 
         mate.append(s)
         return mate
      elif '+' in s: #check move
         m.insert(0,s)
      elif 'x' in s: 
         m.insert(0,s)
      elif len(s)==2 :
         m.insert(0,s)
      elif ('=r' or '=b' or '=n') in s: # remove promotions to roak , knight and bishobs 
         pass
      else:
         m.append(s)
   #print('sorted list >>>>:',m)
   return m


def board_to_game(board):

   '''
   gets PNG chess notation ( full game notation )
   '''
   game = chess.pgn.Game()

    # Undo all moves.
   switchyard = collections.deque()
   while board.move_stack:
      switchyard.append(board.pop())

   game.setup(board)
   node = game

   # Replay all moves.
   while switchyard:
      move = switchyard.pop()
      node = node.add_variation(move)
      board.push(move)

   game.headers["Result"] = board.result()
   return game

def SetupEngine(path='/home/pi/Grad-Project/ChessEngine/WCRAchessEngine/nnue+stockfish/stockfish'):
   '''
   setup stockfish chess engine 
   '''
   engine = chess.engine.SimpleEngine.popen_uci(path)
   print ( ' engine loded sucssesfuly !!!!')
   return engine





def VsEngine (engine,game_state, time_limit) :
   result = engine.play(game_state, chess.engine.Limit(time=time_limit))
   MakeMove(game_state ,result.move)
   return result.move # so we can print the move if needed



def AIvsAI(depth,game_state,vs_Stockfish=True): # Ai vs Ai
   global DEPTH
   DEPTH = depth
   if vs_Stockfish:
      engine = chess.engine.SimpleEngine.popen_uci(b"nnue+stockfish/stockfish")
      while not game_state.is_game_over(): # stockfish will play black 

         allMoves = game_state.legal_moves
         bestMove , _ = findBestMove(game_state,allMoves)
         MakeMove(game_state, bestMove )
         print(game_state)
         move= VsEngine (engine,game_state, 5)
         print('Stockfish move : ', move)
         print(game_state)
      engine.quit()

   else :
      while not (game_state.is_game_over()) :

         allMoves = game_state.legal_moves
         bestMove , _ =  findBestMove(game_state,allMoves)
         MakeMove(game_state, bestMove )
         print(game_state)
         print('************************')

   game = board_to_game(game_state)
   print(game)
   return game

#board = chess.Board()
#AIvsAI(3,board,vs_Stockfish=False)




'''
#board = chess.Board(fen='6k1/3pR3/8/8/2q5/4N3/6QP/7K b - - 2 55')
#board = chess.Board(fen='7k/8/8/3R4/8/8/7P/5Q1K w - - 1 60')

#board = chess.Board(fen='4R3/3p4/6k1/8/2q5/4NQ1p/7P/7K b - - 5 52')
board = chess.Board(fen='2r5/3p1pbk/n5p1/3B3p/6r1/7q/2PQ1PPP/1R2RNK1 w - - 0 30')
#

squares_index = {
  'a': 0,
  'b': 1,
  'c': 2,
  'd': 3,
  'e': 4,
  'f': 5,
  'g': 6,
  'h': 7
}



engine = chess.engine.SimpleEngine.popen_uci(b"/home/pi/Grad-Project/ChessEngine/WCRAchessEngine/stockfish")
print ( 'Stockfish engine loded sucssesfuly !!!!')

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)

engine.quit()

'''
