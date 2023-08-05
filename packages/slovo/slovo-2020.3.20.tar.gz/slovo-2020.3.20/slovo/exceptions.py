class SlovoException(BaseException):
    """ General Exception. """


class SameLangsError(SlovoException):
    """ Same languages in this operation not permitted. """


class DiffLangsError(SlovoException):
    """ Different languages in this operation not permitted. """


class ImmutableClassError(SlovoException):
    """ Different languages in this operation not permitted. """
