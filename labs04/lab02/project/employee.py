"""
Модуль для работы с классом Employee (обычный сотрудник).
Наследуется от AbstractEmployee.
"""

from abstract_employee import AbstractEmployee


class Employee(AbstractEmployee):
    """
    Класс Employee представляет обычного сотрудника компании.
    
    Наследуется от AbstractEmployee и реализует абстрактные методы
    для расчета зарплаты и получения информации.
    """
    
    def __init__(self, employee_id: int, name: str, department: str, base_salary: float):
        """
        Конструктор класса Employee.
        
        Args:
            employee_id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата
        """
        super().__init__(employee_id, name, department, base_salary)
    
    def calculate_salary(self) -> float:
        """
        Рассчитывает итоговую заработную плату.
        
        Для обычного сотрудника итоговая зарплата равна базовой.
        
        Returns:
            Итоговая заработная плата (равна базовой)
        """
        return self.base_salary
    
    def get_info(self) -> str:
        """
        Возвращает полную информацию о сотруднике.
        
        Returns:
            Строка с полной информацией о сотруднике, включая рассчитанную зарплату
        """
        return f"{self.__str__()}, итоговая зарплата: {self.calculate_salary()}"

