"""Паттерн Factory"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Employee, Manager, Developer, Salesperson


class EmployeeFactory:
    """Фабрика для создания сотрудников"""

    def create_employee(self, emp_type: str, **kwargs):
        emp_type = emp_type.lower()

        if emp_type == "employee":
            return Employee(
                kwargs.get("id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary")
            )
        elif emp_type == "manager":
            return Manager(
                kwargs.get("id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary"),
                kwargs.get("bonus", 0.0)
            )
        elif emp_type == "developer":
            return Developer(
                kwargs.get("id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary"),
                kwargs.get("skills", []),
                kwargs.get("seniority_level", "junior")
            )
        elif emp_type == "salesperson":
            return Salesperson(
                kwargs.get("id"),
                kwargs.get("name"),
                kwargs.get("department"),
                kwargs.get("base_salary"),
                kwargs.get("commission_rate", 0.1),
                kwargs.get("sales", 0.0)
            )
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}")
