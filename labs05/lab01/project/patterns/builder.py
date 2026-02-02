"""
Паттерн Builder - пошаговое создание сотрудников
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Employee, Manager, Developer, Salesperson


class EmployeeBuilder:
    """
    Builder для пошагового создания объектов сотрудников.
    Использует fluent-интерфейс (цепочка вызовов).
    """

    def __init__(self):
        self._reset()

    def _reset(self):
        """Сброс всех параметров"""
        self._id = None
        self._name = None
        self._department = None
        self._base_salary = 0.0
        self._type = "employee"
        # для Manager
        self._bonus = 0.0
        # для Developer
        self._tech_stack = []
        self._seniority = "junior"
        # для Salesperson
        self._commission_rate = 0.1
        self._sales = 0.0

    def set_id(self, emp_id: int):
        """Установить ID"""
        self._id = emp_id
        return self

    def set_name(self, name: str):
        """Установить имя"""
        self._name = name
        return self

    def set_department(self, department: str):
        """Установить отдел"""
        self._department = department
        return self

    def set_base_salary(self, salary: float):
        """Установить базовую зарплату"""
        self._base_salary = salary
        return self

    def set_type(self, emp_type: str):
        """Установить тип сотрудника"""
        self._type = emp_type.lower()
        return self

    def set_bonus(self, bonus: float):
        """Установить бонус (для Manager)"""
        self._bonus = bonus
        return self

    def set_tech_stack(self, skills: list):
        """Установить стек технологий (для Developer)"""
        self._tech_stack = skills.copy()
        return self

    def set_seniority(self, level: str):
        """Установить уровень (для Developer)"""
        self._seniority = level
        return self

    def set_commission_rate(self, rate: float):
        """Установить процент комиссии (для Salesperson)"""
        self._commission_rate = rate
        return self

    def set_sales(self, sales: float):
        """Установить объем продаж (для Salesperson)"""
        self._sales = sales
        return self

    def build(self):
        """Построить объект сотрудника"""
        if self._type == "manager":
            result = Manager(self._id, self._name, self._department,
                           self._base_salary, self._bonus)
        elif self._type == "developer":
            result = Developer(self._id, self._name, self._department,
                             self._base_salary, self._tech_stack, self._seniority)
        elif self._type == "salesperson":
            result = Salesperson(self._id, self._name, self._department,
                               self._base_salary, self._commission_rate, self._sales)
        else:
            result = Employee(self._id, self._name, self._department, self._base_salary)

        self._reset()
        return result
