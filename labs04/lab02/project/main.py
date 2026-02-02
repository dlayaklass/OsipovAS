"""
Основной модуль для демонстрации работы системы учета сотрудников.
Демонстрирует наследование, абстракцию и полиморфизм.
"""

from employee import Employee
from manager import Manager
from developer import Developer
from salesperson import Salesperson
from employee_factory import EmployeeFactory


def main():
    """Основная функция для демонстрации работы системы."""
    
    print("=" * 80)
    print("Демонстрация работы системы учета сотрудников")
    print("Часть 2: Наследование и Абстракция")
    print("=" * 80)
    
    # 1. Создание экземпляров каждого типа сотрудника
    print("\n1. Создание экземпляров каждого типа сотрудника:")
    print("-" * 80)
    
    # Обычный сотрудник
    employee = Employee(1, "Иван Петров", "Администрация", 40000.0)
    print(f"Создан обычный сотрудник: {employee.name}")
    
    # Менеджер
    manager = Manager(2, "Мария Сидорова", "Менеджмент", 70000.0, 2000.0)
    print(f"Создан менеджер: {manager.name}")
    
    # Разработчик
    developer = Developer(
        3, "Алексей Иванов", "Разработка", 50000.0,
        ["Python", "SQL", "Docker"], "senior"
    )
    print(f"Создан разработчик: {developer.name}")
    
    # Продавец
    salesperson = Salesperson(4, "Елена Козлова", "Продажи", 35000.0, 0.15, 100000.0)
    print(f"Создан продавец: {salesperson.name}")
    
    # 2. Демонстрация работы с каждым экземпляром
    print("\n2. Информация о каждом сотруднике:")
    print("-" * 80)
    
    employees_list = [employee, manager, developer, salesperson]
    
    for emp in employees_list:
        print(f"\n{emp.get_info()}")
        print(f"  → Рассчитанная зарплата: {emp.calculate_salary()}")
    
    # 3. Демонстрация работы с сеттерами
    print("\n3. Изменение атрибутов через сеттеры:")
    print("-" * 80)
    
    # Изменение зарплаты менеджера
    print(f"До изменения: {manager.get_info()}")
    manager.base_salary = 75000.0
    manager.bonus = 3000.0
    print(f"После изменения: {manager.get_info()}")
    
    # Добавление навыка разработчику
    print(f"\nДо добавления навыка: {developer.get_info()}")
    developer.add_skill("Kubernetes")
    print(f"После добавления навыка: {developer.get_info()}")
    
    # Обновление продаж продавца
    print(f"\nДо обновления продаж: {salesperson.get_info()}")
    salesperson.update_sales(50000.0)
    print(f"После обновления продаж: {salesperson.get_info()}")
    
    # 4. Демонстрация работы фабричного метода
    print("\n4. Создание сотрудников через фабричный метод:")
    print("-" * 80)
    
    # Создание через фабрику
    factory_employee = EmployeeFactory.create_employee(
        "employee",
        employee_id=5,
        name="Петр Смирнов",
        department="Поддержка",
        base_salary=30000.0
    )
    print(f"Создан через фабрику (employee): {factory_employee.get_info()}")
    
    factory_manager = EmployeeFactory.create_employee(
        "manager",
        employee_id=6,
        name="Ольга Новикова",
        department="Менеджмент",
        base_salary=80000.0,
        bonus=5000.0
    )
    print(f"Создан через фабрику (manager): {factory_manager.get_info()}")
    
    factory_developer = EmployeeFactory.create_employee(
        "developer",
        employee_id=7,
        name="Дмитрий Волков",
        department="Разработка",
        base_salary=45000.0,
        tech_stack=["Java", "Spring", "PostgreSQL"],
        seniority_level="middle"
    )
    print(f"Создан через фабрику (developer): {factory_developer.get_info()}")
    
    factory_salesperson = EmployeeFactory.create_employee(
        "salesperson",
        employee_id=8,
        name="Анна Белова",
        department="Продажи",
        base_salary=40000.0,
        commission_rate=0.12,
        sales_volume=150000.0
    )
    print(f"Создан через фабрику (salesperson): {factory_salesperson.get_info()}")
    
    # 5. Демонстрация полиморфного поведения
    print("\n5. Полиморфное поведение - работа с коллекцией объектов:")
    print("-" * 80)
    
    all_employees = [
        employee, manager, developer, salesperson,
        factory_employee, factory_manager, factory_developer, factory_salesperson
    ]
    
    print(f"\nВсего сотрудников: {len(all_employees)}")
    print("\nИнформация о всех сотрудниках:")
    for i, emp in enumerate(all_employees, 1):
        print(f"{i}. {emp.get_info()}")
    
    # Подсчет общей суммы зарплат (демонстрация полиморфизма)
    total_salary = sum(emp.calculate_salary() for emp in all_employees)
    print(f"\nОбщая сумма зарплат всех сотрудников: {total_salary:.2f}")
    
    # Группировка по типам
    print("\n6. Статистика по типам сотрудников:")
    print("-" * 80)
    
    type_counts = {}
    type_salaries = {}
    
    for emp in all_employees:
        emp_type = emp.__class__.__name__
        type_counts[emp_type] = type_counts.get(emp_type, 0) + 1
        type_salaries[emp_type] = type_salaries.get(emp_type, 0) + emp.calculate_salary()
    
    for emp_type, count in type_counts.items():
        avg_salary = type_salaries[emp_type] / count
        print(f"{emp_type}: {count} чел., средняя зарплата: {avg_salary:.2f}")
    
    print("\n" + "=" * 80)
    print("Демонстрация завершена успешно!")
    print("=" * 80)


if __name__ == "__main__":
    main()

