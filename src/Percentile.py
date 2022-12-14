import pandas as pd
import numpy as np
import math
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Percentile(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data = input_data.dropna()
        rank = params.get("rank", 0.5)
        error = params.get("error", 0)

        # header format
        value_header = 'percentile(' + input_data.columns[1]
        param_list = ['rank', 'error']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])

        data = sorted(input_data.iloc[:,1])
        i = math.ceil(len(data) * rank)
        if i > 1 :
            quantile = float(data[i - 1])
        else :
            quantile = float(data[0])
        if error == 0:
            quantile = np.percentile(data, rank*100)
        else:
            a = len(data) * (rank + error)
            b = len(data) * (rank - error)
            for j in range(len(data)):
                if j <a  and j > b:
                    i = j
                    if i > 1 :
                        quantile = float(data[i-1])
                    else :
                        quantile = float(data[0])
        output_data.iloc[0, 1] = quantile
        output_data.iloc[0, 0] = '1970-01-01 08:00:00.000'

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
