import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3 

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

# Helper Method To Make The First Recursive Call.
def findBestMove(gs, validMoves : list):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findNegaMaxMove(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

def findMinMaxIterative(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlaryMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove, bot=True)
        opponentValidMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentMove in opponentValidMoves:
            gs.makeMove(opponentMove, bot=True)
            if gs.checkmate:
                score = -CHECKMATE
            elif gs.stalemate:
                score = 0
            else:
                score = -turnMultiplier * scoreMaterial(gs.board) # it became The opposite Color playing
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove(bot=True)
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlaryMove = playerMove
            
        gs.undoMove(bot=True)

    return bestPlaryMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            oppMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, oppMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            oppMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, oppMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findNegaMaxMove(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = - CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxMove(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gs.undoMove()
    return maxScore

def findNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # Move Ordering - Implement Later
    maxScore = - CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gs.undoMove()
        if maxScore > alpha: #prunnig Hapens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
A Positive Score Means White Is Winnig
A Negative Score Means Black Is Winning
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return - CHECKMATE # Black Wins
        else:
            return CHECKMATE # white Wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def scoreMaterial(board: list):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score