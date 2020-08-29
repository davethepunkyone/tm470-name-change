class Address:
    """This is a class for the handling of addresses.

    The following keyword arguments can be passed in:
    house_name_no (str), line_1 (str), line_2 (str), town_city (str), postcode (str)."""

    def __init__(self, **kwargs):
        self._house_name_no = None
        self._line_1 = None
        self._line_2 = None
        self._town_city = None
        self._postcode = None
        if len(kwargs) > 0:
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
        for key, value in kwargs.items():
            if key == "house_name_no":
                self.house_name_no = value
            elif key == "line_1":
                self.line_1 = value
            elif key == "line_2":
                self.line_2 = value
            elif key == "town_city":
                self.town_city = value
            elif key == "postcode":
                self.postcode = value

    @property
    def house_name_no(self) -> str:
        """Returns the house name or number as a str."""
        return self._house_name_no

    @house_name_no.setter
    def house_name_no(self, add_str: str) -> None:
        """Sets the house name or number.

        Keyword arguments:
        add_str (str) -- The house name or number for this address. """
        self._house_name_no = add_str

    @property
    def line_1(self) -> str:
        """Returns line one of the address as a str."""
        return self._line_1

    @line_1.setter
    def line_1(self, add_str: str) -> None:
        """Sets address line one.

        Keyword arguments:
        add_str (str) -- The first line for this address. """
        self._line_1 = add_str

    @property
    def line_2(self) -> str:
        """Returns line two of the address as a str."""
        return self._line_2

    @line_2.setter
    def line_2(self, add_str: str) -> None:
        """Sets address line two.

        Keyword arguments:
        add_str (str) -- The second line for this address. """
        self._line_2 = add_str

    @property
    def town_city(self) -> str:
        """Returns the town or city of the address as a str."""
        return self._town_city

    @town_city.setter
    def town_city(self, add_str: str) -> None:
        """Sets the town or city.

        Keyword arguments:
        add_str (str) -- The town or city for this address. """
        self._town_city = add_str

    @property
    def postcode(self) -> str:
        """Returns the postcode of the address as a str."""
        return self._postcode

    @postcode.setter
    def postcode(self, add_str: str) -> None:
        """Sets the postcode.

        Keyword arguments:
        add_str (str) -- The postcode for this address. """
        self._postcode = add_str
