from classes.document_class import Document
from globals.global_variables import minimum_age_marriage, maximum_age_marriage


class MarriageCertificate(Document):
    """This is a class for the MarriageCertificate object.

    This contains the following parameters:
    - Marriage Date
    - Age on Certificate
    - Certificate Number
    - Registration District
    - Marriage Number

    This class also inherits all properties from Document class."""

    def __init__(self, **kwargs):
        super().__init__()
        self.document_type = "Marriage Certificate"
        self._age_on_certificate = None
        self._certificate_number = None
        self._registration_district = None
        self._marriage_number = None
        if len(kwargs) > 0:
            self.sort_kwargs_doc(**kwargs)
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key == "age_on_certificate":
                self.age_on_certificate = value
            elif key == "certificate_number":
                self.certificate_number = value
            elif key == "registration_district":
                self.registration_district = value
            elif key == "marriage_number":
                self.marriage_number = value

    @property
    def age_on_certificate(self) -> int:
        return self._age_on_certificate

    @age_on_certificate.setter
    def age_on_certificate(self, age: int) -> None:
        try:
            age_to_use = int(age)
            if age <= minimum_age_marriage:
                raise AttributeError("The age provided ({0}) is too young (minimum = {1})."
                                     .format(age_to_use, minimum_age_marriage))
            elif age >= maximum_age_marriage:
                raise AttributeError("The age provided ({0}) is too old (maximum = {1})."
                                     .format(age_to_use, maximum_age_marriage))
            else:
                self._age_on_certificate = age_to_use
        except ValueError:
            if age is None:
                self._age_on_certificate = None
            else:
                raise ValueError("Document Verified ID provided ({0}) is not numeric or None".format(age))

    @property
    def certificate_number(self) -> str:
        return self._certificate_number

    @certificate_number.setter
    def certificate_number(self, cert: str) -> None:
        self._certificate_number = cert

    @property
    def registration_district(self) -> str:
        return self._registration_district

    @registration_district.setter
    def registration_district(self, district: str) -> None:
        self._registration_district = district

    @property
    def marriage_number(self) -> int:
        return self._marriage_number

    @marriage_number.setter
    def marriage_number(self, marriage_no: int) -> None:
        try:
            marriage_no_to_use = int(marriage_no)
            if marriage_no <= 0:
                raise AttributeError("The marriage number provided ({0}) is too low (minimum = 1).".format(
                    marriage_no_to_use))
            else:
                self._marriage_number = marriage_no_to_use
        except ValueError:
            if marriage_no is None:
                self._marriage_number = None
            else:
                raise ValueError("Document Verified ID provided ({0}) is not numeric or None".format(marriage_no))
