"""Паттерн Observer"""

from abc import ABC, abstractmethod


class Observer(ABC):
    """Абстрактный наблюдатель"""

    @abstractmethod
    def update(self, message: str):
        pass


class NotificationSystem(Observer):
    """Система уведомлений"""

    def __init__(self, name: str = "Система уведомлений"):
        self._name = name
        self._messages = []

    def update(self, message: str):
        self._messages.append(message)

    def get_messages(self):
        return self._messages.copy()

    def clear_messages(self):
        self._messages.clear()


class EmailNotifier(Observer):
    """Уведомления по email"""

    def __init__(self, email: str):
        self._email = email
        self._messages = []

    def update(self, message: str):
        self._messages.append(message)


class LogNotifier(Observer):
    """Логирование уведомлений"""

    def __init__(self, log_file: str = "notifications.log"):
        self._log_file = log_file
        self._messages = []

    def update(self, message: str):
        self._messages.append(message)
