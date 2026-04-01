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


'''
print("numpoints: ", csd.calculateDescriptor("numpoints").floatValue)
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)
print("stdev: ", csd.calculateDescriptor("stdev").floatValue)
'''