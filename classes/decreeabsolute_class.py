from classes.document_class import Document
from classes.marriagecertificate_class import MarriageCertificate


class DecreeAbsolute(Document):
    """This is a class for the handling of Decree Absolute documents.  This inherits the Document class properties
    and methods.

    The following keyword arguments can be passed in specifically for this object:
    marriage_certificate_details (MarriageCertificate), issuing_court (str), number_of_matter (str).

    In addition, passing in any keyword arguments accepted by the Document class will populate within this object."""

    def __init__(self, **kwargs):
        super().__init__()
        self.document_type = "Decree Absolute"
        self._marriage_certificate_details = None  # Use MarriageCertificate object
        self._issuing_court = None
        self._number_of_matter = None
        if len(kwargs) > 0:
            self.sort_kwargs_doc(**kwargs)  # Set Document class keywords first
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        """This sorts through all of the keywords and calls the appropriate function against the given keyword
        and value combination.  This method is only designed to be used with the class initializer."""
        for key, value in kwargs.items():
            if key == "marriage_certificate_details":
                self.marriage_certificate_details = value
            elif key == "issuing_court":
                self.issuing_court = value
            elif key == "number_of_matter":
                self.number_of_matter = value

    @property
    def marriage_certificate_details(self) -> MarriageCertificate:
        """Returns the associated marriage certificate for this object as a MarriageCertificate object."""
        return self._marriage_certificate_details

    @marriage_certificate_details.setter
    def marriage_certificate_details(self, cert_val: MarriageCertificate) -> None:
        """Sets the associated marriage certificate details.

        Keyword arguments:
        cert_val (MarriageCertificate) -- The associated marriage certificate for this object. """
        if isinstance(cert_val, MarriageCertificate):
            self._marriage_certificate_details = cert_val
        else:
            raise ValueError("Added Marriage Details are not in MarriageCertificate class format.")

    @property
    def issuing_court(self) -> str:
        """Returns the issuing court for this decree absolute as a str."""
        return self._issuing_court

    @issuing_court.setter
    def issuing_court(self, issuer: str) -> None:
        """Sets the issuing court.

        Keyword arguments:
        issuer (str) -- The issuing court for this decree absolute."""
        self._issuing_court = issuer

    @property
    def number_of_matter(self) -> str:
        """Returns the number of matter for this decree absolute as a str."""
        return self._number_of_matter

    @number_of_matter.setter
    def number_of_matter(self, no_matter: str) -> None:
        """Sets the number of matter.

        Keyword arguments:
        no_matter (str) -- The number of matter for this decree absolute."""
        self._number_of_matter = no_matter
