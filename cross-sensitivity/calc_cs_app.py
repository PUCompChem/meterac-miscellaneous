'''
A simple console app for calculation of cross sensitivity
'''

import sys
sys.path.append("./")
from cross_sensitivity import *
from ioutils import *
from datetime import datetime

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
           CLIOption("b","baseline-correction", True),
           CLIOption("n","negative-correction", True),
           CLIOption("f","measurements-file", True),
           CLIOption("o","output-file", True),
           CLIOption("d","column-indices", True),
           CLIOption("x","max-number-of-measurements", True),
           CLIOption("t","time-stamp-interval", True),
           CLIOption("r","old-version", False),
           CLIOption("p","polarity-reverse", False),
           CLIOption("m","mass-output", False),
           CLIOption("v","verbose", False),
           CLIOption("h","help", False)]

def check_time_stamp(t: int)-> bool:
    if time_stamp_begin != -1:
        if t < time_stamp_begin:
            return False
    if time_stamp_end != -1:
        if t > time_stamp_end:
            return False
    return True

ics_data_file = "./data/ics_data01.txt"        #default value
cs_setting_file = "./data/cs_settings01.txt"   #default value
flag_negative_correction = True                #default value
flag_baseline_correction = False               #default value
flag_mass_output = False                       #default value
measurements_file = None
output_file_name = None
output_file_separator = " "
column_indices = []
max_number_of_measurements = 100000000000000
flag_old_version = False
polarity_reverse = False
polarity_sign = +1.0
flag_time_stamp_interval = False               #default value
time_stamp_begin = -1
time_stamp_end = -1


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
polarity_reverse = "polarity-reverse" in arguments["boolean_options"]
flag_mass_output = "mass-output" in arguments["boolean_options"]

if polarity_reverse:
    polarity_sign = -1.0

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

#Get baseline-correction option
if "baseline-correction" in arguments["standard_options"].keys():
    bl_corr = arguments["standard_options"]["baseline-correction"]
    if bl_corr != None:
        if bl_corr.lower() == "on" or bl_corr.lower() == "true":
            flag_baseline_correction = True
        elif bl_corr.lower() == "off" or bl_corr.lower() == "false":
            flag_baseline_correction = False
        else:
            errors_out.append("Incorrect argument for Option -b (--baseline-correction): " + bl_corr)
            num_of_errors += 1
    else:
        errors_out.append("Option -b (--baseline-correction) has no argument!")
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
    output_file_name = arguments["standard_options"]["output-file"]
    if output_file_name == None:
        errors_out.append("Option -o (--output-file) has no argument!")
        num_of_errors += 1
    else:
        if output_file_name.lower().endswith(".csv"):
           output_file_separator = ","
        if output_file_name.lower().endswith((".tsv", ".txt")):
           output_file_separator = "\t"

#Get time stamp interval:
#Supported formats: t1-t2,  t1, t1-, -t2
if "time-stamp-interval" in arguments["standard_options"].keys():
    t_arg = arguments["standard_options"]["time-stamp-interval"]
    if t_arg == None:
        errors_out.append("Option -t (--time-stamp-interval) has no argument!")
        num_of_errors += 1
    else:
        t_tokens = t_arg.split("-")
        try:
            if t_tokens[0] != "":
                time_stamp_begin = int(t_tokens[0])
            if len(t_tokens) == 2:
                if t_tokens[1] != "":
                    time_stamp_end = int(t_tokens[1])
            else:
                if len(t_tokens) > 2:
                    raise("Incorrect time stamp interval format")
            #print ("t interval:",time_stamp_begin, time_stamp_end)
            if time_stamp_begin == -1 and time_stamp_end == -1:
                raise("Incorrect time stamp interval format")
        except Exception as e:
            errors_out.append("Incorrect -t (--time-stamp-interval) option " + t_arg)
            num_of_errors += 1
        flag_time_stamp_interval = True

if flag_verbose:
    if flag_old_version:
        print("Working with old version")
    print("ics data is loaded from file: " + ics_data_file)
    print("cs settings are loaded from file: " + cs_setting_file)
    print("Negative values correction = " + str(flag_negative_correction))
    print("Baseline correction = " + str(flag_baseline_correction))    
    print("Polarity reverse = ", polarity_reverse)
    if flag_mass_output:
        print("Output unit: mg/m3")
    else:
        print("Output unit: ppm")

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
    if polarity_reverse:
        print("Input voltages sign is changed (polarity_reverse = True)")

#Perform caclulations for measurements data from file
if measurements_file != None:
    #example indices for raw data: -d 3,23,25,27,28,30,32,33
    id_index = -1
    T_index = -1
    V_indices = []
    time_index = -1

    if len(column_indices) != n+3:
        errors_out.append("Incorrect number of column indices (option -d)")
        errors_out.append("Expected indices for: ID T datetime V1 V2 ... Vn utctime")
        num_of_errors += 1
    else:
        #for all indices: 1-base --> 0-base transforms is done
        id_index = column_indices[0] - 1 
        T_index = column_indices[1] - 1
        time_index = column_indices[n+2] - 1
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
    
    out_file = None
    if output_file_name != None:
        try:
            out_file = open(output_file_name, "w", encoding="utf-8")
            #write header line
            header_line = "id" + output_file_separator + "T" + output_file_separator + "date_time" + output_file_separator 
            for i in range(n):
                header_line += "v_" + str(i+1) + output_file_separator
            for i in range(n):
                header_line += "calc_nc_" + str(i+1) + output_file_separator
            for i in range(n):
                header_line += "calc_" + str(i+1) + output_file_separator
            header_line += "Time"
            out_file.write(header_line)
            out_file.write("\n")
        except:
             print("Error on opening file for writing: ", output_file_name)
             exit()

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
        time_str = line[time_index]
        t_stamp = int(time_str)
        
        if not check_time_stamp(t_stamp):
            continue

        dt = datetime.fromtimestamp(t_stamp)
        #dt_str = str(dt.date()) + " " + str(dt.time())
        voltages = []

        for i in range(n):            
            voltages.append(polarity_sign * float(line[V_indices[i]]))
        if flag_verbose:    
            print("id = ", id, "T=", T, "datetime=", str(dt), "V1=", voltages[0], "V2=", voltages[1], 
                "V3=", voltages[2], "V4=", voltages[3], "V5=", voltages[4], "Time= ", time_str)
        
        output_s_f = ""
        if output_file_name != None:
            output_s_f += id + output_file_separator
            output_s_f += str(T) + output_file_separator
            output_s_f += str(dt) + output_file_separator

            for i in range(n):
                output_s_f += str(voltages[i]) + output_file_separator
        
        '''
        Voltage base line correction is not applied
        #if flag_baseline_correction:
            voltage_baseline_correction(id, voltages, cscd, polarity_sign)
        '''
        #print("Calculating non corrected concentrations:")
        if flag_old_version:
            b = calc_b_00(id, voltages, T,  cscd)   
        else:      
            b = calc_b(id, voltages, T,  cscd)

        if flag_baseline_correction:
            for i in range(n):
                b[i] = ppm_baseline_correction(id, i, b[i], cscd)

        if flag_negative_correction:
            correct_negative_values_list(b)

        output_s = "0  "       
        for i in range(n):
            output_s += format(b[i],".2f") + " "
            if output_file_name != None:
                output_s_f += format(b[i],".2f") + output_file_separator
        
        if flag_verbose:
            print(output_s)

        if flag_old_version:        
            C = calc_concentrations_00(id,voltages, T,  cscd)
        else:
            C = calc_concentrations(id,voltages, T,  cscd)

        if flag_baseline_correction:
            for i in range(n):
                C[i,0] = ppm_baseline_correction(id, i, C[i,0], cscd)

        if flag_negative_correction:
            correct_negative_values_matrix(C)
        
        output_s = "0  "  #First output token is the OK flag (no errors)
        for i in range(n):
            output_s += format(C[i,0],".2f") + " "
            if output_file_name != None:
                output_s_f += format(C[i,0],".2f") + output_file_separator
        
        output_s_f += time_str

        if flag_verbose:
            print(output_s)
            
        if output_file_name != None:
            try:
                out_file.write(output_s_f)
                out_file.write("\n")
            except:
                print("Error writing on file...")    

    
    if output_file_name != None:
        out_file.close()
    
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
        voltages.append(polarity_sign * v)

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
    '''
    Voltage base line correction is not applied
    #if flag_baseline_correction:
        voltage_baseline_correction(id, voltages, cscd, polarity_sign)
    '''
    if flag_uncorrected:
        #print("Calculating non corrected concetrations:")
        if flag_old_version:
            b = calc_b_00(id,voltages, T,  cscd)
        else:
            b = calc_b(id,voltages, T,  cscd)

        if flag_baseline_correction:
            for i in range(n):
                b[i] = ppm_baseline_correction(id, i, b[i], cscd)

        if flag_negative_correction:
            correct_negative_values_list(b)

        output_s = "0  "
        for i in range(n):
            if flag_mass_output:
                output_s += format(ppm_to_mass_concentration(i,b[i],T,cscd),".2f") + " "
            else:
                output_s += format(b[i],".2f") + " "
        print(output_s)
    else:
        if flag_old_version:
            C = calc_concentrations_00(id,voltages, T,  cscd)
        else:
            C = calc_concentrations(id,voltages, T,  cscd)

        if flag_baseline_correction:
            for i in range(n):
                C[i,0] = ppm_baseline_correction(id, i, C[i,0], cscd)

        if flag_negative_correction:
            correct_negative_values_matrix(C)

        output_s = "0  "  #First output token is the OK flag (no errors)
        for i in range(n):
            if flag_mass_output:
                output_s += format(ppm_to_mass_concentration(i,C[i,0],T,cscd),".2f") + " "
            else:
                output_s += format(C[i,0],".2f") + " "

        print(output_s)
else:
    print(str(num_of_errors) + #First output token a aproblem flag (number of errors)
        "  No calculation is performed. Found " + str(num_of_errors) + " error/s!")
    for err_line in errors_out:
        print(err_line)


