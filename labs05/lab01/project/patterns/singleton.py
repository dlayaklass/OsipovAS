"""
Паттерн Singleton - единственное хранилище данных
"""


class DataStorage:
    """
    Singleton для хранения данных о сотрудниках.
    Гарантирует единственный экземпляр хранилища.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._employees = {}
            cls._instance._next_id = 1
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Получить экземпляр хранилища"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_employee(self, employee):
        """Добавить сотрудника"""
        self._employees[employee.id] = employee
        print(f"[Storage] Добавлен: {employee.name}")

    def get_employee(self, emp_id: int):
        """Получить сотрудника по ID"""
        return self._employees.get(emp_id)

    def get_all_employees(self):
        """Получить всех сотрудников"""
        return list(self._employees.values())

    def remove_employee(self, emp_id: int):
        """Удалить сотрудника"""
        if emp_id in self._employees:
            emp = self._employees.pop(emp_id)
            print(f"[Storage] Удален: {emp.name}")
            return emp
        return None

    def get_next_id(self):
        """Получить следующий свободный ID"""
        result = self._next_id
        self._next_id += 1
        return result

    def clear(self):
        """Очистить хранилище"""
        self._employees.clear()
        self._next_id = 1
