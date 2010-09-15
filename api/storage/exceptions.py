from ProvidenceClarity.exceptions import PCException


class StorageException(PCException): pass

class InvalidBackend(StorageException): pass