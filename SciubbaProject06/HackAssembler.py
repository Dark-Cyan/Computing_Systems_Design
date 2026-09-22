import Parser as pr
import sys
inFile = sys.argv[1]
outFile = open(str(sys.argv[1])[:sys.argv[1].index('.')] + ".hack", "w")
#Imports and Ouputs 

#Creates a Parser Object with the given file
parser = pr.Parser(inFile)

#Will put the results of the second runthrough in an output file
while parser.hasMoreLines():
    outFile.write(str(parser.instructionType()) + "\n")
    parser.advance()