import sys
sys.path.append("./")
from ioutils import *
from signaldescriptors import *

CLI_OPTIONS = {'-h', '--help', '-i', '--input', '-g', '--graphics'}

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
    print("  -f, --file <file>      Input file to process")
    print("  -g, --graphics         Visualizes FFT graphics (for test purposes only)")
    print("  -d, --descriptor-list  Print the descriptor list")
    print("  -V, --verbose          Enable verbose/debug output")
    exit()

if has_cli_option("-d", "--descriptor-list"):
    print(get_descriptor_list_as_string())
    exit()

flag_graphics = has_cli_option("-g", "-graphics")
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
    for i in range(n_extra_zerors):
        out_str += "0 "
    print(out_str)

if flag_graphics:
    fft_result = csd.get_fft_result()    
    #print ("number of frequencies", len(fft_result["frequencies"]))
    #print (fft_result["frequencies"])
    #print (fft_result["amplitudes"])
    plot_amplitudes (fft_result)


    
'''
print("numpoints: ", csd.calculateDescriptor("numpoints").floatValue)
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)
print("stdev: ", csd.calculateDescriptor("stdev").floatValue)
'''