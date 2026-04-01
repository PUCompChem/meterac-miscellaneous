import sys
sys.path.append("./")
from ioutils import *
from signaldescriptors import *

if len(sys.argv) < 2:
    print("Requires a file name")
    sys.exit()

signal = readFloatValuesFromSingleLineTextFile(sys.argv[1])
#print(signal)

csd = CalcSignalDescriptors(signal)
dvalues = csd.calculate()

for dname in dvalues.keys():
    dv = dvalues[dname]
    print (dname, dv.floatValue)

fft_result= calculate_rfft(signal, 10)
print ("number of frequencies", len(fft_result["frequencies"]))
#print (fft_result["frequencies"])
#print (fft_result["amplitudes"])

plot_amplitudes (fft_result)

'''
print("numpoints: ", csd.calculateDescriptor("numpoints").floatValue)
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)
print("stdev: ", csd.calculateDescriptor("stdev").floatValue)
'''