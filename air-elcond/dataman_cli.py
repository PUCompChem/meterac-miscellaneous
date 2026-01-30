'''
Console app for managing air spectral data
'''

import sys
import os
sys.path.append("./")
from spectral_data_processing import *
#from graphutils import *

errors_out = []
allowed_operation_list = ["wf-plot", "min-max-plot", "average-spectrum", "metrics"]
operations_str = "metrics"   #Default operations string

#Initial work variable values
pconf = None
cfg = None
input_file = None
output_file = None

operations = []
flag_default_operations = False

num_freq_intervals = None
line_group_size = None

class CLIOption:
    def __init__(self, shortName: str, longName: str, requiresArgument : bool, info: str = ""):
        self.shortName = shortName
        self.longName = longName
        self.requiresArgument = requiresArgument
        self.info = info

    def checkOption(self, arg: str) -> bool:
        #Checking whether the argument is an CLI option:
        # -o  or --option (returns true)        
        if arg.startswith("--"):
            #checking long names
            opt = arg[2:]
            if (opt == self.longName):
                return True
        elif arg.startswith("-"):
            #checking short names
            opt = arg[1:]
            if (opt == self.shortName):
                return True
        return False
    
def extract_arguments(args: list[str], options: list[CLIOption]) -> dict[str, object]:
    arg_dict = {}
    n = len(args)
    arg_dict["app_name"] = args[0]
    main_arguments = []
    boolean_options = []
    standard_options = {}
    #Iterated all arguments and find options
    if n > 1:
        i = 1
        while i < n:
            opt_flag = False
            if options:
                for opt in options:
                    if opt.checkOption(args[i]):
                        opt_flag = True
                        if not opt.requiresArgument:
                            boolean_options.append(opt.longName)
                        else:
                            i+=1 #iterated to next argument to get option value
                            if i < n:
                                standard_options[opt.longName] = args[i]
                            else:
                                standard_options[opt.longName] = None
                        break #get out of opt cycle        
            if not opt_flag:
                main_arguments.append(args[i])
            i+=1

    arg_dict["main_arguments"] = main_arguments
    arg_dict["boolean_options"] = boolean_options
    arg_dict["standard_options"] = standard_options
    return arg_dict

def check_standard_option(opt: str) -> str:
    if opt in arguments["standard_options"].keys():
        optVal = arguments["standard_options"][opt]
    if optVal != None:
        return optVal
    else:
        errors_out.append("Option -i (--input) has no argument!")
        num_of_errors += 1
    
def print_help(options: list[CLIOption]):
    print("CLI application for managing aaronia data.")
    #print("Basic input arguments: ...")
    print("Example argument list:")
    print("   -i <input-file> -o <output-file> -v -p <operations-list>")
    print("If operation (-p) and config (-c) are missing all possible operations are performed: ")
    print("      " + "wf-plot, min-max-plot, average-spectrum, metrics")
    print("Full list of options:")
    for opt in options:
        print("  -"+opt.shortName + "  --" + opt.longName + "    " + opt.info)

#Setting CLI options and default file names
options = [CLIOption("i","input", True, "Input data file."), 
           CLIOption("o","output", True, "Output path/file used for the resutls."),          
           CLIOption("p","operations", True, "Specifies what opration are to be performed"),
           CLIOption("c","config", True, "Specifies a config file."),
           CLIOption("n","num-freq-intervals", True, "Number of frequency intervals."),
           CLIOption("g","group-size", True, "Group size - number of lines in a metrics aggregation group."),
           CLIOption("v","verbose", False, "More detailed info is output to the console."),
           CLIOption("x","metrics-info", False, "Prints detailed metrics info."),           
           CLIOption("h","help", False, "Prints this help.")]




def set_plot_config():
    pconf = PlotConfig()
    pconf.x_ticks_index_step = 500
    pconf.file_dpi = 300
    pconf.figure_width = 12
    pconf.figure_height = 6
    pconf.file_padding = 0.05
    pconf.y_ticks_index_step = 20
    #pconf.hide_x_ticks = True
    pconf.color_map = "gist_ncar_r"
    pconf.set_vmin_vmax = False



#Handle CLI input arguments
num_of_errors = 0
arguments = extract_arguments(sys.argv, options)

if "help" in arguments["boolean_options"]:
    print_help(options)
    exit()

if "metrics-info" in arguments["boolean_options"]:
    print("Full list of metrics:")
    for mi_item in metrics_info:
        print("  ", mi_item)
    exit()

flag_verbose = "verbose" in arguments["boolean_options"]

if "config" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["config"]
    if fname != None:
        cfg = load_spectra_process_config_from_property_file(fname)
        n_err = len(cfg.parse_errors)
        if  n_err > 0:
            for i in range(n_err):
                errors_out.append("Config file error: " + cfg.parser_errors[i])
                num_of_errors += 1
    else:
        errors_out.append("Option -c (--config) has no argument!")
        num_of_errors += 1

if "input" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["input"]
    if fname != None:
        input_file = fname
    else:
        errors_out.append("Option -i (--input) has no argument!")
        num_of_errors += 1
else:
    if cfg == None or cfg.input == None:
        errors_out.append("Option -i (--input) is requred when input is not set via config file!")
        num_of_errors += 1
    else:
        input_file = cfg.input 

if "output" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["output"]
    if fname != None:
        output_file = fname
    else:
        errors_out.append("Option -o (--output) has no argument!")
        num_of_errors += 1        
else:
    if cfg != None and cfg.output != None:
        output_file = cfg.output        
    #errors_out.append("Option -o (--output) is requred!")
    #num_of_errors += 1

if "num-freq-intervals" in arguments["standard_options"].keys():
    nfreq_str = arguments["standard_options"]["num-freq-intervals"]
    if nfreq_str != None:
        try:
            nfreq = int(nfreq_str)
            num_freq_intervals = nfreq 
        except Exception as e:
            errors_out.append("Incorrect option -n (--num-freq-intervals). Must be an integer!")
            num_of_errors += 1
    else:
        errors_out.append("Option -n (--num-freq-intervals) has no argument!")
        num_of_errors += 1         

if "operations" in arguments["standard_options"].keys():
    operations_str = arguments["standard_options"]["operations"]
else:
    if flag_verbose:
        print("Performing default operations: ", operations_str)
        flag_default_operations = True     
#Extract operations from string
tokens = operations_str.split(",")
for tok in tokens:    
    op = tok.strip()
    if op != '':
        operations.append(op)
#Check operations
for op in operations:
    if not (op in allowed_operation_list):        
        errors_out.append("Incorrect operation: " + op)
        num_of_errors += 1

if num_of_errors > 0:
    print("  No operation is performed!")
    for err_line in errors_out:
        print("  " + err_line)
    exit()

#Performs operations
#if flag_verbose and (not flag_default_operations):
print("Performing operations: ", operations_str)

#Load and parse aaronia data file
adata = extract_data_from_aaronia_file(input_file)
if flag_verbose and len(adata.errors) > 0:
    print("There are ", len(adata.errors), " errors on loading aaronia data:")
    adata.print_errors()

#Handle input file name and prepare output file names
input_dir, input_file_name = os.path.split(input_file)
if output_file == None:
    print("Output not specifiad via option -o nor via config file (option -c).")
    print("Using input file directory for output: " + input_dir)
    output_file = input_dir

out_file_prefix = "aaronia-cli-out"
dot_index = input_file_name.rfind(".")
if dot_index != -1:
    out_file_prefix = input_file_name[:dot_index]


# Set default config when -c option is missing
if cfg == None:
    cfg = SpectraProcessConfig ()

# Take default info from config file when needed
if num_freq_intervals == None:
    num_freq_intervals = cfg.num_of_frequency_intervals
if line_group_size == None:
    line_group_size = cfg.group_num_of_lines    

'''
#print(out_file_prefix)
if "wf-plot" in operations:
    if flag_verbose:
        print("wf-plot: genrating waterfall heatmap")
    figFileName = os.path.join(output_file,out_file_prefix+".png")
    if flag_verbose:        
        print("waterfall heatmap output:",figFileName)
    set_plot_config()
    get_heatmap_plot(adata, plotConfig = pconf, fileName = figFileName)
'''

if "metrics" in operations:
    sl_out_file = output_file + "-sl.csv"
    grp_out_file = output_file + "-grp.csv"
    adata.get_even_frequency_intervals(num_freq_intervals)
    numformat = cfg.output_number_format

    #Calc single line metrics
    metr_arr = []
    n = len(adata.data_matrix)
    for i in range(n):
        metr = adata.calc_metrics_for_single_line(i)
        metr_arr.append(metr)    
    save_metrics_data_to_file(metr_arr, sl_out_file, True, ",", numformat)

    #Calc group metrics
    metr_arr = adata.calc_metrics_by_groups(line_group_size)
    save_metrics_data_to_file(metr_arr, grp_out_file, True, ",", numformat)