from random import randint


def generate_unique_access_code() -> str:
    digit1 = str(randint(0, 9))
    digit2 = str(randint(0, 9))
    digit3 = str(randint(0, 9))
    digit4 = str(randint(0, 9))
    digit5 = str(randint(0, 9))
    digit6 = str(randint(0, 9))

    return digit1 + digit2 + digit3 + digit4 + digit5 + digit6
