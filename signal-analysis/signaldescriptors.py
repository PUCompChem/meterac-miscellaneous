from pydantic import BaseModel



class CalcSignalDescriptors(BaseModel):
    signal: list[float] = None
    descriptors: list[str] = None
        
    def calculate(self) -> dict[str, float]:
        #TODO
        print("TBD")
        return None