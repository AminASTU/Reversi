from tkinter import DISABLED

# Массивы для определения полей игровой доски
arrayWord = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '', '']
arrayNumb = [1, 2, 3, 4, 5, 6, 7, 8, '', '']
arrayLineH = ['-', '-', '-', '-', '-', '-', '-', '-', '', '']
arrayLineV = ['|', '|', '|', '|', '|', '|', '|', '|', '', '']

# Заполнение начальной игровой доски
def FillStartBoard():
    col = 8
    row = 8
    board = []
    for i in range(0, row):
        board.append([])
        for j in range(0 , col):
            if (i == 3 and j == 3 or i == 4 and j == 4):
                board[i].append('W')
            elif (i == 3 and j == 4 or i == 4 and j == 3):
                board[i].append('B')
            else:
                board[i].append('*')
    return board

# Вывод игровой доски
def PrintBoard(board):
    z = int(0)
    q = int(0)
    v = int(0)
    h = int(0)
    for i in range(0, 10):
        for j in range(10):
            if(i < 8 and j < 8):
                print(board[i][j], end='  ')
            else:
                if (i == 8):
                    print(arrayLineH[h], end='  ')
                    h+=1
                if (j == 8):
                    print(arrayLineV[v], end='  ')
                    v+=1
                if (i == 9):
                    print(arrayNumb[z], end='  ')
                    z+=1
                if (j == 9):
                    print(arrayWord[q], end='  ')
                    q+=1
        print()