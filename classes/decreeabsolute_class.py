import datetime
from classes.document_class import Document
from classes.marriagecertificate_class import MarriageCertificate


class DecreeAbsolute(Document):
    """This is a class for the DecreeAbsolute object.

    This contains the following parameters:
    - ID"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.document_type = "Decree Absolute"
        self._marriage_certificate_details = None  # Use MarriageCertificate object
        self._issuing_court = None
        self._number_of_matter = None

    @property
    def marriage_certificate_details(self) -> MarriageCertificate:
        return self._marriage_certificate_details

    @marriage_certificate_details.setter
    def marriage_certificate_details(self, cert_val: MarriageCertificate) -> None:
        if isinstance(cert_val, MarriageCertificate):
            self._marriage_certificate_details = cert_val
        else:
            raise ValueError("Added Marriage Details are not in MarriageCertificate class format.")

    @property
    def issuing_court(self) -> str:
        return self._issuing_court

    @issuing_court.setter
    def issuing_court(self, issuer: str) -> None:
        self._issuing_court = issuer

    @property
    def number_of_matter(self) -> str:
        return self._number_of_matter

    @number_of_matter.setter
    def number_of_matter(self, no_matter: str) -> None:
        self._number_of_matter = no_matter
