"""
Демонстрационный скрипт для Part 4: Композиция и Агрегация.
Демонстрирует работу всей системы учета сотрудников.
"""

import sys
import os

# Добавляем путь к корню проекта для импорта
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.core.company import Company
from src.core.department import Department
from src.core.project import Project
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.utils.exceptions import DuplicateIdError, InvalidStatusError


def main():
    """Основная функция демонстрации."""
    
    print("=" * 80)
    print("Демонстрация работы системы учета сотрудников")
    print("Часть 4: Композиция, Агрегация и Работа со сложными структурами")
    print("=" * 80)
    
    # 1. Создание комплексной структуры
    print("\n1. Создание комплексной структуры:")
    print("-" * 80)
    
    company = Company("TechInnovations")
    print(f"Создана компания: {company.name}")
    
    # Создание отделов
    dev_department = Department("Development")
    sales_department = Department("Sales")
    
    company.add_department(dev_department)
    company.add_department(sales_department)
    print(f"Созданы отделы: {[d.name for d in company.get_departments()]}")
    
    # Создание сотрудников
    manager = Manager(1, "Alice Johnson", "Development", 7000.0, 2000.0)
    developer = Developer(2, "Bob Smith", "Development", 5000.0, 
                         ["Python", "SQL"], "senior")
    salesperson = Salesperson(3, "Charlie Brown", "Sales", 4000.0, 0.15, 50000.0)
    
    dev_department.add_employee(manager)
    dev_department.add_employee(developer)
    sales_department.add_employee(salesperson)
    print(f"Добавлены сотрудники в отделы")
    
    # Создание проектов
    ai_project = Project(101, "AI Platform", "Разработка AI системы", "2024-12-31", "active")
    web_project = Project(102, "Web Portal", "Создание веб-портала", "2024-09-30", "planning")
    
    company.add_project(ai_project)
    company.add_project(web_project)
    print(f"Созданы проекты: {[p.name for p in company.get_projects()]}")
    
    # Формирование команд проектов
    ai_project.add_team_member(developer)
    ai_project.add_team_member(manager)
    web_project.add_team_member(developer)
    print(f"Сформированы команды проектов")
    
    # 2. Работа с композицией и агрегацией
    print("\n2. Работа с композицией и агрегацией:")
    print("-" * 80)
    print(f"Отделов в компании: {len(company.get_departments())}")
    print(f"Проектов в компании: {len(company.get_projects())}")
    print(f"Команда проекта AI Platform: {ai_project.get_team_size()} чел.")
    
    # 3. Валидация и обработка ошибок
    print("\n3. Валидация и обработка ошибок:")
    print("-" * 80)
    
    # Попытка добавить дубликат ID
    try:
        duplicate_manager = Manager(1, "Duplicate", "Development", 5000.0, 1000.0)
        dev_department.add_employee(duplicate_manager)
        print("ОШИБКА: Должна была быть ошибка дубликата ID")
    except Exception as e:
        print(f"Корректно обработана ошибка дубликата: {type(e).__name__}")
    
    # Попытка невалидного изменения статуса
    try:
        ai_project.change_status("invalid_status")
        print("ОШИБКА: Должна была быть ошибка невалидного статуса")
    except InvalidStatusError as e:
        print(f"Корректно обработана ошибка статуса: {e}")
    
    # Попытка удаления занятого отдела
    try:
        company.remove_department("Development")
        print("ОШИБКА: Должна была быть ошибка удаления занятого отдела")
    except ValueError as e:
        print(f"Корректно обработана ошибка удаления: {e}")
    
    # 4. Сериализация и экспорт
    print("\n4. Сериализация и экспорт:")
    print("-" * 80)
    
    # Сохранение в JSON
    json_file = "data/json/company_data.json"
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    company.save_to_json(json_file)
    print(f"Компания сохранена в JSON: {json_file}")
    
    # Загрузка из JSON
    loaded_company = Company.load_from_json(json_file)
    print(f"Компания загружена из JSON: {loaded_company.name}")
    
    # Экспорт в CSV
    csv_employees = "data/csv/employees_report.csv"
    csv_projects = "data/csv/projects_report.csv"
    os.makedirs(os.path.dirname(csv_employees), exist_ok=True)
    
    company.export_employees_csv(csv_employees)
    company.export_projects_csv(csv_projects)
    print(f"Экспортированы отчеты в CSV")
    
    # 5. Анализ данных
    print("\n5. Анализ данных:")
    print("-" * 80)
    
    # Статистика по отделам
    dept_stats = company.get_department_stats()
    print("Статистика по отделам:")
    for dept_name, stats in dept_stats.items():
        print(f"  {dept_name}: {stats['employee_count']} сотрудников, "
              f"зарплата: {stats['total_salary']:.2f}")
    
    # Анализ проектов
    proj_analysis = company.get_project_budget_analysis()
    print(f"\nАнализ проектов:")
    print(f"  Всего проектов: {proj_analysis['total_projects']}")
    print(f"  Общий бюджет: {proj_analysis['total_budget']:.2f}")
    
    # Перегруженные сотрудники
    overloaded = company.find_overloaded_employees()
    if overloaded:
        print(f"\nПерегруженные сотрудники: {len(overloaded)}")
        for emp in overloaded:
            print(f"  - {emp.name}")
    else:
        print("\nПерегруженных сотрудников нет")
    
    # 6. Планирование
    print("\n6. Планирование:")
    print("-" * 80)
    
    # Проверка доступности
    available = company.check_employee_availability(2)
    print(f"Сотрудник ID 2 доступен: {available}")
    
    # Назначение на проект
    assigned = company.assign_employee_to_project(3, 102)
    print(f"Сотрудник ID 3 назначен на проект 102: {assigned}")
    
    # 7. Перенос сотрудника
    print("\n7. Перенос сотрудника между отделами:")
    print("-" * 80)
    try:
        company.transfer_employee_between_departments(2, "Development", "Sales")
        print("Сотрудник перенесен между отделами")
    except Exception as e:
        print(f"Ошибка переноса: {e}")
    
    # 8. Финансовый отчет
    print("\n8. Финансовый отчет:")
    print("-" * 80)
    report = company.generate_financial_report()
    print(report)
    
    print("\n" + "=" * 80)
    print("Демонстрация завершена успешно!")
    print("=" * 80)


if __name__ == "__main__":
    main()

