"""Класс проекта"""


class InvalidStatusError(Exception):
    """Ошибка неверного статуса"""
    pass


class Project:
    """Проект компании"""

    VALID_STATUSES = ["planning", "active", "completed", "cancelled"]

    def __init__(self, project_id: int, name: str, description: str,
                 deadline: str, status: str = "planning"):
        self._id = project_id
        self._name = name
        self._description = description
        self._deadline = deadline
        if status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Неверный статус: {status}")
        self._status = status
        self._team = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Неверный статус: {value}")
        self._status = value

    def add_team_member(self, employee):
        if employee not in self._team:
            self._team.append(employee)

    def remove_team_member(self, emp_id: int):
        for i, emp in enumerate(self._team):
            if emp.id == emp_id:
                return self._team.pop(i)
        return None

    def get_team(self) -> list:
        return self._team.copy()

    def get_team_size(self) -> int:
        return len(self._team)

    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self._team)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "deadline": self._deadline,
            "status": self._status,
            "team": [emp.id for emp in self._team]
        }
