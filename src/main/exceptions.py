
class NeedAuthentication(Exception):
    """Throw when user not Authentication on vettedhealth.com"""


class EmptyCliniciansList(Exception):
    """Throw when on clinicians page table with clinicians empty"""


class EmptyCovnoList(Exception):
    """Throw when no active conversations found"""


class NoSuchRecruiterInForm(Exception):
    """Throw when recruiter does not exist in select in transfer form"""