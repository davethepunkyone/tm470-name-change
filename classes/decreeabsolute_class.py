from classes.document_class import Document


class DecreeAbsolute(Document):
    """This is a class for the DecreeAbsolute object.

    This contains the following parameters:
    - ID"""

    def __init__(self):
        super().__init__()
        self._marriage_certificate_details = None  # Use MarriageCertificate object
        self._decree_absolute_date = None
        self._issuing_court = None
        self._number_of_matter = None
