"""Вспомогательные модули."""

from .exceptions import (
    EmployeeNotFoundError,
    DepartmentNotFoundError,
    ProjectNotFoundError,
    InvalidStatusError,
    DuplicateIdError
)

__all__ = [
    'EmployeeNotFoundError',
    'DepartmentNotFoundError',
    'ProjectNotFoundError',
    'InvalidStatusError',
    'DuplicateIdError'
]

