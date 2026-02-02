"""
Часть 3: Тестирование полиморфизма и магических методов
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Employee, Manager, Developer, Salesperson, Department


class TestEmployeeMagicMethods:
    """Тесты магических методов сотрудников"""

    def test_employee_equality_same_id(self):
        """Тест равенства по ID"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 4000)
        assert emp1 == emp2

    def test_employee_not_equal_different_id(self):
        """Тест неравенства по ID"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 5000)
        assert emp1 != emp2

    def test_employee_salary_comparison_lt(self):
        """Тест сравнения зарплат (<)"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        assert emp1 < emp2

    def test_employee_salary_comparison_gt(self):
        """Тест сравнения зарплат (>)"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        assert emp2 > emp1

    def test_employee_addition(self):
        """Тест сложения зарплат"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        assert emp1 + emp2 == 11000

    def test_employee_str(self):
        """Тест строкового представления"""
        emp = Employee(1, "John", "IT", 5000)
        result = str(emp)
        assert "1" in result
        assert "John" in result
        assert "IT" in result
        assert "5000" in result


class TestDepartmentBasic:
    """Базовые тесты Department"""

    def test_department_add_employee(self):
        """Тест добавления сотрудника"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        assert len(dept.get_employees()) == 1

    def test_department_remove_employee(self):
        """Тест удаления сотрудника"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        dept.remove_employee(1)
        assert len(dept.get_employees()) == 0

    def test_department_find_employee_by_id(self):
        """Тест поиска сотрудника по ID"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        found = dept.find_employee_by_id(1)
        assert found is not None
        assert found.name == "John"

    def test_department_find_employee_not_found(self):
        """Тест поиска несуществующего сотрудника"""
        dept = Department("IT")
        found = dept.find_employee_by_id(999)
        assert found is None


class TestDepartmentPolymorphism:
    """Тесты полиморфного поведения в отделе"""

    def test_department_calculate_total_salary(self):
        """Тест полиморфного расчета общей зарплаты"""
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        dept.add_employee(manager)
        dept.add_employee(developer)

        total = dept.calculate_total_salary()
        expected = manager.calculate_salary() + developer.calculate_salary()
        assert total == expected

    def test_department_get_employee_count(self):
        """Тест подсчета сотрудников по типам"""
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        emp = Employee(3, "Charlie", "DEV", 4000)

        dept.add_employee(manager)
        dept.add_employee(developer)
        dept.add_employee(emp)

        counts = dept.get_employee_count()
        assert counts["Manager"] == 1
        assert counts["Developer"] == 1
        assert counts["Employee"] == 1


class TestDepartmentMagicMethods:
    """Тесты магических методов Department"""

    def test_department_len(self):
        """Тест __len__"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        assert len(dept) == 1

    def test_department_getitem(self):
        """Тест __getitem__"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        assert dept[0] == emp

    def test_department_contains(self):
        """Тест __contains__"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        assert emp in dept

    def test_department_iteration(self):
        """Тест итерации по отделу"""
        dept = Department("IT")
        employees = [Employee(i, f"Emp{i}", "IT", 5000) for i in range(3)]
        for emp in employees:
            dept.add_employee(emp)

        count = 0
        for _ in dept:
            count += 1
        assert count == 3


class TestDeveloperIteration:
    """Тесты итерации по навыкам разработчика"""

    def test_developer_skills_iteration(self):
        """Тест итерации по стеку технологий"""
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java", "SQL"], "senior")
        skills = []
        for skill in dev:
            skills.append(skill)
        assert skills == ["Python", "Java", "SQL"]


class TestEmployeeSerialization:
    """Тесты сериализации сотрудников"""

    def test_employee_to_dict(self):
        """Тест сериализации в словарь"""
        emp = Employee(1, "John", "IT", 5000)
        data = emp.to_dict()
        assert data["id"] == 1
        assert data["name"] == "John"
        assert data["department"] == "IT"
        assert data["base_salary"] == 5000

    def test_employee_from_dict(self):
        """Тест десериализации из словаря"""
        data = {"id": 1, "name": "John", "department": "IT", "base_salary": 5000}
        emp = Employee.from_dict(data)
        assert emp.id == 1
        assert emp.name == "John"

    def test_employee_serialization_roundtrip(self):
        """Тест полного цикла сериализации"""
        emp = Employee(1, "John", "IT", 5000)
        data = emp.to_dict()
        new_emp = Employee.from_dict(data)
        assert new_emp.id == emp.id
        assert new_emp.name == emp.name


class TestEmployeeSorting:
    """Тесты сортировки сотрудников"""

    def test_employee_sorting_by_name(self):
        """Тест сортировки по имени"""
        employees = [
            Employee(3, "Charlie", "IT", 7000),
            Employee(1, "Alice", "HR", 5000),
            Employee(2, "Bob", "IT", 6000)
        ]
        sorted_by_name = sorted(employees, key=lambda x: x.name)
        assert sorted_by_name[0].name == "Alice"
        assert sorted_by_name[1].name == "Bob"
        assert sorted_by_name[2].name == "Charlie"

    def test_employee_sorting_by_salary(self):
        """Тест сортировки по зарплате"""
        employees = [
            Employee(3, "Charlie", "IT", 7000),
            Employee(1, "Alice", "HR", 5000),
            Employee(2, "Bob", "IT", 6000)
        ]
        sorted_by_salary = sorted(employees, key=lambda x: x.calculate_salary())
        assert sorted_by_salary[0].calculate_salary() == 5000
        assert sorted_by_salary[1].calculate_salary() == 6000
        assert sorted_by_salary[2].calculate_salary() == 7000


class TestDepartmentIntegration:
    """Интеграционные тесты отдела"""

    def test_department_integration(self):
        """Комплексный тест отдела"""
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")

        dept.add_employee(manager)
        dept.add_employee(developer)

        total_salary = dept.calculate_total_salary()
        expected = manager.calculate_salary() + developer.calculate_salary()

        assert total_salary == expected
        assert dept.get_employee_count()["Manager"] == 1
        assert dept.get_employee_count()["Developer"] == 1
