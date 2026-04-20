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


flag_graphics = has_cli_option("-g", "-graphics")
input_file_name = get_cli_option("-i", "--input")

if input_file_name == None:
    print ("Requires option -i with input file!")
    exit()

signal = readFloatValuesFromSingleLineTextFile(input_file_name)
#print(signal)

csd = CalcSignalDescriptors(signal)
dvalues = csd.calculate()

for dname in dvalues.keys():
    dv = dvalues[dname]
    print (dname, dv.value_to_string())

fft_result= calculate_real_fft(signal, 10)
print ("number of frequencies", len(fft_result["frequencies"]))
#print (fft_result["frequencies"])
#print (fft_result["amplitudes"])

if flag_graphics:
    plot_amplitudes (fft_result)

'''
print("numpoints: ", csd.calculateDescriptor("numpoints").floatValue)
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)
print("stdev: ", csd.calculateDescriptor("stdev").floatValue)
'''