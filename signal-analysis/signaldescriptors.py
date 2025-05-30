import numpy as np


allowed_descriptor_types = ["number", "list", "text"]


class Descriptor:
    def __init__(self, name: str, typestr:str = "number", info: str = None):
        self.name = name
        self.typestr = typestr
        self.info = info

descriptor_list = [
    Descriptor(name = "mean"),
    Descriptor(name = "rms")
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
    def __init__(self, signal: list[float], descriptors: list[str]): 
        self.signal = signal  
        self.descriptors = descriptors
        #TODO handle None descriptors
        
    def calculate(self) -> dict[str, DescriptorValue]:
        #TODO
        print("TBD")
        return None
    
    def calculateDescriptor(self, name: str) -> DescriptorValue:       
        if name == "mean":
            return self.calculateMean()
        if name == "rms":
            return self.calculateRMS()        
        return DescriptorValue(errorMsg = "Descriptor '" + name + "' is not supported")
        
    def calculateMean(self) -> DescriptorValue:
        val = np.mean(self.signal)
        return DescriptorValue(floatValue = val)

    def calculateRMS(self) -> DescriptorValue:
        arr = np.array(self.signal)
        val = np.sqrt(np.mean(arr**2))
        return DescriptorValue(floatValue = val)