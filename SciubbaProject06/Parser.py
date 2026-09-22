from CodeModule import*
import SymbolTable as st

class Parser:
    def __init__(self, inFile):         #Takes in a file
        self.file = open(inFile, "r")
        self.symTab = st.SymbolTable()  #Creates a symbol table for parsing
        self.multiLineComment = False
        self.currentLine = 0
        self.lines = []
        for x in self.file:             #initial run through clears all whitespace, comments, and adds labels to the symbol table based on currentLine
            code, self.multiLineComment = newStrippedString(x, self.multiLineComment)
            if code:
                if '(' in code and ')' in code:
                    self.symTab.addEntry(code[code.index('(') + 1: code.index(')')], self.currentLine)
                    continue
                self.lines.append(code)
                self.currentLine += 1

    #Used to help progress through the lines of code
    def hasMoreLines(self):
        if len(self.lines) > 0:
            return True
        
    #Deletes topmost line of code once no longer needed
    def advance(self):
        self.lines.pop(0)

    #Converts both A anc C instructions
    def instructionType(self):

        #If the hack line contains a '@', it is a A instruction
        if '@' in self.lines[0]:
            xxx = self.lines[0][self.lines[0].index('@') + 1:].strip()
            if not xxx.isnumeric():    #If a symbol -> locate or make new entry in the symbol table to determine value
                if not self.symTab.contains(xxx): 
                    self.symTab.addEntry(xxx,-1)
                xxx = self.symTab.getAddress(xxx)
            #Once a number, convert to binary
            if validNumber(str(xxx)):
                return "0" + toBinary(int(xxx))

        #If the hack line contains a '=' or a ';', it is a C instruction 
        #Can have:
            # a '='
            # a ';'
            # both
        #calls necessary symbolic to binary functions for each case
        if '=' in self.lines[0]:
            if ';' in self.lines[0]:
                return "111" + comp(self.lines[0][self.lines[0].index('=') + 1:self.lines[0].index(';')].strip()) + dest(self.lines[0][0:self.lines[0].index('=')].strip()) + jump(self.lines[0][self.lines[0].index(';') + 1:].strip())
            return "111" + comp(self.lines[0][self.lines[0].index('=') + 1:].strip()) + dest(self.lines[0][0:self.lines[0].index('=')].strip()) + jump("null")
        if ';' in self.lines[0]:
            return "111" + comp(self.lines[0][0:self.lines[0].index(';')].strip()) + "000" + jump(self.lines[0][self.lines[0].index(';') + 1:].strip())

#Returns a line accounting without multiline comments, comments, and whitespace
def newStrippedString(string, mlc):
    start = 0
    stop = 0
    newString = ""
    for i in range(len(string)): 
        instance = string[i:i+2]
        if instance == "//":    #if an inline comment, cannot be anymore potential code so just return what you have already
            return (newString + string[start:i].strip(), False)
        if instance == "/*":    #if start of a multiline comment, continue progressing and keep code before the '/*'
            stop = i
            mlc = True
            newString += string[start:stop].strip() 
        if instance == "*/":    #if end of a multiline comment, continue progressing but mark the end
            start = i
            mlc = False
    if not mlc:
        newString += string[start:].strip() #add the remaining part of the string only if not currently multiline comment
    return (newString, mlc) #return updated values

def validNumber(num):
    if not num.isnumeric(): return False            #if not a number: false
    if not (int(num) >= 0 and int(num) <= 32767): return False  #if number is outside of range: false
    return True                                     #if inside of range: true

def toBinary(num):
    binary = ""                                     #create empty string
    for i in reversed(range(0, 15)): 
        if (num - 2 ** i >= 0):
            num -= 2 ** i
            binary += "1"                           #if current binary index val <= num: add a "1" to binary string and subtract from num
        else:
            binary += "0"                           #if current binary index val > num: add a "0" to binary string
    return binary                                   #return 15 char string