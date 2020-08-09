import datetime
from classes.document_class import Document


class AccessCode:
    """This is a class for the AccessCode object.

    This contains the following parameters:
    - ID"""

    def __init__(self, **kwargs):
        self._code_id = None
        self._user_id = None
        self._uploaded_document = None
        self._generated_code = None
        self._expiry = None
        self._accessed_state = None
        self._added_datetime = None
        self._last_modified_datetime = None

    @property
    def code_id(self) -> int:
        return self._code_id

    @code_id.setter
    def code_id(self, code_id: int) -> None:
        self._code_id = code_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        self._user_id = user_id

    @property
    def uploaded_document(self) -> Document:
        return self._uploaded_document

    @uploaded_document.setter
    def uploaded_document(self, doc: Document) -> None:
        self._uploaded_document = doc

    @property
    def generated_code(self) -> int:
        return self._generated_code

    @generated_code.setter
    def generated_code(self, code_id: int) -> None:
        self._generated_code = code_id

    @property
    def expiry(self) -> datetime.datetime:
        return self._expiry

    @expiry.setter
    def expiry(self, expiry_date: datetime.datetime) -> None:
        self._expiry = expiry_date

    @property
    def expiry_to_string(self) -> str:
        return self._expiry.strftime("%d/%m/%Y %H:%M")

    @property
    def accessed_state(self) -> bool:
        return self._accessed_state

    @accessed_state.setter
    def accessed_state(self, access_state: bool) -> None:
        self._accessed_state = access_state

    @property
    def added_datetime(self) -> datetime.datetime:
        return self._added_datetime

    @added_datetime.setter
    def added_datetime(self, date_to_use: datetime.datetime) -> None:
        self._added_datetime = date_to_use

    @property
    def last_modified_datetime(self) -> datetime.datetime:
        return self._last_modified_datetime

    @last_modified_datetime.setter
    def last_modified_datetime(self, date_to_use: datetime.datetime) -> None:
        self._last_modified_datetime = date_to_use
