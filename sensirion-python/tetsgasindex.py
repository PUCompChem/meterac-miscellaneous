
import csv
from calcgasindex import *



def iterateCsvFile(fileName: str, startLineNumber = 1, maxLineNumber = 1000000000):
    with open(fileName, mode ='r') as file:
        csvFile = csv.reader(file)
        n = 0
        for line in csvFile:
            n = n+1
            if (n < startLineNumber):
                continue            
            if (n > maxLineNumber):
                break
            print(line)    
            lineAction(n, line)

def lineAction(n:int, line: []):
    pass




