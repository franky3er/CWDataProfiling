from abc import ABC, abstractmethod
from pandas import isnull

class BusinessRule(ABC):

    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""

    @abstractmethod
    def is_valid(self, value):
        pass


class NotNullRule(BusinessRule):

    def __init__(self):
        super(NotNullRule, self).__init__()
        self.id = "NotNullRule"
        self.name = "Not NULL"
        self.description = "Wert muss befüllt sein"

    def is_valid(self, value):
        return not isnull(value)
