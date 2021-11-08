animals = ["dog", "cat", "bat", "cock", "cow",
           "pig", "fox", "ant", "bird", "lion",
           "wolf", "deer", "bear", "frog", "hen",
           "mole", "duck", "goat"]


def count_animals(original_text: str) -> int:
    """
    Returns the maximum number of the words from 'animals' list of strings which can be found in the original_text.
    Function implements a high-performance recursive algorithm that doesn't involve caching.
    A list of str 'animals' should be available in the global scope. Strings representing animals should be in lowercase.
    :param original_text: str
    :return: int
    """

    # We don't want our function to be case-sensitive
    original_text = original_text.lower()

    # Getting rid of characters in the original_text that none of the animals contains
    original_text = ''.join(list(filter(lambda character: character in set(''.join(animals)), original_text)))

    total_animals_number = len(animals)

    def check_and_cut(text: str, animal_index: int) -> tuple:
        """
        Checks whether the text contains the word animals[animal_index].
        Returns the tuple (False, '') if the text doesn't contain the animal = animals[animal_index]. Returns the tuple (True, text_without_animal) if the text contains the word animals[animal_index]. In this case the second item in the tuple is the text without letters from the animal string.
        :param text: str
        :param animal_index: int
        :return: tuple(bool, str)
        """
        for character in animals[animal_index]:
            if character in text:
                text = text.replace(character, '', 1)
            else:
                return False, ''  # text doesn't contain the current animal
        return True, text  # text contains the current animal => cut it out

    def get_max_recursion_depth(current_text: str, first_animal_index: int) -> int:
        """
        Recursive function that returns the maximum recursion depth that can be reached when applied to the current_text and with limitations to the available part of the animal list. Animals with indices from first_animal_index to the last index can be used only.
        :param current_text: str, text the function will cut animals from
        :param first_animal_index: int, the index of the first available word in the animal list
        :return: int, maximum recursion depth
        """

        max_recursion_depth = 0

        # Optimization trick: because of commutativity of substring exclusion composition we don't need to start from the first animal in the list over and over again. Every available UNORDERED animal subset will be reached even if we won't go back in the list when recursion is called after cutting out the n-th animal; we just have to check each animal starting with the n-th again. Moreover, subsets will never match; that means WE DON'T NEED CACHE.
        for current_animal_index in range(first_animal_index, total_animals_number):
            check_result = check_and_cut(current_text, current_animal_index)

            # if the animal with index current_animal_index can be found in the current_text - cut it out and go deeper
            if check_result[0]:

                # actual recursion call
                current_recursion_depth = get_max_recursion_depth(check_result[1], current_animal_index)

                # update maximum recursion depth if necessary
                if max_recursion_depth < current_recursion_depth:
                    max_recursion_depth = current_recursion_depth

        # +1 for the call we are in
        return max_recursion_depth + 1

    # -1 because the maximum recursion depth is greater by one than the number of words we can find in the original_text because of the last recursion call where not a single animal was found
    return get_max_recursion_depth(original_text, 0) - 1


if __name__ == '__main__':
    text = 'cockdogwdufrbiraier' * 4
    print(count_animals(text))
