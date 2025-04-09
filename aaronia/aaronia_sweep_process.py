
frequencies = None


def float_values_from_string(s : str, splitter : str = ";" ) -> list[float]:
    tokens = s.split(splitter)
    values = []
    for tok in tokens:
        t = tok.strip()
        if t != '':
            values.append(float(tok))
    return values


def extract_matrix_from_aaronia_file(fileName: str) -> list:
    flag_frequencies = False
    sweepStart = None
    sweepStop = None
    matrix = []
    with open(fileName, mode ='r') as file:
        n = 0
        for line in file:
            n = n+1
            #scip empty line
            if (line.strip() == ''):                
                continue

            #print(n,line)
            if (line.startswith("#")):
                if (line.startswith("# SweepFrequencies=")):
                   flag_frequencies = True
                   continue 
                if (line.startswith("# SweepStart=")):
                    sweepStart = line.strip()[13:]
                    continue
                if (line.startswith("# SweepStop=")):
                    sweepStop = line.strip()[12:]
                    continue

            else:
                values = float_values_from_string(line)
                #print(values)
                matrix.append([sweepStart, sweepStop] + values)
                #Reset work variables
                flag_frequencies = False
                sweepStart = None
                sweepStop = None           

    return matrix