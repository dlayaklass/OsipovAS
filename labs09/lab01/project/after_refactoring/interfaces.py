"""
Интерфейсы системы (ISP - принцип разделения интерфейсов)
"""

from abc import ABC, abstractmethod


class ISalaryCalculable(ABC):
    """Интерфейс для расчета зарплаты"""

    @abstractmethod
    def calculate_salary(self) -> float:
        pass


class IInfoProvidable(ABC):
    """Интерфейс для получения информации"""

    @abstractmethod
    def get_info(self) -> str:
        pass


class ISkillManageable(ABC):
    """Интерфейс для управления навыками"""

    @abstractmethod
    def add_skill(self, skill: str):
        pass


class ISerializable(ABC):
    """Интерфейс для сериализации"""

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class IEmployeeRepository(ABC):
    """Интерфейс репозитория сотрудников (DIP)"""

    @abstractmethod
    def save(self, employee):
        pass

    @abstractmethod
    def find_by_id(self, emp_id: int):
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass
