
class User:
    """This is a class for the User object.

    This contains the following parameters:
    - ID
    - First Name
    - Surname
    - Email Address
    - Verified State"""

    def __init__(self):
        self._id = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._verified_state = None

    def set_first_name(self, first_name):
        self._first_name = first_name

    def get_first_name(self):
        return self._first_name

