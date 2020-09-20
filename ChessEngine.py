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
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"]
        ]
        self.whiteToMove = True
        self.moveLog = []