# Return input data
import json

def get_inputs(filename):
    with open(filename, 'r') as readInputFile:
        data = readInputFile.read()

    inputs = json.loads(data)

    return(inputs)


