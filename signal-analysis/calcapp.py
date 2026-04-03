import sys
sys.path.append("./")
from ioutils import *
from signaldescriptors import *

def is_in_args(value: str) -> bool:
    return value in sys.argv

if len(sys.argv) < 2:
    print("Requires a file name")
    sys.exit()

flag_graphics = is_in_args("-g")

signal = readFloatValuesFromSingleLineTextFile(sys.argv[1])
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