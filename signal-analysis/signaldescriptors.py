import numpy as np


allowed_descriptor_types = ["number", "list", "text"]


class Descriptor:
    def __init__(self, name: str, typestr:str = "number", info: str = None):
        self.name = name
        self.typestr = typestr
        self.info = info

descriptor_list = [
    Descriptor("numpoints"),
    Descriptor("mean"),
    Descriptor("rms"),
    Descriptor("stdev"),
    ]

class DescriptorValue:
    def __init__(self, floatValue: float = None, listValue: list[float] = None, textValue: str = None,
                  errorMsg: str = None, info: str = None):
        self.floatValue = floatValue
        self.listValue = listValue
        self.textValue = textValue
        self.errorMsg = errorMsg
        self.info = info

class CalcSignalDescriptors:
    def __init__(self, signal: list[float], descriptors: list[str] = None): 
        self.signal = signal  
        if descriptors != None:
            #TODO
            self.descriptors = None
        else:                
            self.descriptors = descriptor_list  #by default entire descriptor list is used
        
    def calculate(self) -> dict[str, DescriptorValue]:
        dvalues = {}
        if self.descriptors == None:
            return dvalues
        for d in self.descriptors:
            dv = self.calculateDescriptor(d.name)
            dvalues[d.name] = dv
        return dvalues
    
    def calculateDescriptor(self, name: str) -> DescriptorValue:       
        if name == "numpoints":
            return self.calculateNumOfPoints()
        if name == "mean":
            return self.calculateMean()
        if name == "rms":
            return self.calculateRMS()
        if name == "stdev":
            return self.calculateStDev()       
        return DescriptorValue(errorMsg = "Descriptor '" + name + "' is not supported")
        
    def calculateNumOfPoints(self) -> DescriptorValue:
        val = len (self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateMean(self) -> DescriptorValue:
        val = np.mean(self.signal)
        return DescriptorValue(floatValue = val)

    def calculateRMS(self) -> DescriptorValue:
        arr = np.array(self.signal)
        val = np.sqrt(np.mean(arr**2))
        return DescriptorValue(floatValue = val)
    
    def calculateStDev(self) -> DescriptorValue:
        #arr = np.array(self.signal)
        val = np.std(self.signal)
        return DescriptorValue(floatValue = val)