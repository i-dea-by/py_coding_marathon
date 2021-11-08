def is_pandigital(number: int) -> bool:
    """
    Возвращает True или False в зависимости от того панцифровое это число или нет

    :param number: входное число, тип int
    :return: bool True или False
    """
    digits = '0123456789'  # чтоб не было лишнего импорта
    return set(str(number)) == set(digits)


if __name__ == '__main__':
    # тесты
    assert is_pandigital(1234567890)
    assert not is_pandigital(23456789)
    assert not is_pandigital(90864523148909)
    assert not is_pandigital(112233445566778899)

    print(is_pandigital(98140723568910))
    print(is_pandigital(90864523148909))
    print(is_pandigital(112233445566778899))
    print(is_pandigital(123456789))
