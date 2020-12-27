import pyspiel
import numpy as np

class ChessGame():
    def __init__(self):
        self.game = pyspiel.load_game("chess")
    
    def getInitBoard(self):

        b = self.game.new_initial_state()

        return b
    
    def getBoardSize(self):
        return (8, 8)
    
    def getActionSize(self):
        # 4672
        return 4672

    def getNextState(self, state, player, action):
        # Copy board to new board
        board = state.child(action)

        return (board, -player)

    def getValidMoves(self, state, player):
        valids = state.legal_actions_mask()
        return valids

    def getValidMovesHuman(self):
        return [self.state.action_to_string(x) for x in self.state.legal_actions()]
    
    def getCanonicalForm(self, board, player):
        return board

    def getGameEnded(self, state, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        
        if not state.is_terminal():
            return 0

        rewards = state.rewards()

        if (rewards[0] == 1):
            return 1

        elif (rewards[0] == 0):
            return 1e-5

        elif (rewards[0] == -1):
            return -1

        else:
            print("Error: Result not valid")
            assert 1 == 2
    
    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return str(board)
    
    def arrayRepresentation(self, state):
        return np.array(state.observation_tensor()).reshape(self.game.observation_tensor_shape())
    
    @staticmethod
    def display(state):
        board = chess.Board(str(state))
        print(board)
