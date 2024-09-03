

def readFloatValuesFromTextFile(fileName : str) -> list[float]:
    with open(fileName) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        values.append(float(line))
    return values

    