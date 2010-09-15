## Exception Master
class PCException(Exception):

    message = None

    def __init__(self, msg=None):
        self.message = msg


class InitException(PCException): pass
class InvalidConfig(InitException): pass
class ConfigRequired(InitException): pass

class APIException(PCException): pass
class APINotImplemented(APIException): pass
class APIInvalid(APIException): pass

class ControllerException(PCException): pass
class InvalidController(ControllerException): pass

class ExtensionException(PCException): pass
class ExtensionNotImplemented(ExtensionException): pass
class ExtensionInvalid(ExtensionException): pass