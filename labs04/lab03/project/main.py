"""
Основной модуль для демонстрации работы системы учета сотрудников.
Демонстрирует полиморфизм, магические методы и сериализацию.
"""

import functools
from employee import Employee
from manager import Manager
from developer import Developer
from salesperson import Salesperson
from department import Department


def compare_by_name(emp1: Employee, emp2: Employee) -> int:
    """Компаратор для сортировки по имени."""
    if emp1.name < emp2.name:
        return -1
    elif emp1.name > emp2.name:
        return 1
    return 0


def compare_by_salary(emp1: Employee, emp2: Employee) -> int:
    """Компаратор для сортировки по зарплате."""
    sal1 = emp1.calculate_salary()
    sal2 = emp2.calculate_salary()
    if sal1 < sal2:
        return -1
    elif sal1 > sal2:
        return 1
    return 0


def compare_by_dept_and_name(emp1: Employee, emp2: Employee) -> int:
    """Компаратор для сортировки по отделу и затем по имени."""
    if emp1.department < emp2.department:
        return -1
    elif emp1.department > emp2.department:
        return 1
    # Если отделы одинаковые, сравниваем по имени
    return compare_by_name(emp1, emp2)


def main():
    """Основная функция для демонстрации работы системы."""
    
    print("=" * 80)
    print("Демонстрация работы системы учета сотрудников")
    print("Часть 3: Полиморфизм и Магические методы")
    print("=" * 80)
    
    # 1. Создание отдела и добавление сотрудников
    print("\n1. Создание отдела и добавление сотрудников:")
    print("-" * 80)
    
    dept = Department("Разработка")
    
    manager = Manager(1, "Анна Петрова", "Разработка", 70000.0, 2000.0)
    developer1 = Developer(2, "Иван Сидоров", "Разработка", 50000.0, 
                           ["Python", "SQL"], "senior")
    developer2 = Developer(3, "Мария Козлова", "Разработка", 45000.0,
                           ["Java", "Spring"], "middle")
    salesperson = Salesperson(4, "Петр Иванов", "Разработка", 40000.0, 0.1, 50000.0)
    
    dept.add_employee(manager)
    dept.add_employee(developer1)
    dept.add_employee(developer2)
    dept.add_employee(salesperson)
    
    print(f"Создан отдел: {dept}")
    print(f"Добавлено сотрудников: {len(dept)}")
    
    # 2. Расчет общей зарплаты отдела (полиморфизм)
    print("\n2. Расчет общей зарплаты отдела (полиморфизм):")
    print("-" * 80)
    total = dept.calculate_total_salary()
    print(f"Общая зарплата всех сотрудников отдела: {total:.2f}")
    
    # 3. Перегруженные операторы
    print("\n3. Использование перегруженных операторов:")
    print("-" * 80)
    
    # Сравнение по ID
    print(f"manager == developer1: {manager == developer1}")
    print(f"developer1 == developer1: {developer1 == developer1}")
    
    # Сравнение по зарплате
    print(f"developer1 < developer2: {developer1 < developer2}")
    print(f"manager > salesperson: {manager > salesperson}")
    
    # Сложение зарплат
    sum_salaries = developer1 + developer2
    print(f"developer1 + developer2 = {sum_salaries:.2f}")
    
    # Суммирование списка через sum()
    employees_list = [manager, developer1, developer2, salesperson]
    total_sum = sum(employees_list)
    print(f"sum([manager, developer1, developer2, salesperson]) = {total_sum:.2f}")
    
    # Проверка вхождения
    print(f"manager in dept: {manager in dept}")
    
    # Доступ по индексу
    print(f"dept[0]: {dept[0].name}")
    print(f"dept[1]: {dept[1].name}")
    
    # 4. Итерация по отделу
    print("\n4. Итерация по отделу:")
    print("-" * 80)
    for i, emp in enumerate(dept, 1):
        print(f"{i}. {emp.name} - {emp.calculate_salary():.2f}")
    
    # 5. Итерация по стеку технологий разработчика
    print("\n5. Итерация по стеку технологий разработчика:")
    print("-" * 80)
    print(f"Технологии {developer1.name}:")
    for skill in developer1:
        print(f"  - {skill}")
    
    # 6. Статистика по типам сотрудников
    print("\n6. Статистика по типам сотрудников:")
    print("-" * 80)
    counts = dept.get_employee_count()
    for emp_type, count in counts.items():
        print(f"{emp_type}: {count} чел.")
    
    # 7. Поиск сотрудника по ID
    print("\n7. Поиск сотрудника по ID:")
    print("-" * 80)
    found = dept.find_employee_by_id(2)
    if found:
        print(f"Найден сотрудник: {found.get_info()}")
    
    # 8. Сортировка сотрудников
    print("\n8. Сортировка сотрудников:")
    print("-" * 80)
    
    # По имени (с key)
    sorted_by_name = sorted(dept.get_employees(), key=lambda e: e.name)
    print("Сортировка по имени:")
    for emp in sorted_by_name:
        print(f"  {emp.name}")
    
    # По зарплате (с key)
    sorted_by_salary = sorted(dept.get_employees(), key=lambda e: e.calculate_salary(), reverse=True)
    print("\nСортировка по зарплате (убывание):")
    for emp in sorted_by_salary:
        print(f"  {emp.name}: {emp.calculate_salary():.2f}")
    
    # По отделу и имени (с компаратором)
    employees = dept.get_employees()
    sorted_by_dept_name = sorted(employees, key=functools.cmp_to_key(compare_by_dept_and_name))
    print("\nСортировка по отделу и имени:")
    for emp in sorted_by_dept_name:
        print(f"  {emp.department} - {emp.name}")
    
    # 9. Сериализация и десериализация
    print("\n9. Сериализация и десериализация:")
    print("-" * 80)
    
    filename = "department_data.json"
    dept.save_to_file(filename)
    print(f"Отдел сохранен в файл: {filename}")
    
    loaded_dept = Department.load_from_file(filename)
    print(f"Отдел загружен из файла: {loaded_dept}")
    print(f"  Количество сотрудников: {len(loaded_dept)}")
    
    print("\n" + "=" * 80)
    print("Демонстрация завершена успешно!")
    print("=" * 80)


if __name__ == "__main__":
    main()
