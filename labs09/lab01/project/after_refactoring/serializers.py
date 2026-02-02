"""
Сериализаторы (SRP - вынесли сериализацию в отдельные классы)
"""

import json
import csv


class JsonSerializer:
    """Сериализатор в JSON"""

    @staticmethod
    def save(data: dict, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(filename: str) -> dict:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)


class CsvSerializer:
    """Сериализатор в CSV"""

    @staticmethod
    def save_employees(employees: list, filename: str):
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Имя', 'Отдел', 'Тип', 'Зарплата'])
            for emp in employees:
                writer.writerow([
                    emp.id,
                    emp.name,
                    emp.department,
                    emp.__class__.__name__,
                    emp.calculate_salary()
                ])


class EmployeeSerializer:
    """Сериализатор сотрудников"""

    @staticmethod
    def serialize(employee) -> dict:
        return employee.to_dict()

    @staticmethod
    def serialize_list(employees: list) -> list:
        return [emp.to_dict() for emp in employees]
