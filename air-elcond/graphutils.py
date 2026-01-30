import matplotlib.pyplot as plt
from spectral_data_processing import *

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


def get_heatmap_plot(adata: SpectralData, fileName = None, plotConfig: PlotConfig = None):
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


def get_min_max_average_plot(adata: SpectralData, fileName = None, plotConfig: PlotConfig = None):
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

