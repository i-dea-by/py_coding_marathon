from collections import deque
from random import random, randint

from tabulate import tabulate


def create_random_maze(height: int, width: int, chance: float = 0.25) -> list[list[int]]:
    """
    Создание лабиринта размером height × width элементов заполненную препятствиями с вероятностью 0,25

    :param chance: float - вероятность установки препятствия, по умолчанию = 0,25
    :param width: int - ширина лабиринта
    :param height: int - высота лабиринта
    :return: List[List[int]]
    """
    return [[1 if random() < chance else 0 for _ in range(width)] for _ in range(height)]


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
        result = all([0 <= y < maze_height,
                      0 <= x < maze_width,
                      (y, x) not in vizited,
                     (y, x) not in queue]) and maze[y][x] == 0  # пришлось вынести, чтоб проверка срабатывала после
        return result

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

    # проверяем и сохраняем размеры матрицы
    maze_height, maze_width = check_dimensions(maze)

    # "теневой лабиринт" для сохранения результатов поиска выхода
    shadow_maze = create_random_maze(maze_height, maze_width, chance=0)

    start = (0, 0)          # стартовая ячейка
    queue = deque([start])  # очередь для ячеек для следующего шага ()
    vizited = set()         # хранилище посещенных ячеек

    # поиск в ширшоту
    while queue:
        current_cell = queue.popleft()
        vizited.add(current_cell)

        next_cells = find_next_steps(current_cell[0], current_cell[1])

        for next_cell in next_cells:
            queue.append(next_cell)

    return shadow_maze[-1][-1] > 0


if __name__ == '__main__':
    maze_init = [[0, 1, 1, 1, 1, 1, 1],
                 [0, 0, 1, 1, 0, 1, 1],
                 [1, 0, 0, 0, 0, 1, 1],
                 [1, 1, 1, 1, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 0]]

    # тесты на примерах из задачи
    assert can_exit(maze_init)
    assert not can_exit([[0], [0], [1]])
    assert not can_exit([[0, 1, 1, 1, 1, 1, 1],
                         [0, 0, 1, 0, 0, 1, 1],
                         [1, 0, 0, 0, 0, 1, 1],
                         [1, 1, 0, 1, 0, 0, 1],
                         [1, 1, 0, 0, 1, 1, 1]])
    assert not can_exit([[0, 1, 1, 1, 1, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0],
                         [1, 1, 1, 0, 0, 0, 0],
                         [1, 1, 1, 1, 1, 1, 0],
                         [1, 1, 1, 1, 1, 1, 1]])

    # работаем
    print('Готовый лабиринт:')
    print(tabulate(maze_init, tablefmt="grid"))
    height, length = check_dimensions(maze_init)
    print(f'Размер лабиринта (высота х длина): {height}x{length}')
    print(f'Выход есть?: {can_exit(maze_init)}')
    print('-' * 60)

    print('Рандомный лабиринт:')
    length = randint(4, 9)  # для красоты пусть будет квадратный
    random_maze = create_random_maze(length, length)
    print(tabulate(random_maze, tablefmt="grid"))
    height, length = check_dimensions(random_maze)
    print(f'Размер лабиринта (высота х длина): {height}x{length}')
    print(f'Выход есть?: {can_exit(random_maze)}')
