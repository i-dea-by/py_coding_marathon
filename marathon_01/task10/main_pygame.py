from collections import deque
from random import random

import pygame as pg

# кадров в секунду
FPS = 15
# размер квадрата сетки лабиринта
TILE = 50
# константы цветов
BRICK = '#9E0000'
FOREST = '#317b00'
BURN = '#FF3030'


def create_random_maze(height: int, width: int, chance: float = 0.25) -> list[list[int]]:
    """
    Создание лабиринта размером height × width элементов заполненную препятствиями с вероятностью 0,25

    :param chance: float - вероятность установки препятствия, по умолчанию = 0,25
    :param width: int - ширина лабиринта
    :param height: int - высота лабиринта
    :return: List[List[int]]
    """
    result = [[1 if random() < chance else 0 for _ in range(width)] for _ in range(height)]
    result[0][0] = 0  # на случай, если рандом завалит вход/выход, принудительно освободим его
    result[-1][-1] = 0
    return result


def check_dimensions(maze: list[list[int]]) -> tuple[int, int]:
    """
    Функция выясняющая размеры лабиринта. В случае если длины строк различны, то возвращаемой длиной склада будет
    длина минимальной строки.
    :param maze: Входная матрица лабиринта типа list[list] (двухмерный список)
    :return: Возвращает кортеж из двух чисел представляющие собой размеры лабиринта: (высота, длина)
    """
    if not all(isinstance(lst, list) for lst in maze):
        raise ValueError('check_dimensions() - не правильный тип данных передан в параметрах!')
    return len(maze), len(min(maze, key=len))


def can_exit(maze: list[list[int]]) -> bool:
    # проверяем соответствие типов входных параметров
    if not isinstance(maze, list):
        raise TypeError('can_exit() - аргумент maze должен быть типа list!')

    # проверяем что во входном списке хоть что-то есть
    if not maze or not maze[0]:
        return False

    # внутренние функции
    def is_cell_good(y: int, x: int) -> bool:
        """
        Проверям ячейку лабиринта на предмет возможности в неё шагнуть: выход за пределы, посещенность и препятсвияе

        :param y: int - координата
        :param x: int - координата
        :return: bool - True - можно, False - нельзя
        """
        return all([0 <= y < maze_height,
                    0 <= x < maze_width,
                    (y, x) not in vizited,
                    (y, x) not in queue]) and maze[y][x] == 0  # пришлось вынести, чтоб проверка срабатывала после

    def find_next_steps(y: int, x: int) -> list[tuple]:
        """
        Функция возвращает список кортежей с координатами ячеек в которые можно шагать

        :param y: int - координата текущей ячейки
        :param x: int - координата текущей ячейки
        :return: list[tuple] - список кортежей с координатами
        """
        result = []
        steps = [-1, 0], [0, -1], [1, 0], [0, 1]
        for step_y, step_x in steps:
            if is_cell_good(y + step_y, x + step_x):
                shadow_maze[y + step_y][x + step_x] = shadow_maze[y][x] + 1
                result.append((y + step_y, x + step_x))
        return result

    def get_rect(y: int, x: int, inc=1) -> tuple[int, int, int, int]:
        """
        Функция возвращает кортеж координат и размеров для метода draw.Rect pygame-а

        :param inc: int - отступы от краёв сетки лабиринта
        :param y: int - координата в поле для отрисовки
        :param x: int - координата в поле для отрисовки
        :return: tuple[int, int, int, int] - координаты и размеры прямоугольной области (left, top, width, height)
        """
        return x * TILE + inc, y * TILE + inc, TILE - (inc * 2), TILE - (inc * 2)

    def draw_maze():
        """ Функция отрисовки элементов лабиринта - препятствий, обработанных ячеек и ячеек следующего шага """

        # рисуем лабиринт
        [[sc.blit(brick_surface, get_rect(y, x)) for x, brick in enumerate(row) if brick] for y, row in enumerate(maze)]
        # рисуем результат работы алгоритма поиска
        [pg.draw.rect(sc, pg.Color(FOREST), get_rect(y, x)) for y, x in vizited]
        [pg.draw.rect(sc, pg.Color(BURN), get_rect(y, x)) for y, x in queue]
        # рисуем путь от текущей клетки до начала
        path_dot = current_cell
        while path_dot:
            pg.draw.rect(sc, pg.Color('#FFFFFF'), get_rect(*path_dot, inc=17), TILE, border_radius=TILE // 3)
            path_dot = vizited[path_dot]

    def draw_finish_text():
        """Функция отрисовки заставки текста в конце работы алгоритма"""

        dialog_sc = pg.Surface((TILE * 8, TILE * 8))
        dialog_sc.fill(pg.Color(BRICK))
        dialog_sc.set_alpha(180)

        result_text = 'Выход есть' if is_finished == 1 else 'Выхода нет ('
        text_sc = text.render(result_text, True, (255, 255, 255))

        click_text = 'Нажмите мышкой для рестарта'
        click__sc = small_text.render(click_text, True, (255, 255, 255))

        sc.blit(dialog_sc, (TILE * 3, TILE * 3))
        sc.blit(text_sc, text_sc.get_rect(center=((TILE * maze_width) // 2, (TILE * maze_height) // 2)))
        sc.blit(click__sc, text_sc.get_rect(center=((TILE * maze_width) // 2, (TILE * maze_height) // 2 + 50)))

    # проверяем и сохраняем размеры матрицы
    maze_height, maze_width = check_dimensions(maze)

    # "теневой лабиринт" с нулями для сохранения результатов поиска выхода
    shadow_maze = create_random_maze(maze_height, maze_width, chance=0)

    start = current_cell = (0, 0)  # стартовая ячейка
    queue = deque([start])  # очередь для ячеек для следующего шага ()
    vizited = {start: None}  # хранилище посещенных ячеек

    # флаг окончания работы алгоритма: 0 - работает, 1 - выход есть, 2 - выхода нету
    is_finished = 0

    show_maze = True  # условие выхода из цикла
    while show_maze:

        draw_maze()  # рисуем лабиринт

        if is_finished > 0:  # если наступил конец работы алгоритма)
            draw_finish_text()

        pg.display.update()
        clock.tick(FPS)

        # блок проверки закончил ли работу алгоритм
        if queue and current_cell == (maze_height - 1, maze_width - 1):  # если добрались до выхода
            queue.clear()
            is_finished = 1
        if not queue and current_cell < (maze_height - 1, maze_width - 1):  # если до выхода не добраться
            is_finished = 2

        # алгоритм поиска в ширину
        if queue:
            current_cell = queue.popleft()
            next_cells = find_next_steps(*current_cell)
            for next_cell in next_cells:
                # если добрались до выхода
                if next_cell == (maze_height - 1, maze_width - 1):
                    queue.clear()
                    is_finished = 1
                queue.append(next_cell)
                vizited[next_cell] = current_cell

        # pygame проверка на выход
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                show_maze = False
            if event.type == pg.QUIT:
                show_maze = False
                maze[0][0] = -1  # костыль для нормального завершения работы программы

    return shadow_maze[-1][-1] > 0


if __name__ == '__main__':
    # размеры лабиринта
    height, width = 14, 14
    # признак повторения цикла
    running = True

    # инициализируем pygame
    pg.init()
    sc = pg.display.set_mode((width * TILE, height * TILE))
    pg.display.set_caption("Прохождение лабиринта :: Поиск в ширину (BFS)")
    brick_surface = pg.image.load('resources/brick.bmp')
    pg.display.set_icon(brick_surface)
    clock = pg.time.Clock()
    text = pg.font.Font(None, 48)
    small_text = pg.font.Font(None, 20)

    while running:
        sc.fill(pg.Color('black'))
        random_maze = create_random_maze(height, width, chance=0.2)

        is_exit = can_exit(random_maze)

        if random_maze[0][0] == -1:  # костыль для нормального завершения работы программы
            running = False

    pg.quit()
