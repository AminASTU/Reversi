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