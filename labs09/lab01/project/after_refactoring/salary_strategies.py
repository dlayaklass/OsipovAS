"""
Стратегии расчета зарплаты (OCP - принцип открытости/закрытости)
Паттерн Strategy позволяет добавлять новые способы расчета без изменения кода
"""

from abc import ABC, abstractmethod


class SalaryStrategy(ABC):
    """Базовый класс стратегии расчета зарплаты"""

    @abstractmethod
    def calculate(self, base_salary: float, **kwargs) -> float:
        pass


class BaseSalaryStrategy(SalaryStrategy):
    """Стратегия для обычного сотрудника"""

    def calculate(self, base_salary: float, **kwargs) -> float:
        return base_salary


class ManagerSalaryStrategy(SalaryStrategy):
    """Стратегия для менеджера (базовая + бонус)"""

    def calculate(self, base_salary: float, **kwargs) -> float:
        bonus = kwargs.get('bonus', 0)
        return base_salary + bonus


class DeveloperSalaryStrategy(SalaryStrategy):
    """Стратегия для разработчика (с коэффициентом по уровню)"""

    LEVEL_COEFFICIENTS = {
        'junior': 1.0,
        'middle': 1.5,
        'senior': 2.0
    }

    def calculate(self, base_salary: float, **kwargs) -> float:
        level = kwargs.get('level', 'junior')
        coefficient = self.LEVEL_COEFFICIENTS.get(level, 1.0)
        return base_salary * coefficient


class SalespersonSalaryStrategy(SalaryStrategy):
    """Стратегия для продавца (базовая + комиссия)"""

    def calculate(self, base_salary: float, **kwargs) -> float:
        commission_rate = kwargs.get('commission_rate', 0)
        sales_volume = kwargs.get('sales_volume', 0)
        return base_salary + (sales_volume * commission_rate)


class BonusStrategy(ABC):
    """Стратегия расчета бонусов (OCP)"""

    @abstractmethod
    def calculate_bonus(self, employee) -> float:
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """Бонус за производительность"""

    def __init__(self, performance_rate: float = 0.1):
        self.performance_rate = performance_rate

    def calculate_bonus(self, employee) -> float:
        return employee.base_salary * self.performance_rate


class SeniorityBonusStrategy(BonusStrategy):
    """Бонус за стаж"""

    def __init__(self, years_worked: int = 0):
        self.years_worked = years_worked

    def calculate_bonus(self, employee) -> float:
        return employee.base_salary * 0.02 * self.years_worked
