
class User:
    """This is a class for the User object.

    This contains the following parameters:
    - User ID
    - First Name
    - Surname
    - Email Address
    - Verified State"""

    def __init__(self):
        self._user_id = None
        self._first_name = None
        self._surname = None
        self._email = None
        self._verified_state = None

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id) -> None:
        try:
            id_to_use = int(user_id)
            self._user_id = id_to_use
        except ValueError:
            if user_id is None:
                self._user_id = None
            else:
                raise ValueError("ID provided ({0}) is not numeric or None".format(user_id))

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, first_name) -> None:
        self._first_name = first_name

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, surname) -> None:
        self._surname = surname

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email) -> None:
        self._email = email

    @property
    def verified_state(self) -> bool:
        return self._verified_state

    @verified_state.setter
    def verified_state(self, verified_state) -> None:
        if verified_state not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(verified_state))
        else:
            self._verified_state = verified_state
