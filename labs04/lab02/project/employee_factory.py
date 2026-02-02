"""
Модуль для работы с фабрикой сотрудников EmployeeFactory.
Реализует паттерн Factory Method для создания объектов сотрудников.
"""

from abstract_employee import AbstractEmployee
from employee import Employee
from manager import Manager
from developer import Developer
from salesperson import Salesperson


class EmployeeFactory:
    """
    Фабрика для создания объектов различных типов сотрудников.
    
    Реализует паттерн Factory Method, позволяющий создавать объекты
    различных типов сотрудников на основе строкового параметра.
    """
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создает объект сотрудника указанного типа.
        
        Args:
            emp_type: Тип сотрудника ("employee", "manager", "developer", "salesperson")
            **kwargs: Именованные аргументы для конструктора соответствующего класса
        
        Returns:
            Объект сотрудника указанного типа
        
        Raises:
            ValueError: Если указан неизвестный тип сотрудника
            TypeError: Если не хватает обязательных аргументов для создания объекта
        """
        emp_type_lower = emp_type.lower()
        
        if emp_type_lower == "employee":
            return Employee(
                kwargs.get("employee_id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary")
            )
        
        elif emp_type_lower == "manager":
            return Manager(
                kwargs.get("employee_id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary"),
                kwargs.get("bonus")
            )
        
        elif emp_type_lower == "developer":
            return Developer(
                kwargs.get("employee_id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary"),
                kwargs.get("tech_stack", []),
                kwargs.get("seniority_level", "junior")
            )
        
        elif emp_type_lower == "salesperson":
            return Salesperson(
                kwargs.get("employee_id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary"),
                kwargs.get("commission_rate"),
                kwargs.get("sales_volume", 0.0)
            )
        
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}. "
                           f"Допустимые типы: employee, manager, developer, salesperson")

