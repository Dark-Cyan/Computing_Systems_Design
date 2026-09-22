# Imports
import Parser as pr
import CodeWriter as cw
import sys, os

# Sets up inFile and outFile
inFile = sys.argv[1]
if ".vm" in inFile:
    outFile = str(sys.argv[1])[:sys.argv[1].index(".vm")]
else:
    outFile = os.path.join(inFile, inFile)

# Creates a Parser Object with the given input file and a CodeWriter Object with the name for the output file
codeWriter = cw.CodeWriter(outFile)

# Supplies the correct CodeWriter function with the parsed current command
def passParsedCode():
    if parser.commandType() == "C_ARITHMETIC": 
        codeWriter.writeArithmetic(parser.arg1())
    elif parser.commandType() == "C_PUSH" or parser.commandType() == "C_POP":
        codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())
    elif parser.commandType() == "C_LABEL":
        codeWriter.writeLabel(parser.arg1())
    elif parser.commandType() == "C_GOTO":
        codeWriter.writeGoto(parser.arg1())
    elif parser.commandType() == "C_IF":
        codeWriter.writeIf(parser.arg1())
    elif parser.commandType() == "C_FUNCTION":
         codeWriter.writeFunction(parser.arg1(), parser.arg2())
    elif parser.commandType() == "C_RETURN":
         codeWriter.writeReturn()
    elif parser.commandType() == "C_CALL":
         codeWriter.writeCall(parser.arg1(), parser.arg2())

# Parses every line of the input file(s) and passes that information to codeWriter
if ".vm" in inFile:
    codeWriter.changeCurrentFile(outFile)
    parser = pr.Parser(inFile)
    while parser.hasMoreLines():
        parser.advance()
        passParsedCode()
    codeWriter.close()              # Closes output file once done
else:    
    codeWriter.bootStrap()
    for file in os.listdir(inFile):
        filePath = os.path.join(inFile, file)
        parser = pr.Parser(filePath)
        codeWriter.changeCurrentFile(filePath.split('/')[1].split(".vm")[0])
        while parser.hasMoreLines():
            parser.advance()
            passParsedCode()
    codeWriter.close()              # Closes output file once done