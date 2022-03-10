"""
this is our main Driver File.
Handle user input
current state GameState Object

"""
import pygame as p
import os
import ChessEngine

dir_path = os.path.dirname(os.path.realpath(__file__))
WIDTH = HIGHT = 512 # 400
DIMENSION = 8 # dimensions of chess is 8*8
SQ_size = HIGHT // DIMENSION
BOARD_COLOR = (p.Color('white'), p.Color('gray'))
MAX_FPS = 15
IMAGES = {}

# one-time load in memory
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(dir_path + "/images/" + piece + ".png"), (SQ_size, SQ_size))

    # Not: Get Any image by IMAGES['piece_name'];
# ======================================
# responsible for all the graphics in the current game state
# ======================================
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board

    # => add in piece highlighting later on in the project <= #
    
    drawPieces(screen, gs.board) # draw pieces on top of the board

# ** The top left squre is always white (black bottom left)**
def drawBoard(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = BOARD_COLOR[(i + j) % 2 ] # if it is even it's white, if it is odd it's gray
            p.draw.rect(screen, color, p.Rect(SQ_size * j, SQ_size * i, SQ_size, SQ_size))

# ** Do highlight under the piece but above the square ** #
def drawPieces(screen, b):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = b[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], (SQ_size * col, SQ_size * row))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    # Game State
    gs = ChessEngine.GameState()
    loadImages() # load only once
    running = True
    selectedSq = ()
    sqClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse Handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[1] // SQ_size
                col = location[0] // SQ_size
                
                if selectedSq == (row, col):
                    selectedSq = ()
                    sqClicks = []
                else:
                    selectedSq = (row, col)
                    sqClicks.append(selectedSq)
                
                if len(sqClicks) == 2 and gs.board[sqClicks[0][0]][sqClicks[0][1]] != '--':
                    mov = ChessEngine.Move(sqClicks[0], sqClicks[1], gs.board)
                    print(mov.getMoveNotation())
                    gs.makeMove(mov)
                    selectedSq = ()
                    sqClicks = []
            # Key Handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == '__main__':
    main()

