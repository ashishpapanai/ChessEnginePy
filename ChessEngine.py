"""
This class will store all information about the current state of the game and will determine the valid moves, It will
also contain a move log.
"""
class GameState():
    def __init__(self):
        # 8x8 2d list to represent the board with each element represents each piece.
        # each element has two characters, the first character represents the color of piece.
        # the second character represents the type of the piece.
        # represents empty space "__"
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {"p": self.getPawnMoves, "Q": self.getQueenMoves,
                             "B": self.getBishopMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    """
    MakeMove takes move as  a parameter an makes a move to the opted piece (doesn't work for castling, pawn promotion
    or en-passant
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so that it can be undone later
        self.whiteToMove = not self.whiteToMove #swaps player
    """
    Undo the last move
    """
    def UndoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swaps player back

    """
    All moves considering checks
    """
    def getValidMoves(self):
        return self.getALlPossibleMoves() #ignoring checks

    """
    All moves without considering checks
    """
    def getALlPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board)): # number of column
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls appropiate function
        return moves


    """
    Gets all pawn moves for pawn located at row, column and add these moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": # white pawn moves
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 squares leap
                    moves.append((Move((r, c), (r-2, c), self.board)))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c ), (r - 1, c - 1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r-1][c] == "--": # black pawn moves
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 squares leap
                    moves.append((Move((r, c), (r-2, c), self.board)))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c ), (r - 1, c - 1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))



    """
        Gets all rook moves for rook located at row, column and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        pass

    """
            Gets all knight moves for knight located at row, column and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        pass

    """
            Gets all Bishop moves for bishop located at row, column and add these moves to the list
    """

    def getBishopMoves(self, r, c, moves):
        pass

    """
            Gets all King moves for King located at row, column and add these moves to the list
    """

    def getKingMoves(self, r, c, moves):
        pass

    """
            Gets all rook moves for Queen located at row, column and add these moves to the list
    """

    def getQueenMoves(self, r, c, moves):
        pass
    

class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, Board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = Board[self.startRow][self.startCol]
        self.pieceCaptured = Board[self.endRow][self.endCol]
        self.moveId = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol


    """
    Overriding the equals method
    """

    def __eq__(self, other):
        if(isinstance(other, Move)):
            return  self.moveId == other.moveId
        return False



    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

