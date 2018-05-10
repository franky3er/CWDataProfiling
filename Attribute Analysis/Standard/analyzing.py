class AttributeAnalysis:

    def __init__(self, attribute_name, indicators):
        self.attribute_name = attribute_name
        self.indicators = indicators

    def run(self):
        for indicator in self.indicators:
            indicator.analyze()
            #for result in indicator.get_result():
            #    print (result)