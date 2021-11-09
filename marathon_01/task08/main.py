from pprint import pprint
from random import randint, randrange
from typing import List, Tuple

mines_grid_typing = List[List[str]]

# constants :) for minefield
FREE_CELL = '-'  # empty cell symbol
MINE = '#'  # mine symbol


def create_empty_grid(height: int, width: int) -> mines_grid_typing:
    """
    A function that creates a grid of an empty minefield of height × width.
    The character denoting an empty cell is taken from FREE_CELL

    :param width: int - grid width
    :param height: int - grid height
    :return: List[List[str]] - grid for min type (two-dimensional list)
    """
    # check type matching
    if not all([isinstance(height, int), isinstance(width, int)]):
        raise ValueError('create_empty_grid() - не правильный тип данных передан в параметрах!')

    return [[FREE_CELL] * width for _ in range(height)]


def set_random_mines(grid: mines_grid_typing, mines: int):
    """
    Sets the given number of mines on the grid. ACTHUNG!!11 this function changes the list passed in arguments.
    If mines more than the cells in the grid, then the value is set to the number of cells -1

    :param grid: List [List [str]] - minefield
    :param mines: int - the number of mines to set
    """
    # check type matching
    if not all([all(isinstance(elem, list) for elem in grid), isinstance(mines, int)]):
        raise ValueError('set_random_mines() - не правильный тип данных передан в параметрах!')

    height, width = what_sizes(grid)
    mines_to_install = height * width - 1 if mines >= height * width else mines
    while mines_to_install > 0:
        x = randrange(width)
        y = randrange(height)
        if grid[y][x] == MINE:
            continue
        grid[y][x] = MINE
        mines_to_install -= 1


def what_sizes(grid: mines_grid_typing) -> Tuple[int, int]:
    """
    Function for finding out the size of the minefield. If the lengths of the field have different sizes,
    then the minimum length will be returned.

    :param grid: List [List [str]] - Minefield
    :return: Tuple [int, int] - Dimensions (height, width)
    """
    # check type matching
    if not all(isinstance(elem, list) for elem in grid):
        raise ValueError('what_sizes() - не правильный тип данных передан в параметрах!')

    return len(grid), len(min(grid, key=len))


def count_mines_at_place(grid: mines_grid_typing, height: int, width: int, y: int, x: int) -> str:
    """
    The function counts the number of mines around the cell with coordinates [y, x].
    The cell itself is not checked. ACTHUNG!!11 this function changes the list passed in arguments.

    :param width: int - width of grid
    :param height: int - height of grid
    :param grid: List [List [str]] - Minefield
    :param y: int - The Y coordinate
    :param x: int - The X coordinate
    :return: str - The number of mines around the cell as string
    """
    # check type matching
    if not all([all(isinstance(elem, list) for elem in grid),
                isinstance(height, int),
                isinstance(width, int),
                isinstance(y, int),
                isinstance(x, int)]):
        raise ValueError('count_mines_at_place() - не правильный тип данных передан в параметрах!')

    mines = 0
    bounds = [-1, 0, 1]  # range around cell that is being checked (little bit faster than range(-1, 2))
    for shift_y in bounds:
        for shift_x in bounds:
            cell_x = x + shift_x
            cell_y = y + shift_y
            # check if the coordinates is out of bounds and do not check the current position
            if cell_x < 0 or cell_x >= width or cell_y < 0 or cell_y >= height or (cell_y == y and cell_x == x):
                continue
            if grid[cell_y][cell_x] == MINE:
                mines += 1
    return str(mines)


def num_grid(grid: mines_grid_typing):
    """
    A function that takes a grid of "#" and "-". Each hash (#) represents a mine, and each dash (-) represents
    place without mine.
    Returns a list in which each dash has been replaced by a digit representing the number of mines directly
    adjacent to it (horizontally, vertically and diagonally).

    :param grid: List [List [str]] - Minefield
    :return: List [List [str]] - Minefield with numbers of mines
    """
    # check type matching
    if not all(isinstance(elem, list) for elem in grid):
        raise ValueError('num_grid() - не правильный тип данных передан в параметрах!')

    height, width = what_sizes(grid)
    result = create_empty_grid(height, width)
    for y in range(height):
        for x in range(width):
            result[y][x] = MINE if grid[y][x] == MINE else count_mines_at_place(grid, height, width, y, x)
    return result


if __name__ == '__main__':
    test_grid = [['-', '-', '-', '#', '#'],
                 ['-', '#', '-', '-', '-'],
                 ['-', '-', '#', '-', '-'],
                 ['-', '#', '#', '-', '-'],
                 ['-', '-', '-', '-', '-']]
    test_result = [['1', '1', '2', '#', '#'],
                   ['1', '#', '3', '3', '2'],
                   ['2', '4', '#', '2', '0'],
                   ['1', '#', '#', '2', '0'],
                   ['1', '2', '2', '1', '0']]

    # tests on the data from examples
    assert num_grid([['-', '-', '-'],
                     ['-', '#', '-'],
                     ['-', '-', '-']]) == [['1', '1', '1'],
                                           ['1', '#', '1'],
                                           ['1', '1', '1']]
    assert num_grid([['#', '-', '-'],
                     ['-', '-', '#'],
                     ['-', '#', '-']]) == [['#', '2', '1'],
                                           ['2', '3', '#'],
                                           ['1', '#', '2']]
    assert num_grid(test_grid) == test_result

    # random_height = 1_000
    # random_width = 1_000
    # random_mines = 100

    random_height = randint(3, 10)
    random_width = randint(3, 10)
    random_mines = random_width * random_height // 3

    print(f'Рандомное минное поле ({random_height} × {random_width}) c {random_mines} миной(ами):')
    random_grid = create_empty_grid(random_height, random_width)
    set_random_mines(random_grid, random_mines)
    pprint(random_grid, width=60)
    print(f'Минное поле с количеством мин вокруг пустых клеток:')
    pprint(num_grid(random_grid), width=60)
    # xx = num_grid(random_grid)

    print('\nПоиграем? (y/n)')
    game = input()
    if game in {'y', 'Y', 'н', 'д'}:
        from game import *  # I know it's not right

        play_game()
    else:
        print('Неверный выбор 🤣')
