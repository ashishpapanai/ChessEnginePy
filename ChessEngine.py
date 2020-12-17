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

        self.whiteKingLocation = (7, 4)
        self.BlackKingLocation = (0, 4)

        self.checkMate = False
        self.staleMate = False

        self.enpassantPossible = () #Co-ordinates of a square where enpassant is possible.
        
        self.inCheck = False
        self.pins = []
        self.checks = []


    """
    MakeMove takes move as  a parameter an makes a move to the opted piece (doesn't work for castling, pawn promotion
    or en-passant
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so that it can be undone later
        self.whiteToMove = not self.whiteToMove #swaps player
        # update king's position if needed
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.whiteKingLocation = (move.endRow, move.endCol)

        #pawn promotion 
        if move.isPawnPromotion:
            promotePiece = input("Promote to Q, R, B, or N \n")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotePiece

        
        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] == '--' #capturing the pawn

        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endCol) == 2:
            #only on two square pawn advances 
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol )
        else:
            self.enpassantPossible = ()    




    """
    Undo the last move
    """
    def UndoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swaps player back
            # update king's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            
            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.startCol] = move.pieceCaptured 
                self.enpassantPossible = (move.endRow, move.endCol)
            
            #undo two square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()





    """
    All moves considering checks
    """
    def getValidMoves(self):
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        moves = []
        #tempEnpassentPossible = self.enpassantPossible
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCOl = self.whiteKingLocation[1]
        else:
            kingRow = self.BlackKingLocation[0]
            kingCOl = self.BlackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1: # only one check
                moves = self.getALlPossibleMoves()
                check = self.checks[0] # check details
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # piece giving check
                validSquares = []
                if pieceChecking[1] == "N": # if the piece is a knight, we need to capture it or move the king
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCOl + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                # Get rid of moves that don't block check
                print(validSquares)
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K': #Move doesn't move king, it must be a piece caputure or block
                        print((moves[i].endRow, moves[i].endCol) )
                        if not(moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: # double check, King has to move
                self.getKingMoves(kingRow, kingCOl, moves)
        else: #Not in check, ALl moves will work
            moves = self.getALlPossibleMoves()

        #self.enpassantPossible = tempEnpassentPossible 
        return moves


    """
    Checks if the piece is pinned or king is in check
    """
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColour = "b"
            allyColour = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColour = "w"
            allyColour = "b"
            startRow = self.BlackKingLocation[0]
            startCol = self.BlackKingLocation[1]
        #Check outwards from king for checks and pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColour and endPiece[1] != 'K':
                        if possiblePin == (): # first allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd Allied piece no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColour:
                        type = endPiece[1] 
                        #There are 5 possibilites for 5 types of pieces
                        # 1. Orthogonally away from king, Piece is a rook.
                        # 2. diagonally away from King, Piece is a bishop.
                        # 3. 1 square away from king, piece is a pawn.
                        # 4. Any direction, Piece is a Queen
                        # 5. Any direction, 1 square away and piece is a King
                        if(0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                ((i == 1 and type == 'p') and ((enemyColour == 'w' and 6 <= j <= 7 ) or (enemyColour == 'b' and 4 <= j <= 5 ))) or\
                                                              (type == 'Q') or (i == 1 and type == 'K'):

                            if possiblePin == (): #no piece blocking, No pin
                                #print("hi")
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking, Pin
                                pins.append(possiblePin)
                                break
                        else: # no check
                            break
                else: # off board
                    break

            """
            Possible checks from knight
            """
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                #print(endPiece[0], )
                if endPiece[0] == enemyColour and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


    """
    Checks if current player is under check
    """
    """ def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.BlackKingLocation[0], self.BlackKingLocation[1])"""

    """
    Checks if the square is under attack
    """
    """def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent's turn
        oppMoves = self.getALlPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # swap moves
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square under attack
                return True
        return False"""


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
        piecePinned = False
        pinDirection = ()
        # print((self.pins))
        for i in range(len(self.pins)-1, -1, -1):

            if(self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.whiteToMove:
            if self.board[r-1][c] == "--": # white pawn moves
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": # 2 squares leap
                        moves.append((Move((r, c), (r-2, c), self.board)))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture left
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r, c ), (r - 1, c - 1), self.board))
                    elif (r + 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r, c ), (r - 1, c - 1), self.board, isEnpassantMove=True))


            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture right
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    elif (r - 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r, c ), (r - 1, c + 1), self.board, isEnpassantMove=True))


        else:
            if self.board[r+1][c] == "--": # black pawn moves
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--": # 2 squares leap
                        moves.append((Move((r, c), (r+2, c), self.board)))
            if c-1 >= 0:
                if not piecePinned or pinDirection == (1, -1):
                    if self.board[r+1][c-1][0] == 'w': # enemy piece to capture left
                        moves.append(Move((r, c ), (r + 1, c - 1), self.board))
                    elif (r + 1, c - 1) == self.enpassantPossible:
                        moves.append(Move((r, c ), (r + 1, c - 1), self.board, isEnpassantMove=True))

            if c+1 <= 7:
                if not piecePinned or pinDirection == (1, 1):
                    if self.board[r+1][c+1][0] == 'w': # enemy piece to capture right
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    elif (r + 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r, c ), (r + 1, c + 1), self.board, isEnpassantMove=True))


        # To add: Pawn promotions



    """
        Gets all rook moves for rook located at row, column and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': #added because we use the same function for queen
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up left down right moves
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": # valid empty space
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # capture enemy piece
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        else: # friendly piece skip
                            break
                else: # off board
                    break

    """
            Gets all knight moves for knight located at row, column and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # L shaped movements
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    """
            Gets all Bishop moves for bishop located at row, column and add these moves to the list
    """

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # diagonal movement
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): # bishop can move maximum 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # valid empty space
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # capture enemy piece
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        else:  # friendly piece skip
                            break
                else:  # off board
                    break


    """
            Gets all King moves for King located at row, column and add these moves to the list
    """

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # enemy piece
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.BlackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    #place king in original position
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.BlackKingLocation = (r, c)

    """
            Gets all rook moves for Queen located at row, column and add these moves to the list
    """

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)



class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, Board, isEnpassantMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = Board[self.startRow][self.startCol]
        self.pieceCaptured = Board[self.endRow][self.endCol]
        #pawn-promotion 
        self.isPawnPromotion = False
        #self.promotionChoice = 'Q'
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        
        #en-passant
        #self.isEnpassantMove = False
        self.isEnpassantMove = isEnpassantMove

        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'


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

