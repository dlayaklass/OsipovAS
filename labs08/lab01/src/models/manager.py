"""Класс менеджера"""

from .employee import Employee


class Manager(Employee):
    """Менеджер с бонусом"""

    def __init__(self, employee_id: int, name: str, department: str,
                 base_salary: float, bonus: float = 0.0):
        super().__init__(employee_id, name, department, base_salary)
        self.bonus = bonus

    @property
    def bonus(self) -> float:
        return self._bonus

    @bonus.setter
    def bonus(self, value: float):
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self._bonus = float(value)

    def calculate_salary(self) -> float:
        return self._base_salary + self._bonus + self.calculate_bonus()

    def get_info(self) -> str:
        return f"Менеджер [id: {self._id}], бонус: {self._bonus}, итоговая зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["bonus"] = self._bonus
        return data
