from abc import ABC, abstractmethod

class BaseAIClient(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass