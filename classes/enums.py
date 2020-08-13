from enum import Enum


class VerifiedStates(Enum):
    NOT_VERIFIED = 0
    AWAITING_VERIFICATION = 1
    VERIFICATION_FAILED = 2
    VERIFIED = 9


class AccessStates(Enum):
    ACTIVE = 0
    FAILED_WRONG_ORG = 1
    FAILED_WRONG_USER_DETAILS = 2
    FAILED_TECHNICAL_ERROR = 3
    REVOKED = 7
    EXPIRED = 8
    RETRIEVED = 9
