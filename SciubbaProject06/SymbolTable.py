class SymbolTable:
    def __init__(self):
        #Creates a dictionary already with all the pre-determined variables and nextAvailableRAM
        self.nextAvailableRAM = 16
        self.table = {
            "SCREEN": 16384,
            "KBD": 24576, 

            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,

            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15
        }

    #If address == -1, add the symbol to the nextAvailable RAM
    #Otherwise, add the symbol with the specified address
    def addEntry(self, symbol, address):
        if address == -1: 
            self.table[symbol] = self.nextAvailableRAM
            self.nextAvailableRAM += 1
        else: self.table[symbol] = address

    #Returns true if their is an active key for a symbol
    def contains(self, symbol):
        return self.table.get(symbol) != None
    
    #Returns the address of a given symbol
    def getAddress(self, symbol):
        return self.table[symbol]
