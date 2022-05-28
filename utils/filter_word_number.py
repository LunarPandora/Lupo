def filter_word_number(input: str) -> str:
    """
    Convert all numbers in the input word to alphabets.

    Examples:

    >>> filter_word_number("h1 m0m")
    'hi mom'
    >>> filter_word_number("8r34d")
    'bread'
    """
    WORD_NUMBER = {
        "i": "1",
        "l": "1",
        "e": "3",
        "b": "3",
        "a": "4",
        "s": "5",
        "g": "6",
        "b": "8",
        "g": "9",
        "o": "0"
    }
    res = ""

    word = list(WORD_NUMBER.keys())
    number = list(WORD_NUMBER.values())

    for i in input:
        if i in number:
            pos = number.index(i)
            res += word[pos]
        else:
            res += i

    return res

def main():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    main()
