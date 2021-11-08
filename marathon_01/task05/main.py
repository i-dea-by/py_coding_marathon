import re


def same_length(num: int) -> bool:
    """
    Функция возвращает true если в переданном целом числе за каждой последовательностью единиц (один или более)
    следует последовательность нулей РОВНО той же длины - большее кол-во нулей приводит к false

    :param num: число на входе (int)
    :return: результат обработки (bool)
    :raises: ValueError: если входной тип данных не целое число
    """
    if isinstance(num, int):
        result = False
        for match in re.finditer(r"(1+)(0+)", str(num)):
            if not (result := len(match.group(1)) == len(match.group(2))):
                return False
        return result
    else:
        raise TypeError('same_length(num) - на вход должно подаваться целое число!')


if __name__ == '__main__':
    # тесты
    assert same_length(110011100010)
    assert not same_length(101010110)
    assert same_length(111100001100)
    assert not same_length(111)

    # работаем c готовым числом
    test_number = 110100
    print(f'Проверяем число: {test_number}')
    print(f'Результат: {same_length(test_number)}')
