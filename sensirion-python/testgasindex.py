
import csv
from calcgasindex import *


class TaskType:
    PRINT = 0
    CALC_GAS_INDEX = 1


class VOCTestParams:
    def __init__(self):
        self.fileName = "test.csv"
        self.startRow = 2
        self.endRow = 1000000000
        self.samplingInterval = 300
        self.csvVOCRawColumn = 1
        self.csvVOCIndexColumn = 2
        self.vocParams = GasIndexAlgorithmParams()


def printDictionaty(d: dict):
    for k in d.keys():
        print(k, " = " ,d[k])

def iterateCsvFile(fileName: str, taskType: int, manageInfoObj: object,
    startLineNumber = 1, maxLineNumber = 1000000000):
    with open(fileName, mode ='r') as file:
        csvFile = csv.reader(file)
        n = 0
        for line in csvFile:
            n = n+1
            if (n < startLineNumber):
                continue
            if (n > maxLineNumber):
                break
            lineAction(n, line, taskType, manageInfoObj)


def lineAction(lineNum:int, line: [], taskType :int, manageInfoObj: object):
    if taskType == TaskType.PRINT:
        print(line)
    elif taskType ==TaskType.CALC_GAS_INDEX:
        lineAction_CALC_GAS_INDEX(lineNum, line, manageInfoObj)
        pass


def lineAction_CALC_GAS_INDEX(lineNum:int, line: [], vtp: VOCTestParams):
    k = vtp.csvVOCRawColumn
    l = vtp.csvVOCIndexColumn

    vocRaw = float(line[k])
    vocIndex = int(line[l])
    calcVocIndex = GasIndexAlgorithm_process(vtp.vocParams, vocRaw)
    print(vocRaw, "  ", vocIndex, "  ", calcVocIndex, "   diff =", (vocIndex-calcVocIndex))



def testVOCIndex(vtp: VOCTestParams):
    print("Testing VOC index")
    printDictionaty(vtp.__dict__)
    print()

    #Initialization
    print("Initialization")
    print("--------------")
    voc_params = vtp.vocParams
    GasIndexAlgorithm_init_with_sampling_interval(voc_params,
            GasIndexAlgorithm_ALGORITHM_TYPE_VOC, vtp.samplingInterval)
    printDictionaty(voc_params.__dict__)
    print()
    #Iteration
    print("Iteration")
    print("--------------")
    iterateCsvFile(vtp.fileName, TaskType.CALC_GAS_INDEX, vtp, vtp.startRow, vtp.endRow)
