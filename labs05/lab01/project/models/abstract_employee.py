"""Абстрактный базовый класс сотрудника"""

from abc import ABC, abstractmethod


class AbstractEmployee(ABC):
    """Абстрактный класс для всех типов сотрудников"""

    def __init__(self, employee_id: int, name: str, department: str, base_salary: float):
        self._id = employee_id
        self._name = name
        self._department = department
        self._base_salary = base_salary
        self._observers = []  # для паттерна Observer

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
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
        old_salary = self._base_salary
        self._base_salary = float(value)
        # уведомляем наблюдателей об изменении зарплаты
        self._notify(f"Зарплата сотрудника {self._name} изменена: {old_salary} -> {value}")

    def add_observer(self, observer):
        """Добавить наблюдателя"""
        self._observers.append(observer)

    def remove_observer(self, observer):
        """Удалить наблюдателя"""
        self._observers.remove(observer)

    def _notify(self, message: str):
        """Уведомить всех наблюдателей"""
        for observer in self._observers:
            observer.update(message)

    @abstractmethod
    def calculate_salary(self) -> float:
        """Рассчитать итоговую зарплату"""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Получить информацию о сотруднике"""
        pass

    def __str__(self) -> str:
        return f"[id: {self._id}, {self._name}, {self._department}, зп: {self._base_salary}]"
