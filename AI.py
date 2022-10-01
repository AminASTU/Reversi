from gameplay import FillBoard_White, HodAI, isGameOver, isOverlay, isRowClosure, create_counter, GetBoard

counterAI = create_counter()

def SearchMoves(deep, x, y, board_copy):
    step = counterAI()
    if(step % 2 == 0):
        board_copy[x-1][y-1] = 'W'
    else:
        board_copy[x-1][y-1] = 'B'

    if(deep < 8 and isGameOver(board_copy) == False):
        scores = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if (isOverlay(i, j) == False):
                    if(step % 2 == 0):
                        if(isRowClosure(i, j, 'B', 'W', board_copy, 't') == True):
                            scores += SearchMoves(deep + 1, i, j)
                    else:
                        if(isRowClosure(i, j, 'W', 'B', board_copy, 't') == True):
                            scores += SearchMoves(deep + 1, i, j)         
        return scores
    scores = getScores(board_copy)
    if(isGameOver(board_copy)):
        return 1000 * (scores['White']- scores['Black'])
    return scores['White']- scores['Black']

def getScores(tmp):
    countB = 0
    countW = 0
    for i in range(0, len(tmp)):
        for j in range(0, len(tmp[i])):
            if (tmp[i][j] == 'B'):
                countB+=1
            elif (tmp[i][j] == 'W'):
                countW+=1
    return {'White': countW, 'Black': countB}
