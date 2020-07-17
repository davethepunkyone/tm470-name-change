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
        self._name_change_date = None
        self._registered_with_courts = None

    @property
    def name_change_date(self) -> datetime.date:
        return self._name_change_date

    @name_change_date.setter
    def name_change_date(self, date_val: datetime.date) -> None:
        if isinstance(date_val, datetime.date):
            self._name_change_date = date_val
        else:
            raise ValueError("Added Datetime value provided ({0}) is not date or None".format(date_val))

    @property
    def registered_with_courts(self) -> bool:
        return self._registered_with_courts

    @registered_with_courts.setter
    def registered_with_courts(self, registered: bool) -> None:
        if registered not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(registered))
        else:
            self._registered_with_courts = registered
