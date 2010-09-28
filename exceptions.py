## Exception Master
class PCException(Exception):

    message = None

    def __init__(self, msg=None):
        self.message = msg