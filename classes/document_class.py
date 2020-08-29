import json
import datetime
from classes.enums import VerifiedStates
from classes.address_class import Address


class Document:
    """This is a class for the handling of documents.

    The following keyword arguments can be passed in for this object:
    document_id (int), user_id (int), complete (bool), uploaded_file_path (str), old_forenames (str), old_surname (str),
    new_forenames (str), new_surname (str), address (Address), change_of_name_date (datetime.date),
    document_verified_state (VerifiedStates), document_verified_org (str), document_verified_comment (str),
    added_datetime (datetime.datetime), last_modified_datetime (datetime.datetime)."""

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
        self._document_verified_org = None
        self._document_verified_comment = None
        self._added_datetime = None
        self._last_modified_datetime = None
        if len(kwargs) > 0:
            self.sort_kwargs_doc(**kwargs)

    def sort_kwargs_doc(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
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
            elif key == "document_verified_org":
                self.document_verified_org = value
            elif key == "document_verified_comment":
                self.document_verified_comment = value
            elif key == "added_datetime":
                self.added_datetime = value
            elif key == "last_modified_datetime":
                self.last_modified_datetime = value

    @property
    def document_id(self) -> int:
        """Returns the document id for this document as an int."""
        return self._document_id

    @document_id.setter
    def document_id(self, document_id: int) -> None:
        """Sets the document id.

        Keyword arguments:
        document_id (int) -- The document id for this document. """
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
        """Returns the document type for this document as a str."""
        return self._document_type

    @document_type.setter
    def document_type(self, document_type: str) -> None:
        """Sets the document type.  This should only be set by classes that inherit properties from this class.

        Keyword arguments:
        document_type (str) -- The document type for this document. """
        self._document_type = document_type

    @property
    def user_id(self) -> int:
        """Returns the user id for this document as an int."""
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """Sets the user id.

        Keyword arguments:
        user_id (int) -- The user id for this document. """
        try:
            id_to_use = int(user_id)
            self._user_id = id_to_use
        except ValueError:
            if user_id is None:
                self._user_id = None
            else:
                raise ValueError("User ID provided ({0}) is not numeric or None".format(user_id))

    @property
    def complete(self) -> bool:
        """Returns the completed state for this document as a bool."""
        return self._complete

    @complete.setter
    def complete(self, complete_val: bool) -> None:
        """Sets the complete state.

        Keyword arguments:
        complete_val (bool) -- The complete state for this document. """
        if complete_val not in (1, 0, False, True, None):
            raise ValueError("Complete value provided ({0}) is not boolean or None".format(complete_val))
        else:
            self._complete = complete_val

    @property
    def uploaded_file_path(self) -> str:
        """Returns the uploaded file path for this document as a str."""
        return self._uploaded_file_path

    @uploaded_file_path.setter
    def uploaded_file_path(self, upload_path_val: str) -> None:
        """Sets the uploaded file path.  This is the stored filename given to the file, which should be found in the
        /app/static/uploads directory.

        Keyword arguments:
        upload_path_val (str) -- The uploaded file path for this document. """
        self._uploaded_file_path = upload_path_val

    @property
    def old_forenames(self) -> str:
        """Returns the old forenames for this document as a str."""
        return self._old_forenames

    @old_forenames.setter
    def old_forenames(self, name: str) -> None:
        """Sets the previous forenames.

        Keyword arguments:
        name (str) -- The previous forenames of the user for this document. """
        self._old_forenames = name

    @property
    def old_surname(self) -> str:
        """Returns the old surname for this document as a str."""
        return self._old_surname

    @old_surname.setter
    def old_surname(self, name: str) -> None:
        """Sets the previous surname.

        Keyword arguments:
        name (str) -- The previous surname of the user for this document. """
        self._old_surname = name

    @property
    def new_forenames(self) -> str:
        """Returns the new forenames for this document as a str."""
        return self._new_forenames

    @new_forenames.setter
    def new_forenames(self, name: str) -> None:
        """Sets the new forenames.

        Keyword arguments:
        name (str) -- The new forenames of the user for this document. """
        self._new_forenames = name

    @property
    def new_surname(self) -> str:
        """Returns the new surname for this document as a str."""
        return self._new_surname

    @new_surname.setter
    def new_surname(self, name: str) -> None:
        """Sets the new surname.

        Keyword arguments:
        name (str) -- The new surname of the user for this document. """
        self._new_surname = name

    @property
    def address(self) -> Address:
        """Returns the Address for this document as an Address object."""
        return self._address

    @address.setter
    def address(self, address_val: Address) -> None:
        """Sets the address for this document.

        Keyword arguments:
        address_val (Address) -- The address of the user for this document. """
        if isinstance(address_val, Address):
            self._address = address_val
        else:
            raise ValueError("Address provided is not in Address format.")

    @property
    def change_of_name_date(self) -> datetime.date:
        """Returns the change of name date for this document as a datetime.date object."""
        return self._change_of_name_date

    @change_of_name_date.setter
    def change_of_name_date(self, date_val: datetime.date) -> None:
        """Sets the change of name date for this document.

        Keyword arguments:
        date_val (datetime.date) -- The change of name date of the user for this document. """
        if isinstance(date_val, datetime.date):
            self._change_of_name_date = date_val
        else:
            raise ValueError("Added Datetime value provided ({0}) is not date or None".format(date_val))

    @property
    def change_of_name_date_as_string(self) -> str:
        """Returns the change of name date value as a str in the format dd/mm/yyyy.  The change of name date value must
        already be set or a LookupError will occur."""
        if self._change_of_name_date is not None:
            return self._change_of_name_date.strftime("%d/%m/%Y")
        else:
            raise LookupError("The change of name date has not been set.")

    @property
    def document_verified_state(self) -> VerifiedStates:
        """Returns the verified state for this document as a VerifiedStates object."""
        return self._document_verified_state

    @document_verified_state.setter
    def document_verified_state(self, document_verified_state_val: VerifiedStates) -> None:
        """Sets the verified state for this document.

        Keyword arguments:
        document_verified_state_val (VerifiedStates) -- The verified state of this document. """
        if isinstance(document_verified_state_val, VerifiedStates):
            self._document_verified_state = document_verified_state_val
        else:
            raise ValueError("Document Verified State value provided ({0}) is not a valid Verified State"
                             .format(document_verified_state_val))

    @property
    def document_verified_org(self) -> str:
        """Returns the verifying organisation for this document as a str."""
        return self._document_verified_org

    @document_verified_org.setter
    def document_verified_org(self, org: str) -> None:
        """Sets the verifying organisation for this document.

        Keyword arguments:
        org (str) -- The organisation verifying this document. """
        self._document_verified_org = org

    @property
    def document_verified_comment(self) -> str:
        """Returns the verifying comment for this document as a str."""
        return self._document_verified_comment

    @document_verified_comment.setter
    def document_verified_comment(self, comment: str) -> None:
        """Sets the verifying comment for this document.  This is only used when verification has failed to
        give a reason to the user as to why the verification failed.

        Keyword arguments:
        comment (str) -- The comment associated with verifying this document. """
        self._document_verified_comment = comment

    @property
    def added_datetime(self) -> datetime:
        """Returns the added datetime for this object as a datetime.datetime."""
        return self._added_datetime

    @added_datetime.setter
    def added_datetime(self, date_val: datetime) -> None:
        """Sets the added datetime.

        Keyword arguments:
        date_to_use (datetime.datetime) -- The added datetime for this object."""
        if isinstance(date_val, datetime.datetime):
            self._added_datetime = date_val
        else:
            raise ValueError("Added Datetime value provided ({0}) is not date/time or None".format(date_val))

    @property
    def last_modified_datetime(self) -> datetime:
        """Returns the last modified datetime for this object as a datetime.datetime."""
        return self._last_modified_datetime

    @last_modified_datetime.setter
    def last_modified_datetime(self, date_val: datetime) -> None:
        """Sets the last modified datetime.

        Keyword arguments:
        date_to_use (datetime.datetime) -- The last modified datetime for this object."""
        if isinstance(date_val, datetime.datetime):
            self._last_modified_datetime = date_val
        else:
            raise ValueError("Last Modified Datetime value provided ({0}) is not date/time or None".format(date_val))

    @property
    def doc_type_with_date(self) -> str:
        """This returns the document type with the change of name date formatted in dd/mm/yyyy as a string in the
        following format: Document Type (Change of Name Date)"""
        return self._document_type + " (" + self._change_of_name_date.strftime("%d/%m/%Y") + ")"
