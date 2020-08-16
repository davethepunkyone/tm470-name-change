import json
from classes.document_class import Document
from classes.accesscode_class import AccessCode


class User:
    """This is a class for the User object.

    This contains the following parameters:
    - User ID
    - Forenames
    - Surname
    - Email Address
    - Verified State"""

    def __init__(self, **kwargs):
        self._user_id = None
        self._forenames = None
        self._surname = None
        self._email = None
        self._prototype_password = None
        self._verified_state = None
        self._logged_in = False
        self._docs = []
        self._access_codes = []
        if len(kwargs) > 0:
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key == "user_id":
                self.user_id = value
            elif key == "forenames":
                self.forenames = value
            elif key == "surname":
                self.surname = value
            elif key == "email":
                self.email = value
            elif key == "prototype_password":
                self.prototype_password = value
            elif key == "verified_state":
                self.verified_state = value
            elif key == "docs":
                if isinstance(value, list):
                    for item in value:
                        self.docs = item
                else:
                    self.docs = value
            elif key == "access_codes":
                if isinstance(value, list):
                    for item in value:
                        self.access_codes = item
                else:
                    self.access_codes = value
            else:
                raise KeyError("Keyword ({}) provided is not a valid property".format(key))

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        try:
            id_to_use = int(user_id)
            self._user_id = id_to_use
        except ValueError:
            if user_id is None:
                self._user_id = None
            else:
                raise ValueError("ID provided ({0}) is not numeric or None".format(user_id))

    @property
    def forenames(self) -> str:
        return self._forenames

    @forenames.setter
    def forenames(self, forenames: str) -> None:
        self._forenames = forenames

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, surname: str) -> None:
        self._surname = surname

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email = email

    @property
    def prototype_password(self) -> str:
        return self._prototype_password

    @prototype_password.setter
    def prototype_password(self, pw: str) -> None:
        self._prototype_password = pw

    @property
    def verified_state(self) -> bool:
        return self._verified_state

    @verified_state.setter
    def verified_state(self, verified_state: bool) -> None:
        if verified_state not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(verified_state))
        else:
            self._verified_state = verified_state

    @property
    def logged_in(self) -> bool:
        return self._logged_in

    @logged_in.setter
    def logged_in(self, logged_in_state: bool) -> None:
        if logged_in_state not in (1, 0, False, True, None):
            raise ValueError("Logged In State provided ({0}) is not boolean or None".format(logged_in_state))
        else:
            self._logged_in = logged_in_state

    @property
    def docs(self) -> list:
        return self._docs

    @docs.setter
    def docs(self, document) -> None:
        if isinstance(document, Document):
            self._docs.append(document)
        else:
            raise ValueError("Item provided is not a valid document")

    def get_specific_listed_doc(self, doc_id: int) -> Document:
        for doc in self.docs:
            if doc.document_id == doc_id:
                return doc
        else:
            raise ValueError("Document ID provided ({}) is not in the list of documents".format(doc_id))

    @property
    def access_codes(self) -> list:
        return self._access_codes

    @access_codes.setter
    def access_codes(self, access_code) -> None:
        if isinstance(access_code, AccessCode):
            self._access_codes.append(access_code)
        else:
            raise ValueError("Item provided is not a valid access code")

    @property
    def return_user_as_dict(self) -> dict:
        return {
            "id": self.user_id,
            "forenames": self.forenames,
            "surname": self.surname,
            "email": self.email,
            "verified_state": self.verified_state
        }

    @property
    def return_user_as_json(self) -> json:
        return json.dumps(self.return_user_as_dict, indent=4)
