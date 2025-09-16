'''
A simple console app for calculation of cross sensitivity
'''

import sys
sys.path.append("./")
from cross_sensitivity import *
from ioutils import *

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
    print("Full list of options:")
    for opt in options:
        print("-"+opt.shortName + "  --" + opt.longName)


#Setting CLI options and default file names0
options = [CLIOption("i","ics-data", True), 
           CLIOption("c","cs-settings", True),
           CLIOption("u","uncorrected", False),
           CLIOption("v","verbose", False),
           CLIOption("n","negative-correction", True),
           CLIOption("f","measurements-file", True),
           CLIOption("o","output-file", True),
           CLIOption("d","column-indices", True),
           CLIOption("x","max-number-of-measurements", True),
           CLIOption("r","old-version", False),
           CLIOption("h","help", False)]

ics_data_file = "./data/ics_data01.txt"        #default value
cs_setting_file = "./data/cs_settings01.txt"   #default value
flag_negative_correction = True                #default value
measurements_file = None
output_file = None
output_file_separator = ","
column_indices = []
max_number_of_measurements = None
flag_old_version = False


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
flag_old_version = "old-version" in arguments["boolean_options"]

#Get ics-data from input path
if "ics-data" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["ics-data"]
    if fname != None:
        ics_data_file = fname
    else:
        errors_out.append("Option -i (--ics-data) has no argument!")
        num_of_errors += 1

#Get ics-datacs-settings from input path
if "cs-settings" in arguments["standard_options"].keys():
    fname = arguments["standard_options"]["cs-settings"]
    if fname != None:
        cs_setting_file = fname
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

#Get measurements file
if "measurements-file" in arguments["standard_options"].keys():
    measurements_file = arguments["standard_options"]["measurements-file"]
    if measurements_file == None:
        errors_out.append("Option -f (--measurements-file) has no argument!")
        num_of_errors += 1

#Get column indices and max-number-of-measurements
if measurements_file != None:
    if "column-indices" in arguments["standard_options"].keys():
        column_indices_str = arguments["standard_options"]["column-indices"]
        tokens = column_indices_str.split(",")
        for tok in tokens:
            c = None
            try:
                ind = int(tok)
                column_indices.append(ind) 
            except Exception as e:
                errors_out.append("Incorrect index token in --d(-column-indices) option " + tok)
                num_of_errors += 1

    if "max-number-of-measurements" in arguments["standard_options"].keys():
        max_num_str = arguments["standard_options"]["max-number-of-measurements"]
        try:
            max_val = int(max_num_str)
            max_number_of_measurements = max_val            
        except Exception as e:            
            errors_out.append("Incorrect -x (--max-number-of-measurements) option " + max_num_str)
            num_of_errors += 1
    
#Get output file
if "output-file" in arguments["standard_options"].keys():
    output_file = arguments["standard_options"]["output-file"]
    if output_file == None:
        errors_out.append("Option -o (--output-file) has no argument!")
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

if flag_verbose:
    print("cs.signal_scaling = ", cscd.signal_scaling)
    print("cs.ics_unit_scaling = ", cscd.ics_unit_scaling)

#Perform caclulations for measurements data from file
if measurements_file != None:
    #indices for raw data: -d 3,9,14,16,17,19,21
    id_index = -1
    T_index = -1
    V_indices = []

    if len(column_indices) != n+2:
        errors_out.append("Incorrect number of column indices (option -d)")
        errors_out.append("Expected indices for: ID T V1 V2 ... Vn")       
        num_of_errors += 1
    else:
        #for all indices: 1-base --> 0-base transforms is done
        id_index = column_indices[0] - 1 
        T_index = column_indices[1] - 1
        for i in range(n):
            V_indices.append(column_indices[2+i] - 1)
        print("V_indices: ", V_indices)      

    if num_of_errors > 0:
        print(str(num_of_errors) + #First output token a aproblem flag (number of errors)
            "  No calculation is performed. Found " + str(num_of_errors) + " error/s!")
        for err_line in errors_out:
            print(err_line)
        exit()

    print("working with measurements file: ", measurements_file)
    print("Using columns with indices: ", column_indices)
    
    measurements = load_data(measurements_file, "auto")
    line_count = 0
    for line in measurements:
        line_count +=1
        if line_count > max_number_of_measurements:
            break
        #print (line)
        
        #Prepare input data for calcuation
        id = line[id_index]
        T = float(line[T_index])
        voltages = []
        for i in range(n):            
            voltages.append(float(line[V_indices[i]]))
        print("id = ", id, "T=", T, "V1=", voltages[0], "V2=", voltages[1], 
              "V3=", voltages[2], "V4=", voltages[3], "V5=", voltages[4])

        
        #print("Calculating non corrected concentrations:")
        if flag_old_version:
            b = calc_b_00(id, voltages, T,  cscd)   
        else:      
            b = calc_b(id, voltages, T,  cscd)

        output_s = "0  "
        for i in range(n):
            output_s += str(b[i]) + " "
        print(output_s)

        if flag_old_version:        
            C = calc_concentrations_00(id,voltages, T,  cscd)
        else:
            C = calc_concentrations(id,voltages, T,  cscd)

        if flag_negative_correction:
            correct_negative_values(C)
        output_s = "0  "  #First output token is the OK flag (no errors)
        for i in range(n):
            output_s += str(C[i,0]) + " "
        print(output_s)
        
    exit() # the deafault argumetns from command lines are not used 


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
        if flag_old_version:
            b = calc_b_00(id,voltages, T,  cscd)
        else:
            b = calc_b(id,voltages, T,  cscd)    
        output_s = "0  "
        for i in range(n):
            output_s += str(b[i]) + " "
        print(output_s)
    else:
        if flag_old_version:
            C = calc_concentrations_00(id,voltages, T,  cscd)
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


