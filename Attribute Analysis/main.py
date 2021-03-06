from settings.settings import *
import json
import os
import pandas as pd
from factories import AttributeAnalysisJSONFactory
from renderer import AttributeAnalysisHTMLRenderer, BusinessRulesDetailsHTMLRenderer


data_frame = pd.read_csv(CSV_FILE_PATH, encoding=CSV_FILE_ENCODING, sep=CSV_FILE_SEPARATOR)
data_frame.set_index(PANDAS_INDEX_NAME, inplace=True, drop=False)
report_directory = REPORT_DIRECTORY

for json_file_name in [file_name for file_name in os.listdir(ATTRIBUTE_SETTINGS_LOCATION)
                       if os.path.isfile(os.path.join(ATTRIBUTE_SETTINGS_LOCATION, file_name))
                          and file_name.endswith('.json')]:
    with open(os.path.join(ATTRIBUTE_SETTINGS_LOCATION, json_file_name), encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        attribute_analysis = AttributeAnalysisJSONFactory(json_data, data_frame).create()
        attribute_analysis.run()
        AttributeAnalysisHTMLRenderer(attribute_analysis, report_directory).render()
        BusinessRulesDetailsHTMLRenderer(attribute_analysis, report_directory + "/details").render()