class sequenceObjects(object):
  """generate objects for each vertical and horizontal sequences"""
  def __init__(self, index, length, sumOfInts, isHorizontal):
    self.isFilled = False
    self.index = index
    self.lengthOfSequence = length
    self.sumOfInts = sumOfInts
    reverseIndex = reversed(self.index)
    self.sortBy= list(reverseIndex)
    self.vertices = [(self.index[0] + (not isHorizontal) * 1 * x, self.index[1] + (isHorizontal) * 1 * x) for x in range(length)]
    self.uniqueSolutions = self.getUniqueCombinations(sumOfInts, length)
    self.permutatedSolutions = self.getCombinations(sumOfInts, length) 
    if len(self.uniqueSolutions) == 0:
      raise ValueError("No Valid Solution")
   
  def getCombinations(self, sumOfInts, length):
    """generate a list of all possible combinations for given sum and length"""
    if length == 2:
      combinations = [[sumOfInts - x, x] for x in range(1, 10) if x > 0 and x < 10 and (sumOfInts - x) < 10 and (sumOfInts - x) > 0 and sumOfInts - x != x]
    else:
      combinations = []
      for x in range(1, 10):
        combinations.extend([combination + [x] for combination in self.getCombinations(sumOfInts - x, length - 1) if x not in combination and x > 0 and x < 10])
    combinations.sort()
    return combinations
  
  def getUniqueCombinations(self, sumOfInts, length):
    """generate a list of all possible combinations for given sum and length without their permutations"""
    uniqueList = []
    combinations = self.getCombinations(sumOfInts, length)
    uniqueCombinations = set()
    for item in combinations:
      uniqueCombinations.add(tuple(sorted(item)))
    for item in uniqueCombinations:
      uniqueList.append(list(item))
    uniqueList.sort()
    return (uniqueList)
