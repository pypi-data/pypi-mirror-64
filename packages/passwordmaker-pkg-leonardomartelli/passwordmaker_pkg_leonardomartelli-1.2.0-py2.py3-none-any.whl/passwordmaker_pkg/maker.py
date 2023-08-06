from enum import Enum
import random
import string


class CharacterType(Enum):
    UPPERCASE = 0
    LOWERCASE = 1
    NUMBER = 2


def create_password(character_number, with_uppercase, with_lowercase, with_numbers):
    return mount_password(get_content(with_uppercase, with_lowercase, with_numbers), character_number)


def create_numeric_password(character_number):
    return mount_numeric_password(character_number)


def get_content(with_uppercase, with_lowercase, with_numbers):
    content = list()

    if with_uppercase:
        content.append(CharacterType.UPPERCASE)
    if with_lowercase:
        content.append(CharacterType.LOWERCASE)
    if with_numbers:
        content.append(CharacterType.NUMBER)

    return content


def get_character(content):
    return switch(content[get_type_to_add(len(content) - 1)])


def mount_password(content, character_number):
    characters = []

    for c in range(0, character_number):
        characters.append(get_character(content))

    return ''.join(characters)


def mount_numeric_password(character_number):
    characters = []

    for c in range(0, character_number):
        characters.append(get_number())

    return ''.join(characters)


def switch(argument):
    if argument is CharacterType.UPPERCASE:
        return get_letter().upper()
    elif argument is CharacterType.LOWERCASE:
        return get_letter()
    else:
        return get_number()


def get_letter():
    return random.choice(string.ascii_lowercase)


def get_number():
    return random.randint(0, 9).__str__()


def get_type_to_add(max_index):
    return random.randint(0, max_index)
