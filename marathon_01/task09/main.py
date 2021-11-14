def get_char_as_binary(char: str) -> str:
    """
    Функция возвращает бинарное представление кода символа переданного в аргументе chr.
    Декодируется только первый символ! Так же в результате есть лидирующие нули до 8 либо 16 бит/символов.
    Если входная строка пустая, то функция возвращает 8 нулей

    :param char: входной символ, если передается строке длиной более 1 символа - используется только первый!
    :return: бинарное представление кода символа с лидирующими нулями длиной 8/16 символов
    """
    # проверяем соответствие типов
    if not isinstance(char, str):
        raise ValueError('get_char_as_binary() - не правильный тип данных передан в параметрах!')

    result = '00000000'
    if char:
        binary = bin(ord(char[0])).replace('0b', '')  # получаем двоичное представление кода символа и удаляем '0b'
        result = binary.zfill(16 if len(binary) > 8 else 8)  # добавляем нужное кол-во нулей слева
    return result


def translator(string: str, base: str = 'двуликий') -> str:
    """
    Функция переводит поданные символы в "двоичный" код в виде строки "двуЛиКий" где маленькие буквы вместо 0,
    а большие - вместо 1. Если при кодировке получается 16 битные значения
    (русские буквы) между старшим и младшими

    :param base: базовая строка для кодирования, длина должна быть не меньше 8 символов!
    :param string: str - входная строка символов, если задана пользователем - используется первые 8 символов!
    :return: str - "двуликий код"
    """
    # проверяем соответствие типов
    if not isinstance(string, str):
        raise ValueError('translator() - не правильный тип данных передан в параметрах!')

    if len(base) < 8:
        raise ValueError('translator() - парметр base должен быть длиной >= 8 символов !')

    base_str = base[:8].lower() * 2  # приводим к надлежащему виду, если передана пользовательская строка
    base_upper = base_str.upper()

    result = []

    for char in string:
        binary = get_char_as_binary(char)
        for pos, bin_char in enumerate(binary):
            if pos == 8:  # если русская буква то разделяем половинки через _
                result.append('_')
            result.append(base_upper[pos] if bin_char == '1' else base_str[pos])
        result.append(' ')
    else:
        result.pop()  # удаляем пробел в конце
    return ''.join(result)


def translator_gen(string: str, base: str = 'двуликий') -> str:
    """
    Функция-генератор переводит поданные символы в "двоичный" код в виде строки "двуЛиКий" где маленькие буквы вместо 0,
    а большие - вместо 1. Если при кодировке получается 16 битные значения
    (русские буквы) между старшим и младшими

    :param base: базовая строка для кодирования, длина должна быть не меньше 8 символов!
    :param string: str - входная строка символов, если задана пользователем - используется первые 8 символов!
    :return: str - на выходе "двуликий код" символа в строке
    """
    # проверяем соответствие типов
    if not isinstance(string, str):
        raise ValueError('translator() - не правильный тип данных передан в параметрах!')

    if len(base) < 8:
        raise ValueError('translator() - парметр base должен быть длиной >= 8 символов !')

    base_str = base[:8].lower() * 2  # приводим к надлежащему виду, если передана пользовательская строка
    base_upper = base_str.upper()

    for char in string:
        result = []
        binary = get_char_as_binary(char)
        for pos, bin_char in enumerate(binary):
            if pos == 8:  # если русская буква то разделяем половинки через _
                result.append('_')
            result.append(base_upper[pos] if bin_char == '1' else base_str[pos])
        yield ''.join(result)


def re_translator(string: str) -> str:
    """
    Функция производит обртную кодировку из "двуликого" кода в исходную строку

    :param string: str - входная строка символов
    :return: str - восстановленная строка, если при раскодировании возникла ошибка, вместо символа вставляется ERR
    """
    # проверяем соответствие типов
    if not isinstance(string, str):
        raise ValueError('translator() - не правильный тип данных передан в параметрах!')

    lst = string.split(' ')
    result = []
    for word in lst:
        binary_lst = []
        for char in word:
            if char == '_':
                continue
            binary_lst.append('1') if char.isupper() else binary_lst.append('0')
        binary = ''.join(binary_lst)

        if binary and int(binary, 2) < 0x110000:  # проверяем чтоб не было пустого списка или выхода за пределы для chr()
            result.append(chr(int(binary, 2)))
        else:
            result.append('ERR')
    return ''.join(result)


def check_coded_str(string: str) -> bool:
    """
    Проверяем кодированную строку на правильноое содержание элементов "двуликого" кода:
    только символы слова "двуликий", " " и "_"

    :param string: str - входная строка
    :return: bool - результат проверки
    """
    # проверяем соответствие типов
    if not isinstance(string, str):
        raise ValueError('check_coded_str() - не правильный тип данных передан в параметрах!')

    return set(string.lower()) <= {'л', 'к', 'й', 'у', 'и', 'д', 'в', ' ', '_'}


if __name__ == '__main__':
    # тесты на примерах из задания
    assert translator("Hi") == "дВулИкий дВУлИкиЙ"
    assert translator("123") == "двУЛикиЙ двУЛикИй двУЛикИЙ"
    assert ' '.join(translator_gen("Hi")) == "дВулИкий дВУлИкиЙ"
    assert ' '.join(translator_gen("123")) == "двУЛикиЙ двУЛикИй двУЛикИЙ"

    # работаем
    example_str = 'Я.ru'
    result_str = translator(example_str)
    print(f'translator("{example_str}")="{result_str}"')

    example_str = 'Прывет'
    print(f'translator_gen("{example_str}")="{" ".join(translator_gen(example_str))}"')
    print('А теперь в обратную сторону: ')
    print(f're-translator("{result_str}")="{re_translator(result_str)}"')

    print()
    input_str = input('Введите строку для кодирования: ')
    trans_str = translator(input_str)
    print(f'В кодированном виде это будет: {trans_str}')

    print()
    input_loop = True
    while input_loop:
        input_str = input('Введите строку для декодирования (например: двулиКий_двУЛИкИй дВУЛИкиЙ двУликиЙ): ')
        if not check_coded_str(input_str):
            print('Вы ввели некорректную строку!')
            continue
        trans_str = re_translator(input_str)
        print(f'В декодированном виде это будет: {trans_str if trans_str else "__ ERROR :) __"}')
        input_loop = False
