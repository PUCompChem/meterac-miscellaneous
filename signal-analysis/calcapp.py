import sys
from ioutils import *
from signaldescriptors import *

if len(sys.argv) < 2:
    print("Requires a file name")
    sys.exit()

values = readFloatValuesFromTextFile(sys.argv[1])
#print(values)


csd = CalcSignalDescriptors(signal = values)
#csd.calculate()
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)