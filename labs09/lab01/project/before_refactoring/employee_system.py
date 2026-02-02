"""
Система учета сотрудников (код ДО рефакторинга)
Содержит типичные "запахи кода" и нарушения принципов SOLID
"""

import json


class Employee:
    """Класс сотрудника - содержит слишком много ответственностей"""

    def __init__(self, id, name, department, base_salary, type,
                 bonus=0, tech_stack=None, level=None,
                 commission_rate=0, sales_volume=0):
        self.id = id
        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.type = type  # "employee", "manager", "developer", "salesperson"
        self.bonus = bonus
        self.tech_stack = tech_stack or []
        self.level = level  # junior, middle, senior
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume
        self.skills = []

    def calculate_salary(self):
        """Длинный метод с множеством условий - нарушение OCP"""
        if self.type == "employee":
            return self.base_salary
        elif self.type == "manager":
            return self.base_salary + self.bonus
        elif self.type == "developer":
            if self.level == "junior":
                return self.base_salary * 1.0
            elif self.level == "middle":
                return self.base_salary * 1.5
            elif self.level == "senior":
                return self.base_salary * 2.0
            else:
                return self.base_salary
        elif self.type == "salesperson":
            return self.base_salary + (self.sales_volume * self.commission_rate)
        else:
            return self.base_salary

    def get_info(self):
        """Еще один длинный метод"""
        info = f"ID: {self.id}, Имя: {self.name}, Отдел: {self.department}"
        info += f", База: {self.base_salary}"

        if self.type == "manager":
            info += f", Бонус: {self.bonus}"
        elif self.type == "developer":
            info += f", Уровень: {self.level}"
            info += f", Технологии: {', '.join(self.tech_stack)}"
        elif self.type == "salesperson":
            info += f", Комиссия: {self.commission_rate * 100}%"
            info += f", Продажи: {self.sales_volume}"

        info += f", Итого: {self.calculate_salary()}"
        return info

    def add_skill(self, skill):
        """Добавление навыка - не все типы сотрудников используют"""
        if skill not in self.skills:
            self.skills.append(skill)

    def validate(self):
        """Валидация прямо в классе - нарушение SRP"""
        errors = []
        if not self.name or len(self.name) < 2:
            errors.append("Имя слишком короткое")
        if self.base_salary < 0:
            errors.append("Зарплата не может быть отрицательной")
        if self.type not in ["employee", "manager", "developer", "salesperson"]:
            errors.append("Неизвестный тип сотрудника")
        return errors

    def save_to_file(self, filename):
        """Сериализация прямо в классе - нарушение SRP"""
        data = {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
            "type": self.type,
            "bonus": self.bonus,
            "tech_stack": self.tech_stack,
            "level": self.level,
            "commission_rate": self.commission_rate,
            "sales_volume": self.sales_volume
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def log_action(self, action):
        """Логирование прямо в классе - нарушение SRP"""
        print(f"[LOG] Сотрудник {self.name}: {action}")


class Department:
    """Класс отдела"""

    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, emp):
        # Дублирование валидации
        if emp.name and emp.base_salary >= 0:
            self.employees.append(emp)

    def remove_employee(self, emp_id):
        self.employees = [e for e in self.employees if e.id != emp_id]

    def get_total_salary(self):
        total = 0
        for emp in self.employees:
            total += emp.calculate_salary()
        return total

    def get_employee_info(self):
        """Дублирование логики из Employee"""
        result = ""
        for emp in self.employees:
            result += f"ID: {emp.id}, Имя: {emp.name}, Зарплата: {emp.calculate_salary()}\n"
        return result


class Company:
    """Большой класс со слишком большой ответственностью - нарушение SRP"""

    def __init__(self, name):
        self.name = name
        self.departments = []
        self.projects = []

    def add_department(self, dept):
        self.departments.append(dept)

    def remove_department(self, dept_name):
        self.departments = [d for d in self.departments if d.name != dept_name]

    def find_department(self, name):
        for dept in self.departments:
            if dept.name == name:
                return dept
        return None

    def find_employee(self, emp_id):
        for dept in self.departments:
            for emp in dept.employees:
                if emp.id == emp_id:
                    return emp
        return None

    def get_all_employees(self):
        result = []
        for dept in self.departments:
            for emp in dept.employees:
                result.append(emp)
        return result

    def calculate_total_salary(self):
        """Дублирование логики"""
        total = 0
        for dept in self.departments:
            for emp in dept.employees:
                total += emp.calculate_salary()
        return total

    def generate_report(self):
        """Очень длинный метод - нужно разбить"""
        report = "=" * 50 + "\n"
        report += f"ОТЧЕТ КОМПАНИИ: {self.name}\n"
        report += "=" * 50 + "\n\n"

        # Статистика по отделам
        report += "ОТДЕЛЫ:\n"
        report += "-" * 30 + "\n"
        for dept in self.departments:
            report += f"  {dept.name}: {len(dept.employees)} сотр.\n"
            total = 0
            for emp in dept.employees:
                total += emp.calculate_salary()
            report += f"    Фонд ЗП: {total}\n"

        # Статистика по типам
        report += "\nПО ТИПАМ:\n"
        report += "-" * 30 + "\n"
        types_count = {}
        for dept in self.departments:
            for emp in dept.employees:
                t = emp.type
                if t not in types_count:
                    types_count[t] = 0
                types_count[t] += 1
        for t, c in types_count.items():
            report += f"  {t}: {c}\n"

        # Общие показатели
        report += "\nИТОГО:\n"
        report += "-" * 30 + "\n"
        total_emp = len(self.get_all_employees())
        total_sal = self.calculate_total_salary()
        report += f"  Сотрудников: {total_emp}\n"
        report += f"  Общий ФОТ: {total_sal}\n"

        return report

    def save_to_json(self, filename):
        """Сериализация в классе Company"""
        data = {
            "name": self.name,
            "departments": []
        }
        for dept in self.departments:
            dept_data = {"name": dept.name, "employees": []}
            for emp in dept.employees:
                emp_data = {
                    "id": emp.id,
                    "name": emp.name,
                    "department": emp.department,
                    "base_salary": emp.base_salary,
                    "type": emp.type
                }
                dept_data["employees"].append(emp_data)
            data["departments"].append(dept_data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def export_csv(self, filename):
        """Экспорт в CSV - еще одна ответственность"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ID,Имя,Отдел,Тип,Зарплата\n")
            for emp in self.get_all_employees():
                f.write(f"{emp.id},{emp.name},{emp.department},{emp.type},{emp.calculate_salary()}\n")


def main():
    """Демонстрация работы системы"""
    # Создаем компанию
    company = Company("ООО Рога и Копыта")

    # Создаем отделы
    it_dept = Department("IT")
    sales_dept = Department("Продажи")

    # Создаем сотрудников (разные типы через один класс)
    emp1 = Employee(1, "Иван", "IT", 50000, "developer",
                    tech_stack=["Python", "JS"], level="senior")
    emp2 = Employee(2, "Мария", "IT", 45000, "developer",
                    tech_stack=["Java"], level="middle")
    emp3 = Employee(3, "Петр", "IT", 80000, "manager", bonus=20000)
    emp4 = Employee(4, "Анна", "Продажи", 40000, "salesperson",
                    commission_rate=0.1, sales_volume=100000)
    emp5 = Employee(5, "Сергей", "Продажи", 35000, "employee")

    # Добавляем сотрудников
    it_dept.add_employee(emp1)
    it_dept.add_employee(emp2)
    it_dept.add_employee(emp3)
    sales_dept.add_employee(emp4)
    sales_dept.add_employee(emp5)

    # Добавляем отделы
    company.add_department(it_dept)
    company.add_department(sales_dept)

    # Выводим информацию
    print("=== Информация о сотрудниках ===")
    for emp in company.get_all_employees():
        print(emp.get_info())

    print("\n=== Отчет компании ===")
    print(company.generate_report())


if __name__ == "__main__":
    main()
