class Address:
    """This is a class for the Address object.

    This contains the following parameters:
    - ID"""

    def __init__(self, **kwargs):
        self._house_name_no = None
        self._line_1 = None
        self._line_2 = None
        self._town_city = None
        self._postcode = None
        if len(kwargs) > 0:
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
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
        return self._house_name_no

    @house_name_no.setter
    def house_name_no(self, add_str: str) -> None:
        self._house_name_no = add_str

    @property
    def line_1(self) -> str:
        return self._line_1

    @line_1.setter
    def line_1(self, add_str: str) -> None:
        self._line_1 = add_str

    @property
    def line_2(self) -> str:
        return self._line_2

    @line_2.setter
    def line_2(self, add_str: str) -> None:
        self._line_2 = add_str

    @property
    def town_city(self) -> str:
        return self._town_city

    @town_city.setter
    def town_city(self, add_str: str) -> None:
        self._town_city = add_str

    @property
    def postcode(self) -> str:
        return self._postcode

    @postcode.setter
    def postcode(self, add_str: str) -> None:
        self._postcode = add_str
