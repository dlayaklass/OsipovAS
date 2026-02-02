"""
Модуль с кастомными исключениями для системы учета сотрудников.
"""


class EmployeeNotFoundError(Exception):
    """Исключение, возникающее при отсутствии сотрудника."""
    pass


class DepartmentNotFoundError(Exception):
    """Исключение, возникающее при отсутствии отдела."""
    pass


class ProjectNotFoundError(Exception):
    """Исключение, возникающее при отсутствии проекта."""
    pass


class InvalidStatusError(Exception):
    """Исключение, возникающее при невалидном статусе."""
    pass


class DuplicateIdError(Exception):
    """Исключение, возникающее при дублировании ID."""
    pass

