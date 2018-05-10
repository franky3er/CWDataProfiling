from abc import ABC, abstractmethod
from difflib import SequenceMatcher

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


class SimilarValueIndicator(Indicator):

    def __init__(self, data_frame=None, attribute_name=None, min_ratio=0.9):
        super(SimilarValueIndicator, self).__init__(data_frame=data_frame, attribute_name=attribute_name)
        self.min_ratio = min_ratio
        self.values = self.data_frame[self.attribute_name].unique()
        self.matching_groups = []
        self.name = "Ähnliche Werte"

    def analyze(self):
        for value_a_idx in range(len(self.values)):
            for value_b_idx in range(value_a_idx + 1, len(self.values)):
                if SequenceMatcher(None, str(self.values[value_a_idx]), str(self.values[value_b_idx])).ratio() >= self.min_ratio:
                    self.__assign_to_matching_group(self.values[value_a_idx], self.values[value_b_idx])

    def __assign_to_matching_group(self, value_a, value_b):
        for group in self.matching_groups:
            if value_a in group or value_b in group:
                if value_a not in group:
                    group.append(value_a)
                if value_b not in group:
                    group.append(value_b)
                return

        self.matching_groups.append([value_a, value_b])


    def get_result(self):
        return self.matching_groups