"""
Паттерн Strategy - стратегии расчета бонусов
"""

from abc import ABC, abstractmethod


class BonusStrategy(ABC):
    """Абстрактная стратегия расчета бонуса"""

    @abstractmethod
    def calculate(self, employee) -> float:
        """Рассчитать бонус для сотрудника"""
        pass


class PerformanceBonus(BonusStrategy):
    """Бонус за производительность (процент от зарплаты)"""

    def __init__(self, percent: float = 0.1):
        self._percent = percent

    def calculate(self, employee) -> float:
        return employee.base_salary * self._percent


class SeniorityBonus(BonusStrategy):
    """Бонус за стаж (фиксированная сумма за каждый год)"""

    def __init__(self, years: int = 1, amount_per_year: float = 1000.0):
        self._years = years
        self._amount = amount_per_year

    def calculate(self, employee) -> float:
        return self._years * self._amount


class ProjectBonus(BonusStrategy):
    """Бонус за проект (фиксированная сумма)"""

    def __init__(self, project_bonus: float = 5000.0):
        self._bonus = project_bonus

    def calculate(self, employee) -> float:
        return self._bonus
