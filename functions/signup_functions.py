import random
import string


def generate_signup_code() -> str:
    code = ""
    characters = string.ascii_letters + string.digits
    i = 1
    while i <= 16:
        character_to_use = random.randint(0, len(characters))
        code = code + characters[character_to_use:character_to_use+1]
        i += 1
    return code
