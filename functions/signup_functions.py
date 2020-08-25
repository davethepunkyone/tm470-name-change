import random
import string
import webbrowser
import datetime
import re
from globals.global_variables import live_url
from classes.user_class import User
from classes.signup_verification_class import SignupVerification
from functions.logging_functions import get_logging_directory


def confirm_email_address_value(email: str) -> bool:
    email_regex = re.compile('[0-9A-Za-z.\']+@([0-9A-Za-z.])+([0-9A-Za-z])', re.UNICODE)
    if email_regex.match(email):
        return True
    else:
        return False


def generate_code(no_of_chars: int) -> str:
    code = ""
    characters = string.ascii_letters + string.digits
    i = 1
    while i <= no_of_chars:
        character_to_use = random.randint(0, len(characters))
        code = code + characters[character_to_use:character_to_use + 1]
        i += 1
    return code


def generate_capcha_code() -> str:
    return generate_code(5)


def generate_signup_code() -> str:
    return generate_code(20)


def generate_link(signup_verification: SignupVerification) -> str:
    return live_url + "/new_account_confirm/" + signup_verification.signup_code


def email_user_notepad_version(user: User, signup_verification: SignupVerification) -> None:
    # For now use logging directory to store this as it is in gitignore, final app wouldn't use this anyway
    filepath = get_logging_directory() + "/email_to_user.txt"
    email_string = "TO: \t\t" + user.email + "\n" + \
                   "SUBJECT: \tChange Your Name - Verify Email Address" + "\n" + \
                   "DATE: \t\t" + datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y %H:%M") + "\n" + \
                   "-------------------------------------------------------------" + "\n" + \
                   "Hi " + user.forenames + ", \n\n" + \
                   "To verify your email address with Change Your Name, please click on the link below. \n\n" + \
                   generate_link(signup_verification) + "\n\n" + \
                   "Regards, \n Change Your Name Support"

    eml = open(filepath, "w")
    eml.write(email_string)
    eml.close()
    webbrowser.open(filepath)
