# exceptions.py

class CafeteriaError(Exception):
    """Base class for all custom exceptions in the Cafeteria Management System"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

# exceptions.py

class InvalidInputError(CafeteriaError):
    """Exception raised for invalid input."""
    def __init__(self, message="Invalid input provided"):
        super().__init__(message)

class MenuItemError(CafeteriaError):
    """Exception raised for errors related to menu items."""
    def __init__(self, message="Menu item error"):
        super().__init__(message)

class RecommendationError(CafeteriaError):
    """Exception raised for errors related to recommendations."""
    def __init__(self, message="Recommendation error"):
        super().__init__(message)

class FeedbackError(CafeteriaError):
    """Exception raised for errors related to feedback."""
    def __init__(self, message="Feedback error"):
        super().__init__(message)
