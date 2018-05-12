from abc import ABC, abstractmethod
from analyzing import AttributeAnalysis
from rules import *


#-------------------------------- Attribute Analysis Factories --------------------------------------


class AttributeAnalysisFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class AttributeAnalysisFactory(AttributeAnalysisFactory):

    def __init__(self, json_data, data_frame):
        self.json_data = json_data
        self.data_frame = data_frame

    def create(self):
        json_business_rules_data = self.json_data['business_rules']
        attribute_analysis = AttributeAnalysis(
            self.json_data['attribute_name'],
            self.data_frame
        )
        for json_business_rule_data in json_business_rules_data:
            attribute_analysis.add_business_rule(self.__create_business_rule(json_business_rule_data))

    def __crate_business_rule(self):
        pass

class BusinessRuleFactory(ABC):

    @abstractmethod
    def create(self):
        pass

class BusinessRuleJSONFactory(BusinessRuleFactory):

    def __init__(self, json_data):
        self.json_data = json_data

    def create(self):
        pass