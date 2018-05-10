from abc import ABC, abstractmethod
import datetime
import os

class AttributeAnalysisRenderer(ABC):

    def __init__(self, attribute_analysis):
        self.attribute_analysis = attribute_analysis
        self.html_output = ""

    @abstractmethod
    def render(self):
        pass


class AttributeAnalysisHTMLRenderer(AttributeAnalysisRenderer):

    def __init__(self, attribute_analysis, output_directory):
        super(AttributeAnalysisHTMLRenderer, self).__init__(attribute_analysis)
        self.output_file_path = "{output_directory}/{output_file_name}.html".format(
            output_directory = output_directory,
            output_file_name = attribute_analysis.attribute_name
        )
        os.makedirs(os.path.dirname(self.output_file_path), exist_ok=True)

    def render(self):
        self.__render_header()
        self.__render_indicators()
        self.__render_footer()
        output_file = open(self.output_file_path, "w", encoding="UTF-8")
        output_file.write(self.html_output)
        output_file.close()

    def __render_header(self):
        self.html_output = """
            <!DOCTYPE html>
            <html lang="de">
                <head>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
                    <title>{attribute_name} | Standard Attribut Analyse</title>
                </head>
                <body>
                    <div class="container-fluid">
                        <h1>Standard Attribut Analyse: {attribute_name}</h1>
                        <h3>Metainformationen: </h3>
                        <div class="row"> 
                            <div class="w-50 p-3">
                                <table class="table table-nonfluid">
                                    <tr>
                                        <th>Attributname: </th>
                                        <td>{attribute_name}</td>
                                    </tr>
                                    <tr>
                                        <th>Analysezeitstempel: </th>
                                        <td>{analysis_date}</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                        
                        <div class="accordion" id="accordion">
                            
        """.format(
            attribute_name = self.attribute_analysis.attribute_name,
            analysis_date = datetime.datetime.now()
        )

    def __render_indicators(self):
        from factories import IndicatorHTMLRendererFactory
        for indicator in self.attribute_analysis.indicators:
            self.html_output += IndicatorHTMLRendererFactory(indicator).create().render()

    def __render_footer(self):
        self.html_output += """
                            
                        </div>
                    </div>
                    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
                </body>
            </html>
        """


class IndicatorRenderer(ABC):

    def __init__(self, indicator):
        self.indicator = indicator
        self.html_output = ""

    def render(self):
        self.html_output = """
                    <div class="card">
                        <div class="card-header" id="heading{indicator_type}">
                            <h5 class="mb-0">
                                <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{indicator_type}" aria-expanded="true" aria-controls="collapse{indicator_type}">
                                    {indicator_name}
                                </button>
                            </h5>
                        </div>
                        
                        <div id="collapse{indicator_type}" class="collapse show" aria-labelledby="heading{indicator_type}" data-parent="#accordion">
                            <div class="card-body">
                                {indicator_result}
                            </div>
                        </div>
                    </div>
        """.format(
            indicator_type = type(self.indicator).__name__,
            indicator_name = self.indicator.name,
            indicator_result = self.render_child()
        )
        return self.html_output


class SimilarValueHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(SimilarValueHTMLRenderer, self).__init__(indicator)

    def render_child(self):
        html_output = """
                    <p>______________________________________________________________________</p><br/>
        """
        for matching_group in self.indicator.get_result():
            for matching_group_value in matching_group:
                html_output += """
                            <p>{matching_group_value}</p>    
                """.format(matching_group_value = matching_group_value)
            html_output += """
                        <p>______________________________________________________________________</p><br/>
            """
        return html_output