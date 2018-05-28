from abc import ABC, abstractmethod
from difflib import SequenceMatcher
import operator

class Indicator(ABC):

    def __init__(self, data_frame=None, attribute_name=None):
        self.data_frame = data_frame
        self.attribute_name = attribute_name
        self.name = ""

    @abstractmethod
    def analyze(self):
        pass

    @abstractmethod
    def get_result(self):
        pass


class SimilarValuesIndicator(Indicator):

    def __init__(self, data_frame=None, attribute_name=None, min_ratio=0.9):
        super(SimilarValuesIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.min_ratio = min_ratio
        self.value_counts = self.data_frame[self.attribute_name].value_counts(dropna=True)
        self.matching_value_count_groups = []
        self.name = "Ähnliche Werte"

    def analyze(self):
        cnt = 0
        len_value_counts = sum(1 for _ in self.value_counts)
        for value_count_a in self.value_counts.items():
            cnt += 1
            if cnt < len_value_counts:
                for value_count_b in self.value_counts[cnt:].items():
                    if SequenceMatcher(None, str(value_count_a[0]), str(value_count_b[0])).ratio() >= self.min_ratio:
                        self.__assign_to_matching_value_count_group(value_count_a, value_count_b)

    def __assign_to_matching_value_count_group(self, value_count_a, value_count_b):
        for value_count_group in self.matching_value_count_groups:
            if value_count_a in value_count_group or value_count_b in value_count_group:
                if value_count_a not in value_count_group:
                    value_count_group.append(value_count_a)
                if value_count_b not in value_count_group:
                    value_count_group.append(value_count_b)
                return

        self.matching_value_count_groups.append([value_count_a, value_count_b])

    def get_result(self):
        return self.matching_value_count_groups


class NullValuesIndicator(Indicator):
    def __init__(self, data_frame=None, attribute_name=None):
        super(NullValuesIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.name = "Fehlende Werte"

    def analyze(self):
        values_total = self.data_frame.shape[0]
        missing_values_total = self.data_frame[self.attribute_name].isnull().sum()
        available_values_total = values_total - missing_values_total
        missing_values_percentage = missing_values_total / values_total * 100
        available_values_percentage = available_values_total / values_total * 100

        self.result = {
            'values_total' : values_total,
            'missing_values_total' : missing_values_total,
            'available_values_total' : available_values_total,
            'missing_values_percentage' : round(missing_values_percentage, 2),
            'available_values_percentage' : round(available_values_percentage, 2),
        }

    def get_result(self):
        return self.result

class DistinctValuesIndicator(Indicator):

    def __init__(self, data_frame=None, attribute_name=None):
        super(DistinctValuesIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.name = "Unterschiedliche Werte"

    def analyze(self):
        distinct_values_total = self.data_frame.groupby(self.attribute_name)[self.attribute_name].nunique(dropna=False).sum()
        unique_values_total = self.data_frame.groupby(self.attribute_name).filter(
            lambda g: (g[self.attribute_name].size == 1)).shape[0]
        duplicate_values_total = self.data_frame.groupby(self.attribute_name).filter(
            lambda g: (g[self.attribute_name].size >= 2))[self.attribute_name].nunique()
        unique_values_percentage = round((unique_values_total / distinct_values_total) * 100, 2)
        duplicate_values_percentage = round((duplicate_values_total / distinct_values_total) * 100, 2)
        self.result = {
            'distinct_values_total' : distinct_values_total,
            'unique_values_total' : unique_values_total,
            'unique_values_percentage' : unique_values_percentage,
            'duplicate_values_total' : duplicate_values_total,
            'duplicate_values_percentage' : duplicate_values_percentage
        }

    def get_result(self):
        return self.result


class ValueRangeIndicator(Indicator):

    def __init__(self, data_frame=None, attribute_name=None):
        super(ValueRangeIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.name = "Wertebereich / Wertemenge"

    def analyze(self):
        self.result = self.data_frame[self.attribute_name].value_counts(dropna=False)

    def get_result(self):
        return self.result


class PatternFrequencyIndicator(Indicator):

    def __init__(self, data_frame=None, attribute_name=None):
        super(PatternFrequencyIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.name = "Muster Frequenz"
        self.result = {}

    def analyze(self):
        for value, cnt in self.data_frame[self.attribute_name].value_counts().iteritems():
            value_pattern = self.__get_value_pattern(str(value))
            if value_pattern in self.result:
                self.result[value_pattern] += cnt
            else:
                self.result[value_pattern] = cnt

        self.sorted_result_tuple = sorted(self.result.items(), key=operator.itemgetter(1))

    def __get_value_pattern(self, value):
        value_pattern = ''
        for char in value:
            if char.istitle():
                value_pattern += 'A'
            elif char.isalpha():
                value_pattern += 'a'
            elif char.isdigit():
                value_pattern += '9'
            else:
                value_pattern += char
        return value_pattern

    def get_result(self):
        return self.sorted_result_tuple


class ShortestValuesIndicator(Indicator):

    def __init__(self, data_frame=None, attribute_name=None, number_of_values=100, dropna=True):
        super(ShortestValuesIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.number_of_values=number_of_values
        self.dropna=dropna
        self.name = "Kürzeste Werte"
        self.shortest_values = []

    def analyze(self):
        for value, count in self.data_frame[self.attribute_name].value_counts(dropna=self.dropna).items():
            length = len(str(value))
            self.shortest_values.append((value, length, count))

        self.shortest_values = sorted(self.shortest_values, key=lambda x: x[1])
        self.shortest_values = self.shortest_values[0:100] if len(self.shortest_values) >= 100 else self.shortest_values

    def get_result(self):
        return self.shortest_values