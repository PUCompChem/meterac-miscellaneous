from pydantic import BaseModel, validator
import numpy as np


allowed_descriptor_types = ["number", "list"]


class Descriptor(BaseModel):
    name: str = ""
    info: str = None
    type: str = "number"

    @validator("type")
    def validate_option(cls, v):
        assert v in allowed_descriptor_types , "must be in " + str(allowed_descriptor_types)
        return v

class DescriptorValue(BaseModel):
    floatValue: float =  None
    listValue: list[float] = None
    errorMsg: str = None
    info: str = None


class CalcSignalDescriptors(BaseModel):
    signal: list[float] = None
    descriptors: list[str] = None
        
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