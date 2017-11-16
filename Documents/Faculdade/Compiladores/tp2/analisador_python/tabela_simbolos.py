class SymbolTable(object):
   
    def __init__(self):
        self.symbolTable = {}
    
    def insertEntry(self, lexema, entry):
        self.symbolTable[lexema] = entry
        
    def getEntry(self, lexema):
        if (self.symbolTable[lexema]):
            return self.symbolTable[lexema]
        else: 
            return None
    
class TableEntry(object):
    
    def __init__(self, lexema, tipo, num_linha, ref_valor):
        self.lexema = lexema
        self.tipo = tipo 
        self.num_linha = num_linha
        self.ref_valor = ref_valor 
        
    def setTipo(self, tipo):
        self.tipo = tipo

    def setRefValor(self, rv):
        self.ref_valor = rv
