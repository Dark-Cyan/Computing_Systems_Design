class Parser:

    def __init__(self, inFile):         # Takes in a file
        self.file = open(inFile, "r")
        self.lines = []
        self.currentCommand = None

        # Initial run through clears all comments and whitespace
        for x in self.file:             
            if x[0:2] != "//" and x.strip(): self.lines.append(x.strip())

    # Returns true if there are more lines after the current one
    def hasMoreLines(self):
        if len(self.lines) > 0:
            return True
        
    # Copies then deletes topmost line of code
    def advance(self):
        self.currentCommand = self.lines[0]
        self.lines.pop(0)

    # Returns the command type of the current command
    def commandType(self):
        commandTypes = {
            "add": "C_ARITHMETIC",
            "sub": "C_ARITHMETIC", 
            "neg": "C_ARITHMETIC",
            "eq": "C_ARITHMETIC",
            "gt": "C_ARITHMETIC",
            "lt": "C_ARITHMETIC",
            "and": "C_ARITHMETIC",
            "or": "C_ARITHMETIC",
            "not": "C_ARITHMETIC",

            "push": "C_PUSH",

            "pop": "C_POP",

            "label": "C_LABEL",

            "goto": "C_GOTO",

            "if": "C_IF",

            "function": "C_FUNCTION",

            "return": "C_RETURN",

            "call": "C_CALL",
        }
        return commandTypes[self.currentCommand.split()[0]]
    
    # Returns argument one of the current command 
    # If current command has only one segment, return that (ARITHMETIC)
    def arg1(self):
        commandSegments = self.currentCommand.split()
        return commandSegments[1] if len(commandSegments) > 1 else commandSegments[0]
    
    # Returns argument two of the current command
    def arg2(self):
        return int(self.currentCommand.split()[2])