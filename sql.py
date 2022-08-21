import re
from pandas import merge
from pandasql import sqldf
from FlokAlgorithmLocal import FlokDataFrame
from Integral import Integral
from Mad import Mad
from Median import Median
from Resample import Resample
from Sample import Sample

inputTypes = ['csv']
inputLocation = ['local_fs']
outputPaths = ['./test_out.csv']
outputTypes = ['csv']

while True:
    command = input(">>> ")
    ## constant commands for debugging
    # command = "select Time, \"resample(s2, 'every'='1.0s', 'interp'='BFill', 'aggr'='Min', 'start'='2022-01-01 00:00:02', 'end'='2022-01-01 00:00:08')\" from root_test_d1 where Time <= '2022-01-01 00:00:12';"
    # command = "select Time, \"sample(s3, 'method'='isometric', 'k'='5')\" from root_test_d1 where Time <= '2022-01-01 00:00:12';"
    # command = "select Time, \"median(s1)\" from root_test_d1 where Time <= '2022-01-01 00:00:12';"
    if command in ["exit", "quit", "q"]:
        break
    elif command in ["help", "h"]:
        print("""
        exit, quit, q: exit
        help, h: print this help
        select timeseries from dataframe [where condition]: perform a SQL query
        """)
    else:
        try:
            # preprocess the command by extracting patterns
            pattern = re.findall(r"select\s+\w+,\s+\"(\w+)\((\w+),\s+(.*)\)\"\s+from\s+(.*?)[\s;]+.*", command)[0]
            print(pattern)
            funcName = pattern[0].capitalize()
            params = dict(re.findall(r"\'(\w+)\'\s*=\s*\'([\w\s\-\.:]+)\'", pattern[2]))
            if funcName == 'Sample' and params.get('method') == 'reservoir':
                raise Exception("Sample method 'reservoir' is not supported in SQL query due to the randomness.")
            inputPath = pattern[3]
            inputPaths = [inputPath]

            # run the algorithm
            algorithm = globals()[funcName]()
            data = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes).get(0)
            for series in data.columns[1:]:
                flokdataframe = FlokDataFrame()
                flokdataframe.addDF(data.loc[:, ['Time', series]])
                dataframe = algorithm.run(flokdataframe, params).get(0)
                if inputPath not in globals().keys():
                    globals()[inputPath] = dataframe
                else:
                    globals()[inputPath] = merge(globals()[inputPath], dataframe, on='Time')

            # run the SQL query
            result = sqldf(command)
            print(result.values)
            del globals()[inputPath]

        except Exception as e:
            print(e)
            print("error")