import datetime
from classes.document_class import Document
from classes.organisation_class import Organisation
from classes.enums import AccessStates


class AccessCode:
    """This is a class for the handling of Access Codes.

    The following keyword arguments can be passed in:
    code_id (int), user_id (int), uploaded_document (Document), generated_code (str), duration_time (int),
    duration_denominator (str), expiry (datetime.datetime), accessed_state (AccessStates), access_for_org (str),
    added_datetime (datetime.datetime), last_modified_datetime (datetime.datetime)."""

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
        if len(kwargs) > 0:
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
        for key, value in kwargs.items():
            if key == "code_id":
                self.code_id = value
            elif key == "user_id":
                self.user_id = value
            elif key == "uploaded_document":
                self.uploaded_document = value
            elif key == "generated_code":
                self.generated_code = value
            elif key == "duration_time":
                self.duration_time = value
            elif key == "duration_denominator":
                self.duration_denominator = value
            elif key == "expiry":
                self.expiry = value
            elif key == "accessed_state":
                self.accessed_state = value
            elif key == "access_for_org":
                self.access_for_org = value
            elif key == "added_datetime":
                self.added_datetime = value
            elif key == "last_modified_datetime":
                self.last_modified_datetime = value

    @property
    def code_id(self) -> int:
        """Returns the code id for this access code as an int."""
        return self._code_id

    @code_id.setter
    def code_id(self, code_id: int) -> None:
        """Sets the code id.

        Keyword arguments:
        code_id (int) -- The code id for this access code. """
        self._code_id = code_id

    @property
    def user_id(self) -> int:
        """Returns the user id for this access code as an int."""
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """Sets the code id.

        Keyword arguments:
        user_id (int) -- The user id for this access code. """
        self._user_id = user_id

    @property
    def uploaded_document(self) -> Document:
        """Returns the uploaded document for this access code as a Document object."""
        return self._uploaded_document

    @uploaded_document.setter
    def uploaded_document(self, doc: Document) -> None:
        """Sets the uploaded document.

        Keyword arguments:
        doc (Document) -- The uploaded document for this access code. """
        self._uploaded_document = doc

    @property
    def generated_code(self) -> str:
        """Returns the generated code for this access code as a str."""
        return self._generated_code

    @generated_code.setter
    def generated_code(self, code_id: str) -> None:
        """Sets the generated code.

        Keyword arguments:
        code_id (str) -- The generated code for this access code. """
        self._generated_code = code_id

    @property
    def duration_time(self) -> int:
        """Returns the duration time for this access code as an int."""
        return self._duration_time

    @duration_time.setter
    def duration_time(self, dur_time: int) -> None:
        """Sets the duration time.  This is generally used when creating or modifying an access code to
        assist in generating the expiry time.

        Keyword arguments:
        dur_time (int) -- The duration time for this access code. """
        self._duration_time = dur_time

    @property
    def duration_denominator(self) -> str:
        """Returns the duration denominator for this access code as a str."""
        return self._duration_denominator

    @duration_denominator.setter
    def duration_denominator(self, dur_den: str) -> None:
        """Sets the duration denominator.  This is generally used when creating or modifying an access code to
        assist in generating the expiry time.

        Keyword arguments:
        dur_den (str) -- The duration denominator for this access code. Acceptable values: hours, days."""
        if dur_den in ("hours", "days"):
            self._duration_denominator = dur_den
        else:
            raise ValueError("The denominator provided ({}) is not valid".format(dur_den))

    def generate_expiry_from_duration(self) -> None:
        """Sets the expiry value based on the duration time and duration denominator.  These values must already
        be set for the class object or a LookupError will occur.

        If an expiry time isn't already set, the expiry time is based on the current datetime.  If an
        expiry time has been set, it will add the specified time onto the existing expiry time."""
        if self._duration_time is not None and self._duration_denominator is not None:
            if self.expiry is None:
                current_time = datetime.datetime.now()
            else:
                current_time = self.expiry
            if self._duration_denominator == "hours":
                self.expiry = current_time + datetime.timedelta(hours=self._duration_time)
            elif self._duration_denominator == "days":
                self.expiry = current_time + datetime.timedelta(days=self._duration_time)
        else:
            raise LookupError("The duration time and denominator are not set.")

    @property
    def expiry(self) -> datetime.datetime:
        """Returns the expiry datetime for this access code as a datetime.datetime."""
        return self._expiry

    @expiry.setter
    def expiry(self, expiry_date: datetime.datetime) -> None:
        """Sets the expiry datetime.

        Keyword arguments:
        expiry_date (datetime.datetime) -- The expiry datetime for this access code."""
        self._expiry = expiry_date

    @property
    def expiry_to_string(self) -> str:
        """Returns the expiry datetime value as a str in the format dd/mm/yyyy hh:mm.  The expiry value must
        already be set or a LookupError will occur."""
        if self._expiry is not None:
            return self._expiry.strftime("%d/%m/%Y %H:%M")
        else:
            raise LookupError("The expiry datetime has not been set.")

    @property
    def accessed_state(self) -> AccessStates:
        """Returns the accessed state for this access code as a AccessStates object."""
        return self._accessed_state

    @accessed_state.setter
    def accessed_state(self, access_state: AccessStates) -> None:
        """Sets the accessed state.

        Keyword arguments:
        access_state (AccessStates) -- The current access state for this access code. """
        if isinstance(access_state, AccessStates):
            self._accessed_state = access_state
        else:
            raise ValueError("Access State value provided is not a valid AccessState")

    @property
    def access_for_org(self) -> Organisation:
        """Returns the access for org for this access code as an Organisation object."""
        return self._access_for_org

    @access_for_org.setter
    def access_for_org(self, org: Organisation) -> None:
        """Sets the access for org.

        Keyword arguments:
        org (Organisation) -- The current access state for this access code. """
        if isinstance(org, Organisation):
            self._access_for_org = org
        else:
            raise ValueError("Organisation value provided is not a valid Organisation")

    @property
    def added_datetime(self) -> datetime.datetime:
        """Returns the added datetime for this access code as a datetime.datetime."""
        return self._added_datetime

    @added_datetime.setter
    def added_datetime(self, date_to_use: datetime.datetime) -> None:
        """Sets the added datetime.

        Keyword arguments:
        date_to_use (datetime.datetime) -- The added datetime for this access code."""
        self._added_datetime = date_to_use

    @property
    def last_modified_datetime(self) -> datetime.datetime:
        """Returns the last modified datetime for this access code as a datetime.datetime."""
        return self._last_modified_datetime

    @last_modified_datetime.setter
    def last_modified_datetime(self, date_to_use: datetime.datetime) -> None:
        """Sets the last modified datetime.

        Keyword arguments:
        date_to_use (datetime.datetime) -- The last modified datetime for this access code."""
        self._last_modified_datetime = date_to_use
