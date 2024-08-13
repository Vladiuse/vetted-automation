class VettedParseError(Exception):
    """Common parser exception"""


class NeedAuthentication(VettedParseError):
    """Throw when user not Authentication on vettedhealth.com"""


class EmptyCliniciansList(VettedParseError):
    """Throw when on clinicians page table with clinicians empty"""


class EmptyCovnoList(VettedParseError):
    """Throw when no active conversations found"""


class NoSuchRecruiterInForm(VettedParseError):
    """Throw when recruiter does not exist in select in transfer form"""


class ActionLimitError(VettedParseError):
    """Throw when limit on some action exceeded"""
