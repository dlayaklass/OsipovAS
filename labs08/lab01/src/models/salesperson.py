"""Класс продавца"""

from .employee import Employee


class Salesperson(Employee):
    """Продавец с комиссией от продаж"""

    def __init__(self, employee_id: int, name: str, department: str,
                 base_salary: float, commission_rate: float = 0.1, sales: float = 0.0):
        super().__init__(employee_id, name, department, base_salary)
        self._commission_rate = commission_rate
        self._sales = sales

    @property
    def commission_rate(self) -> float:
        return self._commission_rate

    @property
    def sales(self) -> float:
        return self._sales

    def update_sales(self, amount: float):
        self._sales += amount

    def calculate_salary(self) -> float:
        commission = self._sales * self._commission_rate
        return self._base_salary + commission + self.calculate_bonus()

    def get_info(self) -> str:
        commission = self._sales * self._commission_rate
        return f"Продавец [id: {self._id}], комиссия: {commission}, итоговая зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["commission_rate"] = self._commission_rate
        data["sales"] = self._sales
        return data
