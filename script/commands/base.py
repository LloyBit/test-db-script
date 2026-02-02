from abc import ABC, abstractmethod

# Абстрактный класс для команд
class Command(ABC):
    @abstractmethod
    def run(self):
        pass