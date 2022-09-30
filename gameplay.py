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
        if(isOverlay(x_coord, y_coord)):
            step = counter()
        else:
            if (step % 2 == 0):
                if(isRowClosure(x_coord, y_coord, 'B', 'W')):
                    FillBoard_White(x_coord, y_coord)
                else:
                    step = counter()
            else:
                if(isRowClosure(x_coord, y_coord, 'W', 'B')):
                    FillBoard_Black(x_coord, y_coord)
                else:
                    step = counter()
    
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
def isOverlay(x_coord, y_coord):
    if(board[x_coord - 1][y_coord - 1] == 'W' or board[x_coord - 1][y_coord - 1] == 'B'):
        print('Ошибочный ход. Наложение на фишку')
        return True
    return False

def OnRight(x_coord, y_coord, enemy, you):
    if(board[x_coord - 1][y_coord] == enemy):
        newCoordinates = []
        steps = 8 - y_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord - 1) + str(y_coord + i))
            if (board[x_coord - 1][y_coord + i] != you) and (board[x_coord - 1][y_coord + i] != enemy):
                return -1
            if (board[x_coord - 1][y_coord + i] == you):
                print('x: ', x_coord - 1, 'y: ', y_coord + i)
                return newCoordinates          
    return -1
def OnLeft(x_coord, y_coord, enemy, you):
    if(board[x_coord - 1][y_coord - 2] == enemy):
        newCoordinates = []
        steps = y_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord - 1) + str(y_coord - (2 + i)))
            if (board[x_coord - 1][y_coord - (2 + i)] != you) and (board[x_coord - 1][y_coord - (2 + i)] != enemy):
                return -1
            elif (board[x_coord - 1][y_coord - (2 + i)] == you):
                print('x: ', x_coord - 1, 'y: ', y_coord - (2 + i))
                return newCoordinates          
    return -1
def OnUp(x_coord, y_coord, enemy, you):
    if(board[x_coord - 2][y_coord - 1] == enemy):
        newCoordinates = []
        steps = x_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord - (2 + i)) + str(y_coord - 1))
            if (board[x_coord - (2 + i)][y_coord - 1]  != you) and (board[x_coord - (2 + i)][y_coord - 1] != enemy):
                return -1
            elif (board[x_coord - (2 + i)][y_coord - 1] == you):
                print('x: ', x_coord - (2 + i), 'y: ', y_coord - 1)
                return newCoordinates          
    return -1
def OnDown(x_coord, y_coord, enemy, you):
    if(board[x_coord][y_coord - 1] == enemy):
        newCoordinates = []
        steps = 8 - x_coord
        for i in range(0, steps - 1):
            newCoordinates.append(str(x_coord + i) + str(y_coord - 1))
            if (board[x_coord + i][y_coord - 1] != you) and (board[x_coord + i][y_coord - 1] != enemy):
                return -1
            elif (board[x_coord + i][y_coord - 1] == you):
                print('x: ', x_coord + i, 'y: ', y_coord - 1)
                return newCoordinates          
    return -1

def Reverse(array, you):
    for i in range(0, len(array)):
        board[int(array[i][0])][int(array[i][1])] = you

# Функция для проверки хода (рядом с фишкой соперника + замыкание ряда)
def isRowClosure(x_coord, y_coord, enemy, you):
    if(y_coord-1 == 0 or y_coord-1 == 1):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (board[x_coord - 1][y_coord] == enemy or board[x_coord][y_coord - 1] == enemy or 
                board[x_coord][y_coord] == enemy):
                
                reverseRight = OnRight(x_coord, y_coord, enemy, you)
                if(reverseRight != -1):
                    Reverse(reverseRight, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you)
                if(reverseDown != -1):
                    Reverse(reverseDown, you)
                return True
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy):
                
                reverse = OnUp(x_coord, y_coord, enemy, you)
                if(reverse != -1):
                    Reverse(reverse, you)

                reverseRight = OnRight(x_coord, y_coord, enemy, you)
                if(reverseRight != -1):
                    Reverse(reverseRight, you)
                
                return True
        else:
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy or board[x_coord][y_coord] == enemy or 
                board[x_coord][y_coord - 1] == enemy):
                
                reverseRight = OnRight(x_coord, y_coord, enemy, you)
                if(reverseRight != -1):
                    Reverse(reverseRight, you)

                reverseUp = OnUp(x_coord, y_coord, enemy, you)
                if(reverseUp != -1):
                    Reverse(reverseUp, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you)
                if(reverseDown != -1):
                    Reverse(reverseDown, you)
                

                return True
    elif (y_coord-1 == 7 or y_coord-1 == 6):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (board[x_coord - 1][y_coord - 2] == enemy or board[x_coord][y_coord - 2] == enemy or 
                board[x_coord][y_coord - 1] == enemy):
                # Проверка на замыкание
                reverse = OnLeft(x_coord, y_coord, enemy, you)
                if(reverse != -1):
                    Reverse(reverse, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you)
                if(reverseDown != -1):
                    Reverse(reverseDown, you)
                

                return True
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (board[x_coord - 1][y_coord - 2] == enemy or board[x_coord - 2][y_coord - 2] == enemy or 
                board[x_coord - 2][y_coord - 1] == enemy):
                
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you)
                if(reverseLeft != -1):
                    Reverse(reverseLeft, you)
                
                reverseUp = OnUp(x_coord, y_coord, enemy, you)
                if(reverseUp != -1):
                    Reverse(reverseUp, you)
                
                return True
        else:
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord - 2] == enemy or 
                board[x_coord - 1][y_coord - 2] == enemy or board[x_coord][y_coord - 2] == enemy or 
                board[x_coord][y_coord - 1] == enemy):
                
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you)
                if(reverseLeft != -1):
                    Reverse(reverseLeft, you)
                
                reverseUp = OnUp(x_coord, y_coord, enemy, you)
                if(reverseUp != -1):
                    Reverse(reverseUp, you)

                reverseDown = OnDown(x_coord, y_coord, enemy, you)
                if(reverseDown != -1):
                    Reverse(reverseDown, you)
                

                return True
    elif (y_coord-1 > 1 and y_coord-1 < 6):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (board[x_coord - 1][y_coord - 2] == enemy or board[x_coord][y_coord - 2] == enemy or 
                board[x_coord][y_coord - 1] == enemy or board[x_coord][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy):
                reverse = OnDown(x_coord, y_coord, enemy, you)
                if(reverse != -1):
                    Reverse(reverse, you)
                
                reverseRight = OnRight(x_coord, y_coord, enemy, you)
                if(reverseRight != -1):
                    Reverse(reverseRight, you)
                
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you)
                if(reverseLeft != -1):
                    Reverse(reverseLeft, you)
                
                reverseDown = OnDown(x_coord, y_coord, enemy, you)
                if(reverseDown != -1):
                    Reverse(reverseDown, you)
                
                
                return True
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord - 2] == enemy or 
                board[x_coord - 1][y_coord - 2] == enemy or board[x_coord - 2][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy):
                
                reverseRight = OnRight(x_coord, y_coord, enemy, you)
                if(reverseRight != -1):
                    Reverse(reverseRight, you)
                
                reverseLeft = OnLeft(x_coord, y_coord, enemy, you)
                if(reverseLeft != -1):
                    Reverse(reverseLeft, you)
                
                reverseUp = OnUp(x_coord, y_coord, enemy, you)
                if(reverseUp != -1):
                    Reverse(reverseUp, you)
                

                return True
        else:
            if(board[x_coord - 2][y_coord - 2] == enemy or board[x_coord - 1][y_coord - 2] == enemy or
                board[x_coord - 2][y_coord - 1] == enemy or board[x_coord][y_coord - 1] == enemy or
                board[x_coord - 1][y_coord] == enemy or board[x_coord][y_coord] == enemy or
                board[x_coord][y_coord - 2] == enemy or board[x_coord - 2][y_coord] == enemy):
                
                reverseRight = OnRight(x_coord, y_coord, enemy, you)
                if(reverseRight != -1):
                    Reverse(reverseRight, you)

                reverseLeft = OnLeft(x_coord, y_coord, enemy, you)
                if(reverseLeft != -1):
                    Reverse(reverseLeft, you)

                reverseUp = OnUp(x_coord, y_coord, enemy, you)
                if(reverseUp != -1):
                    Reverse(reverseUp, you)

                reverseDown = OnDown(x_coord, y_coord, enemy, you)
                if(reverseDown != -1):
                    Reverse(reverseDown, you)

                return True
    return False
# Основная функция партии
def GamePlay():
    f_exit = False
    while (f_exit == False or isGameOver(board)):
        PrintBoard(board)
        if (Move() == False):
            f_exit = True
            print('Игрок завершил партию')
    else:
        print('GameOver')

GamePlay()