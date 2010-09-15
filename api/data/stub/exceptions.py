from ProvidenceClarity.api.data.exceptions import DataAPIException


class DataStubException(DataAPIException): pass

class InvalidDataBackend(DataStubException): pass
class InvalidDataSource(DataStubException): pass