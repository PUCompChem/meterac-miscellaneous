import matplotlib.pyplot as plt
import numpy as np

class AaroniaData:
    def __init__(self):        
        self.frequencies = []
        self.data_matrix = []
        self.sweep_start = []
        self.sweep_stop = []

    def check_matrix_dimensions(self):
        min_len = len(self.data_matrix[0])
        max_len = len(self.data_matrix[0])
        min_row = 1 #1-based indexed
        max_row = 1 #1-based indexed
        for i in range(len(self.data_matrix)):            
            n =  len(self.data_matrix[i]) 
            #print((i+1), " --> ", n)
            if min_len > n:
                min_len = n
                min_row = i+1
            if max_len < n:
                max_len = n
                max_row = i+1
        print("frequencies len: ", len(self.frequencies))
        print("data_matrix len: ", len(self.data_matrix))
        print("data_matrix min row len: ", min_len, " at row: ", min_row)
        print("data_matrix max row len: ", max_len, " at row: ", max_row)
        print("sweep_start len: ", len(self.sweep_start))
        print("sweep_stop len: ", len(self.sweep_stop))

class PlotConfig:
    def __init__(self): 
        self.plottype = "imshow"
        self.x_ticks_num = 10
        self.y_ticks_num = 10


def float_values_from_string(s : str, splitter : str = ";" ) -> list[float]:
    tokens = s.split(splitter)
    values = []
    for tok in tokens:
        t = tok.strip()
        if t != '':
            values.append(float(tok))
    return values


def extract_data_from_aaronia_file(fileName: str) -> AaroniaData:
    adata = AaroniaData()
    flag_frequencies = False
    sweepStart = None
    sweepStop = None
    
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
                if flag_frequencies:
                    adata.frequencies = values
                else:
                    #adata.data_matrix.append([sweepStart, sweepStop] + values)
                    adata.data_matrix.append(values)
                    adata.sweep_start.append(sweepStart)
                    adata.sweep_stop.append(sweepStop)
                #Reset work variables
                flag_frequencies = False
                sweepStart = None
                sweepStop = None           
    return adata

def aaronia_file_data_to_csv(aaroniaFileName: str, csvFileName: str):
    adata = extract_data_from_aaronia_file(aaroniaFileName)
    file = open(csvFileName, "wt")
    # Write header line
    file.write("SweepStart,SweepStop")
    for x in adata.frequencies:
        file.write(",")
        file.write(str(x))    
    file.write("\n")    #os.linesep
    #Write matrix rows
    n_rows = len(adata.data_matrix)
    for k in range(n_rows):
        row = adata.data_matrix[k]
        file.write(adata.sweep_start[k] + "," + adata.sweep_stop[k])        
        for x in row:
            file.write("," + str(x))            
        file.write("\n")
    file.close()

def get_heatmap_plot(adata: AaroniaData, fileName = None, plotConfig: PlotConfig = None):
    fig, ax = plt.subplots()
    pconf = plotConfig
    if pconf == None:
        pconf = PlotConfig()

    if pconf.plottype == "pcolormesh": 
        X = np.array(adata.frequencies, dtype='float32')   
        Y = np.array(adata.sweep_stop, dtype='str')
        Z = np.array(adata.data_matrix, dtype='float32')
        pc = ax.pcolormesh(X, Y, Z, vmin=-70, vmax=-40, cmap='RdBu_r')
        #fig.colorbar(pc, ax)
        ax.set_title('pcolormesh()')

    if pconf.plottype == "imshow":
        Z = np.array(adata.data_matrix, dtype='float32')
        im = plt.imshow(Z, cmap='YlGnBu', aspect='auto')
        ax.set_xticks(np.arange(0, 3001, 1000), ['tick1', 'tick2', 'tick3', 'tick4'])
        fig.colorbar(im, ax = ax, extend='both')

    if fileName == None:    
        plt.show()
    else:
        plt.savefig(fileName)           