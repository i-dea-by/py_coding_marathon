import copy
from random import randint
from tabulate import tabulate
from typing import List, Tuple

warehouse_typing = List[List[int]]


def create_matrix(m_height: int, m_width: int, max_num: int) -> warehouse_typing:
    """
    Создание матрицы размером m_height × m_width элементов заполненную элементами случайной величины
    в диапазоне от 0 до max_num
    :param m_width: ширина матрицы
    :param m_height: высота матрицы
    :param max_num: максимальное число в ячейке матрицы
    :return: матрица писем типа List[List[int]] (двухмерный список) c письмами. Минимальные размеры = 3х3
    """
    return [[randint(0, max_num) for _ in range(m_width)] for _ in range(m_height)]


def check_dimensions(warehouse: warehouse_typing) -> Tuple[int, int]:
    """
    Функция выясняющая размеры склада. В случае если длины строк различны, то возвращаемой длиной склада будет
    длина минимальной строки.
    :param warehouse: Входная матрица писем типа list (двухмерный список)
    :return: Возвращает кортеж из двух чисел представляющие собой размеры склада: (высота, длина)
    """
    return len(warehouse), len(min(warehouse, key=len))


def add_zero_borders(warehouse: warehouse_typing) -> warehouse_typing:
    """
    Функция добавляет заполненные нолями нулевые строку и столбец
    :param warehouse: исходная матрица, тип List[List[int]]
    :return: матрица с добавленными строкой и столбцом, тип List[List[int]]
    """
    temp_warehouse = copy.deepcopy(warehouse)
    for row in temp_warehouse:
        row.insert(0, 0)
    temp_warehouse.insert(0, [0 for _ in range(len(temp_warehouse[0]))])
    return temp_warehouse


def remove_zero_borders_in_source(warehouse: warehouse_typing) -> None:
    """
    Функция удаляет нулевые строку и столбец в исходной матрице.
    :param warehouse: исходная матрица, тип List[List[int]]
    :return: None, удаление происход в том списке, который передали
    """
    warehouse.pop(0)
    for row in warehouse:
        row.pop(0)


def restore_and_print_path(warehouse: list, weights: list):
    """
    Функция восстанавливающая путь почтальона по почте (warehouse) по максимальным весам из массива weights.
    Так же функция выводит в консоль таблицу с отображением пути почтальона.
    :param warehouse: 2D почты на складе массив с добавленными 0-ми колонкой и строкой
    :param weights: таблица весов - 2D массив
    :return: None
    """

    warehouse_copy = copy.deepcopy(warehouse)
    i, j = check_dimensions(warehouse_copy)
    i, j = i - 1, j - 1

    warehouse_copy[i][j] = f'({str(warehouse_copy[i][j])})'
    while i > 0 and j >= 0:
        if weights[i][j - 1] == 0 and j == 2:  # редкий интересный случай с такими данными >:)))
            j -= 1
        elif weights[i][j - 1] > weights[i - 1][j]:
            j -= 1
        else:
            i -= 1
        warehouse_copy[i][j] = f'({str(warehouse_copy[i][j])})'

    # удаляем граничные нули в матрице перед выводом в консоль
    remove_zero_borders_in_source(warehouse_copy)

    # выводим матрицу почты с указанием пути
    print(tabulate(warehouse_copy, stralign="center", tablefmt="grid"))


def harry(warehouse: warehouse_typing, show_path=False) -> int:
    """
    Гарри — почтальон. У него есть почтовый участок размером n * m (матричный / 2D-список). Каждый слот в 2D-списке
    представляет количество писем в этом месте.
    Гарри может идти только вправо и вниз. Он начинает обход в (0, 0) и заканчивает в (n-1, m-1).
    n представляет высоту, а m — длину матрицы. Письма Гарри может брать только там, где находится.
    :param show_path: Флаг, показывать путь с максиальной суммой (True) или нет (False). По умолчнию - False
    :param warehouse: Входная матрица писем типа list[list] (двухмерный список)
    :return: Возвращает максимальное число писем которое Гарри может собрать на складе
    """
    # проверяем соответствие типов входных параметров
    if not isinstance(show_path, bool):
        raise TypeError('Ключевой аргумент show_path должен быть типа bool!')
    if not isinstance(warehouse, list):
        raise TypeError('Аргумент warehouse должен быть типа list!')

    # проверяем что во входном списке хоть что-то есть
    if not warehouse[0] or not warehouse:
        return -1

    # проверяем и сохраняем размеры матрицы
    post_height, post_width = check_dimensions(warehouse)

    # копия склада с граничными нулями
    temp_warehouse = add_zero_borders(warehouse)

    # создаём заполненную нолями матрицу для весов
    weights = create_matrix(post_height + 1, post_width + 1, 0)

    # магия
    for i in range(1, post_height + 1):
        for j in range(1, post_width + 1):
            mails = temp_warehouse[i][j]
            weights[i][j] = max(weights[i - 1][j], weights[i][j - 1]) + mails

    # если указан параметр show_path=True
    if show_path:
        restore_and_print_path(temp_warehouse, weights)

    return weights[-1][-1]


if __name__ == '__main__':
    # подготовленный зарание склад с письмами
    warehouse_init = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]

    # тесты
    assert harry([[5, 2], [5, 2]]) == 12
    assert harry(warehouse_init) == 72
    assert harry([[]]) == -1

    # работаем
    print('Готовый склад:')
    print(tabulate(warehouse_init, tablefmt="grid"))
    height, length = check_dimensions(warehouse_init)
    print(f'Размер склада (высота х длина): {height}x{length}')
    print(f'Максимальное количество писем: {harry(warehouse_init)}')
    print('-' * 60)

    # используем случайные значения
    random_mails = create_matrix(randint(1, 10), randint(1, 10), 10)
    print('Случайный склад (с отображением наилучшего пути):')
    height, length = check_dimensions(random_mails)
    print(f'Размер склада (высота х длина): {height}x{length}')
    print(f'Максимальное количество писем: {harry(random_mails, show_path=True)}')
