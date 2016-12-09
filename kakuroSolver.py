import itertools
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

  def intitializeSolver(self):
    """initialize the kakuro board"""
    self.kakuroBoard = [[-1 for x in range(self.columns)] for y in range(self.rows)]
    for key, sequenceObject in self.horizontalSequencesDict.items():
      for index in sequenceObject.vertices:
        a, b = index
        self.kakuroBoard[a][b] = 0

  def printSolution(self):
    for num in self.kakuroBoard:
      for item in num:
        if item == -1:
          print '#', ' ',
        else:
          print item, ' ',
      print
      
  def initializeAll(self):
    self.intitializeSolver()
    self.initializeHorizontalDictionary()
    self.initializeVerticalDictionary()
    self.getIntersectionInformation()
  
  def printInformation(self):
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
              
  def getSolution(self):
    print 
    print "Initial Board"
    self.initializeAll()
    self.printSolution()
    self.fillBoard()

    self.printInformation()
    status = self.testSolution()
    if status is True:
      print
      print "Final Solution"
      self.printSolution()
      print
      print "Congratulations!! You got a valid solution"
      return
    if status is not True:
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
              break
            v_index += 1
        for item in toDelete:
          vertSequence.permutatedSolutions.remove(item)
          
    self.fillBoard()
    status = self.testSolution()
    if status is True:
      print
      print "Final Solution"
      self.printSolution()
      print
      print "Congratulations!! You got a valid solution"
      return
    else:
      print
      print "Final Solution"
      self.printSolution()
      print
      print "Sorry!! You did not get a valid solution"
      return           
          
  def fillBoard(self):
    self.fillUniqueSequences()
    status = self.updateSequences()
    while status is True:
      self.fillUniqueSequences()
      status = self.updateSequences()    
       
  def getIntersectionInformation(self):

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
            
    for horiSequence in self.horizontalSequences:
      h_count = 0
      for num in (horiSequence.vertices):
        vertSequence = self.verticalSequencesDict[(num)]
        v_count = 0
        while num != vertSequence.vertices[v_count]:
          v_count += 1
        for h_item in horiSequence.permutatedSolutions:
          isValid = False
          for v_item in vertSequence.permutatedSolutions:
            if h_item[h_count] == v_item[v_count]:
              isValid = True
          if isValid is not True:
            horiSequence.permutatedSolutions.remove(h_item)
        h_count += 1
            
    for vertSequence in self.verticalSequences:
      v_count = 0
      for num in (vertSequence.vertices):
        horiSequence = self.horizontalSequencesDict[(num)]
        h_count = 0
        while num != horiSequence.vertices[h_count]:
          h_count += 1                               
        for v_item in vertSequence.permutatedSolutions:
          isValid = False
          for h_item in horiSequence.permutatedSolutions:
            if h_item[h_count] == v_item[v_count]:
              isValid = True
          if isValid is not True:
            vertSequence.permutatedSolutions.remove(v_item)
        v_count += 1   
    
  def testSolution(self):
    """this function tests for validity of the solution"""
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
          
  def fillUniqueSequences(self):
    """this function fills the board for horizontal sequences"""
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
        
  def getSmallestSequence(self):
    numPerm = 400000
    returnSequence = None
    for sequenceObject in (self.horizontalSequences + self.verticalSequences):
      if sequenceObject.isFilled is True:
        continue
      if len(sequenceObject.permutatedSolutions) < numPerm:
        returnSequence = sequenceObject
    return returnSequence
    