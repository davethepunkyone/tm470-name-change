from classes.document_class import Document


class DeedPoll(Document):
    """This is a class for the handling of Deed Poll documents.  This inherits the Document class properties
    and methods.

    The following keyword arguments can be passed in specifically for this object:
    registered_with_courts (bool).

    In addition, passing in any keyword arguments accepted by the Document class will populate within this object."""

    def __init__(self, **kwargs):
        super().__init__()
        self.document_type = "Deed Poll"
        self._registered_with_courts = None
        if len(kwargs) > 0:
            self.sort_kwargs_doc(**kwargs)
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
        for key, value in kwargs.items():
            if key == "registered_with_courts":
                self.registered_with_courts = value

    @property
    def registered_with_courts(self) -> bool:
        """Returns if this has been registered with the courts as a bool."""
        return self._registered_with_courts

    @registered_with_courts.setter
    def registered_with_courts(self, registered: bool) -> None:
        """Sets the registered with courts value.

        Keyword arguments:
        registered (bool) -- Has this been registered with the courts? """
        if registered not in (1, 0, False, True, None):
            raise ValueError("Verified State provided ({0}) is not boolean or None".format(registered))
        else:
            self._registered_with_courts = registered
