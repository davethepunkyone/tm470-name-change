from classes.user_class import User
from random import randint
import logging_functions as logger


def generate_access_code(user) -> int:
    if user.email is not None:
        random_code = randint(100000, 999999)
        logger.log_info("Code generated for {0}: {1}".format(user.email, random_code))
        return random_code
    else:
        raise ValueError("The user provided does not have a valid email address.")


x = User()
x.email = "test@123.com"
generate_access_code(x)
