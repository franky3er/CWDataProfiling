from collections import defaultdict

class AttributeAnalysis:

    def __init__(self, attribute_name, data_frame, dropna=True):
        self.attribute_name = attribute_name
        self.data_frame = data_frame
        self.indicators = []
        self.dropna = dropna
        self.business_rules = []
        self.business_rules_results = {}

    def add_indicator(self, indicator):
        self.indicators.append(indicator)

    def add_business_rule(self, business_rule):
        self.business_rules.append(business_rule)

    def run(self):
        print("Run Analysis: '{}'".format(self.attribute_name))
        self.run_indicator_analysis()
        self.run_business_rules_analysis()

    def run_indicator_analysis(self):
        print("     Run Indicator Analysis...")
        for indicator in self.indicators:
            print("          {}".format(indicator.__class__.__name__))
            indicator.analyze()

    def run_business_rules_analysis(self):
        print("     Run Business-Rule Analysis...")
        for value, count in self.data_frame[self.attribute_name].value_counts(dropna=False).items():
            data_sets = self.data_frame[self.data_frame[self.attribute_name] == value]
            if self.dropna and value.isnull():
                continue
            result, valid = self.__validate_data_set(value, count, data_sets)
            if valid:
                self.__append_businss_rule_result(valid, 'overall', count, value, result, data_sets)
            else:
                self.__append_businss_rule_result(valid, 'overall', count, value, result, data_sets)

    def __validate_data_set(self, value, count, data_sets):
        results = {}
        all_rules_valid = True
        for business_rule in self.business_rules:
            rule_valid = business_rule.is_valid(value)
            if not rule_valid:
                all_rules_valid = False
            results[business_rule] = business_rule.is_valid(value)
            self.__append_businss_rule_result(rule_valid, business_rule.__class__.__name__, count, value, results[business_rule], data_sets)
        return results, all_rules_valid

    def __append_businss_rule_result(self, valid, business_rule, count, value, result, data_sets):
        validity = 'valid' if valid else 'invalid'
        self.__create_initial_business_rule_results_if_not_existing(business_rule)
        self.business_rules_results[validity][business_rule]['count'] = (
            self.business_rules_results[validity][business_rule]['count'] + count
        )
        if 'values' not in self.business_rules_results[validity][business_rule]:
            self.business_rules_results[validity][business_rule]['values'] = {}
        self.business_rules_results[validity][business_rule]['values'][value] = {}
        self.business_rules_results[validity][business_rule]['values'][value]['result'] = result
        self.business_rules_results[validity][business_rule]['values'][value]['count'] = count
        self.business_rules_results[validity][business_rule]['values'][value]['data_sets'] = data_sets

    def __create_initial_business_rule_results_if_not_existing(self, business_rule):
        if 'valid' not in self.business_rules_results:
            self.business_rules_results['valid'] = {}
        if business_rule not in self.business_rules_results['valid']:
            self.business_rules_results['valid'][business_rule] = {}
            self.business_rules_results['valid'][business_rule]['count'] = 0

        if 'invalid' not in self.business_rules_results:
            self.business_rules_results['invalid'] = {}
        if business_rule not in self.business_rules_results['invalid']:
            self.business_rules_results['invalid'][business_rule] = {}
            self.business_rules_results['invalid'][business_rule]['count'] = 0
