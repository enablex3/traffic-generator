# Return input data
def get_inputs(filename):
    with open(filename, 'r') as readInputFile:
        data = readInputFile.read()

    data = data.replace("{", "")
    data = data.replace("}", "")
    data = data.replace(" ","")
    data = data.split(",")

    inputs = {}
    for element in data:
        s = element.split(":")
        field = s[0]
        value = s[1]

        inputs[field] = value

    return(inputs)


