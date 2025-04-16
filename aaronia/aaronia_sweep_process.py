import matplotlib.pyplot as plt
import numpy as np

class AaroniaData:
    def __init__(self):        
        self.frequencies = None #list[float]
        self.data_matrix = []
        self.sweep_start = []
        self.sweep_stop = []
        self.frequency_unit = "MHz"
        self.frequency_factor = 1.0e-6
        self.errors = []
        self.min_spectrum = None   #np NDArray
        self.max_spectrum = None   #np NDArray
        self.average_spectrum = None  #np NDArray
    
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

    def get_x_ticks_with_step(self, xIndexStep: int) -> list[int]:
        return range(0,len(self.frequencies), xIndexStep)

    def get_x_ticks_labels(self, x_indices: list[int]) -> list[str]:
        labels = []
        for i in x_indices:
            labels.append(str(self.frequencies[i]*self.frequency_factor) 
                          + " " + self.frequency_unit)
        return labels
    
    def get_y_ticks_with_step(self, yIndexStep: int) -> list[int]:
        return range(0, len(self.sweep_stop), yIndexStep)
    
    def get_y_ticks_labels(self, y_indices: list[int]) -> list[str]:
        labels = []
        for i in y_indices:
            labels.append(str(self.sweep_stop[i]))
        return labels
    
    def print_errors(self):
        for err in self.errors:
            print(err)
    
    def calc_basic_spectrum_statistics(self):
        z = np.array(self.data_matrix, dtype='float32')
        self.average_spectrum = np.mean(z, axis=0)
        self.min_spectrum = np.min(z, axis=0)
        self.max_spectrum = np.max(z, axis=0)

class PlotConfig:
    def __init__(self): 
        self.plottype = "imshow"
        self.file_dpi = 150
        self.figure_width = 10 #inches
        self.figure_height = 6 #inches
        self.file_padding = 0.05 # default plot marging is very tight
        self.x_ticks_num = None
        self.y_ticks_num = 5
        self.x_ticks_index_step = 1000
        self.y_ticks_index_step = 100
        self.hide_x_ticks = False
        self.vmin = -150
        self.vmax = 0
        self.set_vmin_vmax = True
        self.color_map = "gist_ncar_r" #"YlGnBu"

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
    #initial data matrices    
    data_matrix0 = [] 
    sweep_start0 = []
    sweep_stop0 = []
    #work variables and flags
    flag_frequencies = False
    val_SweepFrequencies = -1
    val_SweepPoints = -1
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
                    val_SweepFrequencies = int(line.strip()[19:])                    
                    flag_frequencies = True
                    continue 
                if (line.startswith("# SweepStart=")):
                    sweepStart = line.strip()[13:]
                    continue
                if (line.startswith("# SweepStop=")):
                    sweepStop = line.strip()[12:]
                    continue
                if (line.startswith("# SweepPoints=")):
                    val_SweepPoints = int(line.strip()[14:])
                    continue
                continue    
            else:
                values = float_values_from_string(line)
                if flag_frequencies:
                    if adata.frequencies == None:
                        #adding the frequencies from first occurence of line: # SweepFrequencies=
                        adata.frequencies = values
                    else:
                        if val_SweepFrequencies != len(adata.frequencies):
                            adata.errors.append("On line " + str(n) 
                                                + "  number of frequencies in previous sweep " + str(len(adata.frequencies))
                                                +" is different than current section: # SweepFrequencies=" 
                                                + str(val_SweepFrequencies))
                            if val_SweepFrequencies >= len(adata.frequencies):
                                #adding larger set of frequencies from from occurence of line: # SweepFrequencies=
                                adata.frequencies = values
                else:
                    flag_ok = True
                    if val_SweepPoints == -1:
                        flag_ok = False
                        adata.errors.append("On line " + str(n)
                                + "  line with secton '# SweepPoints=' is missing")
                    if val_SweepPoints != len(values):
                        flag_ok = False
                        adata.errors.append("On line " + str(n)
                                + "  number of ellements is different than section: # SweepPoints=" 
                                                + str(val_SweepPoints))                    
                    if flag_ok:
                        #adata.data_matrix.append([sweepStart, sweepStop] + values)
                        data_matrix0.append(values)
                        sweep_start0.append(sweepStart)
                        sweep_stop0.append(sweepStop)

                #Reset work variables
                flag_frequencies = False
                val_SweepFrequencies = -1
                val_SweepPoints = -1
                sweepStart = None
                sweepStop = None
    # Data cleanup
    # Remove data lines with less points than the current max frequency list lenght
    for i in range(len(data_matrix0)):
        if len(data_matrix0[i]) == len(adata.frequencies):
            adata.data_matrix.append(data_matrix0[i])
            adata.sweep_start.append(sweep_start0[i])
            adata.sweep_stop.append(sweep_stop0[i])
        else:
            adata.errors.append("Matrix line " + str(i+1)
                                + "  contains less data points, " + str(len(data_matrix0[i])) + 
                                ", then the number of frequrncies: " + str(len(adata.frequencies)))
    
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
    pconf = plotConfig
    if pconf == None:        
        pconf = PlotConfig()  #using default configuration
    
    fig, ax = [None, None]
    if fileName == None:
        fig, ax = plt.subplots(figsize=(pconf.figure_width, pconf.figure_height))
    else:
        fig, ax = plt.subplots(figsize=(pconf.figure_width, pconf.figure_height), dpi = pconf.file_dpi)   
    
    if pconf.plottype == "pcolormesh": 
        X = np.array(adata.frequencies, dtype='float32')   
        Y = np.array(adata.sweep_stop, dtype='str')
         
        pc = ax.pcolormesh(X, Y, Z, vmin=-70, vmax=-40, cmap='RdBu_r')
        #fig.colorbar(pc, ax)
        ax.set_title('pcolormesh()')

    if pconf.plottype == "imshow":
        Z = np.array(adata.data_matrix, dtype='float32')
        im = None
        if pconf.set_vmin_vmax:
            im = plt.imshow(Z, cmap=pconf.color_map, aspect='auto', vmin = pconf.vmin, vmax = pconf.vmax)
        else:
            im = plt.imshow(Z, cmap=pconf.color_map, aspect='auto')    
        if pconf.hide_x_ticks:
            ax.set_xticks([])
            #ax.spines['bottom'].set_visible(False)
        else:    
            xticks = adata.get_x_ticks_with_step(pconf.x_ticks_index_step)
            ax.set_xticks(xticks, adata.get_x_ticks_labels(xticks))
        yticks = adata.get_y_ticks_with_step(pconf.y_ticks_index_step)
        ax.set_yticks(yticks, adata.get_y_ticks_labels(yticks))
        fig.colorbar(im, ax = ax, extend='both')
        
    if fileName == None:    
        plt.show() #showing the plot in a GUI window
    else:
        plt.savefig(fileName, bbox_inches='tight', pad_inches=pconf.file_padding)


def get_min_max_average_plot(adata: AaroniaData, fileName = None, plotConfig: PlotConfig = None):
    pconf = plotConfig
    if pconf == None:        
        pconf = PlotConfig()  #using default configuration
    
    fig, ax = [None, None]
    if fileName == None:
        fig, ax = plt.subplots(figsize=(pconf.figure_width, pconf.figure_height))
    else:
        fig, ax = plt.subplots(figsize=(pconf.figure_width, pconf.figure_height), dpi = pconf.file_dpi)

    #xticks = adata.get_x_ticks_with_step(pconf.x_ticks_index_step)
    #ax.set_xticks(xticks, adata.get_x_ticks_labels(xticks))

    freq = np.array(adata.frequencies, dtype='float32')*adata.frequency_factor
    ax.plot(freq, adata.min_spectrum, label='min')
    ax.plot(freq, adata.max_spectrum, label='max')
    ax.plot(freq, adata.average_spectrum, label='average')
    ax.set_xlabel("frequency [MHz]")
    ax.set_ylabel("signal [dB]")
    ax.legend()

    if fileName == None:    
        plt.show() #showing the plot in a GUI window
    else:
        plt.savefig(fileName, bbox_inches='tight', pad_inches=pconf.file_padding)

