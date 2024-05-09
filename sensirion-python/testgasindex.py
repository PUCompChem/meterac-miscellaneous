
import csv
from calcgasindex import *


class TaskType:
    PRINT = 0
    CALC_GAS_INDEX = 1


class VOCTestParams:
    def __init__(self):
        self.fileName = "test.csv"
        self.numberOfPoints = 5
        self.samplingInterval = 300
        pass

def printDictionaty(d: dict):
    for k in d.keys():
        print(k, " = " ,d[k])

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
    if taskType == TaskType.PRINT:
        print(line)
    elif taskType ==TaskType.CALC_GAS_INDEX:
        #TODO
        pass


def testVOCIndex(vtp: VOCTestParams):
    print("Testing VOC index")
    printDictionaty(vtp.__dict__)
    print()

    #Initialization
    print("Initialization")
    voc_params = GasIndexAlgorithmParams()
    GasIndexAlgorithm_init_with_sampling_interval(voc_params,
            GasIndexAlgorithm_ALGORITHM_TYPE_VOC, vtp.samplingInterval)
    printDictionaty(voc_params.__dict__)
