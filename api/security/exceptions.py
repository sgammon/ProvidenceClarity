from ProvidenceClarity.main import PCException


class SecurityException(PCException): pass

## Access Exceptions
class AuthenticationError(SecurityException): pass
class AuthorizationError(SecurityException): pass

## Key Exceptions
class KeyException(SecurityException): pass
class KeyAccessLimitReached(KeyException): pass
class KeyNotActivated(KeyException): pass
class KeyNotFound(KeyException): pass
class KeyExpired(KeyException): pass

class KeyBanned(KeyException):
    
    reason = None
    
    def __init__(self, reason=None):
        
        self.reason = reason