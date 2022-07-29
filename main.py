import pygame
import sys
from logics import *
from database import get_best, cur, insert_result

PLAYERS_DB = get_best()

# в константы записываем основные цвета
WHITE = (255, 255, 255)
BLUE = (177, 204, 227)
BLACK = (0, 0, 0)

# создаём игровое поле
BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = 110 + WIDTH
TITLE_REC = pygame.Rect(0,0, WIDTH, SIZE_BLOCK)
score = 0
USERNAME = None
mas = None
score = None

# задаём цвет клеткам с определённым числом
COLORS = {
    0: (255, 255, 255),
    2: (239, 250, 235),
    4: (223, 244, 215),
    8: (207, 239, 195),
    16: (191, 233, 175),
    32: (174, 227, 155),
    64: (157, 221, 135),
    128: (139, 215, 115),
    256: (119, 209, 95),
    512: (98, 203, 73),
    1024: (73, 196, 49),
    2048: (36, 190, 11),
    4096: (52, 125, 17),
    8192: (91, 125, 17),
    16384: (131, 140, 28),
    32768: (159, 168, 56)
}

# создаём функцию для вывода на экран лучших результатов
def draw_top_results():
    font_top = pygame.font.SysFont("simsun", 25)
    font_player = pygame.font.SysFont("simsun", 18)
    text_head = font_top.render("Best tries:", True, BLACK)
    screen.blit(text_head, (280, 5))
    for index, player in enumerate(PLAYERS_DB):
        name, score = player
        s = f"{index + 1}. {name} - {score}"
        text_player = font_player.render(s, True, BLACK)
        screen.blit(text_player, (280, 32 + 25 * index))

# прорисовываем интерфейс
def draw_interface(score, delta = 0):
    # рисуем панель сверху
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    print(arr)
    # шрифт
    font = pygame.font.SysFont("stxingkai", 70)
    font_score = pygame.font.SysFont("simsun", 48)
    font_delta = pygame.font.SysFont("simsun", 20)
    text_score = font_score.render("Score:", True, BLACK)
    text_score_value = font_score.render(f"{score}", True, BLACK)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, BLACK)
        screen.blit(text_delta, (190, 75))
    print_arr(arr)
    draw_top_results()

    # прорисовка блоков и цифр
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = arr[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                # прикрепляем текст к экрану
                screen.blit(text, (text_x, text_y))

def init_const():
    global score, arr
    arr = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    score = 0
    empty = get_empty_list(arr)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    arr = insert_2_or_4(arr, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    arr = insert_2_or_4(arr, x2, y2)

init_const()

print(get_empty_list(arr))
print(print_arr(arr))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# задаём название игры (отображается в окне игры)
pygame.display.set_caption("YAAAY, IT'S 2048!!!!!")

# прорисовываем начальное окно (при запуске игры)
def draw_intro():
    img2048 = pygame.image.load("icon.png")
    font = pygame.font.SysFont("stxingkai", 70)
    text_welcome = font.render("Welcome!", True, WHITE)
    name = "Enter your name"
    find_name = False
    while not find_name:
        for event in pygame.event.get():
            # прописываем действие при нажатии игроком на крестик
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == "Enter your name":
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        find_name = True
        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, [200,200]), [10,10])
        screen.blit(text_welcome, (240, 80))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)

# прописываем окно конца игры
def draw_gameover():
    global USERNAME, arr, score, PLAYERS_DB
    img2048 = pygame.image.load("icon.png")
    font = pygame.font.SysFont("stxingkai", 65)
    font_small = pygame.font.SysFont("stxingkai", 40)
    text_gameover = font.render("Game over!", True, WHITE)
    text_score = font.render(f"Your score: {score}", True, WHITE)
    text_enter = font_small.render("Press Enter to start new game", True, WHITE)
    text_space = font_small.render("Press Space to continue playing", True, WHITE)
    best_score = PLAYERS_DB[0][1]
    if score > best_score:
        text = "New best score!"
    else:
        text = f"Best score: {best_score}"
    text_record = font.render(text, True, WHITE)
    insert_result(USERNAME, score)
    PLAYERS_DB = get_best()
    make_desicion = False
    while not make_desicion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                # действие для новой игры с тем же именем
                if event.key == pygame.K_SPACE:
                    make_desicion = True
                    init_const()
                # действие для новой игры с новым именем
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_desicion = True
                    init_const()
        screen.fill(BLACK)
        screen.blit(text_gameover, (220, 80))
        screen.blit(text_score, (30, 250))
        screen.blit(text_record, (30, 300))
        screen.blit(text_space, (30, 360))
        screen.blit(text_enter, (30, 410))
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        pygame.display.update()
    screen.fill(BLACK)


def game_loop():
    global score, arr
    draw_interface(score)
    pygame.display.update()
    is_arr_move = False
    while is_empty(arr) or can_move(arr):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    arr, delta, is_arr_move  = move_left(arr)
                elif event.key == pygame.K_RIGHT:
                    arr, delta, is_arr_move = move_right(arr)
                elif event.key == pygame.K_UP:
                    arr, delta, is_arr_move = move_up(arr)
                elif event.key == pygame.K_DOWN:
                    arr, delta, is_arr_move = move_down(arr)
                score += delta

                if is_empty(arr) and is_arr_move:
                    # результат: массив из пустых чисел
                    empty = get_empty_list(arr)
                    # рандомно расставляем переменные
                    random.shuffle(empty)
                    # удаление переменной при её нахождении
                    random_num = empty.pop()
                    # находим индекс удалённой переменной
                    x, y = get_index_from_number(random_num)
                    # заполняем пустое пространство 2 или 4
                    arr = insert_2_or_4(arr, x, y)
                    is_arr_move = False

                draw_interface(score, delta)
                pygame.display.update()

while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_gameover()