"""Класс компании"""

import json


class Company:
    """Компания - корневой объект системы"""

    def __init__(self, name: str):
        self._name = name
        self._departments = []
        self._projects = []

    @property
    def name(self) -> str:
        return self._name

    def add_department(self, department):
        self._departments.append(department)

    def remove_department(self, dept_name: str):
        for i, dept in enumerate(self._departments):
            if dept.name == dept_name:
                if len(dept) > 0:
                    raise ValueError("Cannot delete department with employees")
                return self._departments.pop(i)
        return None

    def get_departments(self) -> list:
        return self._departments.copy()

    def add_project(self, project):
        self._projects.append(project)

    def remove_project(self, project_id: int):
        for i, proj in enumerate(self._projects):
            if proj.id == project_id:
                return self._projects.pop(i)
        return None

    def get_projects(self) -> list:
        return self._projects.copy()

    def find_employee_by_id(self, emp_id: int):
        for dept in self._departments:
            emp = dept.find_employee_by_id(emp_id)
            if emp:
                return emp
        return None

    def get_all_employees(self) -> list:
        employees = []
        for dept in self._departments:
            employees.extend(dept.get_employees())
        return employees

    def calculate_total_monthly_cost(self) -> float:
        return sum(emp.calculate_salary() for emp in self.get_all_employees())

    def get_department_stats(self) -> dict:
        stats = {}
        for dept in self._departments:
            stats[dept.name] = {
                "employee_count": len(dept),
                "total_salary": dept.calculate_total_salary()
            }
        return stats

    def save_to_json(self, filename: str):
        data = {
            "name": self._name,
            "departments": [dept.to_dict() for dept in self._departments],
            "projects": [proj.to_dict() for proj in self._projects]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        company = cls(data["name"])
        return company
