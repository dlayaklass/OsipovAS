"""Класс отдела"""

from .abstract_employee import AbstractEmployee


class DuplicateIdError(Exception):
    """Ошибка дублирования ID сотрудника"""
    pass


class Department:
    """Отдел компании"""

    def __init__(self, name: str):
        self._name = name
        self._employees = []

    @property
    def name(self) -> str:
        return self._name

    def add_employee(self, employee: AbstractEmployee):
        for emp in self._employees:
            if emp.id == employee.id:
                raise DuplicateIdError(f"Сотрудник с ID {employee.id} уже существует")
        self._employees.append(employee)

    def remove_employee(self, emp_id: int):
        for i, emp in enumerate(self._employees):
            if emp.id == emp_id:
                return self._employees.pop(i)
        return None

    def get_employees(self) -> list:
        return self._employees.copy()

    def find_employee_by_id(self, emp_id: int):
        for emp in self._employees:
            if emp.id == emp_id:
                return emp
        return None

    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self._employees)

    def get_employee_count(self) -> dict:
        counts = {}
        for emp in self._employees:
            class_name = emp.__class__.__name__
            counts[class_name] = counts.get(class_name, 0) + 1
        return counts

    def __len__(self):
        return len(self._employees)

    def __getitem__(self, index):
        return self._employees[index]

    def __contains__(self, employee):
        return employee in self._employees

    def __iter__(self):
        return iter(self._employees)

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "employees": [emp.to_dict() for emp in self._employees]
        }
