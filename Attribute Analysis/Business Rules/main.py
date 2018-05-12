from analyzing import AttributeAnalysis
import datetime
import json
import os
import pandas as pd
from rules import NotNullRule
from settings.settings import *

data_frame = pd.read_csv(CSV_FILE_PATH, encoding=CSV_FILE_ENCODING, sep=CSV_FILE_SEPARATOR)
data_frame.set_index(PANDAS_INDEX_NAME, inplace=True)
report_directory = REPORT_DIRECTORY + "/" + datetime.datetime.today().strftime('%Y-%m-%d')

attribute_analysis = AttributeAnalysis('Ansprechpartner_Firma', data_frame, dropna=False)
attribute_analysis.add_business_rule(NotNullRule())
attribute_analysis.analyze()
print(attribute_analysis.invalid_data_sets_results)