class PetoException(Exception):
    pass


class HouseholdNotFound(PetoException):
    pass


class PersonNotFound(PetoException):
    pass


class PersonalQuarantineStatusNotFound(PetoException):
    pass
