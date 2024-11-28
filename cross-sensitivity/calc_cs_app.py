'''
A simple console app for calculation of cross sensitivity
'''

import sys
from cross_sensitivity import *

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

def parse_float(arg: str) -> float:
    v = None
    try:
        v = float(arg)
    except Exception as e:
        errors_out.append("Incorrect float argument: " + arg)
    return v

def print_help(options: list[CLIOption]):
    print("CLI application for calculation of corrected concetrations.")
    print("Basic input arguments: ID T V1 V2 ...")
    print("Full argument list:")
    print("   ID T V1 V2 ... -i <ics-file> -c <cs-file> -u -v")
    print("The application works with default data files:")
    print("   ./data/ics_data01.txt")
    print("   ./data/cs_settings01.txt")


#Setting CLI options and default file names
options = [CLIOption("i","ics-data", True), 
           CLIOption("c","cs-settings", True),
           CLIOption("u","uncorrected", False),
           CLIOption("v","verbose", False),
           CLIOption("n","negative-correction", True),
           CLIOption("h","help", False)]
ics_data_file = "./data/ics_data01.txt"        #default value
cs_setting_file = "./data/cs_settings01.txt"   #default value
flag_negative_correction = True                #default value

#Handle CLI input arguments
# ID T V1 V2 ...Vn -i <ics-file> -c <cs-file> -u -v
num_of_errors = 0
arguments = extract_arguments(sys.argv, options)
flag_help = "help" in arguments["boolean_options"]
if flag_help:
    print_help(options)
    exit()
flag_uncorrected = "uncorrected" in arguments["boolean_options"]
flag_verbose = "verbose" in arguments["boolean_options"]

#Get ics-data from input path
if "ics-data" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["ics-data"]
    if fname != None:
        cs_setting_file = fname
    else:
        errors_out.append("Option -i (--ics-data) has no argument!")
        num_of_errors += 1

#Get ics-datacs-settings from input path
if "cs-settings" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["cs-settings"]
    if fname != None:
        ics_data_file = fname
    else:
        errors_out.append("Option -c (--cs-settings) has no argument!")
        num_of_errors += 1

#Get negative-correction option
if "negative-correction" in arguments["standard_options"].keys():
    neg_corr = arguments["standard_options"]["negative-correction"]
    if neg_corr != None:
        if neg_corr.lower() == "on" or neg_corr.lower() == "true":
            flag_negative_correction = True
        elif neg_corr.lower() == "off" or neg_corr.lower() == "false":
            flag_negative_correction = False
        else:
            errors_out.append("Incorrect argument for Option -n (--negative-correction): " + neg_corr)
            num_of_errors += 1
    else:
        errors_out.append("Option -n (--negative-correction) has no argument!")
        num_of_errors += 1

if flag_verbose:
    print("ics data is loaded from file: " + ics_data_file)
    print("cs settings are loaded from file: " + cs_setting_file)
    print("Negative value correction = " + str(flag_negative_correction))

#Load basic settings for calculation
if flag_verbose:
    print("Loading and parsing cs settings...")
props = load_properties(cs_setting_file)
cscd = parse_properties(props)
load_ics_values(ics_data_file, cscd)
n = cscd.num_of_sensors
id = None
voltages = []
T = None

#Parse arguments
if flag_verbose:
    print("Parsing arguments...")
main_arguments = arguments["main_arguments"]
if len(main_arguments) != n+2:
    errors_out.append("Incorrect number of input arguments!")
    errors_out.append("Expected input arguments: ID T V1 V2 ... Vn")
    errors_out.append("Expecting device ID, Temperature and " + str(n) + " float values!")
    num_of_errors += 1
else:
    id = main_arguments[0]
    T = parse_float(main_arguments[1])
    for i in range(n):
        v = parse_float(main_arguments[2+i])
        if v == None:
            num_of_errors+=1
        voltages.append(v)

#Check device id
if id != None:
    if id not in cscd.ICSs.keys():
        num_of_errors += 1
        errors_out.append("Incorrect device ID!")
        errors_out.append("Availabe devices:")
        errors_out.append("  " + str(list(cscd.ICSs.keys())))

#Perform calculations
#Example worflow:
#Input: ID T CO SO2  H2S O3 NO2 ------> AQI CALCULATOR ------> Output: CO SO2 H2S  O3 NO2
if flag_verbose:
    print("Calculation result:")
if num_of_errors == 0:
    if flag_uncorrected:
        #print("Calculating non corrected concetrations:")
        b = calc_b(id,voltages, T,  cscd)
        output_s = "0  "
        for i in range(n):
            output_s += str(b[i]) + " "
        print(output_s)
    else:
        C = calc_concentrations(id,voltages, T,  cscd)
        if flag_negative_correction:
            correct_negative_values(C)
        output_s = "0  "  #First output token is the OK flag (no errors)
        for i in range(n):
            output_s += str(C[i,0]) + " "
        print(output_s)
else:
    print(str(num_of_errors) + #First output token a aproblem flag (number of errors)
        "  No calculation is performed. Found " + str(num_of_errors) + " error/s!")
    for err_line in errors_out:
        print(err_line)


