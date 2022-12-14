import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Period(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data = input_data.fillna("fillna")
        # header format
        value_header = 'period(' + input_data.columns[1]
        value_header += ')'
        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])
      
        period = input_data.shape[0]
        data = input_data.iloc[:,1]
        flag = 0
        for i in range(1,int(len(data)/2)):
            if data[i] != data[0]:
                pass
            elif data[i] == data[0]:
                if len(data) % i != 0:
                    pass
                else:
                    flag = 1
                    j = 0
                    k = j
                    while k+2*i-1 < len(data):
                        for j in range(k, k+i-1):
                            if data[j] != data[j+i]:
                                flag = 0
                                break
                        if flag == 0:
                            break
                        k = k+i
            if flag == 1:
                period = i
                break
        output_data.iloc[0, 1] = period
        output_data.iloc[0, 0] = '1970-01-01 08:00:00.000'
        
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
