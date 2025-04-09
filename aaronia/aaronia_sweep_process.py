#import os

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
                continue    
            else:
                values = float_values_from_string(line)
                #print(values)
                if flag_frequencies:
                    global frequencies
                    frequencies = values
                else:
                    matrix.append([sweepStart, sweepStop] + values)
                #Reset work variables
                flag_frequencies = False
                sweepStart = None
                sweepStop = None           

    return matrix

def aaronia_file_data_to_csv(aaroniaFileName: str, csvFileName: str):
    matrix = extract_matrix_from_aaronia_file(aaroniaFileName)
    file = open(csvFileName, "wt")
    # Write header line
    file.write("SweepStart,SweepStop")
    for x in frequencies:
        file.write(",")
        file.write(str(x))    
    file.write("\n")    #os.linesep
    #Write matrix rows
    for row in matrix:
        n = len(row)
        for i in range(n):
            file.write(str(row[i]))
            if i < n-1:
                file.write(",")
        file.write("\n")
    file.close()
    