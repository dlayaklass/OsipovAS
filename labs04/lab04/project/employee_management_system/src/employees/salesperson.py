"""
Модуль для работы с классом Salesperson (Продавец).
Наследуется от Employee.
"""

from ..core.employee import Employee


class Salesperson(Employee):
    """
    Класс Salesperson представляет продавца компании.
    
    Наследуется от Employee и добавляет процент комиссии и объем продаж.
    Зарплата = базовая_зарплата + (объем_продаж * процент_комиссии).
    """
    
    def __init__(self, employee_id: int, name: str, department: str,
                 base_salary: float, commission_rate: float, sales_volume: float):
        """
        Конструктор класса Salesperson.
        
        Args:
            employee_id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата
            commission_rate: Процент комиссии (например, 0.1 для 10%)
            sales_volume: Объем продаж
        """
        super().__init__(employee_id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume
    
    @property
    def commission_rate(self) -> float:
        """Геттер для процента комиссии."""
        return self.__commission_rate
    
    @commission_rate.setter
    def commission_rate(self, value: float):
        """Сеттер для процента комиссии."""
        if not isinstance(value, (int, float)):
            raise ValueError("Процент комиссии должен быть числом")
        if value < 0 or value > 1:
            raise ValueError("Процент комиссии должен быть в диапазоне от 0 до 1")
        self.__commission_rate = float(value)
    
    @property
    def sales_volume(self) -> float:
        """Геттер для объема продаж."""
        return self.__sales_volume
    
    @sales_volume.setter
    def sales_volume(self, value: float):
        """Сеттер для объема продаж."""
        if not isinstance(value, (int, float)):
            raise ValueError("Объем продаж должен быть числом")
        if value < 0:
            raise ValueError("Объем продаж не может быть отрицательным")
        self.__sales_volume = float(value)
    
    def update_sales(self, new_sales: float) -> None:
        """Добавляет сумму к текущему объему продаж."""
        if not isinstance(new_sales, (int, float)):
            raise ValueError("Сумма продаж должна быть числом")
        if new_sales < 0:
            raise ValueError("Сумма продаж не может быть отрицательной")
        self.__sales_volume += new_sales
    
    def calculate_salary(self) -> float:
        """Рассчитывает итоговую заработную плату продавца."""
        return self.base_salary + (self.__sales_volume * self.__commission_rate)
    
    def get_info(self) -> str:
        """Возвращает полную информацию о продавце."""
        return (f"{super().__str__()}, процент комиссии: {self.__commission_rate * 100}%, "
                f"объем продаж: {self.__sales_volume}, итоговая зарплата: {self.calculate_salary()}")
    
    def to_dict(self) -> dict:
        """Преобразует объект продавца в словарь."""
        data = super().to_dict()
        data.update({
            "commission_rate": self.__commission_rate,
            "sales_volume": self.__sales_volume
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Salesperson':
        """Создает объект продавца из словаря."""
        return cls(
            data["id"],
            data["name"],
            data["department"],
            data["base_salary"],
            data.get("commission_rate", 0.0),
            data.get("sales_volume", 0.0)
        )

