from abc import ABC, abstractmethod
from analyzing import AttributeAnalysis
from indicators import *
from renderer import (
    SimilarValuesHTMLRenderer,
    NullValuesHTMLRenderer,
    DistinctValuesHTMLRenderer,
    ValueRangeHTMLRenderer
)


#-------------------------------- Attribute Analysis Factories --------------------------------------


class AttributeAnalysisFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class JSONAttributeAnalysisFactory(AttributeAnalysisFactory):

    def __init__(self, json_data, data_frame):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = self.json_data['attribute_name']

    def create(self):
        json_indicators_data = self.json_data['indicators']
        return AttributeAnalysis(self.attribute_name, self.__create_indicators(json_indicators_data))

    def __create_indicators(self, json_indicators_data):
        indicators = []
        for json_indicator_data in json_indicators_data:
            indicators.append(self.__create_indicator(json_indicator_data))
        return indicators

    def __create_indicator(self, json_indicator_data):
        return JSONIndicatorFactory(json_indicator_data, self.data_frame, self.attribute_name).create()


#------------------------------ Indicator Factories ----------------------------------

class IndicatorFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class JSONIndicatorFactory(IndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        self.json_data = json_data
        self.data_frame = data_frame
        self.attribute_name = attribute_name

    def create(self):
        indicator_name = self.json_data['indicator_name']
        if indicator_name == 'SimilarValuesIndicator':
            return JSONSimilarValuesIndicatorFactory(self.json_data, self.data_frame, self.attribute_name).create()
        if indicator_name == 'NullValuesIndicator':
            return JSONNullValuesIndicatorFactory(self.json_data, self.data_frame, self.attribute_name).create()
        if indicator_name == 'DistinctValuesIndicator':
            return JSONDistinctValuesIndicatorFactory(self.json_data, self.data_frame, self.attribute_name).create()
        if indicator_name == 'ValueRangeIndicator':
            return JSONValueRangeIndicatorFactory(self.json_data, self.data_frame, self.attribute_name).create()


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


class JSONSimilarValuesIndicatorFactory(SimilarValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(JSONSimilarValuesIndicatorFactory, self).__init__(
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


class JSONNullValuesIndicatorFactory(NullValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(JSONNullValuesIndicatorFactory, self).__init__(
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


class JSONDistinctValuesIndicatorFactory(DistinctValuesIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(JSONDistinctValuesIndicatorFactory, self).__init__(
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


class JSONValueRangeIndicatorFactory(ValueRangeIndicatorFactory):

    def __init__(self, json_data, data_frame, attribute_name):
        super(JSONValueRangeIndicatorFactory, self).__init__(
            data_frame,
            attribute_name
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
        if type(self.indicator) is SimilarValuesIndicator:
            return SimilarValuesHTMLRenderer(self.indicator)
        if type(self.indicator) is NullValuesIndicator:
            return NullValuesHTMLRenderer(self.indicator)
        if type(self.indicator) is DistinctValuesIndicator:
            return DistinctValuesHTMLRenderer(self.indicator)
        if type(self.indicator) is ValueRangeIndicator:
            return ValueRangeHTMLRenderer(self.indicator)
