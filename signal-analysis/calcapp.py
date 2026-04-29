import sys
sys.path.append("./")
from ioutils import *
from signaldescriptors import *

CLI_OPTIONS = {"-h", "--help", "-i", "-input", "-e", "--no-endline",
                "-V", "--verbose"}

def has_cli_option(short: str, long: str) -> bool:
    return short in sys.argv or long in sys.argv

def get_cli_option(short: str, long: str, reserved: set = CLI_OPTIONS) -> str:   
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg in (short, long) and i + 1 < len(args):
            value = args[i + 1]
            if value in reserved:
                raise ValueError(f"Value '{value}' is a reserved option flag, not a valid value for '{arg}'.")
                return None
            return value
    return None


if has_cli_option("-h", "--help"):
    print("Description:")
    print("   A program for calculation of basic signal descriptors.")
    print("Options:")
    print("  -h, --help             Show this help message and exit")
    print("  -i, --input <file>     Input file to process")   
    print("  -d, --descriptor-list  Print the descriptor list")
    print("  -V, --verbose          Enable verbose/debug output")
    print("  -e, --no-endline       Output without endline symbol")
    exit()

if has_cli_option("-d", "--descriptor-list"):
    print(get_descriptor_list_as_string())
    exit()

flag_no_endline = has_cli_option("-e", "--no-endline")
#flag_graphics = has_cli_option("-g", "-graphics")
flag_verbose = has_cli_option("-V", "-verbose")
input_file_name = get_cli_option("-i", "--input")

if input_file_name == None:
    print ("Requires option -i with input file!")
    exit()

signal = readFloatValuesFromSingleLineTextFile(input_file_name)
#print(signal)

csd = CalcSignalDescriptors(signal)
dvalues = csd.calculate()

n_extra_zerors = 10

if flag_verbose:
    for dname in dvalues.keys():
        dv = dvalues[dname]
        print (dname, dv.value_to_string())
else:
    #Non verbose output in a single line
    out_str = ""
    for dname in dvalues.keys():
        dv = dvalues[dname]
        out_str += dv.value_to_string()
        out_str += " "
    #Extra zeros for future descriptors
    for i in range(n_extra_zerors-1):
        out_str += "0 "
    out_str += "0"

    if flag_no_endline:
        print(out_str, end = "")
    else:    
        print(out_str)

    
'''
print("numpoints: ", csd.calculateDescriptor("numpoints").floatValue)
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)
print("stdev: ", csd.calculateDescriptor("stdev").floatValue)
'''