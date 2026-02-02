"""Класс разработчика"""

from .employee import Employee


class Developer(Employee):
    """Разработчик с уровнем и стеком технологий"""

    SENIORITY_COEF = {"junior": 1.0, "middle": 1.5, "senior": 2.0}

    def __init__(self, employee_id: int, name: str, department: str,
                 base_salary: float, tech_stack: list = None, seniority: str = "junior"):
        super().__init__(employee_id, name, department, base_salary)
        self._tech_stack = tech_stack if tech_stack else []
        self._seniority = seniority.lower()

    @property
    def tech_stack(self) -> list:
        return self._tech_stack.copy()

    @property
    def seniority(self) -> str:
        return self._seniority

    @seniority.setter
    def seniority(self, value: str):
        if value.lower() in self.SENIORITY_COEF:
            self._seniority = value.lower()

    def add_skill(self, skill: str):
        if skill not in self._tech_stack:
            self._tech_stack.append(skill)

    def calculate_salary(self) -> float:
        coef = self.SENIORITY_COEF.get(self._seniority, 1.0)
        return self._base_salary * coef + self.calculate_bonus()

    def get_info(self) -> str:
        skills = ", ".join(self._tech_stack) if self._tech_stack else "нет"
        return f"Разработчик [id: {self._id}], уровень: {self._seniority}, навыки: [{skills}], итоговая зарплата: {self.calculate_salary()}"

    def __iter__(self):
        return iter(self._tech_stack)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["tech_stack"] = self._tech_stack
        data["seniority"] = self._seniority
        return data
