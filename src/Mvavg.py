import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Mvavg(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        window = params.get("window", 10)
        if window<=0:
            window = 10
            params["window"] = 10
        # header format
        value_header = 'mvavg(' + input_data.columns[1]
        param_list = ['window']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        output_data = pd.DataFrame(index=range(input_data.shape[0]), columns=['Time', value_header], dtype=object)

        output_data.iloc[:, 0] = input_data.iloc[:, 0]
        output_data.iloc[:, 1] = input_data.iloc[:, 1].rolling(window).mean()
        output_data = output_data.dropna()

        result = FlokDataFrame()
        result.addDF(output_data)
        return result

