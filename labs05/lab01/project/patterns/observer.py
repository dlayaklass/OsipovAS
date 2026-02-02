"""
Паттерн Observer - система уведомлений
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    """Абстрактный наблюдатель"""

    @abstractmethod
    def update(self, message: str):
        """Получить уведомление"""
        pass


class NotificationSystem(Observer):
    """Система уведомлений - конкретный наблюдатель"""

    def __init__(self, name: str = "Система уведомлений"):
        self._name = name
        self._messages = []

    def update(self, message: str):
        """Обработать уведомление"""
        self._messages.append(message)
        print(f"[{self._name}] {message}")

    def get_messages(self):
        """Получить все сообщения"""
        return self._messages.copy()

    def clear_messages(self):
        """Очистить историю сообщений"""
        self._messages.clear()


class EmailNotifier(Observer):
    """Уведомления по email"""

    def __init__(self, email: str):
        self._email = email

    def update(self, message: str):
        print(f"[Email -> {self._email}] {message}")


class LogNotifier(Observer):
    """Логирование уведомлений"""

    def __init__(self, log_file: str = "notifications.log"):
        self._log_file = log_file

    def update(self, message: str):
        print(f"[Log -> {self._log_file}] {message}")
