'''
A simple console app for calculation of cross sensitivity
'''

import sys
from cross_sensitivity import *

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
            #print(args[i])
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
            if not opt_flag:
                main_arguments.append(args[i])
            i+=1

    arg_dict["main_arguments"] = main_arguments
    arg_dict["boolean_options"] = boolean_options
    arg_dict["standard_options"] = standard_options
    return arg_dict

def parse_float(arg: str) -> float:
    v = None
    try:
        v = float(arg)
    except Exception as e:
        print("Incorrect float argument: " + arg)
    return v


#Setting CLI options and default file names
options = [CLIOption("-i","ics-data", True), 
           CLIOption("-c","cs-settings", True),
           CLIOption("-u","uncorrected", False)]
ics_data_file = "./data/ics_data01.txt"
cs_setting_file = "./data/cs_settings01.txt"

#Handle CLI input arguments
#Example worflow:
#Input: ID T CO SO2  H2S O3 NO2 ------> AQI CALCULATOR ------> Output: CO SO2 H2S  O3 NO2
num_of_errors = 0
arguments = extract_arguments(sys.argv, options)

#Load basic settings for calculation
props = load_properties(cs_setting_file)
cscd = parse_properties(props)
load_ics_values(ics_data_file, cscd)
n = cscd.num_of_sensors
id = None
voltages = []
T = None

#Parse arguments
main_arguments = arguments["main_arguments"]
if len(main_arguments) != n+2:
    print("Incorrect number of input arguments!")
    num_of_errors += 1
else:
    id = main_arguments[0]
    T = parse_float(main_arguments[1])
    for i in range(n):
        v = parse_float(main_arguments[2+i])
        if v == None:
            num_of_errors+=1
        voltages.append(v)

#Check id
if id != None:
    if id not in cscd.ICSs.keys():
        num_of_errors += 1
        print("Incorrect device id!")
        print("Availabe devices:")
        print("  " + str(list(cscd.ICSs.keys())))

#Perform calculations
if num_of_errors == 0:
    C = calc_concentrations(id,voltages, T,  cscd)
    print(C)
else:
    print("No calculation is performed. Found " + str(num_of_errors) + " error/s!")


