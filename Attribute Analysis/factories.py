from abc import ABC, abstractmethod
from analyzing import AttributeAnalysis
from indicators import *
from rules import *
from renderer import *


#-------------------------------- Attribute Analysis Factories --------------------------------------


class AttributeAnalysisFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class AttributeAnalysisJSONFactory(AttributeAnalysisFactory):

    def __init__(self, json_data, data_frame):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = self.json_data['attribute_name']
        self.dropna = self.json_data['dropna']

    def create(self):
        attribute_analysis = AttributeAnalysis(self.attribute_name, self.data_frame, dropna=self.dropna)
        attribute_analysis = self.__append_indicators(attribute_analysis, self.json_data['indicators'])
        attribute_analysis = self.__append_business_rules(attribute_analysis, self.json_data['business_rules'])
        return attribute_analysis

    def __append_indicators(self, attribute_analysis, json_indicators_data):
        for json_indicator_data in json_indicators_data:
            attribute_analysis.add_indicator(
                self.__create_indicator(json_indicator_data)
            )
        return attribute_analysis

    def __append_business_rules(self, attribute_analysis, json_business_rules_data):
        for json_business_rule_data in json_business_rules_data:
            attribute_analysis.add_business_rule(
                self.__create_business_rule(json_business_rule_data)
            )
        return attribute_analysis

    def __create_indicator(self, json_indicator_data):
        return IndicatorJSONFactory(json_indicator_data, self.data_frame, self.attribute_name).create()

    def __create_business_rule(self, json_business_rule_data):
        return BusinessRuleJSONFactory(json_business_rule_data).create()

#------------------------------ Indicator Factories ----------------------------------

class IndicatorFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class IndicatorJSONFactory(IndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        indicator_name = self.json_data['indicator_name']
        if indicator_name == 'SimilarValuesIndicator':
            return SimilarValuesJSONIndicatorFactory(self.json_data, self.data_frame, self.attribute_name).create()
        if indicator_name == 'NullValuesIndicator':
            return NullValuesJSONIndicatorFactory(self.json_data, self.data_frame, self.attribute_name).create()
        if indicator_name == 'DistinctValuesIndicator':
            return DistinctValuesIndicatorJSONFactory(self.json_data, self.data_frame, self.attribute_name).create()
        if indicator_name == 'ValueRangeIndicator':
            return ValueRangeIndicatorJSONFactory(self.json_data, self.data_frame, self.attribute_name).create()


class SimilarValuesIndicatorFactory(ABC):

    def __init__(self, data_frame, attribute_name, min_ratio):
        self.data_frame = data_frame
        self.attribute_name = attribute_name
        self.min_ratio = min_ratio

    def create(self):
        return SimilarValuesIndicator(
            data_frame=self.data_frame,
            attribute_name=self.attribute_name,
            min_ratio=self.min_ratio
        )


class SimilarValuesJSONIndicatorFactory(SimilarValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(SimilarValuesJSONIndicatorFactory, self).__init__(
            data_frame,
            attribute_name,
            json_data['indicator_config']['min_ratio']
        )


class NullValuesIndicatorFactory(ABC):

    def __init__(self, data_frame, attribute_name):
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        return NullValuesIndicator(
            data_frame=self.data_frame,
            attribute_name=self.attribute_name
        )


class NullValuesJSONIndicatorFactory(NullValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(NullValuesJSONIndicatorFactory, self).__init__(
            data_frame,
            attribute_name
        )


class DistinctValuesIndicatorFactory(ABC):

    def __init__(self, data_frame, attribute_name):
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        return DistinctValuesIndicator(
            data_frame=self.data_frame,
            attribute_name=self.attribute_name
        )


class DistinctValuesIndicatorJSONFactory(DistinctValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(DistinctValuesIndicatorJSONFactory, self).__init__(
            data_frame,
            attribute_name
        )


class ValueRangeIndicatorFactory(ABC):

    def __init__(self, data_frame, attribute_name):
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        return ValueRangeIndicator(
            data_frame=self.data_frame,
            attribute_name=self.attribute_name
        )


class ValueRangeIndicatorJSONFactory(ValueRangeIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(ValueRangeIndicatorJSONFactory, self).__init__(
            data_frame,
            attribute_name
        )


#------------------------------Business Rule Factories-------------------------------------------

class BusinessRuleFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class BusinessRuleJSONFactory(BusinessRuleFactory):

    def __init__(self, json_data):
        self.json_data = json_data

    def create(self):
        business_rule_name = self.json_data['business_rule_name']
        if business_rule_name == 'NotNullRule':
            return NotNullRuleJSONFactory().create()


class NotNullRuleFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class NotNullRuleJSONFactory(NotNullRuleFactory):

    def create(self):
        return NotNullRule()


#------------------------------ Indicator Renderer Factories --------------------------------------

class IndicatorRendererFactory(ABC):

    def __init__(self, indicator):
        self.indicator = indicator

    @abstractmethod
    def create(self):
        pass


class IndicatorHTMLRendererFactory(IndicatorRendererFactory):

    def __init__(self, indicator):
        super(IndicatorHTMLRendererFactory, self).__init__(indicator)

    def create(self):
        if type(self.indicator) is SimilarValuesIndicator:
            return SimilarValuesHTMLRenderer(self.indicator)
        if type(self.indicator) is NullValuesIndicator:
            return NullValuesHTMLRenderer(self.indicator)
        if type(self.indicator) is DistinctValuesIndicator:
            return DistinctValuesHTMLRenderer(self.indicator)
        if type(self.indicator) is ValueRangeIndicator:
            return ValueRangeHTMLRenderer(self.indicator)
