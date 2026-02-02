"""
Модуль для работы с классом Department (Отдел).
Реализует полиморфизм и магические методы для работы с коллекциями сотрудников.
"""

import json
from typing import Optional
from .abstract_employee import AbstractEmployee


class Department:
    """
    Класс Department представляет отдел компании.
    
    Содержит коллекцию сотрудников и предоставляет методы для работы с ними.
    Реализует магические методы для удобной работы с объектом.
    """
    
    def __init__(self, name: str):
        """
        Конструктор класса Department.
        
        Args:
            name: Название отдела
        """
        self.__name = name
        self.__employees: list[AbstractEmployee] = []
    
    @property
    def name(self) -> str:
        """Геттер для названия отдела."""
        return self.__name
    
    def add_employee(self, employee: AbstractEmployee) -> None:
        """Добавляет сотрудника в отдел."""
        if employee not in self.__employees:
            self.__employees.append(employee)
    
    def remove_employee(self, employee_id: int) -> None:
        """Удаляет сотрудника из отдела по ID."""
        self.__employees = [emp for emp in self.__employees if emp.id != employee_id]
    
    def get_employees(self) -> list[AbstractEmployee]:
        """Возвращает список всех сотрудников отдела."""
        return self.__employees.copy()
    
    def calculate_total_salary(self) -> float:
        """Вычисляет общую зарплату всех сотрудников отдела."""
        return sum(emp.calculate_salary() for emp in self.__employees)
    
    def get_employee_count(self) -> dict[str, int]:
        """Возвращает словарь с количеством сотрудников каждого типа."""
        counts = {}
        for emp in self.__employees:
            emp_type = emp.__class__.__name__
            counts[emp_type] = counts.get(emp_type, 0) + 1
        return counts
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Находит сотрудника по ID."""
        for emp in self.__employees:
            if emp.id == employee_id:
                return emp
        return None
    
    def __len__(self) -> int:
        """Возвращает количество сотрудников в отделе."""
        return len(self.__employees)
    
    def __getitem__(self, key: int) -> AbstractEmployee:
        """Доступ к сотруднику по индексу."""
        return self.__employees[key]
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        """Проверка принадлежности сотрудника отделу."""
        return employee in self.__employees
    
    def __iter__(self):
        """Итератор по сотрудникам отдела."""
        return iter(self.__employees)
    
    def __str__(self) -> str:
        """Строковое представление отдела."""
        return f"Отдел '{self.__name}' ({len(self.__employees)} сотрудников)"
    
    def save_to_file(self, filename: str) -> None:
        """Сохраняет всех сотрудников отдела в JSON файл."""
        data = {
            "name": self.__name,
            "employees": [emp.to_dict() for emp in self.__employees]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """Загружает отдел из JSON файла."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dept = cls(data["name"])
        
        # Импортируем классы для создания объектов
        from .employee import Employee
        from ..employees.manager import Manager
        from ..employees.developer import Developer
        from ..employees.salesperson import Salesperson
        
        for emp_data in data["employees"]:
            emp_type = emp_data.get("type", "Employee")
            if emp_type == "Manager":
                employee = Manager.from_dict(emp_data)
            elif emp_type == "Developer":
                employee = Developer.from_dict(emp_data)
            elif emp_type == "Salesperson":
                employee = Salesperson.from_dict(emp_data)
            else:
                employee = Employee.from_dict(emp_data)
            dept.add_employee(employee)
        
        return dept
