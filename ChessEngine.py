"""
store the current state.
valid moves.
it will also keep a move log

"""

class GameState():
    def __init__(self) -> None:
        # board is 8*8 2d list with 2 character elemet
        # fist char is piece color (b, W) second char is piece type
        # b is black 
        # w is white
        # -- is blank
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.getFunctionMove = {
            "P": self.getPawnMoves,
            "R": self.getRookMoves,
            "N": self.getKnightMoves,
            "B": self.getBishopMoves,
            "Q": self.getQueenMoves,
            "K": self.getKingMoves,
        }
        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    # all Moves Considering Checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                pieceColor = self.board[r][c][0]
                if (pieceColor == 'w' and self.whiteToMove) or (pieceColor == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.getFunctionMove[piece](r, c, moves)
        print(moves) # Just For Debuging
        return moves

    # =====================================================================
    # PawnMoves (Go Forward, 2 Square Forward, Caputer Right, Capture Left)
    # =====================================================================
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # Just White pawns
            if self.board[r-1][c] == '--': # 1 square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c - 1 >= 0: # cature to the right
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # cature to the left
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        elif not self.whiteToMove:
            if self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c + 1 <= 7: # capture to right 
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
            if c - 1 >= 0: #capture to left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))

    # =====================================================================
    # RookMoves (Forward Vertical, backward Vertical, Forward Horizontal, Backward Horizontal)
    # =====================================================================
    def getRookMoves(self, r, c, moves):
        color = self.board[r][c][0]
        
        i = r + 1
        while i <= 7 and i >= 0: # Move Forward On The Board (vertically on board)
            if self.board[i][c] == '--':
                moves.append(Move((r, c), (i, c), self.board))
            elif self.board[i][c][0] != color:
                moves.append(Move((r, c), (i, c), self.board))
                break
            i += 1
        
        i = r - 1
        while i >= 0 and i <= 7: 
            if self.board[i][c] == '--': # Move backward On The Board (vertically on board)
                moves.append(Move((r, c), (i, c), self.board))
            elif self.board[i][c][0] != color:
                moves.append(Move((r, c), (i, c), self.board))
                break
            i -= 1
        
        j = c + 1
        while j <= 7 and j >= 0: # Move Forward On The Board (Horizontally on board)
            if self.board[r][j] == '--':
                moves.append(Move((r, c), (r, j), self.board))
            elif self.board[r][j][0] != color:
                moves.append(Move((r, c), (r, j), self.board))
                break
            j += 1
        
        j = c - 1
        while j <= 7 and j >= 0: # Move backward On The Board (Horizontally on board)
            if self.board[r][j] == '--':
                moves.append(Move((r, c), (r, j), self.board))
            elif self.board[r][j][0] != color:
                moves.append(Move((r, c), (r, j), self.board))
                break
            j -= 1

    # =====================================================================
    # KnightMoves 
    # =====================================================================
    def getKnightMoves(self, r, c, moves):
        directions = ((-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1))
        color = self.board[r][c][0]
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if self.board[endRow][endCol] != color:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    # =====================================================================
    # BishopMoves Diagonally (Forward-Right, Forward-Left, Backward-Right, Backward-Left)
    # =====================================================================
    def getBishopMoves(self, r, c, moves):
        color = self.board[r][c][0]

        # Move Diagonally Forward-Right
        i = r + 1
        j = c + 1
        while (i <= 7 and i >= 0) and (j <= 7 and j >= 0):
            if self.board[i][j] == '--':
                moves.append(Move((r, c), (i, j), self.board))
            elif self.board[i][j][0] != color:
                moves.append(Move((r, c), (i, j), self.board))
                break
            i += 1
            j += 1

        # Move Diagonally Forward-Left
        i = r + 1
        j = c - 1
        while (i <= 7 and i >= 0) and (j <= 7 and j >= 0):
            if self.board[i][j] == '--':
                moves.append(Move((r, c), (i, j), self.board))
            elif self.board[i][j][0] != color:
                moves.append(Move((r, c), (i, j), self.board))
                break
            i += 1
            j -= 1

        # Move Diagonally Backward-Right
        i = r - 1
        j = c + 1
        while (i <= 7 and i >= 0) and (j <= 7 and j >= 0):
            if self.board[i][j] == '--':
                moves.append(Move((r, c), (i, j), self.board))
            elif self.board[i][j][0] != color:
                moves.append(Move((r, c), (i, j), self.board))
                break
            i -= 1
            j += 1

        # Move Diagonally Backward-Left
        i = r - 1
        j = c - 1
        while (i <= 7 and i >= 0) and (j <= 7 and j >= 0):
            if self.board[i][j] == '--':
                moves.append(Move((r, c), (i, j), self.board))
            elif self.board[i][j][0] != color:
                moves.append(Move((r, c), (i, j), self.board))
                break
            i -= 1
            j -= 1

    # =====================================================================
    # QueenMoves 
    # =====================================================================
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # =====================================================================
    # KingMoves 
    # =====================================================================
    def getKingMoves(self, r, c, moves):
        color = self.board[r][c][0]
        if r + 1 <= 7:
            if self.board[r+1][c][0] != color: # forward
                moves.append(Move((r, c), (r+1, c), self.board))
        if r - 1 >= 0:    
            if self.board[r-1][c][0] != color: # backward
                moves.append(Move((r, c), (r-1, c), self.board))
        
        if c + 1 <= 7:
            if self.board[r][c+1][0] != color: # right
                moves.append(Move((r, c), (r, c+1), self.board))
        if c - 1 >= 0:    
            if self.board[r][c-1][0] != color: # left
                moves.append(Move((r, c), (r, c-1), self.board))
        
        if (r + 1 <= 7 and r + 1 >= 0) and (c + 1 <= 7 and c + 1 >=0):
            if self.board[r+1][c+1][0] != color: # forward-Right
                moves.append(Move((r, c), (r+1, c+1), self.board))
        
        if (r - 1 <= 7 and r - 1 >= 0) and (c - 1 <= 7 and c - 1 >=0):      
            if self.board[r-1][c-1][0] != color: #backward-left
                moves.append(Move((r, c), (r-1, c-1), self.board))
        
        if (r + 1 <= 7 and r + 1 >= 0) and (c - 1 <= 7 and c - 1 >=0):  
            if self.board[r+1][c-1][0] != color: # forward-left
                moves.append(Move((r, c), (r+1, c-1), self.board))
        
        if (r - 1 <= 7 and r - 1 >= 0) and (c + 1 <= 7 and c + 1 >=0):    
            if self.board[r-1][c+1][0] != color: # backward-right
                moves.append(Move((r, c), (r-1, c+1), self.board))

class Move():

    rankToRow = {"1": 7, "2": 6, "3": 5, "4": 4,"5": 3, "6":2, "7": 1, "8": 0}
    rowToRank = {v: k for k, v in rankToRow.items()}
    
    fieldToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colToField = {v: k for k, v in fieldToCol.items()}

    def __init__(self, startSq, endSq, board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    # Generate Real Chess Notation
    def getMoveNotation(self):
        # you Can Add To Generate Correct Notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colToField[c] + self.rowToRank[r]