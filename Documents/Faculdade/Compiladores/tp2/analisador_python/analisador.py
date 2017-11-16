#from Gramatica import *
from Buffer import Buffer
from Lexico import Lexico
from token import *
from tabela_simbolos import *

if __name__ == '__main__':

    Buffer = Buffer()
    Lexico = Lexico()

    vetorTokens = []

    for i in Buffer.load_buffer():
        recept, ident, x = Lexico.token_def(i)
        token = Token(recept,ident,x)
        vetorTokens.append(token)


    print(vetorTokens)
    currentType = None
    currentTableEntry = None
    currentToken = None

    tabSimbolos = SymbolTable()
