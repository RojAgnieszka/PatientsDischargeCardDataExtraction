def fix_polish_chars(text):
    pl_chars = 'Ê¥ñ„¹ó³£êœæ¿¯'
    normal_chars = 'ĘĄńŚąółŁęśćżŻ'
    translator = str.maketrans(pl_chars, normal_chars)
    return text.translate(translator)


def change(text):
    old = '()'
    new = '&&'
    translator = str.maketrans(old, new)
    return text.translate(translator)


def to_float(text):
    return float(text.replace(',', '.'))


def filter(condition, text):
    filtered = ""
    for letter in text:
        if condition(letter):
            filtered += letter

    return filtered


def for_each(action, text):
    for letter in text:
        action(letter)


def take_while(condition, text):
    taken = ""
    for letter in text:
        if condition(letter):
            taken += letter
        else:
            break

    return taken

