"""
Класс отдела (после рефакторинга)
"""


class Department:
    """Класс отдела - только управление сотрудниками"""

    def __init__(self, name: str):
        self._name = name
        self._employees = []

    @property
    def name(self) -> str:
        return self._name

    def add_employee(self, employee):
        if employee not in self._employees:
            self._employees.append(employee)

    def remove_employee(self, emp_id: int):
        self._employees = [e for e in self._employees if e.id != emp_id]

    def get_employees(self) -> list:
        return self._employees.copy()

    def find_by_id(self, emp_id: int):
        for emp in self._employees:
            if emp.id == emp_id:
                return emp
        return None

    def __len__(self) -> int:
        return len(self._employees)

    def __iter__(self):
        return iter(self._employees)

    def __str__(self) -> str:
        return f"Отдел '{self._name}' ({len(self._employees)} сотр.)"
