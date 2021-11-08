from tabulate import tabulate

from main import *  # and it's not right


def play_game():
    def input_coord(height: int, width: int) -> Tuple[int, int]:
        """
        Receive and check input coordinates

        :param height: int - max row input
        :param width: int - max column input
        :return: Tuple[int, int] - tuple of coordinates (x, y)
        """
        input_loop = True
        while input_loop:
            input_str = input('Введите координаты через пробел (X Y) ')
            if len(input_str.split()) != 2:
                print('Должно быть 2 координаты.')
                continue

            input_x, input_y = input_str.split()

            if not input_x.isdigit() or not input_y.isdigit():
                print('Неверные координаты или не цифровые символы!!11')
                continue

            input_x, input_y = int(input_x), int(input_y)

            if input_x <= 0 or input_x > width or input_y <= 0 or input_y > height:
                print('Координаты за пределами поля')
                continue

            input_loop = False

        return input_x - 1, input_y - 1

    def show_around(current_y: int, current_x: int):
        """
        Open cells around (y, x) on player grid

        :param current_y: int - y-coord of current cell
        :param current_x: int - x--coord of current cell
        """
        for shift_y in range(-1, 2):
            for shift_x in range(-1, 2):
                cell_x = current_x + shift_x
                cell_y = current_y + shift_y
                # check if the coordinates is out of bounds and do not check the current position
                if cell_x < 0 or cell_x >= game_width or cell_y < 0 or cell_y >= game_height:
                    continue
                player_grid[cell_y][cell_x] = '💣' if game_grid[cell_y][cell_x] == MINE else game_grid[cell_y][cell_x]

    def check_grid_is_open() -> bool:
        """
        Check player grid. If all cells is open return True for end game, else - return False

        :return:
        """
        check_result = 0
        for cell_y in range(game_height):
            for cell_x in range(game_width):
                if player_grid[cell_y][cell_x] == FREE_CELL:
                    check_result += 1
        return True if check_result == 0 or check_result == 1 else False

    def check_coord(check_y: int, check_x: int) -> int:
        """
        Check what in cell player opened.

        :param check_y: int - y-coord of current cell
        :param check_x: int - x-coord of current cell
        :return: int - -1 - BOOM! player loose; 0 - free cell, continue game
        """
        if player_grid[check_y][check_x] == FREE_CELL and game_grid[check_y][check_x] == MINE:
            show_around(check_y, check_x)
            return -1
        else:
            show_around(check_y, check_x)
            return 0

    def print_grid(fin=False):
        if fin:
            for cell_y in range(1, game_height - 1):
                for cell_x in range(1, game_width - 1):
                    show_around(cell_y, cell_x)

        import os

        os.system('cls||clear')
        print(f'Упрощенный вариант: открываются клетки вокруг выбранной, если там мины нету, конечно же :)')
        print(f'Рандомное минное поле ({game_height} × {game_width}) c {game_mines} миной(ами):')

        headers = [str(header_num) for header_num in range(1, game_width + 1)]
        rows = [str(row_num) for row_num in range(1, game_height + 1)]
        print(tabulate(player_grid,
                       headers,
                       tablefmt="grid",
                       showindex=rows,
                       stralign="center"))

    game_height = randint(4, 6)
    game_width = randint(4, 6)
    game_mines = game_width * game_height // 4
    random_grid = create_empty_grid(game_height, game_width)  # game grid
    set_random_mines(random_grid, game_mines)  # init game grid by mines
    game_grid = num_grid(random_grid)
    player_grid = create_empty_grid(game_height, game_width)  # that grid is shown to the player

    result = 0
    while result == 0:
        print_grid()
        x, y = input_coord(game_height, game_width)
        result = check_coord(y, x) or check_grid_is_open()

    if result == 1:
        print_grid(fin=True)
        print('🏆 Поздравляю вы выиграли!')
    else:
        print_grid(fin=True)
        print('💥 ХАДЫЩЩЩ!!!111 Вы проиграли!')
