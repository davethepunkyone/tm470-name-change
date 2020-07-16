

class AccessCode:
    """This is a class for the AccessCode object.

    This contains the following parameters:
    - ID"""

    def __init__(self, **kwargs):
        self._id = None
        self._user_id = None
        self._uploaded_document_id = None
        self._expiry = None
        self._accessed_state = None
        self._added_datetime = None
        self._last_modified_datetime = None
