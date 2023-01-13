class Converter():
    def __init__(self):
        pass

    def convert_bool_to_int(self, series):
        """
        converts True to 1 and False to 0
        :param series: series type
        :return: series after replacing bool values to int
        """
        series = series.replace({True:1, False:0})
        return series
