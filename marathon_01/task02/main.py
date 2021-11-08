def normalize(input_string: str) -> str:
    """
    Если входная строка состоит только из символов верхнего регистра, то функция приводит ее в нижний регистр
    и добавляет в конце восклицательный знак.

    :param input_string: входная строка (str)
    :return: результат обработки строки (str)
    :raises: ValueError: если входной тип данных не строка
    """

    if isinstance(input_string, str):
        return f'{input_string.capitalize()}!' if input_string.isupper() else input_string
    else:
        raise TypeError('normalize(input_string) - неправильный тип входных данных')


if __name__ == '__main__':
    # тесты
    assert normalize('CAPS LOCK DAY IS OVER') == 'Caps lock day is over!'
    assert normalize('') == ''
    assert normalize('ПРИВЕТ') == 'Привет!'
    assert normalize('1') == '1'
    assert normalize('Hello there.') == 'Hello there.'
    assert normalize('Мама мыла раму, А ПАПА ДВЕРЬ!') == 'Мама мыла раму, А ПАПА ДВЕРЬ!'
    assert normalize('ПАПА ВЫБИЛ ДВЕРЬ') == 'Папа выбил дверь!'

    print(normalize('ПАПА ВЫБИЛ ДВЕРЬ'))
