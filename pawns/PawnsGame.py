import chess
import numpy as np

class PawnsGame():
    def __init__(self):
        self.board = chess.Board()
        self.SQUARE_NAMES = np.array(chess.SQUARE_NAMES)
        self.VALIDS_INDEX = np.arange(64*64).reshape(64,64)
    
    def getInitBoard(self):

        b = chess.Board()
        b.clear()

        # Setup white pawns
        for white in range(8,16):
            b.set_piece_at(white, chess.Piece(chess.PAWN, chess.WHITE))

        for black in range(48,56):
            b.set_piece_at(black, chess.Piece(chess.PAWN, chess.BLACK))
        return b
    
    def getBoardSize(self):
        return (8, 8)
    
    def getActionSize(self):
        # Assume any piece can be moved to any other square
        return 64*64

    def vectorize_board(self, board):
        pos_stack = np.zeros((64, 2))
        a = 0
        for color in [True, False]:
            for p in range(1, 7):
                pos_stack[list(board.pieces(p, color)), a] = p
            a += 1
        vector = np.zeros((2, 8, 8))
        vector[0] = np.swapaxes(pos_stack, 0, 1)[0].reshape(8,8)
        vector[1] = np.swapaxes(pos_stack, 0, 1)[1].reshape(8,8)

        return vector
    
    def uci_to_action(self, uci):
        origin = uci[0:2]
        destination = uci[2:4]
        #print(origin)
        #print(destination)
        origin_square = np.where(self.SQUARE_NAMES == origin)[0][0]
        destination_square = np.where(self.SQUARE_NAMES == destination)[0][0]
        index = self.VALIDS_INDEX[origin_square, destination_square]

        return index

    def getNextState(self, board, player, action):
        # Copy board to new board
        b = board.copy()

        origin = np.where(self.VALIDS_INDEX == action)[0][0]
        destination = np.where(self.VALIDS_INDEX == action)[1][0]

        origin_name = chess.square_name(origin)
        destination_name = chess.square_name(destination)

        move = "".join([origin_name, destination_name])
        #print(move)
        is_promotion = (b.piece_at(origin).piece_type == chess.PAWN and chess.square_rank(destination) in [0, 7])

        
        if is_promotion:
            move = str(move + 'q')
        
        move = chess.Move.from_uci(move)

        #print(move)
        #print(list(board.legal_moves))
        b.push(move)

        return (b.mirror(), -player)

    def getValidMoves(self, board, player):
        valids = np.zeros(self.getActionSize())
        for x in list(board.legal_moves):
            m_str = chess.Move.uci(x)
            index = self.uci_to_action(m_str)
            #print(index)
            valids[index] = 1
        return valids


    def getValidMovesHuman(self, board, player):
        return list(board.legal_moves)
    
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        tempBoard = self.vectorize_board(board)

        for x in tempBoard[1][0]:
            if x > 0:
                if player == -1:
                    return 1
                elif player == 1:
                    return -1

        for x in tempBoard[0][7]:
            if x > 0:
                if player == 1:
                    return 1
                elif player == -1:
                    return -1

        if len(list(board.legal_moves)) == 0:
            return 1e-5

        if player == 1:
            if not 1 in tempBoard[0]:
                return -1
            if not 1 in tempBoard[1]:
                return 1
        
        if player == -1:
            if not 1 in tempBoard[0]:
                return 1
            if not 1 in tempBoard[1]:
                return -1
        
        return 0
    
    def getCanonicalForm(self, board, player):
        return board.mirror()
    
    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.fen()
    
    @staticmethod
    def display(board):
        print(board)
