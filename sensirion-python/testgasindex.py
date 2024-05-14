
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
        self.reportInCSVFormat = False
        self.reportTABDelimeter = False
        self.reportInternalStateParams = False
        self.vocParams = GasIndexAlgorithmParams()
        self.doSubIterations = False
        self.numberOfSubIteration = 10
        self.setCalculationSamplingInterval()
                
    def setCalculationSamplingInterval(self):
        if self.doSubIterations:
            self.calculationSamplingInterval = float(1.0 * self.samplingInterval / numberOfSubIteration)
        else:
            self.calculationSamplingInterval = float(self.samplingInterval)
            

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
    #print(vocRaw, "  ", vocIndex, "  ", calcVocIndex, "   diff =", (vocIndex-calcVocIndex))
    print(getVOCReportLine(vtp, vocRaw, vocIndex, calcVocIndex))


def getDelimiter(vtp: VOCTestParams) -> str:
    if vtp.reportInCSVFormat:
        delim = ','
    else:
        if vtp.reportTABDelimeter:
            delim = '\t'
        else: 
            delim = '  '
    return delim
    
    
def getVOCReportLine(vtp: VOCTestParams, vocRaw: float, vocIndex: int, calcVocIndex: int) -> str:    
    delim = getDelimiter(vtp)
    report = str(vocRaw) + delim + str(vocIndex) + delim + str(calcVocIndex)
    report += (delim + str(vocIndex-calcVocIndex)) 
    
    if vtp.reportInternalStateParams:
        pass
        
    return report


def getVOCReportHeader(vtp: VOCTestParams) -> str:
    delim = getDelimiter(vtp)
    report = 'vocRaw' + delim + 'vocIndex' + delim + 'calcVocIndex' + delim + 'diff'
    return report
    

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
    print(getVOCReportHeader(vtp))
    iterateCsvFile(vtp.fileName, TaskType.CALC_GAS_INDEX, vtp, vtp.startRow, vtp.endRow)
