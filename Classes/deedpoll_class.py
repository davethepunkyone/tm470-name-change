from Classes.document_class import Document


class DeedPoll(Document):
    """This is a class for the DeedPoll object.

    This contains the following parameters:
    - ID"""

    def __init__(self):
        super().__init__()
        self._name_change_date = None
        self._registered_with_courts = None