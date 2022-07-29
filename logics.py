import random
import copy

def print_arr(arr):
    print('-' * 10)
    for row in arr:
        print(*row)
    print('-' * 10)

# функция для получение переменной из индекса
def get_number_from_index(i, j):
    return i*4+j+1

# функция для получения переменной из индекса
def get_index_from_number(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y

# функция для рандомной расстановки 2 или 4 на поле
def insert_2_or_4(arr, x, y):
    if random.random() <= 0.75:
        arr[x][y] = 2
    else:
        arr[x][y] = 4
    return arr

# функция для получения списка индексов со свободными ячейками
def get_empty_list(arr):
    empty = []
    for i in range(4):
        for j in range(4):
            if arr[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty

def is_empty(arr):
    for row in arr:
        if 0 in row:
          return True
    return False

# движение влево
def move_left(arr):
    # сохраняем первоначальный массив
    origin = copy.deepcopy(arr)
    delta = 0
    for row in arr:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            # добавляем справа
            row.append(0)
    for i in range(4):
        for j in range(3):
            if arr[i][j] == arr[i][j+1] and arr[i][j] != 0:
                arr[i][j] *= 2
                delta += arr[i][j]
                arr[i].pop(j+1)
                arr[i].append(0)
    return arr, delta, not origin == arr

# движение вправо
def move_right(arr):
    origin = copy.deepcopy(arr)
    delta = 0
    for row in arr:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            # добавляем слева
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if arr[i][j] == arr[i][j-1] and arr[i][j] != 0:
                arr[i][j] *= 2
                delta += arr[i][j]
                arr[i].pop(j-1)
                arr[i].insert(0, 0)
    return arr, delta, not origin == arr

# движение вверх
def move_up(arr):
    origin = copy.deepcopy(arr)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if arr[i][j] != 0:
                column.append(arr[i][j])
        while len(column) != 4:
            # добавляем нули в конец
            column.append(0)
        for i in range(3):
            if column[i] == column[i+1] and column[i] != 0:
                column[i] *= 2
                delta += arr[i][j]
                column.pop(i+1)
                column.append(0)
        # преобразование массива обратно
        for i in range(4):
            arr[i][j] = column[i]
    return arr, delta, not origin == arr

# движение вниз
def move_down(arr):
    origin = copy.deepcopy(arr)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if arr[i][j] != 0:
                column.append(arr[i][j])
        while len(column) != 4:
            # добавляем нули в начало
            column.insert(0, 0)
        for i in range(3, 0, -1):
            if column[i] == column[i-1] and column[i] != 0:
                column[i] *= 2
                delta += arr[i][j]
                column.pop(i-1)
                column.insert(0, 0)
        # преобразование массива обратно
        for i in range(4):
            arr[i][j] = column[i]
    return arr, delta, not origin == arr

# проверка на возможность движения
def can_move(arr):
    # три потому что обращаемся к соседям рядом
    for i in range(3):
        for j in range(3):
            if arr[i][j]==arr[i][j+1] or arr[i][j] == arr[i+1][j]:
                return True
    return arr[3][3] == arr[2][2] or arr[3][3] == arr[3][2]