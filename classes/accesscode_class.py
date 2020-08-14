import datetime
from classes.document_class import Document
from classes.organisation_class import Organisation
from classes.enums import AccessStates


class AccessCode:
    """This is a class for the AccessCode object.

    This contains the following parameters:
    - ID"""

    def __init__(self, **kwargs):
        self._code_id = None
        self._user_id = None
        self._uploaded_document = None
        self._generated_code = None
        self._duration_time = None
        self._duration_denominator = None
        self._expiry = None
        self._accessed_state = None
        self._access_for_org = None
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
    def duration_time(self) -> int:
        return self._duration_time

    @duration_time.setter
    def duration_time(self, dur_time: int) -> None:
        self._duration_time = dur_time

    @property
    def duration_denominator(self) -> int:
        return self._duration_denominator

    @duration_denominator.setter
    def duration_denominator(self, dur_den: str) -> None:
        if dur_den in ("hours", "days"):
            self._duration_denominator = dur_den
        else:
            raise ValueError("The denominator provided ({}) is not valid".format(dur_den))

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
    def accessed_state(self) -> AccessStates:
        return self._accessed_state

    @accessed_state.setter
    def accessed_state(self, access_state: AccessStates) -> None:
        if isinstance(access_state, AccessStates):
            self._accessed_state = access_state
        else:
            raise ValueError("Access State value provided is not a valid AccessState")

    @property
    def access_for_org(self) -> str:
        return self._access_for_org

    @access_for_org.setter
    def access_for_org(self, org: Organisation) -> None:
        if isinstance(org, Organisation):
            self._access_for_org = org
        else:
            raise ValueError("Organisation value provided is not a valid Organisation")

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
