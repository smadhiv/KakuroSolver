from sequenceObjects import sequenceObjects
from kakuroSolver import kakuroSolver
class extractSequences(object):
  """extract individual sequences from the file for vertical and horizontal"""
  horizontalGrid = []
  verticalGrid = []
  verticalSequencesList = []
  horizontalSequencesList = []
  coordsToHorizontalSequenceDict = {}
  coordsToVerticalSequenceDict = {}

  def __init__(self, inputFileName):
    with open(inputFileName, 'r') as inputFile:
      inputFileData = inputFile.readlines()
      inputFileData = [i.strip() for i in inputFileData if (i != '\n' and i != '')]
      self.rows = int(inputFileData[0].split('=')[1])
      self.columns = int(inputFileData[1].split('=')[1])
                                    
      if inputFileData[2] == "Horizontal":
        for i in range(self.rows):
          self.horizontalGrid.append(inputFileData[3 + i].split(','))
      self.handleHorizontal()
      if inputFileData[3 + self.rows] == "Vertical":
        for j in range(self.columns):
          self.verticalGrid.append([])
        for i in range(self.rows):
          temp = [i for i in inputFileData[i + 4 + self.rows].split(',')]
          for j in range(self.columns):
            self.verticalGrid[j].append(temp[j])
      self.handleVertical()
      
  def handleHorizontal(self):
    """extract horizontal sequences from file"""
    sumOfInts = 0
    length = 0
    index = []
    for indexRow, row in enumerate(self.horizontalGrid):
      for indexElement, element in enumerate(row):
        if element == "#":
          continue
        elif int(element) > 0:
          if sumOfInts > 0:
            self.getSequenceInformationHorizontal(index, length, sumOfInts, self.coordsToHorizontalSequenceDict)
          sumOfInts = int(element)
          length = 0
          index = [indexRow, indexElement + 1]
        elif int(element) == 0:
          length += 1
    if sumOfInts != 0:
      self.getSequenceInformationHorizontal(index, length, sumOfInts, self.coordsToHorizontalSequenceDict)

  def handleVertical(self):
    """extract vertical sequences from file"""
    sumOfInts = 0
    length = 0
    index = []
    for indexRow, row in enumerate(self.verticalGrid):
      for indexElement, element in enumerate(row):
        if element == "#":
          continue
        elif int(element) > 0:
          if sumOfInts > 0:
            self.getSequenceInformationVertical(index, length, sumOfInts, self.coordsToVerticalSequenceDict)
          sumOfInts = int(element)
          length = 0
          index = [indexElement + 1, indexRow]
        elif int(element) == 0:
          length += 1
    if sumOfInts != 0:
      self.getSequenceInformationVertical(index, length, sumOfInts, self.coordsToVerticalSequenceDict)
       
  def getSequenceInformationHorizontal(self, index, length, sumOfInts, coordsToHorizontalSequenceDict):
    """create objects for horizontal sequences that describes the sequence including the location, length and expected sum"""
    sequenceObject = sequenceObjects(index, length, sumOfInts, True)
    self.horizontalSequencesList.append(sequenceObject)
    for _ in range(length):
      coordsToHorizontalSequenceDict[tuple(index)] = sequenceObject
      index[1] += (1)
    
  def getSequenceInformationVertical(self, index, length, sumOfInts, coordsToVerticalSequenceDict):
    """create objects for vertical sequences that describes the sequence including the location, length and expected sum"""
    sequenceObject = sequenceObjects(index, length, sumOfInts, False)
    self.verticalSequencesList.append(sequenceObject)
    for _ in range(length):
      coordsToVerticalSequenceDict[tuple(index)] = sequenceObject
      index[0] += (1)
  
  def getSolution(self):
    """generate solution for kakuro by filling vertical and horizontal sequences with valid sequences generated in getUniqueCombinations"""
    solver = kakuroSolver(self.rows, self.columns, self.coordsToHorizontalSequenceDict, self.coordsToVerticalSequenceDict)
    solver.getSolution()
