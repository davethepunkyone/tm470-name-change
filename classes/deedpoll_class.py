from classes.document_class import Document


class DeedPoll(Document):
    """This is a class for the DeedPoll object.

    This contains the following parameters:
    - Name Change Date
    - Registered With Courts

    This class also inherits all properties from Document class."""

    def __init__(self, **kwargs):
        super().__init__()
        self.document_type = "Deed Poll"
        self._registered_with_courts = None
        if len(kwargs) > 0:
            self.sort_kwargs_doc(**kwargs)
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key == "registered_with_courts":
                self.registered_with_courts = value

    @property
    def registered_with_courts(self) -> bool:
        return self._registered_with_courts

    @registered_with_courts.setter
    def registered_with_courts(self, registered: bool) -> None:
        if registered not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(registered))
        else:
            self._registered_with_courts = registered
