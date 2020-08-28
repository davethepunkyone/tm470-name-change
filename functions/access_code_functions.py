import datetime
from random import randint


def generate_unique_access_code() -> str:
    digit1 = str(randint(0, 9))
    digit2 = str(randint(0, 9))
    digit3 = str(randint(0, 9))
    digit4 = str(randint(0, 9))
    digit5 = str(randint(0, 9))
    digit6 = str(randint(0, 9))

    return digit1 + digit2 + digit3 + digit4 + digit5 + digit6


def check_expiry_date_is_valid(current_expiry: datetime or None, duration_time: int, duration_denominator: str)\
        -> str or None:
    max_datetime_allowed = datetime.datetime.now() + datetime.timedelta(days=31)
    if current_expiry is None:
        calculated_expiry = datetime.datetime.now()
    else:
        calculated_expiry = current_expiry

    if duration_denominator == "hours":
        calculated_expiry = calculated_expiry + datetime.timedelta(hours=duration_time)
    elif duration_denominator == "days":
        calculated_expiry = calculated_expiry + datetime.timedelta(days=duration_time)

    if calculated_expiry > max_datetime_allowed:
        return "The date cannot be more than 31 days after today's date."
    else:
        return None
