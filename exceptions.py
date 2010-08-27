from ProvidenceClarity.main import PCException


class InitException(PCException): pass
class InvalidConfig(InitException): pass
class ConfigRequired(InitException): pass