class AttributeAnalysis:

    def __init__(self, attribute_name, data_frame, dropna=True):
        self.attribute_name = attribute_name
        self.data_frame = data_frame
        self.indicators = []
        self.dropna = dropna
        self.business_rules = []
        self.valid_data_sets_results = {}
        self.invalid_data_sets_results = {}

    def add_indicator(self, indicator):
        self.indicators.append(indicator)

    def add_business_rule(self, business_rule):
        self.business_rules.append(business_rule)

    def run(self):
        self.run_indicator_analysis()
        self.run_business_rules_analysis()

    def run_indicator_analysis(self):
        for indicator in self.indicators:
            indicator.analyze()

    def run_business_rules_analysis(self):
        for index, data_set in self.data_frame.iterrows():
            if self.dropna and data_set[self.attribute_name].isnull():
                continue
            result, valid = self.__validate_data_set(data_set)
            if valid:
                self.valid_data_sets_results[index] = result
            else:
                self.invalid_data_sets_results[index] = result

    def __validate_data_set(self, data_set):
        results = {}
        all_rules_valid = True
        for business_rule in self.business_rules:
            rule_valid = business_rule.is_valid(data_set[self.attribute_name])
            if not rule_valid:
                all_rules_valid = False
            results[business_rule] = business_rule.is_valid(data_set[self.attribute_name])
        return results, all_rules_valid
