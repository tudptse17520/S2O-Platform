class DomainException(Exception):
	"""Base exception for domain layer errors."""
	def __init__(self, message: str = "Domain error", status_code: int = 400):
		super().__init__(message)
		self.message = message
		self.status_code = status_code


class NotFoundException(DomainException):
	def __init__(self, message: str = "Resource not found"):
		super().__init__(message, status_code=404)


class ValidationException(DomainException):
	def __init__(self, message: str = "Validation failed"):
		super().__init__(message, status_code=422)


class DuplicateException(DomainException):
	def __init__(self, message: str = "Duplicate resource"):
		super().__init__(message, status_code=409)


class UnauthorizedException(DomainException):
	def __init__(self, message: str = "Unauthorized"):
		super().__init__(message, status_code=401)


class ConflictException(DomainException):
	def __init__(self, message: str = "Conflict"):
		super().__init__(message, status_code=409)

