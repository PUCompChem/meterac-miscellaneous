import numpy as np
import math


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
    Descriptor("min"),
    Descriptor("max"),
    Descriptor("span"),
    Descriptor("entropy"),
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
        if name == "min":
            return self.calculateMin()
        if name == "max":
            return self.calculateMax()
        if name == "span":
            return self.calculateSpan()
        if name == "entropy":
            #assuming the signal is between -32000 and +32000,
            # bin_delta ~1000 gives around 60 levels for entropy calculation
            return self.calculateEntropy(1000)  
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
    
    def calculateMin(self) -> DescriptorValue:  
        val = np.min(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateMax(self) -> DescriptorValue:
        val = np.max(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateSpan(self) -> DescriptorValue:
        val = np.max(self.signal) - np.min(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateEntropy(self, bin_delta:float) -> DescriptorValue:
        arr = np.array(self.signal)
        val = calc_entropy_based_on_even_bins(arr, bin_delta)
        return DescriptorValue(floatValue = val)

def calc_entropy_based_on_even_bins(data: np.ndarray, bin_delta:float) -> float:
    #print("### data =  ", data)
    min = np.min(data)
    max = np.max(data)
    num_bins = math.ceil((max-min)/bin_delta)
    if num_bins < 1:
       num_bins = 1
    hist, bins = np.histogram(data, bins=num_bins)
    p = hist/len(data)
    entropy = 0.0
    for x in p:
        if x > 0: # some bins might be 0
            entropy = entropy - x*math.log(x,2)
    #print("bins: ", bins)
    #print("hist: ", hist)
    #print("sum p:", np.sum(p))
    #print("len(data):", len(data))
    return entropy