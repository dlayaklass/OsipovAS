"""
Модуль для работы с классом Developer (Разработчик).
Наследуется от Employee.
"""

from ..core.employee import Employee


class Developer(Employee):
    """
    Класс Developer представляет разработчика компании.
    
    Наследуется от Employee и добавляет стек технологий и уровень seniority.
    Зарплата зависит от уровня: junior (x1.0), middle (x1.5), senior (x2.0).
    """
    
    # Коэффициенты для расчета зарплаты в зависимости от уровня
    SENIORITY_COEFFICIENTS = {
        "junior": 1.0,
        "middle": 1.5,
        "senior": 2.0
    }
    
    def __init__(self, employee_id: int, name: str, department: str,
                 base_salary: float, tech_stack: list[str], seniority_level: str):
        """
        Конструктор класса Developer.
        
        Args:
            employee_id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата
            tech_stack: Список технологий, которыми владеет разработчик
            seniority_level: Уровень seniority ("junior", "middle", "senior")
        """
        super().__init__(employee_id, name, department, base_salary)
        self.tech_stack = tech_stack
        self.seniority_level = seniority_level
    
    @property
    def tech_stack(self) -> list[str]:
        """Геттер для стека технологий."""
        return self.__tech_stack.copy()
    
    @tech_stack.setter
    def tech_stack(self, value: list[str]):
        """Сеттер для стека технологий."""
        if not isinstance(value, list):
            raise ValueError("Стек технологий должен быть списком")
        if not all(isinstance(item, str) for item in value):
            raise ValueError("Все элементы стека технологий должны быть строками")
        self.__tech_stack = value.copy()
    
    @property
    def seniority_level(self) -> str:
        """Геттер для уровня seniority."""
        return self.__seniority_level
    
    @seniority_level.setter
    def seniority_level(self, value: str):
        """Сеттер для уровня seniority."""
        if not isinstance(value, str):
            raise ValueError("Уровень seniority должен быть строкой")
        value_lower = value.lower()
        if value_lower not in self.SENIORITY_COEFFICIENTS:
            raise ValueError(f"Уровень seniority должен быть одним из: "
                           f"{', '.join(self.SENIORITY_COEFFICIENTS.keys())}")
        self.__seniority_level = value_lower
    
    def add_skill(self, new_skill: str) -> None:
        """Добавляет новую технологию в стек разработчика."""
        if not isinstance(new_skill, str):
            raise ValueError("Технология должна быть строкой")
        if not new_skill.strip():
            raise ValueError("Технология не может быть пустой строкой")
        if new_skill not in self.__tech_stack:
            self.__tech_stack.append(new_skill)
    
    def calculate_salary(self) -> float:
        """Рассчитывает итоговую заработную плату разработчика."""
        coefficient = self.SENIORITY_COEFFICIENTS[self.__seniority_level]
        return self.base_salary * coefficient
    
    def get_info(self) -> str:
        """Возвращает полную информацию о разработчике."""
        tech_stack_str = ", ".join(self.__tech_stack) if self.__tech_stack else "нет"
        return (f"{super().__str__()}, уровень: {self.__seniority_level}, "
                f"технологии: [{tech_stack_str}], итоговая зарплата: {self.calculate_salary()}")
    
    def __iter__(self):
        """Итератор по стеку технологий разработчика."""
        return iter(self.__tech_stack)
    
    def to_dict(self) -> dict:
        """Преобразует объект разработчика в словарь."""
        data = super().to_dict()
        data.update({
            "tech_stack": self.__tech_stack,
            "seniority_level": self.__seniority_level
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Developer':
        """Создает объект разработчика из словаря."""
        return cls(
            data["id"],
            data["name"],
            data["department"],
            data["base_salary"],
            data.get("tech_stack", []),
            data.get("seniority_level", "junior")
        )

