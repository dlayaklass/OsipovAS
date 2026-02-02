"""
Валидаторы (SRP - вынесли валидацию в отдельный класс)
"""


class EmployeeValidator:
    """Валидатор данных сотрудника"""

    @staticmethod
    def validate_name(name: str) -> list:
        errors = []
        if not name or len(name) < 2:
            errors.append("Имя должно содержать минимум 2 символа")
        return errors

    @staticmethod
    def validate_salary(salary: float) -> list:
        errors = []
        if salary < 0:
            errors.append("Зарплата не может быть отрицательной")
        return errors

    @staticmethod
    def validate_employee(emp_id: int, name: str, salary: float) -> list:
        errors = []
        if emp_id <= 0:
            errors.append("ID должен быть положительным")
        errors.extend(EmployeeValidator.validate_name(name))
        errors.extend(EmployeeValidator.validate_salary(salary))
        return errors


class DeveloperValidator:
    """Валидатор данных разработчика"""

    VALID_LEVELS = ['junior', 'middle', 'senior']

    @staticmethod
    def validate_level(level: str) -> list:
        errors = []
        if level not in DeveloperValidator.VALID_LEVELS:
            errors.append(f"Уровень должен быть: {', '.join(DeveloperValidator.VALID_LEVELS)}")
        return errors


class SalespersonValidator:
    """Валидатор данных продавца"""

    @staticmethod
    def validate_commission(rate: float) -> list:
        errors = []
        if rate < 0 or rate > 1:
            errors.append("Комиссия должна быть от 0 до 1")
        return errors
