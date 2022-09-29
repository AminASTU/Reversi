from board import FillStartBoard, PrintBoard, arrayWord

def isGameOver(game):
    flag = True
    for i in range(0, len(game)):
        for j in range(len(game[i])):
            if (game[i][j] == '*'):
                flag = False
            return flag
def Move():
    print('Твой ход: ')
    xy = input()



game = FillStartBoard()
Move()
if (isGameOver(game)):
    print('GameOver')
else:PrintBoard(game)