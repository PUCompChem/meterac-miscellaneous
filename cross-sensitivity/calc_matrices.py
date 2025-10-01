import sys
sys.path.append("./cross-sensitivity")

from cross_sensitivity import *

def printDictionary(d: dict):
    for k in d.keys():
        print(k, " = ", d[k])

props = load_properties("./data/cs_settings01.txt")
#print(props)

cscd = parse_properties(props)


#load_ics_values("./data/ics_data01.txt", cscd)
#printDictionary(cscd.__dict__)

calc_work_matrix(cscd)
print("A:\n" + str(cscd.A))

#calc_inv_work_matrix(cscd)
get_inv_work_matrix(cscd)

print("invA:")
printMatrix(cscd.invA, ", ")

#print(get_ICS("H41",0,cscd))
#print("b (non corrected concetrations)")
#print(calc_b("H41",[1,2,3,4,5], 30,  cscd))
#print("C (corrected concetrations)")
#print(calc_concentrations("H41",[1,2,3,4,5], 30, cscd))