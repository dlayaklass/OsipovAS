"""
Модуль для работы с классом Manager (Менеджер).
Наследуется от Employee.
"""

from ..core.employee import Employee


class Manager(Employee):
    """
    Класс Manager представляет менеджера компании.
    
    Наследуется от Employee и добавляет бонус к базовой зарплате.
    """
    
    def __init__(self, employee_id: int, name: str, department: str, 
                 base_salary: float, bonus: float):
        """
        Конструктор класса Manager.
        
        Args:
            employee_id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата
            bonus: Бонус менеджера
        """
        super().__init__(employee_id, name, department, base_salary)
        self.bonus = bonus
    
    @property
    def bonus(self) -> float:
        """Геттер для бонуса менеджера."""
        return self.__bonus
    
    @bonus.setter
    def bonus(self, value: float):
        """
        Сеттер для бонуса менеджера.
        
        Args:
            value: Размер бонуса
        
        Raises:
            ValueError: Если бонус не является неотрицательным числом
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Бонус должен быть числом")
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self.__bonus = float(value)
    
    def calculate_salary(self) -> float:
        """
        Рассчитывает итоговую заработную плату менеджера.
        
        Формула: базовая_зарплата + бонус
        
        Returns:
            Итоговая заработная плата менеджера
        """
        return self.base_salary + self.__bonus
    
    def get_info(self) -> str:
        """
        Возвращает полную информацию о менеджере.
        
        Returns:
            Строка с полной информацией о менеджере, включая бонус
        """
        return (f"{super().__str__()}, бонус: {self.__bonus}, "
                f"итоговая зарплата: {self.calculate_salary()}")
    
    def to_dict(self) -> dict:
        """Преобразует объект менеджера в словарь."""
        data = super().to_dict()
        data["bonus"] = self.__bonus
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Manager':
        """Создает объект менеджера из словаря."""
        return cls(
            data["id"],
            data["name"],
            data["department"],
            data["base_salary"],
            data.get("bonus", 0.0)
        )

