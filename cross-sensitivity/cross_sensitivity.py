
class CSCalcData:

    def __init__(self):        
        self.cs = None
        
        
def load_properties(filepath):   
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l != '' and not l.startswith("#"):
                tokens = l.split("=")
                if len(tokens) != 2:
                    continue
                key = tokens[0].strip()
                value = tokens[1].strip()
                if key != '' and value != '': 
                    props[key] = value 
    return props


def parse_properties(props) -> CSCalcData:
    cscd = CSCalcData()
    #TODO
    return cscd
    

def calc_work_matrix(cscd: CSCalcData):
    pass
 
 
def calc_inv_matrix(cscd: CSCalcData):
    pass
 
    
def calc_concentrations(v: list[float]):
    pass
    
    
    
    