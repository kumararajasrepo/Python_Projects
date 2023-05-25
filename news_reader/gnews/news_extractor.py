from abc import ABC, abstractmethod


class NewsExtractor(ABC):
    @abstractmethod
    def extract(self, title):
        pass
