from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def notify(self, articles, title):
        pass
