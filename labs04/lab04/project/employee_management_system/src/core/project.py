"""
Модуль для работы с классом Project (Проект).
Реализует композицию - проект содержит команду сотрудников.
"""

from datetime import datetime
from .abstract_employee import AbstractEmployee
from ..utils.exceptions import InvalidStatusError


class Project:
    """
    Класс Project представляет проект компании.
    
    Использует композицию - содержит список сотрудников команды проекта.
    """
    
    VALID_STATUSES = ["planning", "active", "completed", "cancelled"]
    
    def __init__(self, project_id: int, name: str, description: str, 
                 deadline: str, status: str = "planning"):
        """
        Конструктор класса Project.
        
        Args:
            project_id: Уникальный идентификатор проекта
            name: Название проекта
            description: Описание проекта
            deadline: Срок выполнения (строка в формате YYYY-MM-DD)
            status: Статус проекта
        """
        self.__project_id = project_id
        self.__name = name
        self.__description = description
        self.__deadline = datetime.strptime(deadline, "%Y-%m-%d")
        self.__status = status
        self.__team: list[AbstractEmployee] = []
        
        # Валидация
        if status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Невалидный статус: {status}. Допустимые: {self.VALID_STATUSES}")
    
    @property
    def project_id(self) -> int:
        """Геттер для ID проекта."""
        return self.__project_id
    
    @property
    def name(self) -> str:
        """Геттер для названия проекта."""
        return self.__name
    
    @property
    def description(self) -> str:
        """Геттер для описания проекта."""
        return self.__description
    
    @property
    def deadline(self) -> datetime:
        """Геттер для срока выполнения."""
        return self.__deadline
    
    @property
    def status(self) -> str:
        """Геттер для статуса проекта."""
        return self.__status
    
    def add_team_member(self, employee: AbstractEmployee) -> None:
        """Добавляет сотрудника в команду проекта."""
        if employee not in self.__team:
            self.__team.append(employee)
    
    def remove_team_member(self, employee_id: int) -> None:
        """Удаляет сотрудника из команды по ID."""
        self.__team = [emp for emp in self.__team if emp.id != employee_id]
    
    def get_team(self) -> list[AbstractEmployee]:
        """Возвращает список команды проекта."""
        return self.__team.copy()
    
    def get_team_size(self) -> int:
        """Возвращает размер команды."""
        return len(self.__team)
    
    def calculate_total_salary(self) -> float:
        """Рассчитывает суммарную зарплату команды."""
        return sum(emp.calculate_salary() for emp in self.__team)
    
    def get_project_info(self) -> str:
        """Возвращает полную информацию о проекте."""
        return (f"Проект [{self.__project_id}]: {self.__name}\n"
                f"Описание: {self.__description}\n"
                f"Статус: {self.__status}\n"
                f"Срок: {self.__deadline.strftime('%Y-%m-%d')}\n"
                f"Команда: {len(self.__team)} чел., бюджет: {self.calculate_total_salary():.2f}")
    
    def change_status(self, new_status: str) -> None:
        """Изменяет статус проекта с валидацией."""
        if new_status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Невалидный статус: {new_status}")
        self.__status = new_status
    
    def to_dict(self) -> dict:
        """Преобразует проект в словарь для сериализации."""
        return {
            "project_id": self.__project_id,
            "name": self.__name,
            "description": self.__description,
            "deadline": self.__deadline.strftime("%Y-%m-%d"),
            "status": self.__status,
            "team": [emp.to_dict() for emp in self.__team]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Создает проект из словаря."""
        project = cls(
            data["project_id"],
            data["name"],
            data["description"],
            data["deadline"],
            data["status"]
        )
        # Команда будет восстановлена при загрузке компании
        return project
