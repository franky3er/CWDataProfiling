from abc import ABC, abstractmethod
from pandas import isnull
import regex as re

class BusinessRule(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def is_valid(self, value):
        pass

    @abstractmethod
    def get_description(self):
        pass


class NotNullRule(BusinessRule):

    def __init__(self):
        super(NotNullRule, self).__init__('Nicht NULL')

    def is_valid(self, value):
        return not isnull(value)

    def get_description(self):
        return "Wert muss befüllt sein"


class RegExPatternMatchingRule(BusinessRule):

    def __init__(self, pattern="*"):
        super(RegExPatternMatchingRule, self).__init__("RegEx-Übereinstimmung")
        self.pattern = pattern
        self.regex = re.compile(self.pattern)

    def is_valid(self, value):
        return self.regex.match(value)

    def get_description(self):
        return "Wert muss Regulärem Ausdruck '{regex}' entsprechen".format(
            regex = self.pattern
        )


class DomainListMatchingRule(BusinessRule):

    def __init__(self, values=[]):
        super(DomainListMatchingRule, self).__init__("Domänen-Übereinstimmung")
        self.values = values

    def is_valid(self, value):
        return value in self.values

    def get_description(self):
        return "Wert muss einem Wert aus der folgenden Liste entsprechen: {}".format(
            self.__get_value_list_as_string()
        )

    def __get_value_list_as_string(self):
        list_as_enumeration = "["
        for value in self.values:
            list_as_enumeration += "<br/>&nbsp;&nbsp;&nbsp;'{}', ".format(value)
        list_as_enumeration += "<br/>]"
        return list_as_enumeration

