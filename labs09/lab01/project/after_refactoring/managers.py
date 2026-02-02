"""
Менеджеры (SRP - разделение ответственности класса Company)
"""


class DepartmentManager:
    """Управление отделами"""

    def __init__(self):
        self._departments = []

    def add_department(self, dept):
        if dept not in self._departments:
            self._departments.append(dept)

    def remove_department(self, name: str):
        self._departments = [d for d in self._departments if d.name != name]

    def find_department(self, name: str):
        for dept in self._departments:
            if dept.name == name:
                return dept
        return None

    def get_all_departments(self) -> list:
        return self._departments.copy()

    def get_all_employees(self) -> list:
        result = []
        for dept in self._departments:
            result.extend(dept.get_employees())
        return result


class FinancialCalculator:
    """Финансовые расчеты"""

    @staticmethod
    def calculate_total_salary(employees: list) -> float:
        return sum(emp.calculate_salary() for emp in employees)

    @staticmethod
    def calculate_average_salary(employees: list) -> float:
        if not employees:
            return 0
        return FinancialCalculator.calculate_total_salary(employees) / len(employees)

    @staticmethod
    def get_salary_by_department(departments: list) -> dict:
        result = {}
        for dept in departments:
            result[dept.name] = FinancialCalculator.calculate_total_salary(dept.get_employees())
        return result


class ReportGenerator:
    """Генератор отчетов"""

    def __init__(self, department_manager: DepartmentManager):
        self._dept_manager = department_manager

    def generate_summary(self) -> str:
        lines = []
        lines.append("=" * 50)
        lines.append("ОТЧЕТ ПО КОМПАНИИ")
        lines.append("=" * 50)

        # По отделам
        lines.append("\nОТДЕЛЫ:")
        lines.append("-" * 30)
        for dept in self._dept_manager.get_all_departments():
            total = FinancialCalculator.calculate_total_salary(dept.get_employees())
            lines.append(f"  {dept.name}: {len(dept)} сотр., ФОТ: {total}")

        # Общие показатели
        all_emps = self._dept_manager.get_all_employees()
        total_salary = FinancialCalculator.calculate_total_salary(all_emps)

        lines.append("\nИТОГО:")
        lines.append("-" * 30)
        lines.append(f"  Всего сотрудников: {len(all_emps)}")
        lines.append(f"  Общий ФОТ: {total_salary}")

        return "\n".join(lines)

    def generate_employee_list(self) -> str:
        lines = ["Список сотрудников:", "-" * 40]
        for emp in self._dept_manager.get_all_employees():
            lines.append(f"  {emp.get_info()}")
        return "\n".join(lines)
