def same_length(number):
    num_as_string = str(number)
    while '10' in num_as_string:
        num_as_string = num_as_string.replace('10', '')
    return len(num_as_string) == 0


if __name__ == '__main__':
    print(same_length(110100))
