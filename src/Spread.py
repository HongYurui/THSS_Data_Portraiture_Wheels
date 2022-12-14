from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd
class Spread(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        column = input_data.columns[1]
        output_data = input_data
        output_data.dropna(inplace=True)
        spread = max(output_data[column])-min(output_data[column])
        j = 'spread({})'.format(column)
        output_data = pd.DataFrame(
            {'Time': '1970-01-01 08:00:00.000', j: spread}, index=[0])

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
