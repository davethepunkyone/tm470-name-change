def yesno_to_bool(yes_or_no: str) -> bool:
    if yes_or_no.lower() == "yes":
        return True
    elif yes_or_no.lower() == "no":
        return False
    else:
        raise ValueError("The value provided ({}) is not yes or no.".format(yes_or_no))
