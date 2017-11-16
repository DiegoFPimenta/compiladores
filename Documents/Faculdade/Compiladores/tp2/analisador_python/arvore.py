class AST(object):
    
    def __init__(self, nome, father):
         self.nome = nome
         self.children = []
         self.father = father #cria uma referência para o pai
         self.tipo = None  #inteiro ou ponto flutuante
         self.value = None
         self.hasParenthesis = None
         
    def __str__(self, level=0):
        ret = "\t"*level+ repr(self) +"\n"
        for child in self.children:
            if (child != None):                
                ret += child.__str__(level+1) #level+1
                #print(child.__str__())
        return ret
    
    def __repr__(self):
        return self.nome
    
    def __evaluate__(self):
        print('Avaliando nó ' + str(self.nome))
        for child in self.children:
            if (child != None): 
                child.__evaluate__()
        
    def __checkTypes__(self):  
        for child in self.children:
            if (child != None): 
                child.__checkTypes__()        
        
    #code = " "
    #for child in self.children: 
            #code += child.__codegen__()        
    #return code    
    def __codegen__(self):        
        for child in self.children: 
            print(str(child.__codegen__()))
        

"""
O cabeçalho int main() é gerado antes
"""

class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self,father):
        AST.__init__(self,'Block',father)
        print('Criando um nó do tipo Block.')
        #self.children = []
    def __repr__(self):
        return self.nome
    
    def __codegen__(self):
        code = " "
        for child in self.children: 
            code += child.__codegen__()        
        return "{" + code + "}"

"""
Implementação da verificação de tipos:
 . Durante o caminhamento na árvore, o método checkTypes de cada nó 
 é invocado. 
 . Os nós Assign, ArithOp, LogicalOp e RelOp verificam se o tipo 
 do filho da esquerda (children[0]) é compatível com o tipo do filho da direita (children[1]). 

"""

class Assign(AST):
    def __init__(self, left, op, right, father):
        AST.__init__(self,'Assign',father)
        print('Criando um nó do tipo Assign.')
        self.children.append(left)
        self.children.append(right)
        self.left = left
        self.token = self.op = op
        self.right = right
        self.isDecl = None
    
    def __repr__(self):
        return self.nome
    
    def __setIsDecl__(self, isDecl):
        self.isDecl = isDecl
    
    def __evaluate__(self):
        print('Avaliando atribuição.')        
        id_node = self.children[0]
        lex = id_node.token.lexema
        print('Lexema do lado esquerdo: ' + str(lex))
        #Consulta a entrada da tabela de símbolos para esse id 
        te = tabSimbolos.getEntry(lex)
        expr_value = self.children[1].__evaluate__()        
        #print('Valor da expressão no lado direito ' + str(expr_value))
        te.setRefValor(expr_value)
        id_node.value = expr_value   
        print('Valor do lexema ' + str(lex) +  ': ' + str(expr_value))
        return te.ref_valor
    
    def __codegen__(self):
        if (self.isDecl):
            id_node = self.children[0]
            te = tabSimbolos.getEntry(id_node.token.lexema)
            return typeNames[te.tipo] + " " + self.children[0].__codegen__() + " = " + self.children[1].__codegen__() + "" 
        else:
            return self.children[0].__codegen__() + " = " + self.children[1].__codegen__() + "" 
   
    def __checkTypes__(self): 
        if(self.children[0] != None and self.children[1] != None):
            if(self.children[0].__checkTypes__() == self.children[1].__checkTypes__()):            
                print('Tipos compatíveis.')
                return True
            elif (self.children[0].__checkTypes__() < self.children[1].__checkTypes__()):
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[0].__convertTo__(self.children[1].tipo)
                return True
            else: 
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[1].__convertTo__(self.children[0].tipo)
                return True    
        
    
class If(AST):
    def __init__(self, exp, c_true, c_false, father):
        AST.__init__(self, 'If', father)
        print('Criando um nó do tipo If.')
        self.children.append(exp)
        self.children.append(c_true)
        self.children.append(c_false)
        self.exp = exp         
        self.c_true = c_true 
        self.c_false = c_false 
    
    def __repr__(self):
        return self.nome
    
class While(AST):
    def __init__(self, exp, commands, father):
        AST.__init__(self,'While', father)
        print('Criando um nó do tipo While.')
        self.children.append(exp)
        self.children.append(commands)
        self.exp = exp
        self.commands = commands 
    def __repr__(self):
        return self.nome
        
class Read(AST):
    def __init__(self, id_, father):
        AST.__init__(self,'Read', father)
        print('Criando um nó do tipo Read.')
        self.children.append(id_)
        self.id = id_
    def __repr__(self):
        return self.nome
    
class Print(AST):
    def __init__(self, exp, father):
        AST.__init__(self,'Print', father)
        print('Criando um nó do tipo Print.')
        self.children.append(exp)
        self.exp = exp 
    def __repr__(self):
        return self.nome

class BinOp(AST):
    def __init__(self, nome, left, op, right, father):
        AST.__init__(self,nome, father)
        self.children.append(left)
        self.children.append(right)
        self.left = left
        #self.token = 
        self.op = op
        self.right = right
        
    def __repr__(self):
        #self.left.repr()    
        return self.op
    
    def __evaluate__(self):
        print('Avaliando nó ' + str(self.nome))
        for child in self.children:
            if (child != None): 
                return child.__evaluate__()    

    def __checkTypes__(self): 
        if(self.children[0] != None and self.children[1] != None):
            if(self.children[0].__checkTypes__() == self.children[1].__checkTypes__()):            
                print('Tipos compatíveis.')
                return True
            elif (self.children[0].__checkTypes__() < self.children[1].__checkTypes__()):
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[0].__convertTo__(self.children[1].tipo)
                return True
            else: 
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[1].__convertTo__(self.children[0].tipo)
                return True     

    def __codegen__(self):
        return self.left.__codegen__() + self.op + self.right.__codegen__()
        
class LogicalOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'LogicalOp',left, op, right, father)
        print('Criando um nó do tipo LogicalOp com operador ' + str(op))
        

class ArithOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'ArithOp',left, op, right, father)
        print('Criando um nó do tipo ArithOp com operador ' + str(op))
        #print('Filho da esquerda: ' + str(self.children[0]))
        #print('Filho da direita: ' + str(self.children[1]))

    def __evaluate__(self):
        if(self.op == '+'):
            return self.left.__evaluate__() + self.right.__evaluate__()
        elif(self.op == '-'):
            return self.left.__evaluate__() - self.right.__evaluate__()
        elif(self.op == '*'):
            return self.left.__evaluate__() * self.right.__evaluate__()
        elif(self.op == '/'):
            return self.left.__evaluate__() / self.right.__evaluate__()        

    def __codegen__(self):
        return self.left.__codegen__() + self.op + self.right.__codegen__()

class RelOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'RelOp',left, op, right, father)
        print('Criando um nó do tipo RelOp com operador ' + str(op))

class Id(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token, father):
        AST.__init__(self,'Id', father)
        print('Criando um nó do tipo Id.')
        #self.children.append(token)        
        self.token = token        
        #ref para entrada da tabela de símbolos 
    
    def __repr__(self):
        #return repr(self.token)
        return self.token.lexema
    
    def __evaluate__(self):
        te = tabSimbolos.getEntry(self.token.lexema)
        print('Avaliando nó Id. Valor armazenado: ' + str(te.ref_valor))
        if (te.ref_valor != None):
            return te.ref_valor
        else: 
            return 0
    
    def __codegen__(self): 
        #no caso do assembly, retornaria o local de memória ou registrador associado a esse identificador
        return self.token.lexema

class Num(AST):
    def __init__(self, token, father, tipo):
        AST.__init__(self,'Num', father)
        print('Criando um nó do tipo Num.')
        #self.children.append(token)   
        self.token = token
        self.value = token.lexema  #em python, não precisamos nos preocupar com o tipo de value 
        self.tipo = tipo
        
    def __repr__(self):
        #return repr(self.token)        
        return self.value
    
    def __evaluate__(self):
        return self.value
    
    def __checkTypes__(self):        
        return self.tipo
    
    def __convertTo__(self, novotipo):
        self.tipo = novotipo 
        #testa se o tipo atual é float e o novo tipo é int para realizar um truncamento ou arrendondamento 
    
    def __codegen__(self):         
        return str(self.value)