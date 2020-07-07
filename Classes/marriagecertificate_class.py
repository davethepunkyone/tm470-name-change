from Classes.document_class import Document


class MarriageCertificate(Document):
    """This is a class for the MarriageCertificate object.

    This contains the following parameters:
    - ID"""

    def __init__(self):
        super().__init__()
        self._marriage_date = None
        self._age_on_certificate = None
        self._certificate_number = None
        self._registration_district = None
        self._marriage_number = None