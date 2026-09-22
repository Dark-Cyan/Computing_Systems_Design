import sys

class CodeWriter:
    # Takes in and stores a file name
    # Opens .asm file with given name in write mode
    def __init__(self, outFile):
        self.fileName = outFile
        self.outFile = open(outFile + ".asm", "w")
        self.labelCount = 0

    # Translates arithmetic commands into assembly (and writes to outfile)
    def writeArithmetic(self, string):

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
        if string in binaryArithmeticCommands:
            self.outFile.write("@SP\nAM=M-1\nD=M\nA=A-1\n" + assembly[string] + "\n")
        
        # Translates unary arithmetic/logical commands
        elif string in unaryArithmeticCommands:
            self.outFile.write("@SP\nA=M-1\n" + assembly[string] + "\n")

        # Translates boolean equivalence commands
        elif string in booleanEquivalenceCommands:
            self.outFile.write("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@" + self.fileName + ".becT" + str(self.labelCount)  + "\n" + assembly[string] + "\n@SP\nA=M-1\nM=0\n@" + self.fileName + ".becE" + str(self.labelCount) + "\n0;JMP\n(" + self.fileName + ".becT" + str(self.labelCount) + ")\n@SP\nA=M-1\nM=-1\n(" + self.fileName + ".becE" + str(self.labelCount) + ")\n")
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
                "static": ("@" + self.fileName + "." + str(index) + "\nD=M\n"), 
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
                "static": ("@" + self.fileName + "." + str(index) + "\nD=A\n@R13\nM=D\n"), 
                "pointer": ("@" + str(index + 3) + "\nD=A\n@R13\nM=D\n")
            }
            # Block at the end of every push command
            repeat = ("@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

            self.outFile.write(pop[segment] + repeat)

    # Closes the output file
    def close(self):
        self.outFile.close()