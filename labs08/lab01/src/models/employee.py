"""Класс обычного сотрудника"""

from .abstract_employee import AbstractEmployee


class Employee(AbstractEmployee):
    """Обычный сотрудник"""

    def __init__(self, employee_id: int, name: str, department: str, base_salary: float):
        super().__init__(employee_id, name, department, base_salary)
        self._bonus_strategy = None

    def set_bonus_strategy(self, strategy):
        self._bonus_strategy = strategy

    def calculate_bonus(self) -> float:
        if self._bonus_strategy:
            return self._bonus_strategy.calculate(self)
        return 0.0

    def calculate_salary(self) -> float:
        return self._base_salary + self.calculate_bonus()

    def get_info(self) -> str:
        bonus = self.calculate_bonus()
        info = f"Сотрудник {self}, итоговая зарплата: {self.calculate_salary()}"
        if bonus > 0:
            info += f" (бонус: {bonus})"
        return info

    def __str__(self) -> str:
        return f"Сотрудник [id: {self._id}, имя: {self._name}, отдел: {self._department}, базовая зарплата: {self._base_salary}]"
