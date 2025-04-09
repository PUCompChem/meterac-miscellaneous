


def float_values_from_string(s : str, splitter : str = ";" ) -> list[float]:
    tokens = s.split(splitter)
    values = []
    for tok in tokens:
        t = tok.strip()
        if t != '':
            values.append(float(tok))
    return values


def extract_matrix_from_file(fileName: str):
    prev_line = None
    with open(fileName, mode ='r') as file:
        n = 0
        for line in file:
            n = n+1
            #print(n,line)
            if (not line.startswith("#")):
                values = float_values_from_string(line)
                print(values)