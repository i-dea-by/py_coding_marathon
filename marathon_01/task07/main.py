from typing import Tuple

animals = ["dog", "cat", "bat", "cock", "cow", "pig", "fox", "ant", "bird", "lion", "wolf", "deer", "bear", "frog",
           "hen", "mole", "duck", "goat", "cot"]

animals_typing = Tuple[int, list]


def can_word(animal: list, symbols: list) -> bool:
    """
    Функция определяет можно ли из входных symbols собрать слово animal. Если да, то возвращает True, если нет - False
    :param animal: строка
    :param symbols:
    :return: True если слово animal можно собрать, иначе - False
    """
    l_animal = sorted(animal)

    for item in symbols:
        if item in l_animal:
            l_animal.remove(item)
        if not l_animal:
            return True
    return False


def subtract(animal: list, symbols: list):
    """
    Функция которая вычитает посивольно animal из symbols.
    ПРИ ЭТОМ ИЗМЕНЯЕТСЯ входной аргумент symbols - из него удаляется символы
    :param animal: list
    :param symbols: list
    """
    l_animal = sorted(animal)
    for char in l_animal:
        if char in symbols:
            symbols.remove(char)


def word_counter(animal_list: list, search_string: str) -> animals_typing:
    """
    Функция находит слова в списке animal_list, которые можно собрать из символов search_string, перебирая список слов.
    на выходе кортеж из количества найденных слов и списка этих слов
    :param animal_list: list
    :param search_string: list
    :return: tuple[int, list] - кортеж из количества найденных слов и списка этих слов
    """
    counter = 0
    search_list = list(search_string)
    result = []
    for animal in animal_list:
        repeat = True
        while repeat:
            repeat = can_word(animal, search_list)
            if repeat:
                result.append(animal)
                subtract(list(animal), search_list)
                counter += 1
    return counter, result


def count_animals(txt: str) -> int:
    """
    Функция, которая принимает строку txt и возвращает максимальное количество названий животных,
    которые возможно собрать из символов строки.
    :param txt: строка символов
    :return: int - количество найденных слов
    """
    # проверяем соответствие типов входных параметров
    if not isinstance(txt, str):
        raise TypeError('Ключевой аргумент search_string должен быть типа str!')

    return max(word_counter(animals, txt),
               word_counter(sorted(animals, reverse=True), txt))[0]


if __name__ == '__main__':
    assert count_animals('goatcode') == 2
    assert count_animals('cockdogwdufrbir') == 4
    assert count_animals('dogdogdogdogdog') == 5

    text = 'goatcode'
    print(f'Из "{text}" можно собрать {count_animals(text)} слов(а).')
    print(f'Это слова: {max(word_counter(animals, text), word_counter(sorted(animals, reverse=True), text))[1]}\n')

    text = 'cockdogwdufrbir'
    print(f'Из "{text}" можно собрать {count_animals(text)} слов(а)')
    print(f'Это слова: {max(word_counter(animals, text), word_counter(sorted(animals, reverse=True), text))[1]}\n')

    text = 'cockdogwdufrbiraier' * 3
    print(f'Из "{text}" можно собрать {count_animals(text)} слов(а)')
    print(f'Это слова: {max(word_counter(animals, text), word_counter(sorted(animals, reverse=True), text))[1]}\n')

    text = 'whikpbnpcoiiyaiudpjl' * 3
    print(f'Из "{text}" можно собрать {count_animals(text)} слов(а)')
    print(f'Это слова: {max(word_counter(animals, text), word_counter(sorted(animals, reverse=True), text))[1]}\n')

    text = 'abcdefghiklmnoprtuwx' * 6
    print(f'Из "{text}" можно собрать {count_animals(text)} слов(а)')
    print(f'Это слова: {max(word_counter(animals, text), word_counter(sorted(animals, reverse=True), text))[1]}\n')

    text = 'catcatctoa'
    print(f'Из "{text}" можно собрать {count_animals(text)} слов(а)')
    print(f'Это слова: {max(word_counter(animals, text), word_counter(sorted(animals, reverse=True), text))[1]}\n')
