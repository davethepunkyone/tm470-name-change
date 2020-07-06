

def confirm_email(email):
    if len(email) == 0:
        return "Error"
    else:
        return "Not Error"


print(confirm_email(""))
print(confirm_email("test"))


