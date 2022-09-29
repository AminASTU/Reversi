from board import FillStartBoard, PrintBoard, arrayWord
import re

# Если нет пустых координат - игра закончена
def isGameOver(game):
    flag = True
    for i in range(0, len(game)):
        for j in range(len(game[i])):
            if (game[i][j] == '*'):
                flag = False
            return flag

# Запрос хода
def Move():
    print('Твой ход: ')
    xy = input()
    coordinate = CoordinateRules(xy)
    if(coordinate != 0):
        x_str = coordinate[0]
        y_numb = int(coordinate[1])
        print(type(y_numb))
        print(type(x_str))

# Проверка на вторую координату (буква)
def CheckWordInCoord(check):
    f_word = False
    for word in range(0, len(arrayWord) - 2):
        if(check == arrayWord[word]):
            f_word = True
    return f_word

# Проверка на первую координату (число)
def CheckNumbInCoord(check):
    f_numb = False
    res = int(check)
    for numb in range(1, 9):
        if(res == numb):
            f_numb = True
    return f_numb

# Функция для проверки вводимых координат
def CoordinateRules(xy):
    # error - Флаг для проверки правильности ввода координат
    f_error = False
    if(len(xy) != 2):
        print('Неверный ход!')
        f_error = True
    x = xy[0]
    y = xy[1]
    numb = int()
    str = ''
    # Формирование координаты - (x,y) - (целое, буква)
    if (x.isdigit()):
        if (CheckNumbInCoord(x)):
            numb = x
        else:
            print('Введена неверная числовая координата')
            f_error = True

        if (CheckWordInCoord(y)):
            str = y
        else:
            print('Введена неверная буквенная координата')
            f_error = True
    elif (y.isdigit()):
        if (CheckNumbInCoord(y)):
            numb = y
        else:
            print('Введена неверная числовая координата')
            f_error = True

        if (CheckWordInCoord(x)):
            str = x
        else:
            print('Введена неверная буквенная координата')
            f_error = True
    else:
        print('В вашем ходе нет числовой координаты')
        f_error = True
    if(f_error == False):
        return str + numb
    return 0

game = FillStartBoard()
Move()
if (isGameOver(game)):
    print('GameOver')
else:PrintBoard(game)