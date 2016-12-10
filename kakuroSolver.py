import itertools
import copy
class kakuroSolver(object):
  """this class generates the solution"""
  def __init__(self, rows, columns, horizontalSequencesDict, verticalSequencesDict):
    self.rows = rows
    self.columns = columns
    self.kakuroBoard = []
    self.horizontalSequences = []
    self.verticalSequences = []
    self.horizontalSequencesDict = horizontalSequencesDict
    self.verticalSequencesDict = verticalSequencesDict

  def intitializeKakuroBoard(self):
    """initialize the kakuro board"""
    self.kakuroBoard = [[-1 for x in range(self.columns)] for y in range(self.rows)]
    for key, sequenceObject in self.horizontalSequencesDict.items():
      for index in sequenceObject.vertices:
        a, b = index
        self.kakuroBoard[a][b] = 0

  def initializeHorizontalDictionary(self):
    """convert dictionary to list for easier access of horizontal sequences"""
    for key, sequenceObject in self.horizontalSequencesDict.items():
      self.horizontalSequences.append(sequenceObject)    
    self.horizontalSequences = sorted(list(set(self.horizontalSequences)))
    for sequenceObject in self.horizontalSequences:
      sequenceObject.index[1] -= sequenceObject.lengthOfSequence
      
  def initializeVerticalDictionary(self):
    """convert dictionary to list for easier access of vertical sequences"""
    for key, sequenceObject in self.verticalSequencesDict.items():
      self.verticalSequences.append(sequenceObject)
    self.verticalSequences = list(set(self.verticalSequences))
    for sequenceObject in self.verticalSequences:
      sequenceObject.index[0] -= sequenceObject.lengthOfSequence
    self.verticalSequences.sort(key=lambda x: x.sortBy, reverse=False)

  def initializeEliminateImprobableUniqueSequences(self):
    """this function removes unique sequences and their permutations that are improbable due to interections with other sequences"""
    for horiSequence in self.horizontalSequences:
      for num in (horiSequence.vertices):
        vertSequence = self.verticalSequencesDict[(num)]
        for h_item in horiSequence.uniqueSolutions:
          isValid = False
          for v_item in vertSequence.uniqueSolutions:
            if len(set(h_item) & set(v_item)) > 0:
              isValid = True
          if isValid is not True:
            horiSequence.uniqueSolutions.remove(h_item)
            tempList = list(itertools.permutations(h_item))
            for item in tempList:
              horiSequence.permutatedSolutions.remove(list(item))
            isValid = False
            
    for vertSequence in self.verticalSequences:
      for num in (vertSequence.vertices):
        horiSequence = self.horizontalSequencesDict[(num)]
        for v_item in vertSequence.uniqueSolutions:
          isValid = False
          for h_item in horiSequence.uniqueSolutions:
            if len(set(h_item) & set(v_item)) > 0:
              isValid = True
          if isValid is not True:
            vertSequence.uniqueSolutions.remove(v_item)
            tempList = list(itertools.permutations(v_item))
            for item in tempList:
              vertSequence.permutatedSolutions.remove(list(item))
            isValid = False

  def eliminateSequencePermutations(self):
    """eliminate improbable permuatations of sequences due to intersections"""
    status = False
    for horiSequence in self.horizontalSequences:
      if horiSequence.isFilled is True:
        continue
      toDelete = []
      for h_permSequence in horiSequence.permutatedSolutions:
        h_index = 0
        for h_coordinate in horiSequence.vertices:
          v_index = 0
          vertSequence = self.verticalSequencesDict[(h_coordinate)]
          while h_coordinate != vertSequence.vertices[v_index]:
            v_index += 1
          isMatch = False
          for v_permSequence in vertSequence.permutatedSolutions:
            if h_permSequence[h_index] == v_permSequence[v_index]:
              isMatch = True
              break
          if isMatch is not True:
            toDelete.append(h_permSequence)
            status = True
            break
          h_index += 1
      for item in toDelete:
        horiSequence.permutatedSolutions.remove(item)
      
    for vertSequence in self.verticalSequences:
      if vertSequence.isFilled is True:
        continue
      toDelete = []
      for v_permSequence in vertSequence.permutatedSolutions:
        v_index = 0
        for v_coordinate in vertSequence.vertices:
          h_index = 0
          horiSequence = self.horizontalSequencesDict[(v_coordinate)]
          while v_coordinate != horiSequence.vertices[h_index]:
            h_index += 1
          isMatch = False
          for h_permSequence in horiSequence.permutatedSolutions:
            if v_permSequence[v_index] == h_permSequence[h_index]:
              isMatch = True
              break
          if isMatch is not True:
            toDelete.append(v_permSequence)
            status = True
            break
          v_index += 1
      for item in toDelete:
        vertSequence.permutatedSolutions.remove(item)
    return status
                
  def fillSequences(self):
    """this function fills the board when there is only one sequence is possible"""
    for sequenceObject in (self.horizontalSequences + self.verticalSequences):
      if len(sequenceObject.permutatedSolutions) != 1 or sequenceObject.isFilled is True:
        continue
      numList = sequenceObject.permutatedSolutions
      numList = numList[0]
      i = 0
      for coordinate in sequenceObject.vertices: 
        a, b = coordinate
        self.kakuroBoard[a][b] = numList[i]
        i += 1
      sequenceObject.isFilled = True
    
  def updateSequences(self):
    """this function eliminates sequence permutations based on exisiting board configuration"""
    count = 0
    for sequenceObject in (self.horizontalSequences + self.verticalSequences):
      if len(sequenceObject.permutatedSolutions) == 1:
        continue
      index = 0
      for coordinate in sequenceObject.vertices:
        a, b = coordinate
        if self.kakuroBoard[a][b] != 0:
          toDelete = []
          for solnList in sequenceObject.permutatedSolutions:
            if solnList[index] != self.kakuroBoard[a][b]:
              toDelete.append(solnList)
          for item in toDelete:
            sequenceObject.permutatedSolutions.remove(item)
            count += 1
        else:
          numberList = []
          toDelete = []
          self.checkNumbersInSameRowColumn(numberList, coordinate)
          for solnList in sequenceObject.permutatedSolutions:
            for number in numberList:
              if number == solnList[index]:
                toDelete.append(solnList)
                break
          for item in toDelete:
            sequenceObject.permutatedSolutions.remove(item)
            count += 1
        index += 1
    if count > 0:
      status = True
    else:
      status = False
    return status

  def checkNumbersInSameRowColumn(self, numberList, coordinate):
    """this function checks unfilled elements in the board and eliminates permutations based on filled elements in the same sequence"""
    a, b = coordinate

    row = a   
    while row >= 0:
      if self.kakuroBoard[row][b] == -1:
        break
      elif self.kakuroBoard[row][b] == 0:
        row -= 1
        continue
      else:
        numberList.append(self.kakuroBoard[row][b])
        row -= 1

    row = a
    while row < self.rows:
      if self.kakuroBoard[row][b] == -1:
        break
      elif self.kakuroBoard[row][b] == 0:
        row += 1
        continue
      else:
        numberList.append(self.kakuroBoard[row][b])
        row += 1
        
    column = b
    while column >= 0:
      if self.kakuroBoard[a][column] == -1:
        break
      elif self.kakuroBoard[a][column] == 0:
        column -= 1
        continue
      else:
        numberList.append(self.kakuroBoard[a][column])
        column -= 1

    column = b
    while column < self.columns:
      if self.kakuroBoard[a][column] == -1:
        break
      elif self.kakuroBoard[a][column] == 0:
        column += 1
        continue
      else:
        numberList.append(self.kakuroBoard[a][column])
        column += 1
                
  def getSequenceInformationForMultipleSolution(self):
    """get the sequence that has maximum possible permutations and also returns a copy of sequences that are not filled yet"""
    backupHorizontalSequences = []
    backupVerticalSequences = []
    isHorizontal = False
    maxLengthSequence = None
    maxSize = 1       
    for h_sequence in self.horizontalSequences:
      if len(h_sequence.permutatedSolutions) > 1:
        backupHorizontalSequences.append(copy.deepcopy(h_sequence))
        if len(h_sequence.permutatedSolutions) > maxSize:
          maxSize = len(h_sequence.permutatedSolutions)
          maxLengthSequence = copy.deepcopy(h_sequence)
          isHorizontal = True

    for v_sequence in self.verticalSequences:
      if len(v_sequence.permutatedSolutions) > 1:
        backupVerticalSequences.append(copy.deepcopy(v_sequence))
        if len(v_sequence.permutatedSolutions) > maxSize:
          maxSize = len(v_sequence.permutatedSolutions)
          maxLengthSequence = copy.deepcopy(v_sequence)
      
    backupKakuroBoard = copy.deepcopy(self.kakuroBoard)      
    return isHorizontal, backupKakuroBoard, maxLengthSequence, backupHorizontalSequences, backupVerticalSequences

  def restoreSequences(self, backupKakuroBoard, backupHorizontalSequences, backupVerticalSequences):
    """this function restores sequences before we attempted a secific combination for the case where we have multiple solutions"""
    for h_sequence in backupHorizontalSequences:
      for h_coordinate in h_sequence.vertices:
        self.horizontalSequencesDict[h_coordinate] = copy.deepcopy(h_sequence)
        for sequences in self.horizontalSequences:
          toDelete = []
          if sequences.vertices == h_sequence.vertices and sequences.index == list(h_coordinate):
            toDelete.append(sequences)
            break
        for item in toDelete:
          self.horizontalSequences.remove(item)
        self.horizontalSequences.append(self.horizontalSequencesDict[h_coordinate])
 
    for v_sequence in backupVerticalSequences:
      for v_coordinate in v_sequence.vertices:
        self.verticalSequencesDict[v_coordinate] = copy.deepcopy(v_sequence)
        for sequences in self.verticalSequences:
          toDelete = []
          if sequences.vertices == v_sequence.vertices and sequences.index == list(v_coordinate):
            toDelete.append(sequences)
            break
        for item in toDelete:
          self.verticalSequences.remove(item)
        self.verticalSequences.append(self.verticalSequencesDict[v_coordinate])

    self.kakuroBoard = copy.deepcopy(backupKakuroBoard)
 
  def fillBoard(self):
    """fills the board with elements confirmed through elimination"""
    self.eliminateSequencePermutations()
    self.fillSequences()
    updateStatus = self.updateSequences()
    while updateStatus is True:
      self.fillSequences()
      updateStatus = self.updateSequences()
      if updateStatus is not True:
        eliminateStatus = self.eliminateSequencePermutations()
        if eliminateStatus is True:
          updateStatus = True
       
  def uniqueSolution(self):
    """solve for unique solution"""
    self.fillBoard()
    return self.testSolution()

  def multipleSolutions(self):
    """solve for multiple solutions"""
    solutionNumber = 0
    isHorizontal, backupKakuroBoard, maxSequence, backupHorizontalSequences, backupVerticalSequences = self.getSequenceInformationForMultipleSolution()
          
    for permuatation in maxSequence.permutatedSolutions:        
      newPermutatedSolution = []
      newPermutatedSolution.append(copy.deepcopy(permuatation)) 
        
      if isHorizontal is True:
        sequenceList = self.horizontalSequences
      else:
        sequenceList = self.verticalSequences
          
      for sequence in sequenceList:
        if sequence.vertices == maxSequence.vertices:
          sequence.permutatedSolutions = copy.deepcopy(newPermutatedSolution)
            
      self.fillBoard()
      isValidSolution = self.testSolution()
      if isValidSolution is True:
        solutionNumber += 1
        print
        print "solution number:", solutionNumber
        self.printSolution()
      self.restoreSequences(backupKakuroBoard, backupHorizontalSequences, backupVerticalSequences)
      
    if solutionNumber == 0:
      print 
      print "Sorry!! You did not get a valid solution"
      self.printDebugInformation()
      print
      print "Final Solution"
      self.printSolution()
    return   
      
  def getSolution(self):
    """this function generates the solution"""
    #intitialize sequences and the kakuro board
    self.intitializeKakuroBoard()
    self.initializeHorizontalDictionary()
    self.initializeVerticalDictionary()
    self.initializeEliminateImprobableUniqueSequences()
    
    #solve
    if self.uniqueSolution() is True:
      self.printSuccess()
    else:
      self.multipleSolutions()

        
  def printSuccess(self):
    print
    print "Solution"
    self.printSolution()
    print
    return   

        
  def printSolution(self):
    """this function prints the kakuro board"""
    for num in self.kakuroBoard:
      for item in num:
        if item == -1:
          print '#', ' ',
        else:
          print item, ' ',
      print

      
  def testSolution(self):
    """this function tests for validity of the solution"""
    #horizontal
    for key, sequenceObject in self.horizontalSequencesDict.items():
      sum = 0
      digits = set()
      for index in sequenceObject.vertices:
        a, b = index
        if self.kakuroBoard[a][b] < 1 or self.kakuroBoard[a][b] > 9:
          return False
        digits.add(self.kakuroBoard[a][b])
        sum += self.kakuroBoard[a][b]
      if sum != sequenceObject.sumOfInts or len(digits) != sequenceObject.lengthOfSequence:
        return False
    
    #vertical
    for key, sequenceObject in self.verticalSequencesDict.items():
      sum = 0
      digits = set()
      for index in sequenceObject.vertices:
        a, b = index
        if self.kakuroBoard[a][b] < 1 or self.kakuroBoard[a][b] > 9:
          return False
        digits.add(self.kakuroBoard[a][b])
        sum += self.kakuroBoard[a][b]
      if sum != sequenceObject.sumOfInts or len(digits) != sequenceObject.lengthOfSequence:
        return False
    return True

    
  def printDebugInformation(self):
    """function to debug that prints sequence values"""
    print "Horizontal"
    for h_sequence in self.horizontalSequences:
      if len(h_sequence.permutatedSolutions) > 1:
        print len(h_sequence.permutatedSolutions)
        print h_sequence.permutatedSolutions
    print "Vertical"
    for v_sequence in self.verticalSequences:
      if len(v_sequence.permutatedSolutions) > 1:
        print len(v_sequence.permutatedSolutions)
        print v_sequence.permutatedSolutions
        
