from ProvidenceClarity.main import PCException


class DataAPIException(PCException): pass


class DataControllerException(DataAPIException): pass
class InvalidPolyInput(DataControllerException): pass