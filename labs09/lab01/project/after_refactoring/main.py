"""
Система учета сотрудников (код ПОСЛЕ рефакторинга)
Демонстрация работы с применением принципов SOLID
"""

from employees import Employee, Manager, Developer, Salesperson
from salary_strategies import (
    BaseSalaryStrategy, ManagerSalaryStrategy,
    DeveloperSalaryStrategy, SalespersonSalaryStrategy
)
from department import Department
from managers import DepartmentManager, FinancialCalculator, ReportGenerator
from validators import EmployeeValidator, DeveloperValidator
from repositories import InMemoryEmployeeRepository


def main():
    """Демонстрация работы системы"""

    # Создаем репозиторий (DIP)
    repository = InMemoryEmployeeRepository()

    # Создаем стратегии расчета зарплаты (OCP)
    dev_strategy = DeveloperSalaryStrategy()
    manager_strategy = ManagerSalaryStrategy()
    sales_strategy = SalespersonSalaryStrategy()

    # Создаем сотрудников с внедрением стратегий
    emp1 = Developer(1, "Иван", "IT", 50000, "senior",
                     tech_stack=["Python", "JS"], salary_strategy=dev_strategy)
    emp2 = Developer(2, "Мария", "IT", 45000, "middle",
                     tech_stack=["Java"], salary_strategy=dev_strategy)
    emp3 = Manager(3, "Петр", "IT", 80000, bonus=20000,
                   salary_strategy=manager_strategy)
    emp4 = Salesperson(4, "Анна", "Продажи", 40000,
                       commission_rate=0.1, sales_volume=100000,
                       salary_strategy=sales_strategy)
    emp5 = Employee(5, "Сергей", "Продажи", 35000,
                    salary_strategy=BaseSalaryStrategy())

    # Валидация (SRP - отдельный класс)
    errors = EmployeeValidator.validate_employee(1, "Иван", 50000)
    if errors:
        print("Ошибки валидации:", errors)

    errors = DeveloperValidator.validate_level("senior")
    if errors:
        print("Ошибки:", errors)

    # Сохраняем в репозиторий (DIP)
    for emp in [emp1, emp2, emp3, emp4, emp5]:
        repository.save(emp)

    # Создаем отделы
    it_dept = Department("IT")
    sales_dept = Department("Продажи")

    it_dept.add_employee(emp1)
    it_dept.add_employee(emp2)
    it_dept.add_employee(emp3)
    sales_dept.add_employee(emp4)
    sales_dept.add_employee(emp5)

    # Менеджер отделов (SRP)
    dept_manager = DepartmentManager()
    dept_manager.add_department(it_dept)
    dept_manager.add_department(sales_dept)

    # Вывод информации
    print("=== Информация о сотрудниках ===")
    for emp in dept_manager.get_all_employees():
        print(emp.get_info())

    # Расчеты (SRP - отдельный класс)
    print("\n=== Финансовые расчеты ===")
    all_emps = dept_manager.get_all_employees()
    print(f"Общий ФОТ: {FinancialCalculator.calculate_total_salary(all_emps)}")
    print(f"Средняя ЗП: {FinancialCalculator.calculate_average_salary(all_emps):.2f}")

    # Отчет (SRP - отдельный класс)
    print("\n=== Отчет ===")
    report_gen = ReportGenerator(dept_manager)
    print(report_gen.generate_summary())

    # Демонстрация легкости добавления нового типа
    print("\n=== Демонстрация OCP ===")
    print("Для добавления нового типа сотрудника достаточно:")
    print("1. Создать новый класс (наследник AbstractEmployee)")
    print("2. Создать новую стратегию расчета зарплаты")
    print("Существующий код изменять не нужно!")


if __name__ == "__main__":
    main()
