"""Класс менеджера"""

from .employee import Employee


class Manager(Employee):
    """Менеджер с бонусом"""

    def __init__(self, employee_id: int, name: str, department: str,
                 base_salary: float, bonus: float = 0.0):
        super().__init__(employee_id, name, department, base_salary)
        self._bonus = bonus

    @property
    def bonus(self) -> float:
        return self._bonus

    @bonus.setter
    def bonus(self, value: float):
        self._bonus = float(value)

    def calculate_salary(self) -> float:
        return self._base_salary + self._bonus + self.calculate_bonus()

    def get_info(self) -> str:
        return f"Менеджер {self}, бонус: {self._bonus}, итого: {self.calculate_salary()}"
