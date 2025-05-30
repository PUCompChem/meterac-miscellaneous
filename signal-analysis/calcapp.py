import sys
sys.path.append("./")
from ioutils import *
from signaldescriptors import *

if len(sys.argv) < 2:
    print("Requires a file name")
    sys.exit()

values = readFloatValuesFromSingleLineTextFile(sys.argv[1])
#print(values)


csd = CalcSignalDescriptors(values)
#csd.calculate()
print("mean: ", csd.calculateDescriptor("mean").floatValue)
print("rms: ", csd.calculateDescriptor("rms").floatValue)
print("stdev: ", csd.calculateDescriptor("stdev").floatValue)