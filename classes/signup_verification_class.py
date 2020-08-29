from classes.user_class import User


class SignupVerification:
    """This is a class for the handling of signup verification.

    The following keyword arguments can be passed in for this object:
    user_id (int), signup_code (str)."""

    def __init__(self, **kwargs):
        self._signup_code = None
        self._user_id = None
        self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
        for key, value in kwargs.items():
            if key == "user_id":
                self.user_id = value
            elif key == "signup_code":
                self.signup_code = value
            else:
                raise KeyError("Keyword ({}) provided is not a valid property".format(key))

    @property
    def user_id(self) -> int:
        """Returns the user id for this signup verification as an int."""
        return self._user_id

    @user_id.setter
    def user_id(self, user_to_add: int) -> None:
        """Sets the user id.

        Keyword arguments:
        user_to_add (int) -- The user id for this signup verification. """
        self._user_id = user_to_add

    @property
    def signup_code(self) -> str:
        """Returns the signup code for this signup verification as a str."""
        return self._signup_code

    @signup_code.setter
    def signup_code(self, code: str) -> None:
        """Sets the signup code.

        Keyword arguments:
        code (str) -- The signup code for this signup verification. """
        self._signup_code = code
