from uuid import UUID


class AppException(Exception):
    """Base class for application exceptions"""
    pass


class NoEmployeeInstance(AppException):
    """Raised when a user has no employee instance."""

    def __init__(self, user_id: UUID):
        self.message = f"User {user_id} has no employee instance."
        super().__init__(self.message)
