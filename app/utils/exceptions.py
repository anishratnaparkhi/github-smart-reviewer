class AppError(Exception):
    """Base class for expected application errors."""

class RepositoryScanError(AppError):
    pass

class DocumentBuildError(AppError):
    pass

class VectorStoreError(AppError):
    pass

class ReviewGenerationError(AppError):
    pass

