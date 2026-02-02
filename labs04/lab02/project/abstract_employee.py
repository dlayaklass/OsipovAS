"""
Модуль для работы с абстрактным базовым классом AbstractEmployee.
Реализует принцип абстракции через определение общего интерфейса.
"""

from abc import ABC, abstractmethod


class AbstractEmployee(ABC):
    """
    Абстрактный базовый класс для всех типов сотрудников.
    
    Определяет общий интерфейс и общие атрибуты для всех сотрудников.
    Содержит абстрактные методы, которые должны быть реализованы в дочерних классах.
    """
    
    def __init__(self, employee_id: int, name: str, department: str, base_salary: float):
        """
        Конструктор абстрактного класса AbstractEmployee.
        
        Args:
            employee_id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата
        """
        self.__id = employee_id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
    
    @property
    def id(self) -> int:
        """Геттер для идентификатора сотрудника."""
        return self.__id
    
    @id.setter
    def id(self, value: int):
        """Сеттер для идентификатора сотрудника."""
        if not isinstance(value, int):
            raise ValueError("ID должен быть целым числом")
        if value <= 0:
            raise ValueError("ID должен быть положительным числом")
        self.__id = value
    
    @property
    def name(self) -> str:
        """Геттер для имени сотрудника."""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """Сеттер для имени сотрудника."""
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустой строкой")
        self.__name = value
    
    @property
    def department(self) -> str:
        """Геттер для отдела сотрудника."""
        return self.__department
    
    @department.setter
    def department(self, value: str):
        """Сеттер для отдела сотрудника."""
        if not isinstance(value, str):
            raise ValueError("Отдел должен быть строкой")
        if not value.strip():
            raise ValueError("Отдел не может быть пустой строкой")
        self.__department = value
    
    @property
    def base_salary(self) -> float:
        """Геттер для базовой зарплаты сотрудника."""
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value: float):
        """Сеттер для базовой зарплаты сотрудника."""
        if not isinstance(value, (int, float)):
            raise ValueError("Зарплата должна быть числом")
        if value <= 0:
            raise ValueError("Зарплата должна быть положительным числом")
        self.__base_salary = float(value)
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """
        Абстрактный метод для расчета итоговой заработной платы.
        
        Returns:
            Итоговая заработная плата сотрудника
        """
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        """
        Абстрактный метод для получения полной информации о сотруднике.
        
        Returns:
            Строка с полной информацией о сотруднике
        """
        pass
    
    def __str__(self) -> str:
        """
        Возвращает базовое строковое представление объекта.
        
        Returns:
            Строка с базовой информацией о сотруднике
        """
        return (f"Сотрудник [id: {self.__id}, имя: {self.__name}, "
                f"отдел: {self.__department}, базовая зарплата: {self.__base_salary}]")

