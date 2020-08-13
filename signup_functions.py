from classes.user_class import User
from classes.marriagecertificate_class import MarriageCertificate
from random import randint
from datetime import datetime, timedelta
import logging_functions as logger


def generate_new_account_code(user: User) -> int:
    if user.email is not None:
        random_code = randint(100000, 999999)
        logger.log_info("Code generated for {0}: {1}".format(user.email, random_code))
        return random_code
    else:
        raise ValueError("The user provided does not have a valid email address.")


def generate_email(user: User):
    access_code = generate_new_account_code(user)
    expiry_date = datetime.now() + timedelta(hours=2)
    email_body = "Hello {0}, \n Your new account code for Change Your Name is: {1} \n This code will expire at: {2}."\
        .format(user.first_name, access_code, expiry_date.strftime("%d/%m/%Y %H:%M:%S"))
    print(email_body)


# TODO - Remove below, for testing only
x = User()
x.first_name = "Testy"
x.email = "test@123.com"
y = MarriageCertificate()
y.document_id = 1
z = MarriageCertificate()
z.document_id = 5
x.docs = y
x.docs = z
a = x.get_specific_listed_doc(5)
print("doc id: " + a.document_id.__str__())
generate_email(x)
print("---")
print(str(x.return_user_as_json))
