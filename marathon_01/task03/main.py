from pprint import pprint
from random import randint

# типы известных формаций
FORMATION_TYPES = ['Empty', 'Stalactites', 'Stalagmites', 'Both']

# размер формации
FORMATION_SIZE = 4

unknown_formation = [
    [0, 0, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 1, 1],
    [0, 1, 1, 1]
]

random_formation: list[list[int]] = []


def fill_random_formation(size_x_y: int) -> list[list[int]]:
    """
    Функция случайного заполнения исследуемой формации

    :param size_x_y: размер матрицы
    :return: двумерный список заполненный случайными 0 и 1
    """
    return [[randint(0, 1) for _ in range(size_x_y)] for _ in range(size_x_y)]


def mineral_formation(formation: list[list[int]]) -> str:
    """
    Функция, которая определяет, представляют ли входные данные из себя «stalactites» (сталактиты)
    или «stalagmites» (сталагмиты). Если ввод содержит и сталактиты, и сталагмиты, возвращает «both» («оба»).

    :param formation: Входная матрица 4х4 типа list (двухмерный список) определяющая вид выясняемой формации минералов
    :return: Возвращает строку описывающую тип входной формации минералов
    """
    return FORMATION_TYPES[(1 in formation[0]) + (1 in formation[FORMATION_SIZE - 1]) * 2]


if __name__ == '__main__':
    # тесты
    assert mineral_formation([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == 'Empty'
    assert mineral_formation([[0, 0, 0, 0], [0, 1, 0, 1], [0, 1, 1, 1], [0, 1, 1, 1]]) == 'Stalagmites'
    assert mineral_formation([[0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1], [0, 0, 0, 0]]) == 'Stalactites'
    assert mineral_formation([[1, 0, 1, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 1]]) == 'Both'

    # работаем
    # сначала про готовую формацию
    pprint(unknown_formation, width=20)
    print(f'Исследуемая формация представляет из себя: {mineral_formation(unknown_formation)}')
    print()

    # заполняем случайными значениями
    random_formation = fill_random_formation(FORMATION_SIZE)
    print('Случайная формация:')
    pprint(random_formation, width=20)
    print(f'Исследуемая формация представляет из себя: {mineral_formation(random_formation)}')
