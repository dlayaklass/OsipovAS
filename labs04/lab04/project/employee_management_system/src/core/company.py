"""
Модуль для работы с классом Company (Компания).
Реализует агрегацию - компания содержит отделы и проекты.
Включает методы экспорта, анализа данных и планирования.
"""

import json
import csv
from typing import Optional
from datetime import datetime
from .department import Department
from .project import Project
from .abstract_employee import AbstractEmployee
from ..utils.exceptions import (
    DepartmentNotFoundError, 
    ProjectNotFoundError, 
    EmployeeNotFoundError,
    DuplicateIdError
)


class Company:
    """
    Класс Company представляет компанию.
    
    Использует агрегацию - содержит отделы и проекты, которые могут существовать независимо.
    """
    
    def __init__(self, name: str):
        """
        Конструктор класса Company.
        
        Args:
            name: Название компании
        """
        self.__name = name
        self.__departments: list[Department] = []
        self.__projects: list[Project] = []
        self.__employee_ids: set[int] = set()  # Для проверки уникальности ID
        self.__project_ids: set[int] = set()   # Для проверки уникальности ID проектов
    
    @property
    def name(self) -> str:
        """Геттер для названия компании."""
        return self.__name
    
    def _check_employee_id_unique(self, employee_id: int) -> None:
        """Проверяет уникальность ID сотрудника."""
        if employee_id in self.__employee_ids:
            raise DuplicateIdError(f"Сотрудник с ID {employee_id} уже существует")
        self.__employee_ids.add(employee_id)
    
    def _check_project_id_unique(self, project_id: int) -> None:
        """Проверяет уникальность ID проекта."""
        if project_id in self.__project_ids:
            raise DuplicateIdError(f"Проект с ID {project_id} уже существует")
        self.__project_ids.add(project_id)
    
    def add_department(self, department: Department) -> None:
        """Добавляет отдел в компанию."""
        if department not in self.__departments:
            self.__departments.append(department)
            # Проверяем уникальность ID всех сотрудников отдела
            for emp in department.get_employees():
                self._check_employee_id_unique(emp.id)
    
    def remove_department(self, department_name: str) -> None:
        """Удаляет отдел из компании."""
        dept = self.find_department(department_name)
        if dept:
            if len(dept) > 0:
                raise ValueError(f"Нельзя удалить отдел '{department_name}': в нем есть сотрудники")
            self.__departments.remove(dept)
        else:
            raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
    
    def get_departments(self) -> list[Department]:
        """Возвращает список отделов."""
        return self.__departments.copy()
    
    def add_project(self, project: Project) -> None:
        """Добавляет проект в компанию."""
        if project not in self.__projects:
            self._check_project_id_unique(project.project_id)
            self.__projects.append(project)
    
    def remove_project(self, project_id: int) -> None:
        """Удаляет проект из компании."""
        project = self.find_project(project_id)
        if project:
            if project.get_team_size() > 0:
                raise ValueError(f"Нельзя удалить проект '{project.name}': над ним работает команда")
            self.__projects.remove(project)
            self.__project_ids.discard(project_id)
        else:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")
    
    def get_projects(self) -> list[Project]:
        """Возвращает список проектов."""
        return self.__projects.copy()
    
    def get_all_employees(self) -> list[AbstractEmployee]:
        """Возвращает всех сотрудников компании."""
        employees = []
        for dept in self.__departments:
            employees.extend(dept.get_employees())
        return employees
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Находит сотрудника по ID во всех отделах."""
        for dept in self.__departments:
            emp = dept.find_employee_by_id(employee_id)
            if emp:
                return emp
        return None
    
    def find_department(self, name: str) -> Optional[Department]:
        """Находит отдел по названию."""
        for dept in self.__departments:
            if dept.name == name:
                return dept
        return None
    
    def find_project(self, project_id: int) -> Optional[Project]:
        """Находит проект по ID."""
        for project in self.__projects:
            if project.project_id == project_id:
                return project
        return None
    
    def calculate_total_monthly_cost(self) -> float:
        """Рассчитывает общие месячные затраты на зарплаты."""
        return sum(dept.calculate_total_salary() for dept in self.__departments)
    
    def get_projects_by_status(self, status: str) -> list[Project]:
        """Фильтрует проекты по статусу."""
        return [p for p in self.__projects if p.status == status]
    
    def transfer_employee_between_departments(self, employee_id: int, 
                                             from_dept_name: str, 
                                             to_dept_name: str) -> None:
        """
        Переносит сотрудника между отделами.
        
        Args:
            employee_id: ID сотрудника
            from_dept_name: Название отдела-источника
            to_dept_name: Название отдела-назначения
        
        Raises:
            EmployeeNotFoundError: Если сотрудник не найден
            DepartmentNotFoundError: Если отдел не найден
        """
        from_dept = self.find_department(from_dept_name)
        to_dept = self.find_department(to_dept_name)
        
        if not from_dept:
            raise DepartmentNotFoundError(f"Отдел '{from_dept_name}' не найден")
        if not to_dept:
            raise DepartmentNotFoundError(f"Отдел '{to_dept_name}' не найден")
        
        employee = from_dept.find_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе '{from_dept_name}'")
        
        from_dept.remove_employee(employee_id)
        to_dept.add_employee(employee)
        employee.department = to_dept_name
    
    def assign_employee_to_project(self, employee_id: int, project_id: int) -> bool:
        """
        Назначает сотрудника на проект.
        
        Args:
            employee_id: ID сотрудника
            project_id: ID проекта
        
        Returns:
            True, если назначение успешно, False иначе
        """
        employee = self.find_employee_by_id(employee_id)
        project = self.find_project(project_id)
        
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        if not project:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")
        
        if employee not in project.get_team():
            project.add_team_member(employee)
            return True
        return False
    
    def check_employee_availability(self, employee_id: int) -> bool:
        """
        Проверяет доступность сотрудника (не перегружен ли он).
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            True, если сотрудник доступен (участвует менее чем в 3 проектах)
        """
        employee = self.find_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        
        project_count = sum(1 for proj in self.__projects if employee in proj.get_team())
        return project_count < 3
    
    def find_overloaded_employees(self) -> list[AbstractEmployee]:
        """
        Находит перегруженных сотрудников (участвующих в 3+ проектах).
        
        Returns:
            Список перегруженных сотрудников
        """
        overloaded = []
        all_employees = self.get_all_employees()
        
        for emp in all_employees:
            project_count = sum(1 for proj in self.__projects if emp in proj.get_team())
            if project_count >= 3:
                overloaded.append(emp)
        
        return overloaded
    
    def get_department_stats(self) -> dict:
        """
        Возвращает статистику по отделам.
        
        Returns:
            Словарь со статистикой по каждому отделу
        """
        stats = {}
        for dept in self.__departments:
            employees = dept.get_employees()
            stats[dept.name] = {
                "employee_count": len(employees),
                "total_salary": dept.calculate_total_salary(),
                "average_salary": dept.calculate_total_salary() / len(employees) if employees else 0,
                "employee_types": dept.get_employee_count()
            }
        return stats
    
    def get_project_budget_analysis(self) -> dict:
        """
        Анализирует бюджеты проектов.
        
        Returns:
            Словарь с анализом бюджетов
        """
        analysis = {
            "total_projects": len(self.__projects),
            "total_budget": sum(proj.calculate_total_salary() for proj in self.__projects),
            "by_status": {},
            "average_team_size": 0,
            "projects": []
        }
        
        total_team_size = 0
        for proj in self.__projects:
            team_size = proj.get_team_size()
            total_team_size += team_size
            budget = proj.calculate_total_salary()
            
            status = proj.status
            if status not in analysis["by_status"]:
                analysis["by_status"][status] = {"count": 0, "total_budget": 0}
            analysis["by_status"][status]["count"] += 1
            analysis["by_status"][status]["total_budget"] += budget
            
            analysis["projects"].append({
                "id": proj.project_id,
                "name": proj.name,
                "status": status,
                "team_size": team_size,
                "budget": budget
            })
        
        analysis["average_team_size"] = total_team_size / len(self.__projects) if self.__projects else 0
        return analysis
    
    def export_employees_csv(self, filename: str) -> None:
        """
        Экспортирует отчет по сотрудникам в CSV.
        
        Args:
            filename: Имя файла для сохранения
        """
        employees = self.get_all_employees()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'Имя', 'Отдел', 'Тип', 'Базовая зарплата', 
                'Итоговая зарплата', 'Дополнительная информация'
            ])
            
            for emp in employees:
                emp_type = emp.__class__.__name__
                additional_info = ""
                
                if emp_type == "Manager":
                    additional_info = f"Бонус: {emp.bonus}"
                elif emp_type == "Developer":
                    additional_info = f"Уровень: {emp.seniority_level}, Технологии: {', '.join(emp.tech_stack)}"
                elif emp_type == "Salesperson":
                    additional_info = f"Комиссия: {emp.commission_rate*100}%, Продажи: {emp.sales_volume}"
                
                writer.writerow([
                    emp.id,
                    emp.name,
                    emp.department,
                    emp_type,
                    emp.base_salary,
                    emp.calculate_salary(),
                    additional_info
                ])
    
    def export_projects_csv(self, filename: str) -> None:
        """
        Экспортирует отчет по проектам в CSV.
        
        Args:
            filename: Имя файла для сохранения
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID проекта', 'Название', 'Описание', 'Статус', 
                'Срок', 'Размер команды', 'Бюджет', 'Состав команды'
            ])
            
            for proj in self.__projects:
                team_members = ', '.join([emp.name for emp in proj.get_team()])
                writer.writerow([
                    proj.project_id,
                    proj.name,
                    proj.description,
                    proj.status,
                    proj.deadline.strftime('%Y-%m-%d'),
                    proj.get_team_size(),
                    proj.calculate_total_salary(),
                    team_members
                ])
    
    def generate_financial_report(self) -> str:
        """
        Генерирует текстовый отчет по финансовым показателям компании.
        
        Returns:
            Строка с финансовым отчетом
        """
        report = []
        report.append("=" * 80)
        report.append(f"ФИНАНСОВЫЙ ОТЧЕТ КОМПАНИИ: {self.__name}")
        report.append("=" * 80)
        report.append("")
        
        # Общая информация
        report.append(f"Общие месячные затраты: {self.calculate_total_monthly_cost():.2f}")
        report.append(f"Количество отделов: {len(self.__departments)}")
        report.append(f"Количество проектов: {len(self.__projects)}")
        report.append(f"Общее количество сотрудников: {len(self.get_all_employees())}")
        report.append("")
        
        # Статистика по отделам
        report.append("СТАТИСТИКА ПО ОТДЕЛАМ:")
        report.append("-" * 80)
        dept_stats = self.get_department_stats()
        for dept_name, stats in dept_stats.items():
            report.append(f"  {dept_name}:")
            report.append(f"    Сотрудников: {stats['employee_count']}")
            report.append(f"    Общая зарплата: {stats['total_salary']:.2f}")
            report.append(f"    Средняя зарплата: {stats['average_salary']:.2f}")
            report.append(f"    Типы сотрудников: {stats['employee_types']}")
        report.append("")
        
        # Анализ проектов
        report.append("АНАЛИЗ ПРОЕКТОВ:")
        report.append("-" * 80)
        proj_analysis = self.get_project_budget_analysis()
        report.append(f"  Всего проектов: {proj_analysis['total_projects']}")
        report.append(f"  Общий бюджет проектов: {proj_analysis['total_budget']:.2f}")
        report.append(f"  Средний размер команды: {proj_analysis['average_team_size']:.2f}")
        report.append("  По статусам:")
        for status, data in proj_analysis['by_status'].items():
            report.append(f"    {status}: {data['count']} проектов, бюджет: {data['total_budget']:.2f}")
        report.append("")
        
        # Перегруженные сотрудники
        overloaded = self.find_overloaded_employees()
        if overloaded:
            report.append("ПЕРЕГРУЖЕННЫЕ СОТРУДНИКИ (участвуют в 3+ проектах):")
            report.append("-" * 80)
            for emp in overloaded:
                project_count = sum(1 for proj in self.__projects if emp in proj.get_team())
                report.append(f"  {emp.name} (ID: {emp.id}): участвует в {project_count} проектах")
        report.append("")
        
        report.append("=" * 80)
        return "\n".join(report)
    
    def save_to_json(self, filename: str) -> None:
        """Сохраняет всю компанию в JSON файл."""
        data = {
            "name": self.__name,
            "departments": [
                {
                    "name": dept.name,
                    "employees": [emp.to_dict() for emp in dept.get_employees()]
                }
                for dept in self.__departments
            ],
            "projects": [proj.to_dict() for proj in self.__projects]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_json(cls, filename: str) -> 'Company':
        """Загружает компанию из JSON файла."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        company = cls(data["name"])
        
        # Импортируем классы
        from .employee import Employee
        from ..employees.manager import Manager
        from ..employees.developer import Developer
        from ..employees.salesperson import Salesperson
        
        # Загружаем отделы
        for dept_data in data["departments"]:
            dept = Department(dept_data["name"])
            for emp_data in dept_data["employees"]:
                emp_type = emp_data.get("type", "Employee")
                if emp_type == "Manager":
                    emp = Manager.from_dict(emp_data)
                elif emp_type == "Developer":
                    emp = Developer.from_dict(emp_data)
                elif emp_type == "Salesperson":
                    emp = Salesperson.from_dict(emp_data)
                else:
                    emp = Employee.from_dict(emp_data)
                dept.add_employee(emp)
                company.__employee_ids.add(emp.id)
            company.add_department(dept)
        
        # Загружаем проекты
        for proj_data in data["projects"]:
            project = Project.from_dict(proj_data)
            company.__project_ids.add(project.project_id)
            # Восстанавливаем команду
            for emp_data in proj_data["team"]:
                emp_id = emp_data["id"]
                emp = company.find_employee_by_id(emp_id)
                if emp:
                    project.add_team_member(emp)
            company.add_project(project)
        
        return company
