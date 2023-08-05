import getpass
import os
from datetime import datetime

from cli import __version__


def camel_to_snake(text: str):
    if len(text) > 0 and text[0].islower():
        return text
    letters = []
    last_letter = None
    for letter in text:
        if last_letter and \
            (letter.isdigit() != last_letter.isdigit() or
                letter.isupper() and not last_letter.isupper()):
            letters.append('_'+letter.lower())
        else:
            letters.append(letter.lower())
        last_letter = letter

    result = "".join(letters)
    return result


def snake_to_camel(text: str):
    if len(text) > 0 and text[0].isupper():
        return text
    letters = []
    got_underline = True
    for letter in text:
        if not letter.isalpha():
            got_underline = True
            if letter == '_':
                continue

        if got_underline:
            letter = letter.upper()
            got_underline = False
        letters.append(letter)

    return "".join(letters)


def get_words(line: str, nwords: int = 0, sep: str = ';'):
    words = [word.strip() for word in line.split(sep)]
    if nwords > 0:
        while len(words) < nwords:
            words.append(None)
    else:
        nwords = len(words)

    return words[:nwords]


def padr(string: str, size: int):
    if size > 0:
        layout = "{0:"+str(size)+"}"
        return layout.format(string)

    return string


def created_by():
    return "# CANAA-BASE-MODEL-CREATOR v{0} IN {1} : {2}".format(
        __version__,
        datetime.now(),
        getpass.getuser()
    )


def get_file_extension(filename):
    se = os.path.splitext(filename)
    return "" if len(se) < 2 else se[1]
