class DomainException(Exception):
    """Base exception for domain logic."""
    pass

class ResourceNotFoundException(DomainException):
    pass

class InvalidOperationException(DomainException):
    pass
