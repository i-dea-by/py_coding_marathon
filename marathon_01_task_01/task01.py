from functools import reduce


def hamming_distance(str1: str, str2: str) -> int:
    result = 0
    for x in range(len(str1)):
        if str1[x] != str2[x]:
            result += 1
    return result


def hamming_distance_v2(str1: str, str2: str) -> int:
    return len([str1[x] for x in range(len(str1)) if str1[x] != str2[x]])


def hamming_distance_v3(str1: str, str2: str) -> int:
    return list(map(lambda x, y: x == y, str1, str2)).count(False)


def hamming_distance_enum(str1: str, str2: str) -> int:
    """ """
    result = 0
    for x, char in enumerate(str1):
        result += char != str2[x]
    return result


def hamming_distance_red(str1: str, str2: str) -> int:
    return reduce(lambda a, b: a + b, map(lambda x, y: x != y, str1, str2))


if __name__ == '__main__':
    print(f'{hamming_distance("abcd0", "bcdef")=}')  # 5
    print(f'{hamming_distance_v2("abcd0", "bcdef")=}')  # 5
    print(f'{hamming_distance_v3("abcd0", "bcdef")=}')  # 5
    print(f'{hamming_distance_enum("abcd0", "bcdef")=}')  # 5
    print(f'{hamming_distance_red("abcd0", "bcdef")=}')  # 5
