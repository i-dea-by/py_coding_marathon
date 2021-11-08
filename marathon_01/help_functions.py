import random
import time


def typed(type_):
    """
    Декоратор проверки типов данных для функций с одним параметром
    :param type_: Типа данных передаваемых в функцию (int, str  и тд)
    """
    def real_decorator(function):
        def wrapped(*args):
            for arg in args:
                if not isinstance(arg, type_):
                    raise ValueError(f'{function.__name__}() - не правильный тип данных! Должен быть {type_}')
            return function(*args)

        return wrapped

    return real_decorator


def time_it(function):
    """ Декоратор для замера времени работы функции
    :param function:
    :return:
    """

    def wrapped(*args, **kwargs):
        start_time = time.perf_counter()
        res = function(*args, **kwargs)
        end_time = time.perf_counter() - start_time
        print(f'Функция - {function.__name__}(). Время выполнения: {end_time} сек.')
        return res

    return wrapped


def repeat_timer(n=1000):
    """ Декоратор для замера времени выполнения функции с n повторами. По умаолчанию n=1000

    :param n: int - количество повторений. По умолчанию n=1000
    :return:
    """

    def _repeat(function):
        def wrapped(*args, **kwargs):
            start_time = time.perf_counter()
            for _ in range(n):
                res = function(*args, **kwargs)
            end_time = time.perf_counter() - start_time
            print(f'Функция - {function.__name__}(). Повторов: {n=:,}. Время выполнения: {end_time} сек.')
            return res

        return wrapped

    # не забываем ее вернуть!
    return _repeat


@time_it
def one_simple_function():
    print('one_simple_function()')


@repeat_timer(2)
def two_simple_function():
    print('two_simple_function()')


@typed(int)
def three_simple_function(num : int):
    print(f'Число: {num}')

def crossing_lists(main_list, compare_list):
    """ На выходе выдает пересечение списков. Пример: [3,2,1] | [1,3] -> [3,1]
        если пересечения нет - пустой список
    """
    result = []
    for char in main_list:
        if char in result:
            continue
        for c_char in compare_list:
            if char == c_char:
                result.append(char)
                break
    return result


def generate_random_string(length: int) -> str:
    """ Функция генерирует строку из рандомных символов из набора ascii_lowercase длинной length

    :param length: длинна генерируемой строки
    :return: строка из рандомных маленьких английских буков (str)
    """
    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'  # чтоб не импортировать string.ascii_lowercase
    return ''.join(random.choice(ascii_lowercase) for _ in range(length))


if __name__ == '__main__':
    pass
    # one_simple_function()
    # two_simple_function()
    # three_simple_function(1)
    # print(f'{generate_random_string(10)=}')
    # print(f'Пересечение списков [1,3,2,4] и [1,4] = {crossing_lists([4, 3, 2, 1], [1, 4])}')
