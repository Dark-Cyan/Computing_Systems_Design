# Imports
import Parser as pr
import CodeWriter as cw
import sys
inFile = sys.argv[1]
outFile = str(sys.argv[1])[:sys.argv[1].index('.')]

# Creates a Parser Object with the given input file and a CodeWriter Object with the name for the output file
parser = pr.Parser(inFile)
codeWriter = cw.CodeWriter(outFile)

# Supplies the correct CodeWriter function with the parsed current command
def passParsedCode():
    if parser.commandType() == "C_ARITHMETIC": 
        codeWriter.writeArithmetic(parser.arg1())
    elif parser.commandType() == "C_PUSH" or parser.commandType() == "C_POP":
        codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())

# Parses every line of the input file and passes that information to codeWriter
while parser.hasMoreLines():
    parser.advance()
    passParsedCode()
codeWriter.close()              # Closes output file once done