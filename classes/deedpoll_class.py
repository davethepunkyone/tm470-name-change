import datetime
from classes.document_class import Document


class DeedPoll(Document):
    """This is a class for the DeedPoll object.

    This contains the following parameters:
    - Name Change Date
    - Registered With Courts

    This class also inherits all properties from Document class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.document_type = "Deed Poll"
        self._registered_with_courts = None

    @property
    def registered_with_courts(self) -> bool:
        return self._registered_with_courts

    @registered_with_courts.setter
    def registered_with_courts(self, registered: bool) -> None:
        if registered not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(registered))
        else:
            self._registered_with_courts = registered
