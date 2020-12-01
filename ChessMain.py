"""
This file will handle current games, It's the main driver file and this will take all inputs and display the state
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
# because of low resolution images
DIMENSION = 8
# dimension of the chess board 8X8
SQ_SIZE = HEIGHT//DIMENSION
# size of the square of chess board

MAX_FPS = 15
# Will be used in animations

IMAGES = {}
# Global dictionary of images, will be called only once in main
def loadImages():
    pieces = ["bp", "bR", "bQ", "bK", "bN", "bB", "wp", "wR", "wQ", "wK", "wN", "wB"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # stored images in the dictionary and scaled images to occupy the square.
# Now we can get the images by using the dictionary.


"""
Main driver, This will handle user input and will update the graphics. 
"""

def main():
    # initialise pygame
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  #flag to check the move made

    loadImages()
    running = True
    sqSelected = ()  #keeps track of last click of the user, Tuple
    playerClicks = []  #keeps a track of player clicks, Two tuples. (
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Listener
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x,y cords of mouse click
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = () # deselect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # reset clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # Keyboard Listener
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when z is pressed
                    gs.UndoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Manages all graphics within current game state
"""


def drawGameState(screen, gs):
    drawBoard(screen)
    #draws board on screen
    drawPieces(screen, gs.board)
    #draws pieces on screen

"""
Draws square on the screen, Top left chess board is always light
"""
def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) %2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    """
    Draws pieces based on current game state
    """
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__" :
    main()
