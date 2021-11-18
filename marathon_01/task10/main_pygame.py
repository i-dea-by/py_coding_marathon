from collections import deque
from random import random, randint

import pygame as pg

# кадров в секунду
FPS = 15
# размер квадрата сетки лабиринта
CELL_SIZE = 50
# константы цветов
BRICK = '#9E0000'
FOREST = '#317b00'
BURN = '#FF3030'
WHITE = '#FFFFFF'


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


def can_exit(maze: list[list[int]]) -> int:
    # проверяем соответствие типов входных параметров
    if not isinstance(maze, list):
        raise TypeError('can_exit() - аргумент maze должен быть типа list!')

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

    def find_next_steps(y: int, x: int) -> list[tuple[int, int]]:
        """
        Функция возвращает список кортежей с координатами ячеек в которые можно шагать

        :param y: int - координата текущей ячейки
        :param x: int - координата текущей ячейки
        :return: list[tuple[int, int]] - список кортежей с координатами
        """
        result = []
        steps = [-1, 0], [0, -1], [1, 0], [0, 1]
        for step_y, step_x in steps:
            if is_cell_good(y + step_y, x + step_x):
                shadow_maze[y + step_y][x + step_x] = shadow_maze[y][x] + 1
                result.append((y + step_y, x + step_x))
        return result

    def get_rect(y: int, x: int, margin=1) -> tuple[int, int, int, int]:
        """
        Функция возвращает кортеж координат и размеров для метода draw.Rect pygame-а

        :param margin: int - отступы от краёв сетки лабиринта. по умолчанию = 1, чтоб не рисовать черныу сетку
        :param y: int - координата в поле для отрисовки
        :param x: int - координата в поле для отрисовки
        :return: tuple[int, int, int, int] - координаты и размеры прямоугольной области (left, top, width, height)
        """
        return x * CELL_SIZE + margin, y * CELL_SIZE + margin, CELL_SIZE - (margin * 2), CELL_SIZE - (margin * 2)

    def draw_maze():
        """ Функция отрисовки элементов лабиринта - препятствий, обработанных ячеек и ячеек следующего шага """
        # рисуем лабиринт, точнее препятствия
        for y, row in enumerate(maze):
            for x, brick in enumerate(row):
                if brick == 1:
                    sc.blit(brick_surface, get_rect(y, x))
        # выводим посещенные клетки
        for y, x in vizited:
            pg.draw.rect(sc, pg.Color(FOREST), get_rect(y, x))
        # выводим «подожженые» клетки из очереди
        for y, x in queue:
            pg.draw.rect(sc, pg.Color(BURN), get_rect(y, x))
        # рисуем путь от текущей клетки до начала
        path = current_cell
        while path:
            pg.draw.rect(sc, pg.Color(WHITE), get_rect(*path, margin=17), CELL_SIZE, border_radius=CELL_SIZE // 3)
            path = vizited[path]

    def draw_finish_text():
        """Функция отрисовки заставки текста в конце работы алгоритма"""
        center_rect = ((CELL_SIZE * maze_width) // 2, (CELL_SIZE * maze_height) // 2)

        dialog_sc = pg.Surface((CELL_SIZE * 8, CELL_SIZE * 8))
        dialog_sc.fill(pg.Color(BRICK))
        dialog_sc.set_alpha(200)

        result_text = 'Выход есть' if is_finished == 1 else 'Выхода нет ('
        text_sc = text.render(result_text, True, WHITE)

        click_text = 'Нажмите мышкой для рестарта'
        click_sc = small_text.render(click_text, True, WHITE)

        # отображаем на основную поверхность
        sc.blit(dialog_sc, dialog_sc.get_rect(center=center_rect))
        sc.blit(text_sc, text_sc.get_rect(center=center_rect))
        sc.blit(click_sc, text_sc.get_rect(center=((CELL_SIZE * maze_width) // 2, (CELL_SIZE * maze_height) // 2 + 50)))

    # проверяем и сохраняем размеры матрицы
    maze_height, maze_width = check_dimensions(maze)

    # "теневой лабиринт" с нулями для сохранения результатов поиска выхода
    shadow_maze = create_random_maze(maze_height, maze_width, chance=0)

    current_cell = (0, 0)  # стартовая ячейка
    queue = deque([current_cell])  # очередь для ячеек для следующего шага
    vizited = {current_cell: None}  # хранилище посещенных ячеек

    # флаг окончания работы алгоритма: 0 - работает, 1 - выход есть, 2 - выхода нету, 3 - окно закрыли
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
                is_finished = 3
                show_maze = False

    return is_finished


if __name__ == '__main__':
    # инициализируем pygame (неплохоб бы в отдельную функцию, но лень:)
    pg.init()
    pg.display.set_caption("Прохождение лабиринта :: Поиск в ширину (BFS)")
    brick_surface = pg.image.load('resources/brick.bmp')
    pg.display.set_icon(brick_surface)
    clock = pg.time.Clock()
    text = pg.font.Font(None, 48)
    small_text = pg.font.Font(None, 20)

    # признак повторения цикла
    running = 0
    while running < 3:
        # размеры лабиринта
        height, width = randint(6, 15), randint(6, 15)
        sc = pg.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
        sc.fill(pg.Color('black'))

        random_maze = create_random_maze(height, width, chance=0.2)
        running = can_exit(random_maze)

    pg.quit()
