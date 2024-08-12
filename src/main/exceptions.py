
class NeedAuthentication(Exception):
    """Throw when user not Authentication on vettedhealth.com"""


class EmptyCliniciansList(Exception):
    """Throw when on clinicians page table with clinicians empty"""