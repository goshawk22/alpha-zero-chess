import numpy as np
import chess

class RandomPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        if valids[a] == 1:
            return a
        else:
            print("Random action not valid")
            assert 1==2

class HumanChessPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        valids = self.game.getValidMovesHuman(board,1)
        breaker = 0
        while breaker == 0:

            a = input()

            for x in valids:
                #print(chess.Move.uci(x))
                #print(type(chess.Move.uci(x)))
                if chess.Move.uci(x) == a:
                    breaker = 1
            else:
                print("Invalid: Please try again.")

        return a