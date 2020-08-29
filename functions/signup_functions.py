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
    """This verifies that the email address provided is in a valid email format and returns the outcome as a bool.
    Valid = True, Invalid = False.

    Keyword arguments:
    email (str) -- The email address to check."""
    email_regex = re.compile('[0-9A-Za-z.\']+@([0-9A-Za-z.])+([0-9A-Za-z])', re.UNICODE)
    if email_regex.match(email):
        return True
    else:
        return False


def confirm_password_value(pwd: str) -> str or None:
    """This verifies that the prototype password provided meets the expected criteria and returns an error message
    if not.  Returns str if invalid, or None if valid.

    Requirements: Must be at least 8 characters in length, with at least 1 uppercase letter, 1 lowercase letter and
    1 number.

    Keyword arguments:
    pwd (str) -- The password value to check."""
    caps_check = re.compile('[A-Z]', re.UNICODE)
    lower_check = re.compile('[a-z]', re.UNICODE)
    num_check = re.compile('[0-9]', re.UNICODE)

    if len(pwd) < 8:
        return "The password must be at least 8 characters."
    elif caps_check.search(pwd) is None:
        return "The password requires at least one uppercase letter."
    elif lower_check.search(pwd) is None:
        return "The password requires at least one lowercase letter."
    elif num_check.search(pwd) is None:
        return "The password requires at least one numeric character."
    else:
        return None


def generate_code(no_of_chars: int) -> str:
    """This generates a random alphanumeric code based on the number of characters needed and returns it as a str.

    Keyword arguments:
    no_of_chars (int) -- The number of characters needed in the code."""
    code = ""
    characters = string.ascii_letters + string.digits
    i = 1
    while i <= no_of_chars:
        character_to_use = random.randint(0, len(characters))
        code = code + characters[character_to_use:character_to_use + 1]
        i += 1
    return code


def generate_capcha_code() -> str:
    """This generates a random five-digit alphanumeric code for use as the CAPCHA on the signup form, and returns
    it as a str."""
    return generate_code(5)


def generate_signup_code() -> str:
    """This generates a random twenty-digit alphanumeric code for use in the email verification process, and returns
    it as a str."""
    return generate_code(20)


def generate_link(signup_verification: SignupVerification) -> str:
    """This generates a URL for a user to access to confirm the verification of their user account and returns it
    as a str.

    Keyword arguments:
    signup_verification (SignupVerification) -- The signup verification object that contains the code associated
    with the user."""
    return live_url + "/new_account_confirm/" + signup_verification.signup_code


def email_user_notepad_version(user: User, signup_verification: SignupVerification) -> None:
    """This creates a fake email in a text file that is designed to look like a representation of the actual email
    a user would receive from the system.  This opens in notepad once generated.

    NOTE: This currently logs in the logging directory (which is included in the gitignore) but the final product
    obviously would not work in this way.

    Keyword arguments:
    user (User) -- The user that this email is intended for.
    signup_verification (SignupVerification) -- The signup verification object associated with the user."""
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
