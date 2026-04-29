import sys
sys.path.append("./")
from ioutils import *
from signaldescriptors import *
import matplotlib.pyplot as plt


CLI_OPTIONS = {"-h", "--help", "-i", "-input", "-g", "--graphics", "-d", "--descriptor-list" 
                "-V", "--verbose", "-m", "--mode"}

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

def plot_amplitudes(fft_result: dict) -> None:
    """
    Plot the amplitude spectrum from an RFFT result.

    Args:
        fft_result: Dictionary returned by calculate_rfft(), containing
                    'frequencies' and 'amplitudes' arrays
    """
    frequencies = fft_result["frequencies"]
    amplitudes = fft_result["amplitudes"]

    plt.figure(figsize=(10, 5))
    plt.stem(frequencies, amplitudes, basefmt=" ")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Amplitude Spectrum")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if has_cli_option("-h", "--help"):
    print("Description:")
    print("   A program for signal data analysis based on signal descriptors.")
    print("Options:")
    print("  -h, --help             Show this help message and exit")
    print("  -i, --input <file>     Input file to process")
    print("  -g, --graphics         Visualizes FFT graphics (for test purposes only)")
    print("  -d, --descriptor-list  Print the descriptor list")
    print("  -V, --verbose          Enable verbose/debug output")
    exit()

if has_cli_option("-d", "--descriptor-list"):
    print(get_descriptor_list_as_string())
    exit()

mode = "single-line"  #defualt

flag_graphics = has_cli_option("-g", "-graphics")
flag_verbose = has_cli_option("-V", "-verbose")
input_file_name = get_cli_option("-i", "--input")

if input_file_name == None:
    print ("Requires option -i with input file!")
    exit()


if mode == "single-line":
    signal = readFloatValuesFromSingleLineTextFile(input_file_name)
    csd = CalcSignalDescriptors(signal)
    dvalues = csd.calculate()
    #print descriptors
    for dname in dvalues.keys():
        dv = dvalues[dname]
        print (dname, dv.value_to_string())
    
    if flag_graphics:
        fft_result = csd.get_fft_result()    
        #print ("number of frequencies", len(fft_result["frequencies"]))
        #print (fft_result["frequencies"])
        #print (fft_result["amplitudes"])
        plot_amplitudes (fft_result)

