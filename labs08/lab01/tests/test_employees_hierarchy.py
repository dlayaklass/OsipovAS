"""
Часть 2: Тестирование наследования и абстрактных классов
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Employee, Manager, Developer, Salesperson
from models.abstract_employee import AbstractEmployee
from patterns.factory import EmployeeFactory


class TestAbstractEmployee:
    """Тесты для абстрактного класса"""

    def test_cannot_instantiate_abstract_class(self):
        """Нельзя создать экземпляр AbstractEmployee"""
        with pytest.raises(TypeError):
            AbstractEmployee(1, "Test", "IT", 5000)


class TestManager:
    """Тесты для класса Manager"""

    def test_manager_salary_calculation(self):
        """Тест расчета зарплаты менеджера"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        salary = manager.calculate_salary()
        assert salary == 6000

    def test_manager_get_info_includes_bonus(self):
        """Тест: get_info содержит информацию о бонусе"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        info = manager.get_info()
        assert "1000" in info
        assert "6000" in info

    def test_manager_invalid_bonus(self):
        """Тест: отрицательный бонус вызывает ошибку"""
        with pytest.raises(ValueError):
            Manager(1, "John", "Management", 5000, -1000)

    def test_manager_bonus_setter(self):
        """Тест сеттера бонуса"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        manager.bonus = 2000
        assert manager.bonus == 2000
        assert manager.calculate_salary() == 7000


class TestDeveloper:
    """Тесты для класса Developer"""

    def test_developer_junior_salary(self):
        """Тест зарплаты junior разработчика"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        assert dev.calculate_salary() == 5000

    def test_developer_middle_salary(self):
        """Тест зарплаты middle разработчика"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "middle")
        assert dev.calculate_salary() == 7500

    def test_developer_senior_salary(self):
        """Тест зарплаты senior разработчика"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "senior")
        assert dev.calculate_salary() == 10000

    @pytest.mark.parametrize("level,expected_salary", [
        ("junior", 5000),
        ("middle", 7500),
        ("senior", 10000)
    ])
    def test_developer_salary_by_level(self, level, expected_salary):
        """Параметризованный тест зарплат по уровню"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], level)
        assert dev.calculate_salary() == expected_salary

    def test_developer_add_skill(self):
        """Тест добавления навыка"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        dev.add_skill("Java")
        assert "Java" in dev.tech_stack
        assert len(dev.tech_stack) == 2

    def test_developer_add_duplicate_skill(self):
        """Тест: дубликат навыка не добавляется"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        dev.add_skill("Python")
        assert dev.tech_stack.count("Python") == 1

    def test_developer_get_info_includes_skills(self):
        """Тест: get_info содержит информацию о навыках"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "Java"], "senior")
        info = dev.get_info()
        assert "Python" in info
        assert "Java" in info
        assert "senior" in info


class TestSalesperson:
    """Тесты для класса Salesperson"""

    def test_salesperson_salary_with_commission(self):
        """Тест зарплаты с комиссией"""
        sp = Salesperson(1, "Bob", "Sales", 4000, 0.1, 10000)
        assert sp.calculate_salary() == 5000  # 4000 + 10000*0.1

    def test_salesperson_update_sales(self):
        """Тест обновления продаж"""
        sp = Salesperson(1, "Bob", "Sales", 4000, 0.1, 10000)
        sp.update_sales(5000)
        assert sp.sales == 15000
        assert sp.calculate_salary() == 5500

    def test_salesperson_get_info_includes_commission(self):
        """Тест: get_info содержит информацию о комиссии"""
        sp = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        info = sp.get_info()
        assert "7500" in info  # комиссия 50000*0.15


class TestEmployeeFactory:
    """Тесты для EmployeeFactory"""

    def test_factory_create_employee(self):
        """Тест создания обычного сотрудника"""
        factory = EmployeeFactory()
        emp = factory.create_employee("employee", id=1, name="Test",
                                      department="IT", base_salary=5000)
        assert isinstance(emp, Employee)
        assert emp.calculate_salary() == 5000

    def test_factory_create_manager(self):
        """Тест создания менеджера"""
        factory = EmployeeFactory()
        emp = factory.create_employee("manager", id=1, name="Test",
                                      department="MAN", base_salary=5000, bonus=1000)
        assert isinstance(emp, Manager)
        assert emp.calculate_salary() == 6000

    def test_factory_create_developer(self):
        """Тест создания разработчика"""
        factory = EmployeeFactory()
        emp = factory.create_employee("developer", id=1, name="Test",
                                      department="DEV", base_salary=5000,
                                      skills=["Python"], seniority_level="middle")
        assert isinstance(emp, Developer)
        assert emp.calculate_salary() == 7500

    def test_factory_create_salesperson(self):
        """Тест создания продавца"""
        factory = EmployeeFactory()
        emp = factory.create_employee("salesperson", id=1, name="Test",
                                      department="SAL", base_salary=4000,
                                      commission_rate=0.1, sales=10000)
        assert isinstance(emp, Salesperson)
        assert emp.calculate_salary() == 5000

    def test_factory_unknown_type(self):
        """Тест: неизвестный тип вызывает ошибку"""
        factory = EmployeeFactory()
        with pytest.raises(ValueError):
            factory.create_employee("unknown", id=1, name="Test",
                                   department="IT", base_salary=5000)


class TestPolymorphism:
    """Тесты полиморфного поведения"""

    def test_polymorphic_salary_calculation(self):
        """Тест полиморфного расчета зарплаты"""
        employees = [
            Employee(1, "Alice", "IT", 5000),
            Manager(2, "Bob", "MAN", 5000, 1000),
            Developer(3, "Charlie", "DEV", 5000, ["Python"], "senior"),
            Salesperson(4, "Diana", "SAL", 5000, 0.1, 10000)
        ]

        salaries = [emp.calculate_salary() for emp in employees]

        assert salaries[0] == 5000   # Employee
        assert salaries[1] == 6000   # Manager: 5000 + 1000
        assert salaries[2] == 10000  # Developer senior: 5000 * 2
        assert salaries[3] == 6000   # Salesperson: 5000 + 10000*0.1

    def test_all_employees_have_get_info(self):
        """Тест: все типы сотрудников имеют метод get_info"""
        employees = [
            Employee(1, "Alice", "IT", 5000),
            Manager(2, "Bob", "MAN", 5000, 1000),
            Developer(3, "Charlie", "DEV", 5000, ["Python"], "senior"),
            Salesperson(4, "Diana", "SAL", 5000, 0.1, 10000)
        ]

        for emp in employees:
            info = emp.get_info()
            assert isinstance(info, str)
            assert len(info) > 0
