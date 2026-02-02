"""
Репозитории (DIP - инверсия зависимостей)
"""

from interfaces import IEmployeeRepository


class InMemoryEmployeeRepository(IEmployeeRepository):
    """Репозиторий в памяти"""

    def __init__(self):
        self._employees = {}

    def save(self, employee):
        self._employees[employee.id] = employee

    def find_by_id(self, emp_id: int):
        return self._employees.get(emp_id)

    def get_all(self) -> list:
        return list(self._employees.values())

    def delete(self, emp_id: int):
        if emp_id in self._employees:
            del self._employees[emp_id]


class FileEmployeeRepository(IEmployeeRepository):
    """Репозиторий с сохранением в файл"""

    def __init__(self, filename: str):
        self._filename = filename
        self._employees = {}

    def save(self, employee):
        self._employees[employee.id] = employee
        self._save_to_file()

    def find_by_id(self, emp_id: int):
        return self._employees.get(emp_id)

    def get_all(self) -> list:
        return list(self._employees.values())

    def _save_to_file(self):
        from serializers import JsonSerializer
        data = [emp.to_dict() for emp in self._employees.values()]
        JsonSerializer.save({'employees': data}, self._filename)
