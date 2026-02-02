"""
Часть 1: Тестирование инкапсуляции и базового класса Employee
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Employee


class TestEmployee:
    """Тесты для класса Employee"""

    def test_employee_creation_valid_data(self):
        """Тест создания сотрудника с валидными данными"""
        emp = Employee(1, "Alice", "IT", 5000)

        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000

    def test_employee_invalid_id_raises_error(self):
        """Тест: отрицательный ID вызывает ValueError"""
        with pytest.raises(ValueError):
            Employee(-1, "Alice", "IT", 5000)

    def test_employee_invalid_salary_raises_error(self):
        """Тест: отрицательная зарплата вызывает ValueError"""
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", -5000)

    def test_employee_empty_name_raises_error(self):
        """Тест: пустое имя вызывает ValueError"""
        with pytest.raises(ValueError):
            Employee(1, "", "IT", 5000)

    def test_employee_whitespace_name_raises_error(self):
        """Тест: имя из пробелов вызывает ValueError"""
        with pytest.raises(ValueError):
            Employee(1, "   ", "IT", 5000)

    def test_employee_calculate_salary(self):
        """Тест расчета зарплаты обычного сотрудника"""
        emp = Employee(1, "Alice", "IT", 5000)
        salary = emp.calculate_salary()
        assert salary == 5000

    def test_employee_str_representation(self):
        """Тест строкового представления"""
        emp = Employee(1, "Alice", "IT", 5000)
        result = str(emp)
        assert "id: 1" in result
        assert "Alice" in result
        assert "IT" in result
        assert "5000" in result

    def test_employee_get_info(self):
        """Тест метода get_info"""
        emp = Employee(1, "Alice", "IT", 5000)
        info = emp.get_info()
        assert "5000" in info
        assert "Alice" in info

    @pytest.mark.parametrize("emp_id,name,dept,salary", [
        (1, "Alice", "IT", 5000),
        (100, "Bob", "HR", 3000),
        (999, "Charlie", "DEV", 10000),
    ])
    def test_employee_parametrized_creation(self, emp_id, name, dept, salary):
        """Параметризованный тест создания сотрудников"""
        emp = Employee(emp_id, name, dept, salary)
        assert emp.id == emp_id
        assert emp.name == name
        assert emp.department == dept
        assert emp.base_salary == salary

    @pytest.mark.parametrize("invalid_id", [-1, -100, -999])
    def test_employee_invalid_ids(self, invalid_id):
        """Параметризованный тест невалидных ID"""
        with pytest.raises(ValueError):
            Employee(invalid_id, "Alice", "IT", 5000)

    @pytest.mark.parametrize("invalid_salary", [-1, -100, -5000])
    def test_employee_invalid_salaries(self, invalid_salary):
        """Параметризованный тест невалидных зарплат"""
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", invalid_salary)

    def test_employee_setter_id_invalid(self):
        """Тест сеттера id с невалидным значением"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(ValueError):
            emp.id = -5

    def test_employee_setter_salary_invalid(self):
        """Тест сеттера base_salary с невалидным значением"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(ValueError):
            emp.base_salary = -1000

    def test_employee_setter_name_empty(self):
        """Тест сеттера name с пустой строкой"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(ValueError):
            emp.name = ""

    def test_employee_zero_id_allowed(self):
        """Тест: ID равный 0 разрешен"""
        emp = Employee(0, "Alice", "IT", 5000)
        assert emp.id == 0

    def test_employee_zero_salary_allowed(self):
        """Тест: зарплата 0 разрешена"""
        emp = Employee(1, "Alice", "IT", 0)
        assert emp.base_salary == 0
