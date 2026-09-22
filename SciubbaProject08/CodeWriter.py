import sys

class CodeWriter:
    # Takes in and stores a file name
    # Opens .asm file with given name in write mode
    def __init__(self, outFile):
        self.fileName = outFile.split('/')[0]
        self.currentFile = "NA"
        self.outFile = open(outFile + ".asm", "w")
        self.labelCount = 0
        self.returnAddressCount = 0

    # Translates arithmetic commands into assembly (and writes to outfile)
    def writeArithmetic(self, command):

        # Local Variables
        binaryArithmeticCommands = ["add", "sub", "and", "or"]
        unaryArithmeticCommands = ["neg", "not"]
        booleanEquivalenceCommands = ["eq", "lt", "gt"]
        assembly = {
            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=D&M",
            "or": "M=D|M", 
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "lt": "D;JLT",
            "gt": "D;JGT"
        }

        # Translates binary arithmetic/logical commands
        if command in binaryArithmeticCommands:
            self.outFile.write("@SP\nAM=M-1\nD=M\nA=A-1\n" + assembly[command] + "\n")
        
        # Translates unary arithmetic/logical commands
        elif command in unaryArithmeticCommands:
            self.outFile.write("@SP\nA=M-1\n" + assembly[command] + "\n")

        # Translates boolean equivalence commands
        elif command in booleanEquivalenceCommands:
            self.outFile.write("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@" + self.currentFile + ".becT" + str(self.labelCount)  + "\n" + assembly[command] + "\n@SP\nA=M-1\nM=0\n@" + self.currentFile + ".becE" + str(self.labelCount) + "\n0;JMP\n(" + self.currentFile + ".becT" + str(self.labelCount) + ")\n@SP\nA=M-1\nM=-1\n(" + self.currentFile + ".becE" + str(self.labelCount) + ")\n")
            self.labelCount += 1

    # Translates push/pop commands into assembly (and writes to outfile)
    def writePushPop(self, command, segment, index):
        
        # Local Variables
        symbols = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "TEMP",
        }

        # Translates push commands
        if command == "C_PUSH":
            dynamicallyAllocatedSegments = ("@" + symbols.get(segment, "") + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n")
            push = {
                "constant": ("@" + str(index) + "\nD=A\n"),
                "local": dynamicallyAllocatedSegments,
                "argument": dynamicallyAllocatedSegments,
                "this": dynamicallyAllocatedSegments,
                "that": dynamicallyAllocatedSegments,
                "temp": ("@" + str(index + 5) + "\nD=M\n"),
                "static": ("@" + self.currentFile + "." + str(index) + "\nD=M\n"), 
                "pointer": ("@" + str(index + 3) + "\nD=M\n")
            }
            # Block at the end of every pop command
            repeat = ("@SP\nA=M\nM=D\n@SP\nM=M+1\n")

            self.outFile.write(push[segment] + repeat)

        # Translates pop commands
        elif command == "C_POP":
            dynamicallyAllocatedSegments = ("@" + symbols.get(segment, "") + "\nD=M\n@" + str(index) + "\nD=D+A\n@R13\nM=D\n")
            pop = {
                "local": dynamicallyAllocatedSegments,
                "argument": dynamicallyAllocatedSegments,
                "this": dynamicallyAllocatedSegments,
                "that": dynamicallyAllocatedSegments,
                "temp": ("@" + str(index + 5) + "\nD=A\n@R13\nM=D\n"),
                "static": ("@" + self.currentFile + "." + str(index) + "\nD=A\n@R13\nM=D\n"), 
                "pointer": ("@" + str(index + 3) + "\nD=A\n@R13\nM=D\n")
            }
            # Block at the end of every push command
            repeat = ("@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

            self.outFile.write(pop[segment] + repeat)

    # Translates label commands into assembly (and writes to outfile)
    def writeLabel(self, label):
        self.outFile.write("("+label+")\n")

    # Translates goto commands into assembly (and writes to outfile)
    def writeGoto(self, label):
        self.outFile.write("@"+label+"\n0;JMP\n")

    # Translates ifgoto commands into assembly (and writes to outfile)
    def writeIf(self, label):
        self.outFile.write("@SP\nAM=M-1\nD=M\n@" + label + "\nD;JNE\n")

    # Translates function declaration into assembly (and writes to outfile)
    def writeFunction(self, functionName, nVars):
        self.outFile.write("("+functionName+")\n")
        for i in range(nVars):
            self.writePushPop("C_PUSH", "constant", 0)

    # Translates function calls into assembly (and writes to outfile)
    def writeCall(self, functionName, nArgs):
        variables = ["LCL", "ARG", "THIS", "THAT"]
        self.outFile.write("@"+functionName+"$ret."+str(self.returnAddressCount)+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        for i in variables:
            self.outFile.write("@"+i+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.outFile.write("@SP\nD=M\n@5\nD=D-A\n@"+str(nArgs)+"\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n")
        self.writeGoto(functionName)
        self.writeLabel(functionName+"$ret."+str(self.returnAddressCount))
        self.returnAddressCount += 1

    # Translates return commands into assembly (and writes to outfile)
    def writeReturn(self):
        self.outFile.write("@LCL\nD=M\n@frame\nM=D\n@5\nA=D-A\nD=M\n@retAddr\nM=D\n")
        self.writePushPop("C_POP", "argument", 0)
        self.outFile.write("@ARG\nD=M\n@SP\nM=D+1\n@frame\nD=M-1\nAM=D\nD=M\n@THAT\nM=D\n@frame\nD=M-1\nAM=D\nD=M\n@THIS\nM=D\n@frame\nD=M-1\nAM=D\nD=M\n@ARG\nM=D\n@frame\nD=M-1\nAM=D\nD=M\n@LCL\nM=D\n@retAddr\nA=M\n0;JMP\n")

    # Closes the output file
    def close(self):
        self.outFile.close()

    # Adds the Bootstrap code
    def bootStrap(self):
        self.outFile.write("@256\nD=A\n@SP\nM=D\n")
        self.writeCall("Sys.init", 0)

    # Changes the value of current file for the purposes of static variables
    def changeCurrentFile(self, newFile):
        self.currentFile = newFile