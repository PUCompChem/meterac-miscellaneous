

def readFloatValuesFromTextFile(fileName : str) -> list[float]:
    with open(fileName) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        values.append(float(line))
    return values


def readFloatValuesFromSingleLineTextFile(fileName : str) -> list[float]:
    with open(fileName) as f:
        lines = f.readlines()

    values = []
    line = lines[0]
    tokens = line.split(" ")
    values = []
    for tok in tokens:
        t = tok.strip()
        if t != '':
            values.append(float(tok))
    return values  