from copy import copy, deepcopy
import time
from board import FillStartBoard, PrintBoard, arrayWord

# Счетчик для ходов (Черные начинают партию)
def create_counter():
    i = 0
    def func():
        nonlocal i
        i += 1
        return i
    return func

counter = create_counter()

board = FillStartBoard()

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
    step = counter()

    f_whitePass = False
    f_blackPass = False
    if (step % 2 == 0):
        if (isNotMove('W', 'B') == True):
            print('Белые пропускают ход')
            f_whitePass = True
            step = counter()
            if (isNotMove('B', 'W') == True):
                print('Черные пропускают ход')
                f_blackPass = True
    else:
        if (isNotMove('B', 'W') == True):
            print('Черные пропускают ход')
            f_blackPass = True
            step = counter()
            if (isNotMove('W', 'B') == True):
                print('Белые пропускают ход')
                f_whitePass = True
    # Если оба игрока вынуждены сделать пропуск - конец игры (ходов больше нет)
    if(f_blackPass and f_whitePass):
        return True
    
    if (step % 2 == 0):
        print('Ход Белых: ')
    else:
        print('Ход Черных: ')

    xy = input()
    if(xy.lower() == 'exit'):
        return False
    else: 
        coordinate = CoordinateRules(xy.lower())
        # Получение готовых координат
        x_coord = int()
        y_coord = int()
        if(coordinate != 0):
            x_coord = int(coordinate[1])
            y_coord = int(coordinate[0])
        # Если произошло наложение на фишку, то повторить ход
        if(isOverlay(x_coord, y_coord, board)):
            print('Ошибочный ход. Наложение на фишку')
            step = counter()
        else:
            if (step % 2 == 0):
                if(isRowClosure(x_coord, y_coord, 'B', 'W', board, 'f')):
                    FillBoard_White(x_coord, y_coord)
                else:
                    step = counter()
            else:
                if(isRowClosure(x_coord, y_coord, 'W', 'B', board, 'f')):
                    FillBoard_Black(x_coord, y_coord)
                else:
                    step = counter()

# Возможен ли ход? Оптимизированная функция - БОЛЬШАЯ - не дописана :(
def isNotMoveOpt(you, enemy):
    points = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if(board[i][j] == enemy):
                points.append(str(i) + str(j))
    moves = []
    for i in range(0, len(points)):
        if(int(points[i][0]) == 0):
            if(int(points[i][1]) == 0):
                moves.append(points[i])
                moves.append(str(int(points[i][0]) + 1) + points[i][1])
                moves.append(points[i][0] + str(int(points[i][1]) + 1))
                moves.append(str(int(points[i][0]) + 1) + str(int(points[i][1]) + 1))
    return False

def isNotMove(you, enemy):
    for i in range(1, 9):
        for j in range(1, 9):
            if (isOverlay(i, j, board) == False):
                if(isRowClosure(i, j, enemy, you, board, 't') == True):
                    return False
    return True
# Проверка на вторую координату (буква)
def CheckWordInCoord(check):
    for word in range(0, len(arrayWord) - 2):
        if(check == arrayWord[word]):
            return word + 1
    return -1

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
    x_coord = int()
    y_coord = int()
    # Формирование координаты - (x,y) - (целое, буква)
    if (x.isdigit()):
        if (CheckNumbInCoord(x)):
            x_coord = x
        else:
            print('Введена неверная числовая координата')
            f_error = True

        if (CheckWordInCoord(y) != -1):
            y_coord = str(CheckWordInCoord(y))
        else:
            print('Введена неверная буквенная координата')
            f_error = True
    elif (y.isdigit()):
        if (CheckNumbInCoord(y)):
            x_coord = y
        else:
            print('Введена неверная числовая координата')
            f_error = True

        if (CheckWordInCoord(x) != -1):
            y_coord = str(CheckWordInCoord(x))
        else:
            print('Введена неверная буквенная координата')
            f_error = True
    else:
        print('В вашем ходе нет числовой координаты')
        f_error = True
    if(f_error == False):
        return x_coord + y_coord
    return 0

# Функция для хода белых
def FillBoard_White(x_coord, y_coord):
    board[x_coord - 1][y_coord - 1] = 'W'

# Функция для хода черных
def FillBoard_Black(x_coord, y_coord):
    board[x_coord - 1][y_coord - 1] = 'B'

# Функция для проверки хода (наложение на другую фишку)
def isOverlay(x_coord, y_coord, board_check):
    if(board_check[x_coord - 1][y_coord - 1] == 'W' or board_check[x_coord - 1][y_coord - 1] == 'B'):
        return True
    return False

def OnRight(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord - 1][y_coord] == enemy):
        newCoordinates = []
        steps = 8 - y_coord
        for i in range(0, steps):
            newCoordinates.append(str(x_coord - 1) + str(y_coord + i))
            if (_board[x_coord - 1][y_coord + i] != you) and (_board[x_coord - 1][y_coord + i] != enemy):
                return -1
            if (_board[x_coord - 1][y_coord + i] == you):
                return newCoordinates          
    return -1
def OnLeft(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord - 1][y_coord - 2] == enemy):
        newCoordinates = []
        steps = y_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord - 1) + str(y_coord - (2 + i)))
            if (_board[x_coord - 1][y_coord - (2 + i)] != you) and (_board[x_coord - 1][y_coord - (2 + i)] != enemy):
                return -1
            elif (_board[x_coord - 1][y_coord - (2 + i)] == you):
                return newCoordinates          
    return -1
def OnUp(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord - 2][y_coord - 1] == enemy):
        newCoordinates = []
        steps = x_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord - (2 + i)) + str(y_coord - 1))
            if (_board[x_coord - (2 + i)][y_coord - 1]  != you) and (_board[x_coord - (2 + i)][y_coord - 1] != enemy):
                return -1
            elif (_board[x_coord - (2 + i)][y_coord - 1] == you):
                return newCoordinates          
    return -1
def OnDown(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord][y_coord - 1] == enemy):
        newCoordinates = []
        steps = 8 - x_coord
        for i in range(0, steps):
            newCoordinates.append(str(x_coord + i) + str(y_coord - 1))
            if (_board[x_coord + i][y_coord - 1] != you) and (_board[x_coord + i][y_coord - 1] != enemy):
                return -1
            elif (_board[x_coord + i][y_coord - 1] == you):
                return newCoordinates          
    return -1

def OnUpLeft(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord - 2][y_coord - 2] == enemy):
        newCoordinates = []
        steps = x_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord - (2 + i)) + str(y_coord  - (2 + i)))
            if (_board[x_coord - (2 + i)][y_coord - (2 + i)] != you) and (_board[x_coord - (2 + i)][y_coord  - (2 + i)] != enemy):
                return -1
            elif (_board[x_coord - (2 + i)][y_coord  - (2 + i)] == you):
                return newCoordinates          
    return -1

def OnUpRight(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord - 2][y_coord] == enemy):
        newCoordinates = []
        steps = 8 - y_coord
        for i in range(0, steps):
            newCoordinates.append(str(x_coord - (2 + i)) + str(y_coord + i))
            if (_board[x_coord - (2 + i)][y_coord + i] != you) and (_board[x_coord - (2 + i)][y_coord + i] != enemy):
                return -1
            elif (_board[x_coord - (2 + i)][y_coord + i] == you):
                return newCoordinates          
    return -1

def OnDownLeft(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord][y_coord - 2] == enemy):
        newCoordinates = []
        steps = 8 - x_coord
        for i in range(0, steps):
            newCoordinates.append(str(x_coord + i) + str(y_coord - (2 + i)))
            if (_board[x_coord + i][y_coord - (2 + i)] != you) and (_board[x_coord + i][y_coord - (2 + i)] != enemy):
                return -1
            elif (_board[x_coord + i][y_coord - (2 + i)] == you):
                return newCoordinates          
    return -1

def OnDownRight(x_coord, y_coord, enemy, you, _board):
    if(_board[x_coord][y_coord] == enemy):
        newCoordinates = []
        steps = 8 - y_coord
        for i in range(0, steps):
            newCoordinates.append(str(x_coord + i) + str(y_coord + i))
            print('x: ', x_coord + i, 'y: ', y_coord + i)
            if (_board[x_coord + i][y_coord + i] != you) and (_board[x_coord + i][y_coord + i] != enemy):
                return -1
            elif (_board[x_coord + i][y_coord + i] == you):
                return newCoordinates          
    return -1
def Reverse(array, you):
    for i in range(0, len(array)):
        board[int(array[i][0])][int(array[i][1])] = you

def GetBoard():
    return board

# Функция для проверки хода (рядом с фишкой соперника + замыкание ряда)
# f_check - Флаг для проверки возможности хода
# 't' - проверяется наличие хода - делать Reverse - не нужно
def isRowClosure(x_coord, y_coord, enemy, you, _board, f_check):
    if(y_coord-1 == 0 or y_coord-1 == 1):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (_board[x_coord - 1][y_coord] == enemy or _board[x_coord][y_coord - 1] == enemy or 
                _board[x_coord][y_coord] == enemy):
                
                # Проверка на замыкание
                reverseRight = OnRight(x_coord, y_coord, enemy, you, _board)
                if(reverseRight != -1 and f_check == 'f'):
                    Reverse(reverseRight, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you, _board)
                if(reverseDown != -1 and f_check == 'f'):
                    Reverse(reverseDown, you)
                
                reverseDownRight = OnDownRight(x_coord, y_coord, enemy, you, _board)
                if(reverseDownRight != -1 and f_check == 'f'):
                    Reverse(reverseDownRight, you)
                
                if (reverseDown != -1 or reverseDownRight != -1 or reverseRight != -1):
                    return True
                return False
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (_board[x_coord - 2][y_coord - 1] == enemy or _board[x_coord - 2][y_coord] == enemy or 
                _board[x_coord - 1][y_coord] == enemy):
                
                # Проверка на замыкание
                reverseUp = OnUp(x_coord, y_coord, enemy, you, _board)
                if(reverseUp != -1 and f_check == 'f'):
                    Reverse(reverseUp, you)

                reverseRight = OnRight(x_coord, y_coord, enemy, you, _board)
                if(reverseRight != -1 and f_check == 'f'):
                    Reverse(reverseRight, you)
                
                reverseUpRight = OnUpRight(x_coord, y_coord, enemy, you, _board)
                if(reverseUpRight != -1 and f_check == 'f'):
                    Reverse(reverseUpRight, you)
                
                if (reverseUp != -1 or reverseUpRight != -1 or reverseRight != -1):
                    return True
                return False
        else:
            if (_board[x_coord - 2][y_coord - 1] == enemy or _board[x_coord - 2][y_coord] == enemy or 
                _board[x_coord - 1][y_coord] == enemy or _board[x_coord][y_coord] == enemy or 
                _board[x_coord][y_coord - 1] == enemy):
                
                # Проверка на замыкание
                reverseRight = OnRight(x_coord, y_coord, enemy, you, _board)
                if(reverseRight != -1 and f_check == 'f'):
                    Reverse(reverseRight, you)

                reverseUp = OnUp(x_coord, y_coord, enemy, you, _board)
                if(reverseUp != -1 and f_check == 'f'):
                    Reverse(reverseUp, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you, _board)
                if(reverseDown != -1 and f_check == 'f'):
                    Reverse(reverseDown, you)
                
                reverseDownRight = OnDownRight(x_coord, y_coord, enemy, you, _board)
                if(reverseDownRight != -1 and f_check == 'f'):
                    Reverse(reverseDownRight, you)

                reverseUpRight = OnUpRight(x_coord, y_coord, enemy, you, _board)
                if(reverseUpRight != -1 and f_check == 'f'):
                    Reverse(reverseUpRight, you)
                
                if (reverseUp != -1 or reverseUpRight != -1 or reverseRight != -1 or reverseDownRight != -1 or reverseDown != -1):
                    return True
                return False
    elif (y_coord-1 == 7 or y_coord-1 == 6):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (_board[x_coord - 1][y_coord - 2] == enemy or _board[x_coord][y_coord - 2] == enemy or 
                _board[x_coord][y_coord - 1] == enemy):
                
                # Проверка на замыкание
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseLeft != -1 and f_check == 'f'):
                    Reverse(reverseLeft, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you, _board)
                if(reverseDown != -1 and f_check == 'f'):
                    Reverse(reverseDown, you)
                
                reverseDownLeft = OnDownLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseDownLeft != -1 and f_check == 'f'):
                    Reverse(reverseDownLeft, you)

                if (reverseLeft != -1 or reverseDownLeft != -1 or reverseDown != -1):
                    return True
                return False
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (_board[x_coord - 1][y_coord - 2] == enemy or _board[x_coord - 2][y_coord - 2] == enemy or 
                _board[x_coord - 2][y_coord - 1] == enemy):
                
                # Проверка на замыкание
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseLeft != -1 and f_check == 'f'):
                    Reverse(reverseLeft, you)
                
                reverseUp = OnUp(x_coord, y_coord, enemy, you, _board)
                if(reverseUp != -1 and f_check == 'f'):
                    Reverse(reverseUp, you)
                
                reverseUpLeft = OnUpLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseUpLeft != -1 and f_check == 'f'):
                    Reverse(reverseUpLeft, you)

                if (reverseLeft != -1 or reverseUpLeft != -1 or reverseUp != -1):
                    return True
                return False
        else:
            if (_board[x_coord - 2][y_coord - 1] == enemy or _board[x_coord - 2][y_coord - 2] == enemy or 
                _board[x_coord - 1][y_coord - 2] == enemy or _board[x_coord][y_coord - 2] == enemy or 
                _board[x_coord][y_coord - 1] == enemy):
                
                # Проверка на замыкание
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseLeft != -1 and f_check == 'f'):
                    Reverse(reverseLeft, you)
                
                reverseUp = OnUp(x_coord, y_coord, enemy, you, _board)
                if(reverseUp != -1 and f_check == 'f'):
                    Reverse(reverseUp, you)

                reverseDown = OnDown(x_coord, y_coord, enemy, you, _board)
                if(reverseDown != -1 and f_check == 'f'):
                    Reverse(reverseDown, you)
                
                reverseDownLeft = OnDownLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseDownLeft != -1 and f_check == 'f'):
                    Reverse(reverseDownLeft, you)

                reverseUpLeft = OnUpLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseUpLeft != -1 and f_check == 'f'):
                    Reverse(reverseUpLeft, you)
                
                if (reverseLeft != -1 or reverseUpLeft != -1 or reverseUp != -1 or reverseDown != -1 or reverseDownLeft != -1):
                    return True
                return False
    elif (y_coord-1 > 1 and y_coord-1 < 6):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (_board[x_coord - 1][y_coord - 2] == enemy or _board[x_coord][y_coord - 2] == enemy or 
                _board[x_coord][y_coord - 1] == enemy or _board[x_coord][y_coord] == enemy or 
                _board[x_coord - 1][y_coord] == enemy):
                
                # Проверка на замыкание
                reverseRight = OnRight(x_coord, y_coord, enemy, you, _board)
                if(reverseRight != -1 and f_check == 'f'):
                    Reverse(reverseRight, you)
                
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseLeft != -1 and f_check == 'f'):
                    Reverse(reverseLeft, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you, _board)
                if(reverseDown != -1 and f_check == 'f'):
                    Reverse(reverseDown, you)
                
                reverseDownRight = OnDownRight(x_coord, y_coord, enemy, you, _board)
                if(reverseDownRight != -1 and f_check == 'f'):
                    Reverse(reverseDownRight, you)
                
                reverseDownLeft = OnDownLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseDownLeft != -1 and f_check == 'f'):
                    Reverse(reverseDownLeft, you)

                if (reverseLeft != -1 or reverseRight != -1 or reverseDownRight != -1 or reverseDown != -1 or reverseDownLeft != -1):
                    return True
                return False
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (_board[x_coord - 2][y_coord - 1] == enemy or _board[x_coord - 2][y_coord - 2] == enemy or 
                _board[x_coord - 1][y_coord - 2] == enemy or _board[x_coord - 2][y_coord] == enemy or 
                _board[x_coord - 1][y_coord] == enemy):
                
                # Проверка на замыкание
                reverseRight = OnRight(x_coord, y_coord, enemy, you, _board)
                if(reverseRight != -1 and f_check == 'f'):
                    Reverse(reverseRight, you)
                
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseLeft != -1 and f_check == 'f'):
                    Reverse(reverseLeft, you)
                
                reverseUp = OnUp(x_coord, y_coord, enemy, you, _board)
                if(reverseUp != -1 and f_check == 'f'):
                    Reverse(reverseUp, you)
                
                reverseUpRight = OnUpRight(x_coord, y_coord, enemy, you, _board)
                if(reverseUpRight != -1 and f_check == 'f'):
                    Reverse(reverseUpRight, you)

                reverseUpLeft = OnUpLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseUpLeft != -1 and f_check == 'f'):
                    Reverse(reverseUpLeft, you)

                if (reverseLeft != -1 or reverseRight != -1 or reverseUp != -1 or reverseUpRight != -1 or reverseUpLeft != -1):
                    return True
                return False
        else:
            if(_board[x_coord - 2][y_coord - 2] == enemy or _board[x_coord - 1][y_coord - 2] == enemy or
                _board[x_coord - 2][y_coord - 1] == enemy or _board[x_coord][y_coord - 1] == enemy or
                _board[x_coord - 1][y_coord] == enemy or _board[x_coord][y_coord] == enemy or
                _board[x_coord][y_coord - 2] == enemy or _board[x_coord - 2][y_coord] == enemy):
                
                # Проверка на замыкание
                reverseRight = OnRight(x_coord, y_coord, enemy, you, _board)
                if(reverseRight != -1 and f_check == 'f'):
                    Reverse(reverseRight, you)

                reverseLeft = OnLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseLeft != -1 and f_check == 'f'):
                    Reverse(reverseLeft, you)

                reverseUp = OnUp(x_coord, y_coord, enemy, you, _board)
                if(reverseUp != -1 and f_check == 'f'):
                    Reverse(reverseUp, you)

                reverseDown = OnDown(x_coord, y_coord, enemy, you, _board)
                if(reverseDown != -1 and f_check == 'f'):
                    Reverse(reverseDown, you)

                reverseDownRight = OnDownRight(x_coord, y_coord, enemy, you, _board)
                if(reverseDownRight != -1 and f_check == 'f'):
                    Reverse(reverseDownRight, you)

                reverseDownLeft = OnDownLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseDownLeft != -1 and f_check == 'f'):
                    Reverse(reverseDownLeft, you)

                reverseUpRight = OnUpRight(x_coord, y_coord, enemy, you, _board)
                if(reverseUpRight != -1 and f_check == 'f'):
                    Reverse(reverseUpRight, you)
                
                reverseUpLeft = OnUpLeft(x_coord, y_coord, enemy, you, _board)
                if(reverseUpLeft != -1 and f_check == 'f'):
                    Reverse(reverseUpLeft, you)
                
                if (reverseLeft != -1 or reverseRight != -1 or reverseUp != -1 or reverseUpRight != -1 or reverseUpLeft != -1
                    or reverseDown != -1 or reverseDownRight != -1 or reverseDownLeft != -1):
                    return True
                return False
    return False
def Result():
    countW = 0
    countB = 0
    countEm = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if (board[i][j] == 'W'):
                countW+=1
            elif (board[i][j] == 'B'):
                countB+=1
            else:
                countEm+=1
    if(countW > countB):
        print('Со счетом: ', countW, ' - ', countB, ' победили БЕЛЫЕ фишки. Пустых полей: ', countEm)
    elif (countW > countB):
        print('Со счетом: ', countB, ' - ', countW, ' победили ЧЕРНЫЕ фишки. Пустых полей: ', countEm)
    else:
        print('Ничья: ', countB, ' - ', countW, '. Пустых полей: ', countEm)

# Запрос хода
def WithAI():
    step = counter()

    f_whitePass = False
    f_blackPass = False
    if (step % 2 == 0):
        if (isNotMove('W', 'B') == True):
            print('Белые пропускают ход')
            f_whitePass = True
            step = counter()
            if (isNotMove('B', 'W') == True):
                print('Черные пропускают ход')
                f_blackPass = True
    else:
        if (isNotMove('B', 'W') == True):
            print('Черные пропускают ход')
            f_blackPass = True
            step = counter()
            if (isNotMove('W', 'B') == True):
                print('Белые пропускают ход')
                f_whitePass = True
    # Если оба игрока вынуждены сделать пропуск - конец игры (ходов больше нет)
    if(f_blackPass and f_whitePass):
        return True
    xy = ''
    if (step % 2 == 0):
        print('Ход Белых: ')
        MoveAI()
        step = counter()
    else:
        print('Ход Черных: ')
        xy = input()
    if(xy.lower() == 'exit'):
        return False
    else: 
        coordinate = CoordinateRules(xy.lower())
        # Получение готовых координат
        x_coord = int()
        y_coord = int()
        if(coordinate != 0):
            x_coord = int(coordinate[1])
            y_coord = int(coordinate[0])
        # Если произошло наложение на фишку, то повторить ход
        if(isOverlay(x_coord, y_coord, board)):
            print('Ошибочный ход. Наложение на фишку')
            step = counter()
        else:
            if(isRowClosure(x_coord, y_coord, 'W', 'B', board, 'f')):
                FillBoard_Black(x_coord, y_coord)
            else:
                step = counter()

counterAI = create_counter()
def SearchMoves(deep, x, y, board_copy):
    step = counterAI() + 1
    if(step % 2 == 0):
        board_copy[x-1][y-1] = 'W'
    else:
        board_copy[x-1][y-1] = 'B'
    if(deep < 8 and isGameOver(board_copy) == False):
        scores = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if (isOverlay(i, j, board_copy) == False):
                    if(step % 2 == 0):
                        if(isRowClosure(i, j, 'W', 'B', board_copy, 't') == True):
                            scores += SearchMoves(deep + 1, i, j, board_copy)
                    else:
                        if(isRowClosure(i, j, 'B', 'W', board_copy, 't') == True):
                            scores += SearchMoves(deep + 1, i, j, board_copy)         
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

def MoveAI():
    bestScore = -10000
    dict = {}
    newBoard = deepcopy(board)
    for i in range(1, 9):
        for j in range(1, 9):
            if (isOverlay(i, j, board) == False):
                if(isRowClosure(i, j, 'B', 'W', newBoard, 't') == True):
                    newScore = SearchMoves(0, i, j, newBoard) 
                    if (newScore > bestScore):
                        bestScore = newScore
                        dict = {'x': i, 'y': j}
                        print('x: ', dict['x'], 'y: ', dict['y'])
    FillBoard_White(dict['x'], dict['y'])

# Основная функция партии
def GamePlay():
    f_exit = False
    f_AI = False
    print('Игра с ботом? Введите: Да/Нет')
    answer = input()
    if(answer.lower() == 'да'):
        f_AI = True
    print(answer, f_AI)
    if (f_AI):
        while (f_exit == False):
            PrintBoard(board)
            history = WithAI()
            if (history == False):
                f_exit = True
                print('Игрок остановил партию. Нет результата')
            elif (history == True):
                f_exit = True
                print('Партия завершена')
                print()
                Result()   
    else:
        while (f_exit == False):
            PrintBoard(board)
            history = Move()
            if (history == False):
                f_exit = True
                print('Игрок остановил партию. Нет результата')
            elif (history == True):
                f_exit = True
                print('Партия завершена')
                print()
                Result()        
        
GamePlay()