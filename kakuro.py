from extractSequences import extractSequences
import sys

if len(sys.argv) != 2:
  raise ValueError("Need 1 argument : python kakuro.py inputFile")
problem = extractSequences(sys.argv[1])
problem.getSolution()
