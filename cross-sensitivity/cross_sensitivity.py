
class CSCalcData:

    def __init__(self):        
        self.num_of_sensors = None
        self.sensors = None
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
    errors = []

    num_of_sensors_prop = props.get("num_of_sensors")
    if (num_of_sensors_prop!= None):
        try:
            ns = int(num_of_sensors_prop)
        except Exception as e:
            errors.append("num_of_sensors is not correct integer: " + num_of_sensors_prop)
        else:
            cscd.num_of_sensors = ns
    else:    
        errors.append("Property 'num_of_sensors' is missing")

    n = cscd.num_of_sensors
    if (n != None):
        #Parse sensor names
        cscd.sensors = []
        for i in range(n):
            pname = "sensor_" + str(i+1)
            p = props.get(pname)
            cscd.sensors.append(p)
            print(cscd.sensors[i])
            if (p == None):
                errors.append("Property '" + pname + "' is missing")

    #Handle property parsing errors as an excpetion
    if len(errors) > 0:
        errorMsg = "There are property parsing errors:\n"
        for err in errors:
            errorMsg += "  " + err + "\n"
        raise Exception(errorMsg)
    
    return cscd
    

def calc_work_matrix(cscd: CSCalcData):
    pass
 
 
def calc_inv_matrix(cscd: CSCalcData):
    pass
 
    
def calc_concentrations(v: list[float]):
    pass
    
    
    
    