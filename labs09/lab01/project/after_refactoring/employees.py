"""
Классы сотрудников (SRP, LSP)
Каждый класс отвечает только за свою логику
"""

from abc import abstractmethod
from interfaces import ISalaryCalculable, IInfoProvidable, ISerializable
from salary_strategies import SalaryStrategy, BaseSalaryStrategy


class AbstractEmployee(ISalaryCalculable, IInfoProvidable, ISerializable):
    """Абстрактный базовый класс сотрудника"""

    def __init__(self, emp_id: int, name: str, department: str,
                 base_salary: float, salary_strategy: SalaryStrategy = None):
        self._id = emp_id
        self._name = name
        self._department = department
        self._base_salary = base_salary
        self._salary_strategy = salary_strategy or BaseSalaryStrategy()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def department(self) -> str:
        return self._department

    @property
    def base_salary(self) -> float:
        return self._base_salary

    def calculate_salary(self) -> float:
        return self._salary_strategy.calculate(self._base_salary, **self._get_salary_params())

    def _get_salary_params(self) -> dict:
        """Переопределяется в дочерних классах"""
        return {}

    @abstractmethod
    def get_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'id': self._id,
            'name': self._name,
            'department': self._department,
            'base_salary': self._base_salary
        }

    def __str__(self) -> str:
        return f"{self._name} (ID: {self._id})"


class Employee(AbstractEmployee):
    """Обычный сотрудник"""

    def get_info(self) -> str:
        return f"Сотрудник: {self._name}, Отдел: {self._department}, ЗП: {self.calculate_salary()}"


class Manager(AbstractEmployee):
    """Менеджер"""

    def __init__(self, emp_id: int, name: str, department: str,
                 base_salary: float, bonus: float, salary_strategy: SalaryStrategy = None):
        super().__init__(emp_id, name, department, base_salary, salary_strategy)
        self._bonus = bonus

    @property
    def bonus(self) -> float:
        return self._bonus

    def _get_salary_params(self) -> dict:
        return {'bonus': self._bonus}

    def get_info(self) -> str:
        return f"Менеджер: {self._name}, Бонус: {self._bonus}, ЗП: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['bonus'] = self._bonus
        return data


class Developer(AbstractEmployee):
    """Разработчик"""

    def __init__(self, emp_id: int, name: str, department: str,
                 base_salary: float, level: str, tech_stack: list = None,
                 salary_strategy: SalaryStrategy = None):
        super().__init__(emp_id, name, department, base_salary, salary_strategy)
        self._level = level
        self._tech_stack = tech_stack or []

    @property
    def level(self) -> str:
        return self._level

    @property
    def tech_stack(self) -> list:
        return self._tech_stack.copy()

    def add_skill(self, skill: str):
        if skill not in self._tech_stack:
            self._tech_stack.append(skill)

    def _get_salary_params(self) -> dict:
        return {'level': self._level}

    def get_info(self) -> str:
        techs = ', '.join(self._tech_stack) if self._tech_stack else 'нет'
        return f"Разработчик: {self._name}, Уровень: {self._level}, Стек: [{techs}], ЗП: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['level'] = self._level
        data['tech_stack'] = self._tech_stack
        return data


class Salesperson(AbstractEmployee):
    """Продавец"""

    def __init__(self, emp_id: int, name: str, department: str,
                 base_salary: float, commission_rate: float,
                 sales_volume: float = 0, salary_strategy: SalaryStrategy = None):
        super().__init__(emp_id, name, department, base_salary, salary_strategy)
        self._commission_rate = commission_rate
        self._sales_volume = sales_volume

    @property
    def commission_rate(self) -> float:
        return self._commission_rate

    @property
    def sales_volume(self) -> float:
        return self._sales_volume

    def update_sales(self, amount: float):
        self._sales_volume += amount

    def _get_salary_params(self) -> dict:
        return {
            'commission_rate': self._commission_rate,
            'sales_volume': self._sales_volume
        }

    def get_info(self) -> str:
        return f"Продавец: {self._name}, Комиссия: {self._commission_rate*100}%, Продажи: {self._sales_volume}, ЗП: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['commission_rate'] = self._commission_rate
        data['sales_volume'] = self._sales_volume
        return data
