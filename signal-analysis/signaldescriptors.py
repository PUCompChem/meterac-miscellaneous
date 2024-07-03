from pydantic import BaseModel, validator



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
    listValue: float = None
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
        #TODO
        return DescriptorValue()
        