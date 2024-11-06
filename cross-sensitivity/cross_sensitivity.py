import numpy as np

class CSCalcData:
    def __init__(self):        
        self.num_of_sensors = None
        self.sensors = None         #list of names (designations)
        self.cs = None              #list of lists (cross sensitivity matrix)
        self.R = None               #list of float values (resistences in KOms)
        self.ICS = None             #list of float values (Individual Codes of Sensitivity)
        self.A = None               #numpy array with the working matrix
        self.invA = None            #numpy array with the inverse wotking matrix
        self.b = None               #numpy array with voltage scaled/processed matrix
        self.C = None               #numpy array with caclualted concetrations

        
def load_properties(filepath: str):
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


def parse_properties(props: dict) -> CSCalcData:
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
            #print(cscd.sensors[i])
            if (p == None):
                errors.append("Property '" + pname + "' is missing")

        #Parse cross-sensitivity matrix (properties cs_1, cs_2,...)
        cscd.cs = []
        for i in range(n):
            pname = "cs_" + str(i+1)
            p = props.get(pname)
            tokens = p.split(",")
            values = []
            if len(tokens) != n:
                errors.append("Incorrect number of values in '" + pname + "': " + str(len(tokens))
                              + ". It must be " + str(n))
            else:
                for tok in tokens:
                    t = tok.strip()
                    v = None
                    if t == '':
                        errors.append("There is an empty token in '" + pname + "'") 
                    else:    
                        try:
                           v = float(t) 
                        except Exception as e:
                           errors.append("Incorrect float token in '" + pname + "': " + t)                        
                        values.append(v)

                cscd.cs.append(values)
      
        #Parse resistances
        cscd.R = []
        for i in range(n):
            pname = "R" + str(i+1)
            p = props.get(pname)
            if (p == None):
                errors.append("Property '" + pname + "' is missing")
            else:
                v = None
                try:
                    v = float(p)
                except Exception as e:
                    errors.append("Incorrect float '" + pname + "': " + p)
                cscd.R.append(v)

        #Parse Individual Codes of Sensitivity
        cscd.ICS = []
        for i in range(n):
            pname = "ICS" + str(i+1)
            p = props.get(pname)
            if (p == None):
                errors.append("Property '" + pname + "' is missing")
            else:
                v = None
                try:
                    v = float(p)
                except Exception as e:
                    errors.append("Incorrect float '" + pname + "': " + p)
                cscd.ICS.append(v)

    #Handle property parsing errors as an excpetion
    if len(errors) > 0:
        errorMsg = "There are property parsing errors:\n"
        for err in errors:
            errorMsg += "  " + err + "\n"
        raise Exception(errorMsg)
    
    return cscd
    

def calc_work_matrix(cscd: CSCalcData):
    '''
    Calculatin a work matrix for solving a system of ecuations for { Ci | i = 1..n }
        Ci = Vi/ICSi .TCSi(T).Ri  + ZSi(T) + Summa(CSij.Cj | for all j != i)

    denote:
        bi = Vi/ICSi .TCSi(T).Ri  + ZSi(T) 

    then the system is reformulated 
        Ci = bi + Summa(CSij.Cj)

    and additionally 
        Ci - Summa(CSij.Cj) = bi  

    Hence:
        the working matrix is the CS matrix 
        with reverse sign of the non diagonal elements      
    '''

    n = cscd.num_of_sensors
    A = np.array(cscd.cs)    
    for i in range(n):
        for j in range(n):
            if i!=j:
                A[i][j] = -A[i][j]
    cscd.A = A


def calc_inv_work_matrix(cscd: CSCalcData):
    invA = np.linalg.inv(cscd.A)
    cscd.invA = invA    


def calc_b_matrix(voltages: list[float], temp:float, cscd: CSCalcData):
    pass


def solve_system(cscd: CSCalcData):
    pass 


def calc_concentrations(voltages: list[float], temp:float, cscd: CSCalcData):
    pass


def outputCSResult(cscd: CSCalcData, sep: str):
    print("Working matrix (A)")
    printMatrix(cscd.A, sep)
    print()
    print("Inverse working matrix (invA)")
    printMatrix(cscd.invA, sep)
    print()


def printMatrix(M:np.array, sep:str):
    n = len(M)
    for i in range(n):
        line = ""
        for j in range(n):
            line += str(M[i][j])
            if j < n-1:
                line +=(sep)
        print(line)
    