"""
Часть 4: Тестирование композиции, агрегации и сложных структур
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Employee, Manager, Developer, Salesperson
from models import Department, Project, Company
from models.department import DuplicateIdError
from models.project import InvalidStatusError


class TestProject:
    """Тесты класса Project"""

    def test_project_creation(self):
        """Тест создания проекта"""
        project = Project(1, "AI Platform", "Разработка AI", "2024-12-31", "planning")
        assert project.id == 1
        assert project.name == "AI Platform"
        assert project.status == "planning"

    def test_project_team_management(self):
        """Тест управления командой проекта"""
        project = Project(1, "AI Platform", "Разработка", "2024-12-31", "planning")
        dev = Developer(1, "John", "DEV", 5000, ["Python"], "senior")

        project.add_team_member(dev)
        assert len(project.get_team()) == 1
        assert project.get_team_size() == 1

        project.remove_team_member(1)
        assert len(project.get_team()) == 0

    def test_project_total_salary(self):
        """Тест расчета суммарной зарплаты команды"""
        project = Project(1, "AI Platform", "Разработка", "2024-12-31", "planning")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")

        project.add_team_member(manager)
        project.add_team_member(developer)

        total = project.calculate_total_salary()
        expected = manager.calculate_salary() + developer.calculate_salary()
        assert total == expected

    def test_project_invalid_status_raises_error(self):
        """Тест: неверный статус вызывает ошибку"""
        with pytest.raises(InvalidStatusError):
            Project(1, "Test", "Test", "2024-12-31", "invalid")

    @pytest.mark.parametrize("invalid_status", ["invalid", "done", "in_progress"])
    def test_project_invalid_statuses(self, invalid_status):
        """Параметризованный тест невалидных статусов"""
        with pytest.raises(InvalidStatusError):
            Project(1, "Test", "Test", "2024-12-31", invalid_status)

    def test_project_valid_statuses(self):
        """Тест валидных статусов"""
        for status in ["planning", "active", "completed", "cancelled"]:
            project = Project(1, "Test", "Test", "2024-12-31", status)
            assert project.status == status


class TestCompany:
    """Тесты класса Company"""

    def test_company_department_management(self):
        """Тест управления отделами"""
        company = Company("TechCorp")
        dept = Department("Development")

        company.add_department(dept)
        assert len(company.get_departments()) == 1

        company.remove_department("Development")
        assert len(company.get_departments()) == 0

    def test_company_find_employee(self):
        """Тест поиска сотрудника"""
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)

        dept.add_employee(emp)
        company.add_department(dept)

        found = company.find_employee_by_id(1)
        assert found is not None
        assert found.name == "John"

    def test_company_find_employee_not_found(self):
        """Тест поиска несуществующего сотрудника"""
        company = Company("TechCorp")
        found = company.find_employee_by_id(999)
        assert found is None

    def test_cannot_delete_department_with_employees(self):
        """Тест: нельзя удалить отдел с сотрудниками"""
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)

        dept.add_employee(emp)
        company.add_department(dept)

        with pytest.raises(ValueError, match="Cannot delete department with employees"):
            company.remove_department("Development")


class TestDuplicateId:
    """Тесты дублирования ID"""

    def test_duplicate_employee_id_raises_error(self):
        """Тест: дублирование ID вызывает ошибку"""
        dept = Department("Development")
        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(1, "Jane", "DEV", 6000)

        dept.add_employee(emp1)
        with pytest.raises(DuplicateIdError):
            dept.add_employee(emp2)


class TestCompanySerialization:
    """Тесты сериализации компании"""

    def test_company_save_and_load(self, tmp_path):
        """Тест сохранения и загрузки компании"""
        company = Company("TechCorp")
        dept = Department("Development")
        company.add_department(dept)

        filename = tmp_path / "test_company.json"
        company.save_to_json(str(filename))

        loaded = Company.load_from_json(str(filename))
        assert loaded.name == "TechCorp"


class TestCompanyStatistics:
    """Тесты статистики компании"""

    def test_department_statistics(self):
        """Тест статистики по отделам"""
        company = Company("TechCorp")
        dept = Department("Development")
        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(2, "Jane", "DEV", 6000)

        dept.add_employee(emp1)
        dept.add_employee(emp2)
        company.add_department(dept)

        stats = company.get_department_stats()
        assert "Development" in stats
        assert stats["Development"]["employee_count"] == 2
        assert stats["Development"]["total_salary"] == 11000


class TestComplexCompanyStructure:
    """Тесты сложной структуры компании"""

    def test_complex_company_structure(self):
        """Комплексный тест структуры компании"""
        company = Company("TechInnovations")

        dev_department = Department("Development")
        sales_department = Department("Sales")

        manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
        developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
        salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)

        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)

        company.add_department(dev_department)
        company.add_department(sales_department)

        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3

    def test_company_total_monthly_cost(self):
        """Тест общих расходов компании"""
        company = Company("TechCorp")
        dept = Department("Development")

        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")

        dept.add_employee(manager)
        dept.add_employee(developer)
        company.add_department(dept)

        expected = manager.calculate_salary() + developer.calculate_salary()
        assert company.calculate_total_monthly_cost() == expected

    def test_get_all_employees(self):
        """Тест получения всех сотрудников"""
        company = Company("TechCorp")
        dept1 = Department("Development")
        dept2 = Department("Sales")

        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(2, "Jane", "SAL", 4000)

        dept1.add_employee(emp1)
        dept2.add_employee(emp2)
        company.add_department(dept1)
        company.add_department(dept2)

        all_employees = company.get_all_employees()
        assert len(all_employees) == 2
