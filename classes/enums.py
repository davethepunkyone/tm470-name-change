from enum import Enum


class VerifiedStates(Enum):
    NOT_VERIFIED = 0
    AWAITING_VERIFICATION = 1
    VERIFICATION_FAILED = 2
    VERIFIED = 9
