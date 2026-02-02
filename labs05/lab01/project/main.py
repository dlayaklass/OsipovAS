"""
Демонстрация паттернов проектирования
Лабораторная работа №5
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Employee, Manager, Developer, Salesperson
from patterns.singleton import DataStorage
from patterns.builder import EmployeeBuilder
from patterns.strategy import PerformanceBonus, SeniorityBonus, ProjectBonus
from patterns.observer import NotificationSystem, EmailNotifier


def demo_singleton():
    """Демонстрация паттерна Singleton"""
    print("\n" + "=" * 60)
    print("1. ПАТТЕРН SINGLETON")
    print("=" * 60)

    # Получаем два экземпляра
    storage1 = DataStorage.get_instance()
    storage2 = DataStorage.get_instance()

    # Проверяем что это один и тот же объект
    print(f"storage1 is storage2: {storage1 is storage2}")
    print(f"ID storage1: {id(storage1)}")
    print(f"ID storage2: {id(storage2)}")

    # Добавляем сотрудника через storage1
    emp = Employee(1, "Иван Петров", "IT", 50000)
    storage1.add_employee(emp)

    # Получаем через storage2
    found = storage2.get_employee(1)
    print(f"Найден через storage2: {found.name if found else 'не найден'}")


def demo_builder():
    """Демонстрация паттерна Builder"""
    print("\n" + "=" * 60)
    print("2. ПАТТЕРН BUILDER")
    print("=" * 60)

    builder = EmployeeBuilder()

    # Создаем обычного сотрудника
    employee = (builder
                .set_id(1)
                .set_name("Анна Сидорова")
                .set_department("HR")
                .set_base_salary(40000)
                .build())
    print(f"Создан: {employee.get_info()}")

    # Создаем разработчика
    developer = (builder
                 .set_id(2)
                 .set_name("Петр Иванов")
                 .set_department("Разработка")
                 .set_base_salary(60000)
                 .set_type("developer")
                 .set_tech_stack(["Python", "SQL", "Docker"])
                 .set_seniority("senior")
                 .build())
    print(f"Создан: {developer.get_info()}")

    # Создаем менеджера
    manager = (builder
               .set_id(3)
               .set_name("Мария Козлова")
               .set_department("Управление")
               .set_base_salary(80000)
               .set_type("manager")
               .set_bonus(15000)
               .build())
    print(f"Создан: {manager.get_info()}")

    # Создаем продавца
    salesperson = (builder
                   .set_id(4)
                   .set_name("Алексей Новиков")
                   .set_department("Продажи")
                   .set_base_salary(35000)
                   .set_type("salesperson")
                   .set_commission_rate(0.15)
                   .set_sales(200000)
                   .build())
    print(f"Создан: {salesperson.get_info()}")

    return [employee, developer, manager, salesperson]


def demo_strategy(employees):
    """Демонстрация паттерна Strategy"""
    print("\n" + "=" * 60)
    print("3. ПАТТЕРН STRATEGY")
    print("=" * 60)

    employee = employees[0]  # Анна Сидорова

    print(f"\nСотрудник: {employee.name}, базовая зп: {employee.base_salary}")

    # Стратегия 1: бонус за производительность (10%)
    strategy1 = PerformanceBonus(0.1)
    employee.set_bonus_strategy(strategy1)
    print(f"Стратегия PerformanceBonus (10%): бонус = {employee.calculate_bonus()}")
    print(f"  Итоговая зп: {employee.calculate_salary()}")

    # Стратегия 2: бонус за стаж (3 года * 2000)
    strategy2 = SeniorityBonus(years=3, amount_per_year=2000)
    employee.set_bonus_strategy(strategy2)
    print(f"Стратегия SeniorityBonus (3 года): бонус = {employee.calculate_bonus()}")
    print(f"  Итоговая зп: {employee.calculate_salary()}")

    # Стратегия 3: проектный бонус
    strategy3 = ProjectBonus(10000)
    employee.set_bonus_strategy(strategy3)
    print(f"Стратегия ProjectBonus: бонус = {employee.calculate_bonus()}")
    print(f"  Итоговая зп: {employee.calculate_salary()}")

    # Сбрасываем стратегию
    employee.set_bonus_strategy(None)


def demo_observer(employees):
    """Демонстрация паттерна Observer"""
    print("\n" + "=" * 60)
    print("4. ПАТТЕРН OBSERVER")
    print("=" * 60)

    developer = employees[1]  # Петр Иванов

    # Создаем наблюдателей
    notification_system = NotificationSystem("HR-отдел")
    email_notifier = EmailNotifier("boss@company.ru")

    # Подписываем на уведомления
    developer.add_observer(notification_system)
    developer.add_observer(email_notifier)

    print(f"\nСотрудник {developer.name} подписан на уведомления")
    print("Меняем зарплату...")

    # Изменяем зарплату - наблюдатели получат уведомление
    developer.base_salary = 75000

    print("\nМеняем зарплату ещё раз...")
    developer.base_salary = 80000

    # Отписываем email
    developer.remove_observer(email_notifier)
    print("\nEmail отписан. Меняем зарплату...")
    developer.base_salary = 85000

    # История уведомлений
    print(f"\nВсего уведомлений в HR-отдел: {len(notification_system.get_messages())}")


def demo_combined():
    """Демонстрация взаимодействия паттернов"""
    print("\n" + "=" * 60)
    print("5. КОМБИНИРОВАННЫЙ ПРИМЕР")
    print("=" * 60)

    # Singleton - хранилище
    storage = DataStorage.get_instance()
    storage.clear()

    # Observer - система уведомлений
    hr_system = NotificationSystem("HR-система")

    # Builder - создаем сотрудников
    builder = EmployeeBuilder()

    employees = [
        (builder.set_id(storage.get_next_id())
               .set_name("Сергей Волков")
               .set_department("IT")
               .set_base_salary(55000)
               .set_type("developer")
               .set_tech_stack(["Java", "Spring"])
               .set_seniority("middle")
               .build()),

        (builder.set_id(storage.get_next_id())
               .set_name("Ольга Белова")
               .set_department("Продажи")
               .set_base_salary(40000)
               .set_type("salesperson")
               .set_commission_rate(0.12)
               .set_sales(150000)
               .build()),
    ]

    # Добавляем в хранилище и подписываем на уведомления
    for emp in employees:
        storage.add_employee(emp)
        emp.add_observer(hr_system)

    # Strategy - назначаем бонусы
    employees[0].set_bonus_strategy(PerformanceBonus(0.15))
    employees[1].set_bonus_strategy(ProjectBonus(8000))

    print("\nСотрудники в системе:")
    for emp in storage.get_all_employees():
        print(f"  {emp.get_info()}")

    print("\nПовышаем зарплату первому сотруднику...")
    employees[0].base_salary = 65000

    print(f"\nОбновленная информация: {employees[0].get_info()}")


def main():
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №5")
    print("Применение паттернов проектирования")
    print("=" * 60)

    # 1. Singleton
    demo_singleton()

    # 2. Builder
    employees = demo_builder()

    # 3. Strategy
    demo_strategy(employees)

    # 4. Observer
    demo_observer(employees)

    # 5. Комбинированный пример
    demo_combined()

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == "__main__":
    main()
