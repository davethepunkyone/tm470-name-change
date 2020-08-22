import json
import datetime
from classes.enums import VerifiedStates
from classes.address_class import Address


class Document:
    """This is a class for the Document object.

    This contains the following parameters:
    - ID"""

    def __init__(self, **kwargs):
        self._document_id = None
        self._document_type = None
        self._user_id = None
        self._complete = None
        self._uploaded_file_path = None
        self._old_forenames = None
        self._old_surname = None
        self._new_forenames = None
        self._new_surname = None
        self._address = None
        self._change_of_name_date = None
        self._document_verified_state = VerifiedStates.NOT_VERIFIED
        self._document_verified_id = None
        self._added_datetime = None
        self._last_modified_datetime = None
        if len(kwargs) > 0:
            self.sort_kwargs_doc(**kwargs)

    def sort_kwargs_doc(self, **kwargs):
        for key, value in kwargs.items():
            if key == "document_id":
                self.document_id = value
            elif key == "user_id":
                self.user_id = value
            elif key == "complete":
                self.complete = value
            elif key == "uploaded_file_path":
                self.uploaded_file_path = value
            elif key == "old_forenames":
                self.old_forenames = value
            elif key == "old_surname":
                self.old_surname = value
            elif key == "new_forenames":
                self.new_forenames = value
            elif key == "new_surname":
                self.new_surname = value
            elif key == "address":
                self.address = value
            elif key == "change_of_name_date":
                self.change_of_name_date = value
            elif key == "document_verified_state":
                self.document_verified_state = value
            elif key == "document_verified_id":
                self.document_verified_id = value
            elif key == "added_datetime":
                self.added_datetime = value
            elif key == "last_modified_datetime":
                self.last_modified_datetime = value

    @property
    def document_id(self) -> int:
        return self._document_id

    @document_id.setter
    def document_id(self, document_id: int) -> None:
        try:
            id_to_use = int(document_id)
            self._document_id = id_to_use
        except ValueError:
            if document_id is None:
                self._document_id = None
            else:
                raise ValueError("Document ID provided ({0}) is not numeric or None".format(document_id))

    @property
    def document_type(self) -> str:
        return self._document_type

    @document_type.setter
    def document_type(self, document_type: str) -> None:
        self._document_type = document_type

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
                raise ValueError("User ID provided ({0}) is not numeric or None".format(user_id))

    @property
    def complete(self) -> int:
        return self._complete

    @complete.setter
    def complete(self, complete_val: bool) -> None:
        if complete_val not in (1, 0, False, True, None):
            raise ValueError("Complete value provided ({0}) is not boolean or None".format(complete_val))
        else:
            self._complete = complete_val

    @property
    def uploaded_file_path(self) -> str:
        return self._uploaded_file_path

    @uploaded_file_path.setter
    def uploaded_file_path(self, upload_path_val: str) -> None:
        self._uploaded_file_path = upload_path_val

    @property
    def old_forenames(self) -> str:
        return self._old_forenames

    @old_forenames.setter
    def old_forenames(self, name: str) -> None:
        self._old_forenames = name

    @property
    def old_surname(self) -> str:
        return self._old_surname

    @old_surname.setter
    def old_surname(self, name: str) -> None:
        self._old_surname = name

    @property
    def new_forenames(self) -> str:
        return self._new_forenames

    @new_forenames.setter
    def new_forenames(self, name: str) -> None:
        self._new_forenames = name

    @property
    def new_surname(self) -> str:
        return self._new_surname

    @new_surname.setter
    def new_surname(self, name: str) -> None:
        self._new_surname = name

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, address_val: Address) -> None:
        if isinstance(address_val, Address):
            self._address = address_val
        else:
            raise ValueError("Address provided is not in Address format.")

    @property
    def change_of_name_date(self) -> datetime.date:
        return self._change_of_name_date

    @change_of_name_date.setter
    def change_of_name_date(self, date_val: datetime.date) -> None:
        if isinstance(date_val, datetime.date):
            self._change_of_name_date = date_val
        else:
            raise ValueError("Added Datetime value provided ({0}) is not date or None".format(date_val))

    @property
    def change_of_name_date_as_string(self) -> str:
        return self._change_of_name_date.strftime("%d/%m/%Y")

    @property
    def document_verified_state(self) -> VerifiedStates:
        return self._document_verified_state

    @document_verified_state.setter
    def document_verified_state(self, document_verified_state_val: VerifiedStates) -> None:
        if isinstance(document_verified_state_val, VerifiedStates):
            self._document_verified_state = document_verified_state_val
        else:
            raise ValueError("Document Verified State value provided ({0}) is not a valid Verified State"
                             .format(document_verified_state_val))

    @property
    def document_verified_id(self) -> int:
        return self._document_verified_id

    @document_verified_id.setter
    def document_verified_id(self, document_verified_id_val: int) -> None:
        try:
            id_to_use = int(document_verified_id_val)
            self._document_verified_id = id_to_use
        except ValueError:
            if document_verified_id_val is None:
                self._document_verified_id = None
            else:
                raise ValueError("Document Verified ID provided ({0}) is not numeric or None"
                                 .format(document_verified_id_val))

    @property
    def added_datetime(self) -> datetime:
        return self._added_datetime

    @added_datetime.setter
    def added_datetime(self, date_val: datetime) -> None:
        if isinstance(date_val, datetime.datetime):
            self._added_datetime = date_val
        else:
            raise ValueError("Added Datetime value provided ({0}) is not date/time or None".format(date_val))

    @property
    def last_modified_datetime(self) -> datetime:
        return self._last_modified_datetime

    @last_modified_datetime.setter
    def last_modified_datetime(self, date_val: datetime) -> None:
        if isinstance(date_val, datetime.datetime):
            self._last_modified_datetime = date_val
        else:
            raise ValueError("Last Modified Datetime value provided ({0}) is not date/time or None".format(date_val))

    @property
    def doc_type_with_date(self) -> str:
        return self._document_type + " (" + self._change_of_name_date.strftime("%d/%m/%Y") + ")"
