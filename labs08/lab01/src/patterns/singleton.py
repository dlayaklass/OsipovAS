"""Паттерн Singleton"""


class DataStorage:
    """Singleton для хранения данных"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._employees = {}
            cls._instance._next_id = 1
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_employee(self, employee):
        self._employees[employee.id] = employee

    def get_employee(self, emp_id: int):
        return self._employees.get(emp_id)

    def get_all_employees(self):
        return list(self._employees.values())

    def remove_employee(self, emp_id: int):
        if emp_id in self._employees:
            return self._employees.pop(emp_id)
        return None

    def get_next_id(self):
        result = self._next_id
        self._next_id += 1
        return result

    def clear(self):
        self._employees.clear()
        self._next_id = 1

    @classmethod
    def reset_instance(cls):
        """Сброс инстанса для тестов"""
        cls._instance = None
