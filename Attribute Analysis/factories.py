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
        indicator_factories = {
            'SimilarValuesIndicator' : SimilarValuesIndicatorJSONFactory,
            'NullValuesIndicator' : NullValuesIndicatorJSONFactory,
            'DistinctValuesIndicator' : DistinctValuesIndicatorJSONFactory,
            'ValueRangeIndicator' : ValueRangeIndicatorJSONFactory,
            'PatternFrequencyIndicator' : PatternFrequencyIndicatorJSONFactory
        }

        return indicator_factories[self.json_data['indicator_name']](
            self.json_data,
            self.data_frame,
            self.attribute_name
        ).create()


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


class SimilarValuesIndicatorJSONFactory(SimilarValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        super(SimilarValuesIndicatorJSONFactory, self).__init__(
            self.data_frame,
            self.attribute_name,
            self.json_data['indicator_config']['min_ratio']
        )
        return super(SimilarValuesIndicatorJSONFactory, self).create()


class NullValuesIndicatorFactory(ABC):

    def __init__(self, data_frame, attribute_name):
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        return NullValuesIndicator(
            data_frame=self.data_frame,
            attribute_name=self.attribute_name
        )


class NullValuesIndicatorJSONFactory(NullValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        super(NullValuesIndicatorJSONFactory, self).__init__(
            self.data_frame,
            self.attribute_name
        )
        return super(NullValuesIndicatorJSONFactory, self).create()


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
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        super(DistinctValuesIndicatorJSONFactory, self).__init__(
            self.data_frame,
            self.attribute_name
        )
        return super(DistinctValuesIndicatorJSONFactory, self).create()


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
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        super(ValueRangeIndicatorJSONFactory, self).__init__(
            self.data_frame,
            self.attribute_name
        )
        return super(ValueRangeIndicatorJSONFactory, self).create()


class PatternFrequencyIndicatorFactory(ABC):

    def __init__(self, data_frame, attribute_name):
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        return PatternFrequencyIndicator(
            data_frame=self.data_frame,
            attribute_name=self.attribute_name
        )


class PatternFrequencyIndicatorJSONFactory(PatternFrequencyIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        super(PatternFrequencyIndicatorJSONFactory, self).__init__(
            self.data_frame,
            self.attribute_name
        )
        return super(PatternFrequencyIndicatorJSONFactory, self).create()


#------------------------------Business Rule Factories-------------------------------------------

class BusinessRuleFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class BusinessRuleJSONFactory(BusinessRuleFactory):

    def __init__(self, json_data):
        self.json_data = json_data

    def create(self):
        business_rule_factories = {
            'NotNullRule' : NotNullRuleJSONFactory,
            'RegExPatternMatchingRule' : RegExPatternMatchingRuleJSONFactory,
            'DomainListMatchingRule' : DomainListMatchingRuleJSONFactory,
        }

        return business_rule_factories.get(self.json_data['business_rule_name'])(
            self.json_data
        ).create()

class NotNullRuleFactory(BusinessRuleFactory):

    def __init__(self):
        pass

    def create(self):
        return NotNullRule()


class NotNullRuleJSONFactory(NotNullRuleFactory):

    def __init__(self, json_data):
        super(NotNullRuleJSONFactory, self).__init__()



class RegExPatternMatchingRuleFactory(BusinessRuleFactory):

    def __init__(self, pattern):
        self.pattern = pattern

    def create(self):
        return RegExPatternMatchingRule(pattern=self.pattern)


class RegExPatternMatchingRuleJSONFactory(RegExPatternMatchingRuleFactory):

    def __init__(self, json_data):
        self.json_data = json_data
        super(RegExPatternMatchingRuleJSONFactory, self).__init__(
            self.json_data['business_rule_config']['pattern']
        )


class DomainListMatchingRuleFactory(BusinessRuleFactory):

    def __init__(self, values):
        self.values = values

    def create(self):
        return DomainListMatchingRule(self.values)


class DomainListMatchingRuleJSONFactory(DomainListMatchingRuleFactory):

    def __init__(self, json_data):
        self.json_data = json_data
        super(DomainListMatchingRuleJSONFactory, self).__init__(
            self.json_data['business_rule_config']['values']
        )


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
        indicator_html_renderer = {
            SimilarValuesIndicator : SimilarValuesHTMLRenderer,
            NullValuesIndicator : NullValuesHTMLRenderer,
            DistinctValuesIndicator : DistinctValuesHTMLRenderer,
            ValueRangeIndicator : ValueRangeHTMLRenderer,
            PatternFrequencyIndicator : PatternFrequencyHTMLRenderer
        }

        return indicator_html_renderer.get(type(self.indicator))(self.indicator)