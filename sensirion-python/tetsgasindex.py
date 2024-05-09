
import csv
from calcgasindex import *


class TaskType:
    PRINT = 0
    CALC_GAS_INDEX = 1


def iterateCsvFile(fileName: str, taskType: int, startLineNumber = 1, maxLineNumber = 1000000000):
    with open(fileName, mode ='r') as file:
        csvFile = csv.reader(file)
        n = 0
        for line in csvFile:
            n = n+1
            if (n < startLineNumber):
                continue            
            if (n > maxLineNumber):
                break
            lineAction(n, line, taskType)


def lineAction(n:int, line: [], taskType :int):
    match taskType:
        case TaskType.PRINT:
            print(line)
            
        case TaskType.CALC_GAS_INDEX:
            #TODO
            pass
         




