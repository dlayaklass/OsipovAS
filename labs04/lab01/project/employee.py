"""
Модуль для работы с классом Employee (Сотрудник).
Реализует принцип инкапсуляции через приватные атрибуты и свойства.
"""


class Employee:
    """
    Класс Employee представляет сотрудника компании.
    
    Инкапсулирует данные о сотруднике через приватные атрибуты
    и предоставляет доступ к ним через свойства с валидацией.
    """
    
    def __init__(self, employee_id: int, name: str, department: str, base_salary: float):
        """
        Конструктор класса Employee.
        
        Args:
            employee_id: Уникальный идентификатор сотрудника (положительное целое число)
            name: Имя сотрудника (непустая строка)
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата (положительное вещественное число)
        
        Raises:
            ValueError: Если переданные данные невалидны
        """
        # Устанавливаем значения через свойства для валидации
        self.id = employee_id
        self.name = name
        self.department = department
        self.base_salary = base_salary
    
    @property
    def id(self) -> int:
        """Геттер для идентификатора сотрудника."""
        return self.__id
    
    @id.setter
    def id(self, value: int):
        """
        Сеттер для идентификатора сотрудника.
        
        Args:
            value: Идентификатор сотрудника
        
        Raises:
            ValueError: Если идентификатор не является положительным целым числом
        """
        if not isinstance(value, int):
            raise ValueError("ID должен быть целым числом")
        if value <= 0:
            raise ValueError("ID должен быть положительным числом")
        self.__id = value
    
    @property
    def name(self) -> str:
        """Геттер для имени сотрудника."""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """
        Сеттер для имени сотрудника.
        
        Args:
            value: Имя сотрудника
        
        Raises:
            ValueError: Если имя является пустой строкой
        """
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустой строкой")
        self.__name = value
    
    @property
    def department(self) -> str:
        """Геттер для отдела сотрудника."""
        return self.__department
    
    @department.setter
    def department(self, value: str):
        """
        Сеттер для отдела сотрудника.
        
        Args:
            value: Название отдела
        
        Raises:
            ValueError: Если отдел является пустой строкой
        """
        if not isinstance(value, str):
            raise ValueError("Отдел должен быть строкой")
        if not value.strip():
            raise ValueError("Отдел не может быть пустой строкой")
        self.__department = value
    
    @property
    def base_salary(self) -> float:
        """Геттер для базовой зарплаты сотрудника."""
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value: float):
        """
        Сеттер для базовой зарплаты сотрудника.
        
        Args:
            value: Базовая зарплата
        
        Raises:
            ValueError: Если зарплата не является положительным числом
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Зарплата должна быть числом")
        if value <= 0:
            raise ValueError("Зарплата должна быть положительным числом")
        self.__base_salary = float(value)
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Employee.
        
        Returns:
            Строка с информацией о сотруднике
        """
        return (f"Сотрудник [id: {self.__id}, имя: {self.__name}, "
                f"отдел: {self.__department}, базовая зарплата: {self.__base_salary}]")


if __name__ == "__main__":
    print("=" * 60)
    print("Демонстрация работы класса Employee")
    print("=" * 60)
    
    # Создание объектов с корректными данными
    print("\n1. Создание сотрудников с корректными данными:")
    print("-" * 60)
    
    try:
        employee1 = Employee(1, "Иван Петров", "Разработка", 50000.0)
        print(f"Создан: {employee1}")
        
        employee2 = Employee(2, "Мария Сидорова", "Продажи", 45000.0)
        print(f"Создан: {employee2}")
        
        employee3 = Employee(3, "Алексей Иванов", "Менеджмент", 60000.0)
        print(f"Создан: {employee3}")
    except ValueError as e:
        print(f"Ошибка при создании: {e}")
    
    # Демонстрация работы с геттерами
    print("\n2. Получение значений через свойства (геттеры):")
    print("-" * 60)
    print(f"Сотрудник {employee1.id}: {employee1.name}, отдел: {employee1.department}, зарплата: {employee1.base_salary}")
    print(f"Сотрудник {employee2.id}: {employee2.name}, отдел: {employee2.department}, зарплата: {employee2.base_salary}")
    
    # Демонстрация работы с сеттерами
    print("\n3. Изменение значений через свойства (сеттеры):")
    print("-" * 60)
    try:
        print(f"До изменения: {employee1}")
        employee1.name = "Иван Петрович"
        employee1.department = "Тестирование"
        employee1.base_salary = 55000.0
        print(f"После изменения: {employee1}")
    except ValueError as e:
        print(f"Ошибка при изменении: {e}")
    
    # Демонстрация обработки невалидных данных
    print("\n4. Попытка установки невалидных значений:")
    print("-" * 60)
    
    # Невалидный ID
    try:
        invalid_employee = Employee(-1, "Тест", "Отдел", 10000)
        print(f"ОШИБКА: Не должно быть создано: {invalid_employee}")
    except ValueError as e:
        print(f"Корректно обработана ошибка ID: {e}")
    
    # Пустое имя
    try:
        employee1.name = ""
        print(f"ОШИБКА: Не должно быть установлено пустое имя")
    except ValueError as e:
        print(f"Корректно обработана ошибка имени: {e}")
    
    # Отрицательная зарплата
    try:
        employee1.base_salary = -1000
        print(f"ОШИБКА: Не должна быть установлена отрицательная зарплата")
    except ValueError as e:
        print(f"Корректно обработана ошибка зарплаты: {e}")
    
    # Невалидный тип для ID
    try:
        employee1.id = "не число"
        print(f"ОШИБКА: Не должен быть установлен невалидный тип для ID")
    except ValueError as e:
        print(f"Корректно обработана ошибка типа ID: {e}")
    
    # Вывод всех объектов
    print("\n5. Вывод всех созданных объектов:")
    print("-" * 60)
    employees = [employee1, employee2, employee3]
    for emp in employees:
        print(emp)
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена успешно!")
    print("=" * 60)

