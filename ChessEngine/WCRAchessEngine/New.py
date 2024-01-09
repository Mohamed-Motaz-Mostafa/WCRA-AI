
import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci(b"/home/pi/Grad-Project/ChessEngine/WCRAchessEngine/stockfish")
print ( ' engine loded sucssesfuly !!!!')






engine.quit()


'''
  
from chess import uci

class StockfishPlayer(object):
    def __init__(self):
        self._engine = uci.popen_engine('stockfish')
        self._engine.uci()

    def select_move(self, board):
        self._engine.position(board)
        result = self._engine.go(movetime=1000)
        return result.bestmove



        board = chess.Board()
info = chess.engine.Score()
print("Score:", str(info["score"]))
# Score: PovScore(Cp(+20), WHITE)

board = chess.Board("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")
info = engine.analyse(board, chess.engine.Limit(depth=20))
print("Score:", info["score"])
# Score: PovScore(Mate(+1), WHITE)

        '''