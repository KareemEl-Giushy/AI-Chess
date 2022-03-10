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
        moves = [Move((6, 6), (4, 6), self.board)]
        for r in range(8):
            for c in range(8):
                pieceColor = self.board[r][c][0]
                if (pieceColor == 'w' and self.whiteToMove) or (pieceColor == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves()
                    elif piece == 'R':
                        self.getRookMoves()
        return moves

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