from enum import Enum


class VerifiedStates(Enum):
    """These states are used to identify the current state of a Document object."""
    NOT_VERIFIED = 0  # No verification has taken place
    AWAITING_VERIFICATION = 1  # Verification is underway
    VERIFICATION_FAILED = 2  # Verification failed
    NOT_APPLICABLE = 8  # No verification possible
    VERIFIED = 9  # Document is verified


class AccessStates(Enum):
    """These states are used to identify the current access state of an AccessCode object."""
    ACTIVE = 0  # The access code is active
    FAILED_WRONG_ORG = 1  # The access code has deactivated as the wrong org tried to access it
    FAILED_WRONG_USER_DETAILS = 2  # The access code has deactivated as the wrong user details were provided
    FAILED_TECHNICAL_ERROR = 3  # The access code has deactivated due to a technical error
    DOCUMENT_NO_LONGER_AVAILABLE = 6  # The document associated with the access code is no longer available
    REVOKED = 7  # The access code has been revoked by the user
    EXPIRED = 8  # The access code has expired due to lack of access
    RETRIEVED = 9  # The access code has been accessed successfully
