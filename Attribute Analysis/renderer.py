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
        self.output_directory = output_directory
        self.output_file_path = "{output_directory}/{output_file_name}.html".format(
            output_directory = self.output_directory,
            output_file_name = attribute_analysis.attribute_name
        )
        os.makedirs(os.path.dirname(self.output_file_path), exist_ok=True)

    def render(self):
        print("     Render Result")
        self.__render_header()
        self.__render_indicators()
        self.__render_business_rules()
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
                    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
                    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/numeric/1.2.6/numeric.min.js"></script>
                    <title>{attribute_name} | Standard Attribut Analyse</title>
                </head>
                <body>
                    <div class="container-fluid">
                        <h1>Attribut Analyse: "{attribute_name}"</h1><br/>
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
                        <br/>                            
        """.format(
            attribute_name = self.attribute_analysis.attribute_name,
            analysis_date = datetime.datetime.now()
        )

    def __render_indicators(self):
        print("          Indicators")
        from factories import IndicatorHTMLRendererFactory
        self.html_output += """
                        <h3>Standard-Analyse:</h3>
                        <div class="accordion" id="accordion">
        """
        for indicator in self.attribute_analysis.indicators:
            self.html_output += IndicatorHTMLRendererFactory(indicator).create().render()

        self.html_output += """
                        </div><br/>
        """

    def __render_business_rules(self):
        print("          Business Rules")
        self.html_output += BusinessRulesHTMLRenderer(self.attribute_analysis).render()

    def __render_footer(self):
        self.html_output += """      
                    
                    </div>
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
                                
                                <div id="collapse{indicator_type}" class="collapse" aria-labelledby="heading{indicator_type}" >
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

    @abstractmethod
    def render_child(self):
        pass


class SimilarValuesHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(SimilarValuesHTMLRenderer, self).__init__(indicator)

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


class NullValuesHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(NullValuesHTMLRenderer, self).__init__(indicator)
        self.values_total = self.indicator.get_result()['values_total'],
        self.missing_values_total = self.indicator.get_result()['missing_values_total'],
        self.missing_values_total = self.missing_values_total[0]
        self.missing_values_percentage = self.indicator.get_result()['missing_values_percentage'],
        self.available_values_total = self.indicator.get_result()['available_values_total'],
        self.available_values_total = self.available_values_total[0]
        self.available_values_percentage = self.indicator.get_result()['available_values_percentage'],

    def render_child(self):
        html_output = """
                                        <div class="row">
                                            <div class="col-md-6">
                                                <table class="table" style="margin-top: 110px">
                                                    <tr>
                                                        <th>Werte Insgesamt: </th>
                                                        <td>{values_total}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Fehlende Werte Insgesamt: </th>
                                                        <td>{missing_values_total}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Fehlende Werte (%): </th>
                                                        <td>{missing_values_percentage}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Vorhandene Werte Insgesamt: </th>
                                                        <td>{available_values_total}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Vorhandene Werte (%):</th>
                                                        <td>{available_values_percentage}</td>
                                                    </tr>
                                                </table>
                                            </div>
                                            <div class="col-md-6">
                                                {pie_chart}
                                            </div>
                                        </div>
        """.format(
            values_total = self.indicator.get_result()['values_total'],
            missing_values_total = self.indicator.get_result()['missing_values_total'],
            missing_values_percentage = self.indicator.get_result()['missing_values_percentage'],
            available_values_total = self.indicator.get_result()['available_values_total'],
            available_values_percentage = self.indicator.get_result()['available_values_percentage'],
            pie_chart = PlotlyPieChartHTMLRenderer(
                topic="nullValues",
                attribute_name=self.indicator.attribute_name,
                labels=['Fehlend', "Vorhanden"],
                values=[self.missing_values_total, self.available_values_total],
                colors=['rgb(255, 0, 0', 'rgb(0, 255, 0']
            ).render()
        )

        return html_output


class DistinctValuesHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(DistinctValuesHTMLRenderer, self).__init__(indicator)
        self.distinct_values_total = self.indicator.get_result()['distinct_values_total']
        self.unique_values_total = self.indicator.get_result()['unique_values_total']
        self.unique_values_percentage = self.indicator.get_result()['unique_values_percentage']
        self.duplicate_values_total = self.indicator.get_result()['duplicate_values_total']
        self.duplicate_values_percentage = self.indicator.get_result()['duplicate_values_percentage']

    def render_child(self):
        return """
                                        <div class="row">
                                            <div class="col-md-6">
                                                <table class="table" style="margin-top: 110px">
                                                    <tr>
                                                        <th>Unterschiedliche Werte Insgesamt (Distinct): </th>
                                                        <td>{distinct_values_total}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Einzigartige Werte Insgesamt (Unique): </th>
                                                        <td>{unique_values_total}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Einzigartige Werte (%): </th>
                                                        <td>{unique_values_percentage}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Duplikat Werte Insgesamt (Duplicate): </th>
                                                        <td>{duplicate_values_total}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Duplikat Werte (%):</th>
                                                        <td>{duplicate_values_percentage}</td>
                                                    </tr>
                                                </table>
                                            </div>
                                            <div class="col-md-6">
                                                {pie_chart}
                                            </div>
                                        </div>
        """.format(
            distinct_values_total=self.distinct_values_total,
            unique_values_total=self.unique_values_total,
            unique_values_percentage=self.unique_values_percentage,
            duplicate_values_total=self.duplicate_values_total,
            duplicate_values_percentage=self.duplicate_values_percentage,
            pie_chart=PlotlyPieChartHTMLRenderer(
                topic="distinctValues",
                attribute_name=self.indicator.attribute_name,
                labels=['Einzigartig (Unique)', "Duplikate (Duplicates)"],
                values=[self.unique_values_total, self.duplicate_values_total],
                colors=['rgb(202, 249, 232)', 'rgb(252, 225, 129)']
            ).render()
        )


class ValueRangeHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(ValueRangeHTMLRenderer, self).__init__(indicator)

    def render_child(self):
        return """
                                <div class="row">
                                    <div class="col">
                                        <table class="table table-striped">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th>Wert</th>
                                                    <th>Häufigkeit</th>
                                                    <th>Relative Häufigkeit (%)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {value_counts}
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="col">
                                        {pie_chart}
                                    </div>
                                </div>
        """.format(
            value_counts = self.__render_value_counts(),
            pie_chart = self.__render_pie_chart()
        )

    def __render_value_counts(self):
        html_output = ""
        for value, count in self.indicator.get_result().iteritems():
            html_output += """
                                            <tr>
                                                <td>{value}</td>
                                                <td>{count}</td>
                                                <td>{count_percentage}</td>
                                            </tr>
            """.format(
                value=value,
                count=count,
                count_percentage=round((count / len(self.indicator.data_frame[self.indicator.attribute_name])) * 100, 2)
            )
        return html_output

    def __render_pie_chart(self):
        values = []
        frequencies = []

        for value, frequency in self.indicator.get_result().iteritems():
            values.append(str(value))
            frequencies.append(frequency)

        return PlotlyPieChartHTMLRenderer(
            topic="valueFrequency",
            attribute_name=self.indicator.attribute_name,
            labels=values,
            values=frequencies,
            colors=None
        ).render()


class PatternFrequencyHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(PatternFrequencyHTMLRenderer, self).__init__(indicator)
        self.result = self.indicator.get_result()


    def render_child(self):
        return """
                                <div class="row">
                                    <div class="col">
                                        <table class="table table-striped">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th>Muster</th>
                                                    <th>Häufigkeit</th>
                                                    <th>Relative Häufigkeit (%)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {pattern_frequencies}
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="col">
                                        {pie_chart}
                                    </div>
                                </div>
        """.format(
            pattern_frequencies = self.__render_pattern_frequencies(),
            pie_chart = self.__render_pie_chart()
        )

    def __render_pattern_frequencies(self):
        html_output = ""
        for pattern, frequency in reversed(self.result):
            html_output += """
                                            <tr>
                                                <td>{pattern}</td>
                                                <td>{frequency}</td>
                                                <td>{frequency_percentage}</td>
                                            </tr>
            """.format(
                pattern = pattern,
                frequency = frequency,
                frequency_percentage = round((frequency / len(self.indicator.data_frame[self.indicator.attribute_name])) * 100, 2)
            )
        return html_output

    def __render_pie_chart(self):
        patterns = [pattern_frequency[0] for pattern_frequency in self.result]
        frequencies = [pattern_frequency[1] for pattern_frequency in self.result]

        return PlotlyPieChartHTMLRenderer(
            topic="patternFrequency",
            attribute_name=self.indicator.attribute_name,
            labels=patterns,
            values=frequencies,
            colors=None
        ).render()


class ShortestValuesHTMLRenderer(IndicatorRenderer):

    def __init__(self, indicator):
        super(ShortestValuesHTMLRenderer, self).__init__(indicator)
        self.result = self.indicator.get_result()

    def render_child(self):
        return """
                                        <table class="table table-striped">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th>Wert</th>
                                                    <th>Länge</th>
                                                    <th>Häufigkeit</th>
                                                <tr>
                                            </thead>
                                            <tbody>
                                                {shortest_values}
                                            </tbody>
                                        </table>
        """.format(
            shortest_values=self.__render_shortest_values()
        )

    def __render_shortest_values(self):
        html_output = ""
        for shortest_value in self.result:
            html_output += """
                                                <tr>
                                                    <td>'{value}'</td>
                                                    <td>{length}</td>
                                                    <td>{count}</td>
                                                </tr>
            """.format(
                value=shortest_value[0],
                length=shortest_value[1],
                count=shortest_value[2]
            )
        return html_output

class BusinessRulesRenderer(ABC):

    def __init__(self, attribute_analysis):
        self.attribute_analysis = attribute_analysis

    @abstractmethod
    def render(self):
        pass


class BusinessRulesHTMLRenderer(BusinessRulesRenderer):

    def __init__(self, attribute_analysis):
        super(BusinessRulesHTMLRenderer, self).__init__(attribute_analysis)
        self.html_output = "<h3>Geschäftsregel</h3>"

    def render(self):
        if not self.attribute_analysis.business_rules:
            return self.html_output + """
                <p>Keine Geschäftsregeln spezifiziert!</p>
            """
        self.html_output += """
                                {business_rules_metadata}
                                {business_rules_result_overview}
                                {invalid_rows}
                """.format(
            business_rules_metadata=self.__render_business_rules_result_overview_metadata(),
            business_rules_result_overview=self.__render_business_rules_result_overview_pie_charts(),
            invalid_rows=self.__render_invalid_data_sets()
        )

        return self.html_output

    def __render_business_rules_result_overview_metadata(self):
        business_rule_metadata = """
                        <h5>Ergebnissübersicht:</h5>
                        <table class="table">
                            <tr>
                                <th>Id</th>
                                <th>Name</th>
                                <th>Beschreibung</th>
                                <th>Valide Werte</th>
                                <th>Valide Werte (%)</th>
                                <th>Invalide Werte</th>
                                <th>Invalide Werte (%)</th>
                            </tr>
        """
        for business_rule in self.attribute_analysis.business_rules:
            business_rule_id = business_rule.__class__.__name__
            business_rule_valid_values_count = (
                self.attribute_analysis.business_rules_results['valid'][business_rule_id]['count']
            )
            business_rule_invalid_values_count = (
                self.attribute_analysis.business_rules_results['invalid'][business_rule_id]['count']
            )
            values_total = business_rule_valid_values_count + business_rule_invalid_values_count
            business_rule_valid_values_percentage = round((business_rule_valid_values_count / values_total) * 100, 2)
            business_rule_invalid_values_percentage = round((business_rule_invalid_values_count / values_total) * 100, 2)
            business_rule_metadata += """
                            <tr>
                                <td><a href="{business_rule_details_file_path}">{business_rule_id}</td>
                                <td>{business_rule_name}</td>
                                <td>{business_rule_desciption}</td>
                                <td>{business_rule_valid_values_count}</td>
                                <td>{business_rule_valid_values_percentage}</td>
                                <td>{business_rule_invalid_values_count}</td>
                                <td>{business_rule_invalid_values_percentage}</td>
                            </tr>
            """.format(
                business_rule_details_file_path="./details/{}/{}.html".format(
                    self.attribute_analysis.attribute_name,
                    business_rule_id
                ),
                business_rule_id=business_rule_id,
                business_rule_name=business_rule.name,
                business_rule_desciption=business_rule.get_description(),
                business_rule_valid_values_count=business_rule_valid_values_count,
                business_rule_valid_values_percentage=business_rule_valid_values_percentage,
                business_rule_invalid_values_count=business_rule_invalid_values_count,
                business_rule_invalid_values_percentage=business_rule_invalid_values_percentage
            )

        business_rule_id = business_rule.__class__.__name__
        business_rule_valid_values_count = (
            self.attribute_analysis.business_rules_results['valid']['overall']['count']
        )
        business_rule_invalid_values_count = (
            self.attribute_analysis.business_rules_results['invalid']['overall']['count']
        )
        values_total = business_rule_valid_values_count + business_rule_invalid_values_count
        business_rule_valid_values_percentage = round((business_rule_valid_values_count / values_total) * 100, 2)
        business_rule_invalid_values_percentage = round((business_rule_invalid_values_count / values_total) * 100, 2)
        business_rule_metadata += """
                            <tr>
                                <td>Overall</td>
                                <td>Alle Geschäftsregeln</td>
                                <td>Übereinstimmung von allen Geschäftsregeln</td>
                                <td>{business_rule_valid_values_count}</td>
                                <td>{business_rule_valid_values_percentage}</td>
                                <td>{business_rule_invalid_values_count}</td>
                                <td>{business_rule_invalid_values_percentage}</td>
                            </tr>
                        </table>
        """.format(
            business_rule_valid_values_count=business_rule_valid_values_count,
            business_rule_valid_values_percentage=business_rule_valid_values_percentage,
            business_rule_invalid_values_count=business_rule_invalid_values_count,
            business_rule_invalid_values_percentage=business_rule_invalid_values_percentage
        )
        return business_rule_metadata

    def __render_business_rules_result_overview_pie_charts(self):
        number_of_pie_charts = len(self.attribute_analysis.business_rules) + 1
        html_output = """
                        <div class="row">
                            <div class="col">
                                {pie_chart_overall}
                            </div>
        """.format(
            pie_chart_overall=PlotlyPieChartHTMLRenderer(
                title="Overall",
                topic="business_rules_result_overview_overall",
                attribute_name=self.attribute_analysis.attribute_name,
                labels=['valide', "invalide"],
                values=[
                    self.attribute_analysis.business_rules_results['invalid']['overall']['count'],
                    self.attribute_analysis.business_rules_results['valid']['overall']['count'],
                ],
                colors=['rgb(255, 0, 0', 'rgb(0, 255, 0'],
                num_charts=number_of_pie_charts,
                width_by_num_charts=True
            ).render()
        )

        for business_rule in self.attribute_analysis.business_rules:
            business_rule_id = business_rule.__class__.__name__
            html_output += """
                            <div class="col">
                                {pie_chart_business_rule}
                            </div>
            """.format(
                pie_chart_business_rule=PlotlyPieChartHTMLRenderer(
                    title=business_rule_id,
                    topic="business_rules_result_overview_{}".format(business_rule_id),
                    attribute_name=self.attribute_analysis.attribute_name,
                    labels=['invalide', 'valide'],
                    values=[
                        self.attribute_analysis.business_rules_results['invalid'][business_rule_id]['count'],
                        self.attribute_analysis.business_rules_results['valid'][business_rule_id]['count'],
                    ],
                    colors=['rgb(255, 0, 0', 'rgb(0, 255, 0'],
                    num_charts=number_of_pie_charts,
                    width_by_num_charts=True
            ).render()
            )

        html_output += """
                        </div>
        """

        return html_output



    def __render_invalid_data_sets(self):
        pass
        invalid_data_sets = """
                        <h5>Invalide Werte:</h5>
                        <div id="accordionInvalidValues">
                        <p>{invalid_data_sets_cnt}</p>
                        <p>{invalid_values_cnt}</p>
        """.format(
            invalid_data_sets_cnt = "<b>{}</b> invalide Datensätze gefunden von <b>{}</b> Datensätzen insgesamt".format(
                str(self.attribute_analysis.business_rules_results['invalid']['overall']['count']),
                str(len(self.attribute_analysis.data_frame[self.attribute_analysis.attribute_name]))
            ),
            invalid_values_cnt = "<b>{}</b> invalide Werte gefunden von <b>{}</b> unterschiedlichen Werten insgesamt".format(
                str(len(self.attribute_analysis.business_rules_results['invalid']['overall']['values']))
                if 'values' in self.attribute_analysis.business_rules_results['invalid']['overall'] else 0,
                self.attribute_analysis.data_frame[self.attribute_analysis.attribute_name].nunique(dropna=False)
            )
        )
        if 'values' in self.attribute_analysis.business_rules_results['invalid']['overall']:
            value_idx = 1
            for value, results in self.attribute_analysis.business_rules_results['invalid']['overall']['values'].items():
                invalid_data_sets += self.__render_invalid_data_set(value, results, value_idx)
                value_idx += 1

        invalid_data_sets += """
                        </div>
        """
        return invalid_data_sets

    def __render_invalid_data_set(self, value, results, value_idx):
        invalid_data_set = """
                            <div class="card">
                                <div class="card-header" id="headingInvalidValue{value_id}">
                                    <h5 class="mb-0">
                                        <button class="btn btn-link" data-toggle="collapse" data-target="#collapseInvalidValue{value_id}" aria-expanded="true" aria-controls="collapseInvalidValue{value_id}">
                                            Wert: "{value}"
                                        </button>
                                    </h5>
                                </div>
                                    
                                <div id="collapseInvalidValue{value_id}" class="collapse" aria-labelledby="headingInvalidValue{value_id}">
                                    <div class="card-body">
                                        <table class="table">
                                            <tr>
                                                <th>Geschäftsregel</th>
                                                <th>Valide</th>
                                            </tr>
                                    
        """.format(
            value=value,
            value_id=value_idx,
        )

        for business_rule, valid in results['result'].items():
            invalid_data_set += """
                                            <tr>
                                                <td>{business_rule_description}</td>
                                                <td>{valid}</td>
                                            </tr>
            """.format(
                business_rule_description=business_rule.get_description(),
                valid= """<div class="alert alert-success">JA</div>""" if valid else """<div class="alert alert-danger">NEIN</div>"""
            )

        invalid_data_set += """
                                        </table>
                                        <h6><b>{count}</b> betroffene Datensätze:</h6>
                                        <p>{data_sets_indexes}</p>
                                    </div>
                                </div>
                            </div>
        """.format(
            count=results['count'],
            data_sets_indexes=list(results['data_sets'].index.values)
        )

        return invalid_data_set


class PlotlyPieChartHTMLRenderer:

    def __init__(self, topic="", attribute_name="", labels=[], values=[], colors=[], title=None, num_charts=1, width_by_num_charts=False):
        self.topic = topic
        self.attribute_name = attribute_name
        self.labels = labels
        self.values = values
        self.colors = colors
        self.title = title
        self.num_diagrams_in_one_row = num_charts
        self.width_by_num_charts = width_by_num_charts

    def render(self):
        return """
                                                <div id="{topic}{attribute_name}"></div>
                                                <script>
                                                    var chart_width = (screen.width / {num_diagrams_in_one_row})-50;
                                                    var data = [{{
                                                        labels: {labels},
                                                        values: {values},
                                                        {colors}
                                                        type: 'pie'
                                                    }}];
                                                    var layout = {{
                                                        {title}
                                                        {width}
                                                    }}
                                                    Plotly.newPlot('{topic}{attribute_name}', data, layout);
                                                </script>
        """.format(
            attribute_name = self.attribute_name,
            topic=self.topic,
            labels=self.labels,
            values=self.values,
            colors=self.__render_colors() if self.colors else "",
            num_diagrams_in_one_row=str(self.num_diagrams_in_one_row),
            title="title: '{}',".format(self.title) if self.title else "",
            width="width: chart_width," if self.width_by_num_charts else ""
        )

    def __render_colors(self):
        return """
                                                        marker: {{
                                                            colors: {colors}
                                                        }},
        """.format(
            colors = self.colors
        )


class BusinessRulesDetailsHTMLRenderer():

    def __init__(self, attribute_analysis, output_directory):
        self.attribute_analysis = attribute_analysis
        self.output_directory = output_directory

    def render(self):
        for business_rule in self.attribute_analysis.business_rules:
            BusinessRuleDetailsHTMLRenderer(
                business_rule,
                self.attribute_analysis,
                "{output_directory}/{attribute_name}/".format(
                    output_directory = self.output_directory,
                    attribute_name = self.attribute_analysis.attribute_name,
                )
            ).render()


class BusinessRuleDetailsHTMLRenderer():

    def __init__(self, business_rule, attribute_analysis, output_directory):
        self.business_rule = business_rule
        self.attribute_analysis = attribute_analysis
        self.output_directory = output_directory
        self.html_output = ""
        self.output_file_path = "{output_directory}{business_rule_details_file_name}.html".format(
            output_directory=self.output_directory,
            business_rule_details_file_name=self.business_rule.__class__.__name__
        )
        os.makedirs(os.path.dirname(self.output_directory), exist_ok=True)

    def render(self):
        self.html_output = self.__render_html_output()
        output_file = open(self.output_file_path, "w", encoding="UTF-8")
        output_file.write(self.html_output)
        output_file.close()

    def __render_html_output(self):
        return """
            <!DOCTYPE html>
            <html lang="de">
                <head>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
                    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
                    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/numeric/1.2.6/numeric.min.js"></script>
                    <title>{attribute_name} | {business_rule_id}-Details</title>
                </head>
                <body>
                    <div class="container-fluid">
                    {body}
                    </div>
                </body>
            </html>
        """.format(
            attribute_name = self.attribute_analysis.attribute_name,
            business_rule_id = self.business_rule.__class__.__name__,
            body = self.__render_body()
        )

    def __render_body(self):
        return """
                    <h1>{business_rule_id}-Details: "{attribute_name}"</h1>
                    <br/><br/>
                    {meta_infos}
                    {invalid_values}
        """.format(
            attribute_name=self.attribute_analysis.attribute_name,
            business_rule_id=self.business_rule.__class__.__name__,
            meta_infos = self.__render_meta_infos(),
            invalid_values = self.__render_invalid_values()
        )

    def __render_meta_infos(self):
        business_rule_id = self.business_rule.__class__.__name__

        valid_values_total = (
            self.attribute_analysis.business_rules_results['valid'][business_rule_id]['count']
        )
        invalid_values_total = (
            self.attribute_analysis.business_rules_results['invalid'][business_rule_id]['count']
        )
        values_total = valid_values_total + invalid_values_total
        valid_values_total_percentage = round((valid_values_total / values_total) * 100, 2)
        invalid_values_total_percentage = round((invalid_values_total / values_total) * 100, 2)

        values_distinct = (
            self.attribute_analysis.data_frame[self.attribute_analysis.attribute_name].nunique(dropna=False)
        )
        invalid_values_distinct = 0
        if 'values' in self.attribute_analysis.business_rules_results['invalid'][business_rule_id]:
            invalid_values_distinct = (
                len(self.attribute_analysis.business_rules_results['invalid'][business_rule_id]['values'])
            )
        valid_values_distinct = values_distinct - invalid_values_distinct
        valid_values_distinct_percentage = round((valid_values_distinct / values_distinct) * 100, 2)
        invalid_values_distinct_percentage = round((invalid_values_distinct / values_distinct) * 100, 2)

        return """
            <div class="row">
                <div class="col-md-6">
                    <table class="table">
                        <tr>
                            <th>Attribut</th>
                            <td>{attribute_name}</td>
                        </tr>
                        <tr>
                            <th>Geschäftsregel-Id</th>
                            <td>{business_rule_id}</td>
                        </tr>
                        <tr>
                            <th>Geschäftsregel-Name</th>
                            <td>business_rule_name</td>
                        </tr>
                        <tr>
                            <th>Geschäftsregel-Beschreibung</th>
                            <td>{business_rule_description}</td>
                        </tr>
                        <tr>
                            <th>Relative Häufigkeit (Alle validen Werte)</th>
                            <td>{valid_values_total} / {values_total} ({valid_values_total_percentage} %)</td>
                        </tr>
                        <tr>
                            <th>Relative Häufigkeit (Alle invaliden Werte)</th>
                            <td>{invalid_values_total} / {values_total} ({invalid_values_total_percentage} %)</td>
                        </tr>
                        <tr>
                            <th>Relative Häufigkeit (Distinct valide Werte)</th>
                            <td>{valid_values_distinct} / {values_distinct} ({valid_values_distinct_percentage} %)</td>
                        </tr>
                        <tr>
                            <th>Relative Häufigkeit (Distinct invalide Werte)</th>
                            <td>{invalid_values_distinct} / {values_distinct} ({invalid_values_distinct_percentage} %)</td>
                        </tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <div class="row">
                        <div class="col-md-6">
                            {pie_chart_invalid_values_total}
                        </div>
                        <div class="col-md-6">
                            {pie_chart_invalid_values_distinct}
                        </div>
                    </div>
                </div>
            </div>
        """.format(
            attribute_name = self.attribute_analysis.attribute_name,
            business_rule_id = self.business_rule.__class__.__name__,
            business_rule_name = self.business_rule.name,
            business_rule_description = self.business_rule.get_description(),
            values_total=values_total,
            valid_values_total=valid_values_total,
            invalid_values_total = invalid_values_total,
            valid_values_total_percentage=valid_values_total_percentage,
            invalid_values_total_percentage = invalid_values_total_percentage,
            values_distinct=values_distinct,
            valid_values_distinct=valid_values_distinct,
            invalid_values_distinct = invalid_values_distinct,
            valid_values_distinct_percentage=valid_values_distinct_percentage,
            invalid_values_distinct_percentage = invalid_values_distinct_percentage,
            pie_chart_invalid_values_total=PlotlyPieChartHTMLRenderer(
                title="Alle Werte",
                topic="invalid_values_total{}".format(business_rule_id),
                attribute_name=self.attribute_analysis.attribute_name,
                labels=['invalide', 'valide'],
                values=[
                    invalid_values_total,
                    valid_values_total,
                ],
                colors=['rgb(255, 0, 0', 'rgb(0, 255, 0'],
            ).render(),
            pie_chart_invalid_values_distinct=PlotlyPieChartHTMLRenderer(
                title="Distinct Werte",
                topic="invalid_values_distinct{}".format(business_rule_id),
                attribute_name=self.attribute_analysis.attribute_name,
                labels=['invalide', 'valide'],
                values=[
                    invalid_values_distinct,
                    valid_values_distinct,
                ],
                colors=['rgb(255, 0, 0', 'rgb(0, 255, 0'],
            ).render()
        )

    def __render_invalid_values(self):
        return """
            <br/>
            <h3>Invalide Werte:</h3>
            <table class="table table-striped">
                <thead class="thead-dark">
                    <tr>
                        <th>Wert</th>
                        <th>Häufigkeit</th>
                        <th>Indizes</th>
                    </tr>
                </thead>
                <tbody>
                    {invalid_values}
                </tbody>
            </table>
        """.format(
            invalid_values=self.__render_invalid_values_details()
        )

    def __render_invalid_values_details(self):
        html_output = ""
        if 'values' not in self.attribute_analysis.business_rules_results['invalid'][self.business_rule.__class__.__name__]:
            return html_output
        for value, results in self.attribute_analysis.business_rules_results['invalid'][self.business_rule.__class__.__name__]['values'].items():
            html_output += """
                <tr>
                    <td>"{value}"</td>
                    <td>{count}</td>
                    <td>{index}</td>
                </tr>
            """.format(
                value=value,
                count=results['count'],
                index=list(results['data_sets'].index.values)
            )
        return html_output