from ProvidenceClarity.exceptions import PCException


class ReceiverException(PCException): pass

class ReceiverNotFound(ReceiverException): pass
class ReceiverDisabled(ReceiverException): pass
class ReceiverPayloadMissing(ReceiverException): pass

class InvalidDataHandler(ReceiverException): pass