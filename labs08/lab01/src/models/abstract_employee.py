"""Абстрактный базовый класс сотрудника"""

from abc import ABC, abstractmethod


class AbstractEmployee(ABC):
    """Абстрактный класс для всех типов сотрудников"""

    def __init__(self, employee_id: int, name: str, department: str, base_salary: float):
        self.id = employee_id
        self.name = name
        self._department = department
        self.base_salary = base_salary
        self._observers = []

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if value < 0:
            raise ValueError("ID не может быть отрицательным")
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or value.strip() == "":
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str):
        self._department = value

    @property
    def base_salary(self) -> float:
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value: float):
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        old_salary = getattr(self, '_base_salary', None)
        self._base_salary = float(value)
        if old_salary is not None:
            self._notify(f"Зарплата изменена: {old_salary} -> {value}")

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def _notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "department": self._department,
            "base_salary": self._base_salary,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["id"], data["name"], data["department"], data["base_salary"])

    def __str__(self) -> str:
        return f"Сотрудник [id: {self._id}, имя: {self._name}, отдел: {self._department}, базовая зарплата: {self._base_salary}]"

    def __eq__(self, other):
        if isinstance(other, AbstractEmployee):
            return self._id == other._id
        return False

    def __lt__(self, other):
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() < other.calculate_salary()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() > other.calculate_salary()
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() + other.calculate_salary()
        return NotImplemented
