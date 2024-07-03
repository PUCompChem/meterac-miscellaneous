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


class CalcSignalDescriptors(BaseModel):
    signal: list[float] = None
    descriptors: list[str] = None
        
    def calculate(self) -> dict[str, float]:
        #TODO
        print("TBD")
        return None
    
    def calculateDescriptor(self, name: str) -> float | list[float]:
        #TODO
        return 0.0
        