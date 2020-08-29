def yesno_to_bool(yes_or_no: str) -> bool:
    """This takes a yes or no value and converts into a bool: True for yes, and False for no.

    Keyword arguments:
    yes_or_no (str) -- The yes or no value to be converted to a bool value."""
    if yes_or_no.lower() == "yes":
        return True
    elif yes_or_no.lower() == "no":
        return False
    else:
        raise ValueError("The value provided ({}) is not yes or no.".format(yes_or_no))
