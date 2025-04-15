'''
Console app for managing aaronia data
'''

import sys
from aaronia_sweep_process import *

errors_out = []

class CLIOption:
    def __init__(self, shortName: str, longName: str, requiresArgument : bool):
        self.shortName = shortName
        self.longName = longName
        self.requiresArgument = requiresArgument

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
    
    pass

def print_help(options: list[CLIOption]):
    print("CLI application for managing aaronia data.")
    print("Basic input arguments: ...")
    print("Full argument list:")
    print("   -i <input-file> -o <output-file> -v")
    


#Setting CLI options and default file names
options = [CLIOption("i","input", True), 
           CLIOption("o","output", False),          
           CLIOption("p","operation", False),
           CLIOption("v","verbose", False),           
           CLIOption("h","help", False)]

input_file = None
output_file = None
operation = "heatmap"

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
        ics_data_file = fname
    else:
        errors_out.append("Option -i (--input) has no argument!")
        num_of_errors += 1
else:
    errors_out.append("Option -i (--input) is requred!")
    num_of_errors += 1


if num_of_errors > 0:
    print("  No operation is performed!")
    for err_line in errors_out:
        print("  " + err_line)
    exit()
