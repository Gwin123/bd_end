from fuzzywuzzy import fuzz


def is_names_equal(name_1: str, name_2: str) -> bool:
    is_equal = False
    name_1 = name_1.split()
    for word in name_1:
        a = fuzz.WRatio(word.lower(), name_2.lower())
        if a > 90:
            is_equal = True

    return is_equal
