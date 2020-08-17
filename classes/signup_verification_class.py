from classes.user_class import User


class SignupVerification:

    def __init__(self, **kwargs):
        self._signup_code = None
        self._user_id = None
        self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key == "user_id":
                self.user_id = value
            elif key == "signup_code":
                self.signup_code = value
            else:
                raise KeyError("Keyword ({}) provided is not a valid property".format(key))

    @property
    def signup_code(self) -> str:
        return self._signup_code

    @signup_code.setter
    def signup_code(self, code: str) -> None:
        self._signup_code = code

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_to_add: int) -> None:
        self._user_id = user_to_add
