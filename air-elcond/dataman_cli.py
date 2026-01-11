'''
Console app for managing aaronia data
'''

import sys
import os
sys.path.append("./")
from aaronia_sweep_process import *

errors_out = []
allowed_operation_list = ["wf-plot", "min-max-plot", "stat", "average-spectrum"]
operations_str = "wf-plot, min-max-plot, stat, average-spectrum"

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
    print("Full argument list:")
    print("   -i <input-file> -o <output-file> -v -p <operations-list>")
    print("If operation is missing all possible operations are performed: ")
    print("      " + "wf-plot, min-max-plot, stat, average-spectrum")
    for opt in options:
        print("-"+opt.shortName + "  --" + opt.longName + "    " + opt.info)

#Setting CLI options and default file names
options = [CLIOption("i","input", True), 
           CLIOption("o","output", True),          
           CLIOption("p","operations", True),
           CLIOption("c","config", True),
           CLIOption("v","verbose", False),           
           CLIOption("h","help", False)]

pconf = None

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

input_file = None
output_file = None

operations = []
flag_default_operations = False

#Handle CLI input arguments
num_of_errors = 0
arguments = extract_arguments(sys.argv, options)

flag_help = "help" in arguments["boolean_options"]
if flag_help:
    print_help(options)
    exit()

flag_verbose = "verbose" in arguments["boolean_options"]

if "input" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["input"]
    if fname != None:
        input_file = fname
    else:
        errors_out.append("Option -i (--input) has no argument!")
        num_of_errors += 1
else:
    errors_out.append("Option -i (--input) is requred!")
    num_of_errors += 1

if "output" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["output"]
    if fname != None:
        output_file = fname
    else:
        errors_out.append("Option -o (--output) has no argument!")
        num_of_errors += 1        
else:
    #errors_out.append("Option -o (--output) is requred!")
    #num_of_errors += 1
    pass

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
if flag_verbose and (not flag_default_operations):
    print("Performing operations: ", operations_str)

#Load and parse aaronia data file
adata = extract_data_from_aaronia_file(input_file)
if flag_verbose and len(adata.errors) > 0:
    print("There are ", len(adata.errors), " errors on loading aaronia data:")
    adata.print_errors()

#Handle input file name and prepare output file names
input_dir, input_file_name = os.path.split(input_file)
if output_file == None:
    print("Using input file directory for output: " + input_dir)
    output_file = input_dir

out_file_prefix = "aaronia-cli-out"
dot_index = input_file_name.rfind(".")
if dot_index != -1:
    out_file_prefix = input_file_name[:dot_index]

#print(out_file_prefix)
if "wf-plot" in operations:
    if flag_verbose:
        print("wf-plot: genrating waterfall heatmap")
    figFileName = os.path.join(output_file,out_file_prefix+".png")
    if flag_verbose:
        print("waterfall heatmap output:",figFileName)
    set_plot_config()
    get_heatmap_plot(adata, plotConfig = pconf, fileName = figFileName)