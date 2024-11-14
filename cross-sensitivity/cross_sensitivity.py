import numpy as np

class CSCalcData:
    def __init__(self):        
        self.num_of_sensors = None
        self.signal_scaling = None
        self.ics_unit_scaling = None
        self.sensors = None         #list of names (designations)
        self.cs = None              #list of lists (cross sensitivity matrix)
        self.R = None               #list of float values (resistences in KOms)
        self.TCSCoeffs = None       #list of lists Temperature Coefficient of Span (interpolated as a polynomial)
        self.ZSCoeffs = None        #list of lists Zero Shift (interpolated as a polynomial)
        self.ICSs = None            #dictinary of lists of float values (Individual Codes of Sensitivity for a set of nodes)
        self.A = None               #numpy array with the working matrix
        self.invA = None            #numpy array with the inverse wotking matrix
        self.invAPrecalc = None     #numpy array with the inverse wotking matrix loaded from file
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

def load_ics_values(filepath: str, cscd: CSCalcData):
    '''
    File format
    #info line
    node, CO, SO2, H2S, O3, NO2
    H40, 4.40, 32.76, 150.51, -37.39, -31.94
    ...    
    '''
    ICSs = {}
    errors = []
    n = cscd.num_of_sensors
    lineNum = 0
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            lineNum += 1
            if l != '' and not l.startswith("#"):
                tokens = l.split(",")
                if len(tokens) != n+1:
                    errors.append("On line " + str(lineNum) + ": incorrect number of tokens! "+
                                  "It must be " + str(n+1))
                    continue
                key = tokens[0].strip()
                if key == '':
                    errors.append("On line " + str(lineNum) + ": first token is empty!")
                    continue

                if key == 'node':
                    #Checking senso names
                    for i in range(n):
                        t = tokens[i+1].strip()
                        if t != cscd.sensors[i]:
                            errors.append("On line " + str(lineNum) + ": the name of sensor #"
                                          + str (i+1) + " '" + t +
                                          "' is not corresponding to the loaded sensor name '" + cscd.sensors[i] + "'")
                else:
                    #loading ics values
                    values =[]
                    for i in range(n):
                        t = tokens[i+1].strip()
                        v = None
                        if t == '':
                            errors.append("On line " + str(lineNum) + ": token #"
                                          + str (i+1) + " is empty")
                        else:
                            try:
                                v = float(t)
                            except Exception as e:
                                errors.append("On line " + str(lineNum) + ": Incorrect float token #"
                                          + str (i+1) + " --> " + t)
                        values.append(v)
                    ICSs[key] = values

    #Handle line reading and parsing errors as an excpetion
    if len(errors) > 0:
        errorMsg = "There are errors on reading and parsing ICS values from file: " + filepath + "\n"
        for err in errors:
            errorMsg += "  " + err + "\n"
        raise Exception(errorMsg)
    else:
       cscd.ICSs = ICSs

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
    
    signal_scaling_prop = props.get("signal_scaling")
    if (signal_scaling_prop!= None):
        try:
            ss = float(signal_scaling_prop)
        except Exception as e:
            errors.append("signal_scaling is not correct float: " + signal_scaling_prop)
        else:
            cscd.signal_scaling = ss
    else:    
        errors.append("Property 'signal_scaling' is missing")

    ics_unit_scaling_prop = props.get("ics_unit_scaling")
    if (ics_unit_scaling_prop!= None):
        try:
            us = float(ics_unit_scaling_prop)
        except Exception as e:
            errors.append("ics_unit_scaling is not correct float: " + ics_unit_scaling_prop)
        else:
            cscd.ics_unitl_scaling = us
    else:    
        errors.append("Property 'ics_unit_scaling' is missing")    

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

        #Parse invA precalculated matrix (properties invA_1, invA_2,...)
        if props.get("invA_1") != None:
            cscd.invAPrecalc = []
            for i in range(n):
                pname = "invA_" + str(i+1)
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
                    cscd.invAPrecalc.append(values)
      
        #Parse resistances
        cscd.R = []
        for i in range(n):
            pname = "R_" + str(i+1)
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

        #Parse TCS polynomial coefficients
        cscd.TCSCoeffs = []
        for i in range(n):
            pname = "TCS_" + str(i+1)
            p = props.get(pname)
            tokens = p.split(",")
            coeffs = []
            for tok in tokens:
                t = tok.strip()
                c = None
                if t == '':
                    errors.append("There is an empty token in '" + pname + "'") 
                else:    
                    try:
                        c = float(t) 
                    except Exception as e:
                           errors.append("Incorrect float token in '" + pname + "': " + t)                        
                    coeffs.append(c)
            cscd.TCSCoeffs.append(coeffs)

        #Parse ZS polynomial coefficients
        cscd.ZSCoeffs = []
        for i in range(n):
            pname = "ZS_" + str(i+1)
            p = props.get(pname)
            tokens = p.split(",")
            coeffs = []
            for tok in tokens:
                t = tok.strip()
                c = None
                if t == '':
                    errors.append("There is an empty token in '" + pname + "'") 
                else:    
                    try:
                        c = float(t) 
                    except Exception as e:
                           errors.append("Incorrect float token in '" + pname + "': " + t)                        
                    coeffs.append(c)
            cscd.ZSCoeffs.append(coeffs)    
   
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

def get_inv_work_matrix(cscd: CSCalcData):
    if cscd.invAPrecalc == None:
        #the matrix is calculated
        calc_work_matrix(cscd)
        calc_inv_work_matrix(cscd)
    else:
        #the matrix is taken from file (pre-calculated)
        cscd.invA = cscd.invAPrecalc

def calc_polynomial_value(x: float, coeffs: list[float]) -> float:
    '''
    coeffs are given in order:
    from power zero to highest power n: c0, c1, ...
    p(x) = c0 + c1*x + c2*x^2 + c3*x^3 + ...
    '''
    p = 0.0
    x_power = 1.0
    n = len(coeffs)
    for i in range(n):
        p += coeffs[i]*x_power
        x_power *= x
    return p

def calc_TCS(sensor_num: int, temperature:float, cscd: CSCalcData) -> float:
    #sensor_num is 0-based
    v = calc_polynomial_value (temperature, cscd.TCSCoeffs[sensor_num])
    return v

def calc_ZS(sensor_num: int, temperature:float, cscd: CSCalcData) -> float:
    #sensor_num is 0-based
    v = calc_polynomial_value (temperature, cscd.ZSCoeffs[sensor_num])
    return v

def getc_ICS(device: str, sensor_num: int, cscd: CSCalcData) -> float:
    #TODO
    return 0

def calc_b_matrix(device: str, voltages: list[float], temperature:float, cscd: CSCalcData):
    # bi = Vi/ICSi .TCSi(T).Ri  + ZSi(T)
    pass

def solve_system(cscd: CSCalcData):
    pass 


def calc_concentrations(device: str, voltages: list[float], temp:float, cscd: CSCalcData):
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
    