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
    print(step)

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
                if(isRowClosure(x_coord, y_coord, 'B')):
                    FillBoard_White(x_coord, y_coord)
                else:
                    step = counter()
            else:
                if(isRowClosure(x_coord, y_coord, 'W')):
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

# Функция для проверки хода (рядом с фишкой соперника + замыкание ряда)
def isRowClosure(x_coord, y_coord, enemy):
    if(y_coord-1 == 0 or y_coord-1 == 1):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (board[x_coord - 1][y_coord] == enemy or board[x_coord][y_coord - 1] == enemy or 
                board[x_coord][y_coord] == enemy):
                # Проверка на замыкание
                return True
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy):
                # Проверка на замыкание
                return True
        else:
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy or board[x_coord][y_coord] == enemy or 
                board[x_coord][y_coord - 1] == enemy):
                # Проверка на замыкание
                return True
    elif (y_coord-1 == 7 or y_coord-1 == 6):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (board[x_coord - 1][y_coord - 2] == enemy or board[x_coord][y_coord - 2] == enemy or 
                board[x_coord][y_coord - 1] == enemy):
                # Проверка на замыкание
                return True
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (board[x_coord - 1][y_coord - 2] == enemy or board[x_coord - 2][y_coord - 2] == enemy or 
                board[x_coord - 2][y_coord - 1] == enemy):
                # Проверка на замыкание
                return True
        else:
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord - 2] == enemy or 
                board[x_coord - 1][y_coord - 2] == enemy or board[x_coord][y_coord - 2] == enemy or 
                board[x_coord][y_coord - 1] == enemy):
                # Проверка на замыкание
                return True
    elif (y_coord-1 > 1 and y_coord-1 < 6):
        if (x_coord-1 == 0 or x_coord-1 == 1):
            if (board[x_coord - 1][y_coord - 2] == enemy or board[x_coord][y_coord - 2] == enemy or 
                board[x_coord][y_coord - 1] == enemy or board[x_coord][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy):
                # Проверка на замыкание
                return True
        elif (x_coord-1 == 7 or x_coord-1 == 6):
            if (board[x_coord - 2][y_coord - 1] == enemy or board[x_coord - 2][y_coord - 2] == enemy or 
                board[x_coord - 1][y_coord - 2] == enemy or board[x_coord - 2][y_coord] == enemy or 
                board[x_coord - 1][y_coord] == enemy):
                # Проверка на замыкание
                return True
        else:
            if(board[x_coord - 2][y_coord - 2] == enemy or board[x_coord - 1][y_coord - 2] == enemy or
                board[x_coord - 2][y_coord - 1] == enemy or board[x_coord][y_coord - 1] == enemy or
                board[x_coord - 1][y_coord] == enemy or board[x_coord][y_coord] == enemy or
                board[x_coord][y_coord - 2] == enemy or board[x_coord - 2][y_coord] == enemy):
                # Проверка на замыкание
                return True
    return False
# Основная функция партии
def GamePlay():
    f_exit = False
    while (f_exit == False):
        f_exit = isGameOver(board)
        PrintBoard(board)
        if (Move() == False):
            f_exit = True
            print('Игрок завершил партию')
    else:
        print('GameOver')

GamePlay()