
class Organisation:
    """This is a class for the handling of Organisations.

    The following keyword arguments can be passed in for this object:
    org_id (int), org_name (str), requires_verified (bool), avg_time_to_process_days (int)."""

    def __init__(self, **kwargs):
        self._org_id = None
        self._org_name = None
        self._requires_verified = None
        self._avg_time_to_process_days = None
        if len(kwargs) > 0:
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
        for key, value in kwargs.items():
            if key == "org_id":
                self.org_id = value
            elif key == "org_name":
                self.org_name = value
            elif key == "requires_verified":
                self.requires_verified = value
            elif key == "avg_time_to_process_days":
                self.avg_time_to_process_days = value
            else:
                raise KeyError("Keyword ({}) provided is not a valid property".format(key))

    @property
    def org_id(self) -> int:
        """Returns the organisation id for this organisation as an int."""
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: int) -> None:
        """Sets the organisation id.

        Keyword arguments:
        org_id (int) -- The organisation id for this organisation. """
        self._org_id = org_id

    @property
    def org_name(self) -> str:
        """Returns the organisation name for this organisation as a str."""
        return self._org_name

    @org_name.setter
    def org_name(self, org_name_to_use: str) -> None:
        """Sets the organisation name.

        Keyword arguments:
        org_name_to_use (str) -- The organisation name for this organisation. """
        self._org_name = org_name_to_use

    @property
    def requires_verified(self) -> bool:
        """Returns the organisation requires verification state for this organisation as a bool."""
        return self._requires_verified

    @requires_verified.setter
    def requires_verified(self, req_ver: bool) -> None:
        """Sets the organisation requires verification state.

        Keyword arguments:
        req_ver (bool) -- The requires verification state for this organisation. """
        self._requires_verified = req_ver

    @property
    def avg_time_to_process_days(self) -> int:
        """Returns the average time to process in days for this organisation as an int."""
        return self._avg_time_to_process_days

    @avg_time_to_process_days.setter
    def avg_time_to_process_days(self, process_time: int) -> None:
        """Sets the average time to process in days.

        Keyword arguments:
        process_time (int) -- The average time to process in days for this organisation. """
        self._avg_time_to_process_days = process_time
