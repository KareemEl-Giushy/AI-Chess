"""
this is our main Driver File.
Handle user input
current state GameState Object

"""
import pygame as p
import os
import ChessEngine
import ChessAi

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
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # draw pieces on top of the board

# ** The top left squre is always white (black bottom left)**
def drawBoard(screen):
    global color
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

# ======================================================
# Highlight Square Selected And Moves For Piece Selected
# ======================================================
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # Square Selected is a piece that can move
            # highlight Selected Square
            s = p.Surface((SQ_size, SQ_size))
            s.set_alpha(100) #transparency 0 - 255
            s.fill(p.Color("blue"))
            screen.blit(s, (SQ_size * c, SQ_size * r))
            # highlight Valid Moves
            s.fill(p.Color("yellow"))
            for m in validMoves:
                if m.startRow == r and m.startCol == c:
                    screen.blit(s, (SQ_size * m.endCol, SQ_size * m.endRow))

# ==================
# Animating Movement
# ==================
def animateMove(move, screen, board, clock):
    global color
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = color[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_size, move.endRow * SQ_size, SQ_size, SQ_size)
        p.draw.rect(screen, color, endSquare)
        #draw The Captured Piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size))
        p.display.flip()
        clock.tick(60)

# ===============================================
# Drawing Text On The Screen (Wins and Stalemate)
# ===============================================
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("gray"))
    textLocation = p.Rect(0, 0, WIDTH, HIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("black"))
    screen.blit(textObject, textLocation.move(2, 2))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    # Game State
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag Variable to triger movement
    animate = False # animate Flag Variable To triger Animation

    loadImages() # load only once
    running = True
    selectedSq = ()
    sqClicks = []
    gameOver = False
    playerOne = True # If Human Is White This will Be True
    playerTwo = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse Handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    row = location[1] // SQ_size
                    col = location[0] // SQ_size
                    
                    if selectedSq == (row, col):
                        selectedSq = ()
                        sqClicks = []
                    else:
                        selectedSq = (row, col)
                        sqClicks.append(selectedSq)
                    
                    if len(sqClicks) == 2:
                        mov = ChessEngine.Move(sqClicks[0], sqClicks[1], gs.board)
                        print(mov.getMoveNotation())
                        # ====================
                        # It is Extremely Important To Make The Engine Generated Move NOT The User Move
                        # This is Becasue It Has The Extra Flags Used In The Logic But The User Move Doesn't
                        # ====================
                        for v in validMoves:
                            if mov == v:
                                gs.makeMove(v)
                                moveMade = True
                                animate = True
                                selectedSq = ()
                                sqClicks = []
                        if not moveMade:
                            sqClicks = [selectedSq]
            # Key Handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                elif e.key == p.K_r: # Reset The Board When R is Pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    selectedSq = ()
                    sqClicks = []
                    moveMade = False
                    animate = False

        # AI Move Finder Logic
        if not gameOver and not humanTurn:
            bestMove = ChessAi.findBestMove(gs, validMoves)
            if bestMove is None:
                bestMove = ChessAi.findRandomMove(validMoves)
            gs.makeMove(bestMove)
            moveMade = True
            animate = True

        if moveMade:
            if len(gs.moveLog) and animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, selectedSq)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black Wins By Checkmate")
            else:
                drawText(screen, "White Wins By Checkmate")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == '__main__':
    main()

