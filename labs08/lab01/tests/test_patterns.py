"""
Часть 5: Тестирование паттернов проектирования
"""

import pytest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Employee, Manager, Developer, Salesperson
from patterns.singleton import DataStorage
from patterns.builder import EmployeeBuilder
from patterns.strategy import PerformanceBonus, SeniorityBonus, ProjectBonus
from patterns.observer import NotificationSystem, EmailNotifier
from patterns.factory import EmployeeFactory


class TestSingleton:
    """Тесты паттерна Singleton"""

    def setup_method(self):
        """Сброс инстанса перед каждым тестом"""
        DataStorage.reset_instance()

    def test_singleton_same_instance(self):
        """Тест: get_instance возвращает один и тот же объект"""
        db1 = DataStorage.get_instance()
        db2 = DataStorage.get_instance()
        assert db1 is db2
        assert id(db1) == id(db2)

    def test_singleton_new_same_instance(self):
        """Тест: __new__ возвращает один и тот же объект"""
        db1 = DataStorage()
        db2 = DataStorage()
        assert db1 is db2

    def test_singleton_add_and_get_employee(self):
        """Тест добавления и получения сотрудника"""
        storage = DataStorage.get_instance()
        emp = Employee(1, "John", "IT", 5000)
        storage.add_employee(emp)

        found = storage.get_employee(1)
        assert found is not None
        assert found.name == "John"

    def test_singleton_remove_employee(self):
        """Тест удаления сотрудника"""
        storage = DataStorage.get_instance()
        emp = Employee(1, "John", "IT", 5000)
        storage.add_employee(emp)
        storage.remove_employee(1)

        assert storage.get_employee(1) is None

    def test_singleton_clear(self):
        """Тест очистки хранилища"""
        storage = DataStorage.get_instance()
        emp = Employee(1, "John", "IT", 5000)
        storage.add_employee(emp)
        storage.clear()

        assert len(storage.get_all_employees()) == 0


class TestBuilder:
    """Тесты паттерна Builder"""

    def test_builder_create_employee(self):
        """Тест создания обычного сотрудника"""
        emp = (EmployeeBuilder()
               .set_id(1)
               .set_name("John")
               .set_department("IT")
               .set_base_salary(5000)
               .build())

        assert emp.id == 1
        assert emp.name == "John"
        assert isinstance(emp, Employee)

    def test_builder_create_manager(self):
        """Тест создания менеджера"""
        manager = (EmployeeBuilder()
                   .set_id(1)
                   .set_name("Alice")
                   .set_department("MAN")
                   .set_base_salary(7000)
                   .set_type("manager")
                   .set_bonus(2000)
                   .build())

        assert isinstance(manager, Manager)
        assert manager.calculate_salary() == 9000

    def test_builder_create_developer(self):
        """Тест создания разработчика через Builder"""
        developer = (EmployeeBuilder()
                     .set_id(101)
                     .set_name("John Doe")
                     .set_department("DEV")
                     .set_base_salary(5000)
                     .set_skills(["Python", "Java"])
                     .set_seniority("senior")
                     .build())

        assert developer.id == 101
        assert developer.name == "John Doe"
        assert isinstance(developer, Developer)
        assert developer.calculate_salary() == 10000

    def test_builder_create_salesperson(self):
        """Тест создания продавца"""
        sp = (EmployeeBuilder()
              .set_id(1)
              .set_name("Bob")
              .set_department("SAL")
              .set_base_salary(4000)
              .set_type("salesperson")
              .set_commission_rate(0.1)
              .set_sales(10000)
              .build())

        assert isinstance(sp, Salesperson)
        assert sp.calculate_salary() == 5000

    def test_builder_fluent_interface(self):
        """Тест fluent-интерфейса (цепочка вызовов)"""
        builder = EmployeeBuilder()
        result = builder.set_id(1).set_name("Test").set_department("IT")
        assert result is builder


class TestStrategy:
    """Тесты паттерна Strategy"""

    def test_performance_bonus_strategy(self):
        """Тест стратегии бонуса за производительность"""
        emp = Employee(1, "John", "IT", 5000)
        strategy = PerformanceBonus(0.2)  # 20%

        emp.set_bonus_strategy(strategy)
        assert emp.calculate_bonus() == 1000
        assert emp.calculate_salary() == 6000

    def test_seniority_bonus_strategy(self):
        """Тест стратегии бонуса за стаж"""
        emp = Employee(1, "John", "IT", 5000)
        strategy = SeniorityBonus(years=3, amount_per_year=1000)

        emp.set_bonus_strategy(strategy)
        assert emp.calculate_bonus() == 3000

    def test_project_bonus_strategy(self):
        """Тест стратегии бонуса за проект"""
        emp = Employee(1, "John", "IT", 5000)
        strategy = ProjectBonus(5000)

        emp.set_bonus_strategy(strategy)
        assert emp.calculate_bonus() == 5000

    def test_change_strategy(self):
        """Тест смены стратегии"""
        emp = Employee(1, "John", "IT", 5000)

        emp.set_bonus_strategy(PerformanceBonus(0.1))
        assert emp.calculate_bonus() == 500

        emp.set_bonus_strategy(SeniorityBonus(years=2, amount_per_year=1500))
        assert emp.calculate_bonus() == 3000


class TestObserver:
    """Тесты паттерна Observer"""

    def test_observer_receives_notification(self):
        """Тест: наблюдатель получает уведомление"""
        emp = Employee(1, "John", "IT", 5000)
        observer = NotificationSystem("TestSystem")

        emp.add_observer(observer)
        emp.base_salary = 6000

        messages = observer.get_messages()
        assert len(messages) > 0

    def test_multiple_observers(self):
        """Тест с несколькими наблюдателями"""
        emp = Employee(1, "John", "IT", 5000)
        observer1 = NotificationSystem("System1")
        observer2 = NotificationSystem("System2")

        emp.add_observer(observer1)
        emp.add_observer(observer2)
        emp.base_salary = 6000

        assert len(observer1.get_messages()) > 0
        assert len(observer2.get_messages()) > 0

    def test_remove_observer(self):
        """Тест удаления наблюдателя"""
        emp = Employee(1, "John", "IT", 5000)
        observer = NotificationSystem("TestSystem")

        emp.add_observer(observer)
        emp.remove_observer(observer)
        emp.base_salary = 6000

        assert len(observer.get_messages()) == 0

    def test_observer_with_mock(self):
        """Тест наблюдателя с mock-объектом"""
        emp = Employee(1, "John", "IT", 5000)
        mock_observer = Mock()

        emp.add_observer(mock_observer)
        emp.base_salary = 6000

        mock_observer.update.assert_called_once()


class TestFactory:
    """Тесты паттерна Factory Method"""

    def test_factory_create_employee(self):
        """Тест фабрики для Employee"""
        factory = EmployeeFactory()
        emp = factory.create_employee("employee", id=1, name="Test",
                                      department="IT", base_salary=5000)
        assert isinstance(emp, Employee)

    def test_factory_create_developer(self):
        """Тест фабрики для Developer"""
        factory = EmployeeFactory()
        emp = factory.create_employee("developer", id=1, name="Test",
                                      department="DEV", base_salary=5000,
                                      skills=["Python"], seniority_level="middle")
        assert isinstance(emp, Developer)
        assert emp.calculate_salary() == 7500

    def test_factory_unknown_type_error(self):
        """Тест: неизвестный тип вызывает ошибку"""
        factory = EmployeeFactory()
        with pytest.raises(ValueError):
            factory.create_employee("unknown", id=1, name="Test",
                                   department="IT", base_salary=5000)


class TestPatternIntegration:
    """Интеграционные тесты паттернов"""

    def setup_method(self):
        DataStorage.reset_instance()

    def test_singleton_with_factory(self):
        """Тест Singleton + Factory"""
        storage = DataStorage.get_instance()
        factory = EmployeeFactory()

        dev = factory.create_employee("developer", id=1, name="John",
                                     department="DEV", base_salary=5000,
                                     skills=["Python"], seniority_level="senior")
        storage.add_employee(dev)

        found = storage.get_employee(1)
        assert found is not None
        assert found.calculate_salary() == 10000

    def test_builder_with_strategy(self):
        """Тест Builder + Strategy"""
        emp = (EmployeeBuilder()
               .set_id(1)
               .set_name("John")
               .set_department("IT")
               .set_base_salary(5000)
               .build())

        emp.set_bonus_strategy(PerformanceBonus(0.2))
        assert emp.calculate_salary() == 6000

    def test_factory_with_observer(self):
        """Тест Factory + Observer"""
        factory = EmployeeFactory()
        emp = factory.create_employee("employee", id=1, name="John",
                                      department="IT", base_salary=5000)

        observer = NotificationSystem("HR")
        emp.add_observer(observer)
        emp.base_salary = 6000

        assert len(observer.get_messages()) > 0

    def test_complex_pattern_interaction(self):
        """Комплексный тест взаимодействия паттернов"""
        DataStorage.reset_instance()

        storage = DataStorage.get_instance()
        factory = EmployeeFactory()

        dev = factory.create_employee("developer", id=1, name="John",
                                     department="DEV", base_salary=5000,
                                     skills=["Python"], seniority_level="senior")
        manager = (EmployeeBuilder()
                   .set_id(2)
                   .set_name("Alice")
                   .set_department("MAN")
                   .set_base_salary(7000)
                   .set_type("manager")
                   .set_bonus(2000)
                   .build())

        storage.add_employee(dev)
        storage.add_employee(manager)

        all_employees = storage.get_all_employees()
        assert len(all_employees) == 2

        total = sum(e.calculate_salary() for e in all_employees)
        assert total == 19000
