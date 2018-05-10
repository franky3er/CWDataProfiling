from settings.settings import *
import json
import os
import pandas as pd
from factories import JSONAttributeAnalysisFactory
from renderer import AttributeAnalysisHTMLRenderer
import datetime


data_frame = pd.read_csv(CSV_FILE_PATH, encoding=CSV_FILE_ENCODING, sep=CSV_FILE_SEPARATOR)
report_directory = REPORT_DIRECTORY + "/" + datetime.datetime.today().strftime('%Y-%m-%d')

for json_file_name in [file_name for file_name in os.listdir(ATTRIBUTE_SETTINGS_LOCATION)
                       if os.path.isfile(os.path.join(ATTRIBUTE_SETTINGS_LOCATION, file_name))
                          and file_name.endswith('.json')]:
    with open(os.path.join(ATTRIBUTE_SETTINGS_LOCATION, json_file_name)) as json_file:
        json_data = json.load(json_file)
        attribute_analysis = JSONAttributeAnalysisFactory(json_data, data_frame).create()
        attribute_analysis.run()
        renderer = AttributeAnalysisHTMLRenderer(attribute_analysis, report_directory)
        renderer.render()