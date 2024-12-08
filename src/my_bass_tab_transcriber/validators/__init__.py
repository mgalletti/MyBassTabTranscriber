from abc import ABC, abstractmethod


class BaseValidator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def validate(self, *args):
        raise NotImplementedError("Subclasses must implement the validate method.")
