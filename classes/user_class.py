import json
from classes.document_class import Document
from classes.accesscode_class import AccessCode


class User:
    """This is a class for the handling of users.

    The following keyword arguments can be passed in:
    user_id (int), forenames (str), surname (str), email (str), prototype_password (str),
    verified_state (bool), docs (Document), access_codes (AccessCode)."""

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
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
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
        """Returns the user id for this user as an int."""
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """Sets the user id.

        Keyword arguments:
        user_id (int) -- The user id for this user. """
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
        """Returns the forenames for this user as a str."""
        return self._forenames

    @forenames.setter
    def forenames(self, forenames: str) -> None:
        """Sets the user forenames.

        Keyword arguments:
        forenames (str) -- The forenames for this user. """
        self._forenames = forenames

    @property
    def surname(self) -> str:
        """Returns the surname for this user as a str."""
        return self._surname

    @surname.setter
    def surname(self, surname: str) -> None:
        """Sets the user surname.

        Keyword arguments:
        surname (str) -- The surname for this user. """
        self._surname = surname

    @property
    def email(self) -> str:
        """Returns the email address for this user as a str."""
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        """Sets the user email address.

        Keyword arguments:
        email (str) -- The email address for this user. """
        self._email = email

    @property
    def prototype_password(self) -> str:
        """Returns the prototype password for this user as a str.

        NOTE: This value is not encrypted and this only exists in this format because this is a locally-run
        prototype, not a finished product."""
        return self._prototype_password

    @prototype_password.setter
    def prototype_password(self, pw: str) -> None:
        """Sets the user prototype password.

        NOTE: This value is not encrypted and this only exists in this format because this is a locally-run
        prototype, not a finished product.

        Keyword arguments:
        pw (str) -- The prototype password for this user. """
        self._prototype_password = pw

    @property
    def verified_state(self) -> bool:
        """Returns the verified state for this user as a bool."""
        return self._verified_state

    @verified_state.setter
    def verified_state(self, verified_state: bool) -> None:
        """Sets the user verified state.

        Keyword arguments:
        verified_state (bool) -- The verified state for this user. """
        if verified_state not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(verified_state))
        else:
            self._verified_state = verified_state

    @property
    def logged_in(self) -> bool:
        """Returns the logged in state for this user as a bool."""
        return self._logged_in

    @logged_in.setter
    def logged_in(self, logged_in_state: bool) -> None:
        """Sets the logged in state.

        Keyword arguments:
        logged_in_state (bool) -- The logged in state for this user. """
        if logged_in_state not in (1, 0, False, True, None):
            raise ValueError("Logged In State provided ({0}) is not boolean or None".format(logged_in_state))
        else:
            self._logged_in = logged_in_state

    @property
    def docs(self) -> list:
        """Returns the documents associated with this user as a list."""
        return self._docs

    @docs.setter
    def docs(self, document: Document) -> None:
        """Adds a document to the user documents list.

        Keyword arguments:
        document (Document) -- The document for this user. """
        if isinstance(document, Document):
            self._docs.append(document)
        else:
            raise ValueError("Item provided is not a valid document")

    def get_specific_listed_doc(self, doc_id: int) -> Document:
        """Returns a specific document from the users document list as a Document object.

        Keyword arguments:
        doc_id (int) -- The document id for the document associated with this user. """
        for doc in self.docs:
            if doc.document_id == doc_id:
                return doc
        else:
            raise ValueError("Document ID provided ({}) is not in the list of documents".format(doc_id))

    @property
    def access_codes(self) -> list:
        """Returns the access codes associated with this user as a list."""
        return self._access_codes

    @access_codes.setter
    def access_codes(self, access_code: AccessCode) -> None:
        """Adds a document to the user access codes list.

        Keyword arguments:
        access_code (AccessCode) -- The access code for this user. """
        if isinstance(access_code, AccessCode):
            self._access_codes.append(access_code)
        else:
            raise ValueError("Item provided is not a valid access code")

    @property
    def return_user_as_dict(self) -> dict:
        """This returns some of the user properties as a dict object for JSON conversion.

        NOTE: This functionality is not used, I planned to have a API to UI interface for this prototype
        but that didn't end up happening due to time constraints."""
        return {
            "id": self.user_id,
            "forenames": self.forenames,
            "surname": self.surname,
            "email": self.email,
            "verified_state": self.verified_state
        }

    @property
    def return_user_as_json(self) -> json:
        """This returns some of the user properties as a JSON object.

        NOTE: This functionality is not used, I planned to have a API to UI interface for this prototype
        but that didn't end up happening due to time constraints."""
        return json.dumps(self.return_user_as_dict, indent=4)
