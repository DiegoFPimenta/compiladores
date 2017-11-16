class Gramatica(object):

    def match(tok,vetorTokens):

        if(token.type == tok):
            print('Token ' + repr(token) + ' reconhecido na entrada.')
            i = i + 1
            if (i < len(vetorTokens)):
                token = vetorTokens[i]
        else:
            print('Erro sintático. Token ' + repr(token) + ' não esperado na entrada.')
            i = i - 1
            token = vetorTokens[i]
            print('Tokens ' + str(Follow[token.type]) + ' esperados na entrada.')
            i = i+ 1
            token = vetorTokens[i]

    def Programa(token, vetorTokens, tabSimbolos, currentType, currentTableEntry, currentToken):

        match("INT",vetorTokens)
        match(MAIN,vetorTokens)
        match(LBRACKET,vetorTokens)
        match(RBRACKET,vetorTokens)
        match(LBRACE,vetorTokens)
        match(RBRACE,vetorTokens)
        lista = AST('Astnode',None,tabSimbolos)
        ast = Decl_Comando(lista)
        if(token.type == EOF):
            match(EOF,vetorTokens)
            print('Fim da análise sintática.')
        return ast

    def Decl_Comando(lista):
        global token, tabSimbolos, currentType, currentTableEntry, currentToken

        if (token.type == INT or token.type == FLOAT):
            lista2 = Declaracao(lista)
            return  Decl_Comando(lista2)
        elif (token.type == LBRACE or token.type == ID or token.type == IF or token.type == WHILE or token.type == READ or token.type == PRINT):
            lista2 = Comando(lista) #Criamos nós na ast para cada comando encontrado
            return Decl_Comando(lista2)
        else:
            return lista

    def Declaracao(lista):
        global token, tabSimbolos, currentType, currentTableEntry, currentToken
        Tipo()
        if (token.type == ID):
            currentToken = token
            te = TableEntry(token.lexema, currentType, None, None)
            currentTableEntry = te
            tabSimbolos.insertEntry(token.lexema, te)
            match(ID,vetorTokens) #cria uma entrada na tabela de símbolos para esse identificador
            return Decl2(lista)
        return lista


    def Tipo():
        global token, tabSimbolos, currentType, currentTableEntry, currentToken
        if (token.type == INT):
            match(INT,vetorTokens)
            currentType = int_type
        elif (token.type == FLOAT):
            match(FLOAT,vetorTokens)
            currentType = float_type

    #COMMA ID Decl2 | PCOMMA | ATTR Expressao Decl2
    def Decl2(lista):
        global token, tabSimbolos, currentType, currentTableEntry, currentToken
        if (token.type == COMMA):
            match(COMMA,vetorTokens)
            if (token.type == ID):
                currentToken = token
                te = TableEntry(token.lexema, currentType, None, None)
                currentTableEntry = te
                tabSimbolos.insertEntry(token.lexema, te)
                match(ID,vetorTokens) #cria uma entrada na tabela de símbolos para esse identificador
                return Decl2(lista)
        elif (token.type == PCOMMA):
            match(PCOMMA,vetorTokens)
            return lista
        elif (token.type == ATTR):
            id_node = Id(currentToken,None)
            match(ATTR,vetorTokens)
            expr_node = Expressao()
            attr_node = Assign(id_node, '=', expr_node, None)
            attr_node.__setIsDecl__(True)
            lista.children.append(attr_node)
            return Decl2(lista)
        return lista# vazio e

    def Comando(lista):
        global token, tabSimbolos, currentType, currentTableEntry, currentToken

        if (token.type == ID): #nesse momento, podemos buscar informações sobre esse Id na tabela de símbolos
            Atribuicao(lista)
        elif (token.type == IF):
            ComandoSe(lista)
        elif (token.type == WHILE):
            ComandoEnquanto(lista)
        elif (token.type == PRINT):
            ComandoPrint(lista)
        elif (token.type == READ):
            ComandoRead(lista)
        elif (token.type == LBRACE):#Abre chave {
            bloco(lista)

        return lista

    def Bloco(lista):
        match("LBRACE",vetorTokens)
        lista = Decl_Comando()
        match("RBRACE",vetorTokens)
        return lista


    def Atribuicao(lista):
        id_node = Id(token,None,tabSimbolos)
        te = tabSimbolos.get_entry(token.valor)
        match("ID",vetorTokens)
        match("ATTR",vetorTokens)
        exp_node = Expressao()
        lista.children.append(Assign(id_node,"=",expr_node,None,tabSimbolos))
        match("PCOMMA",vetorTokens)
        return lista


    def ComandoSe(lista):
        match("IF",vetorTokens)
        match("LBRACKET",vetorTokens)
        cond = Expressao()
        match("RBRACKET",vetorTokens)

        if_true = AST('if_true',None,tabSimbolos)
        node_true = Comando(if_true)

        if_false = AST('If_false',None,tabSimbolos)
        node_false = ComandoSenao(if_false)

        if_node = If(condicao,node_true,node_false,None,tabSimbolos)
        lista.children.append(if_node)


    def ComandoSenao(lista):

        if(token.type == "ELSE"):
            match("ELSE",vetorTokens)
            node = Comando(lista)
            return node
        else:
            return None


    def ComandoEnquanto(lista):

        match("WHILE",vetorTokens)
        match("LBRACKET",vetorTokens)
        cond =  Expressao(lista)
        match("RBRACKET",vetorTokens)

        ver = AST('while_true',None,tabSimbolos)
        nodo = comando(ver)
        wile_node = While(condicao,nodo,None,tabSimbolos)
        lista.children.append(wile_node)

        return lista

    def ComandoRead(lista):

        match("READ",vetorTokens)
        id_node = Id(token,None,tabSimbolos)
        te = tabSimbolos.get_entry(token.valor)
        match("ID",vetorTokens)
        match("PCOMMA",vetorTokens)
        node_read = Read(id_node,None,tabSimbolos)
        lista.children.append(node_read)

        return lista

    def ComandoPrint(lista):

        match("PRINT",vetorTokens)
        match("LBRACKET",vetorTokens)
        exp = Expressao()
        match("RBRACKET",vetorTokens)
        match("PCOMMA",vetorTokens)

        node_print = Print(exp,None,tabSimbolos)
        lista.children.append(node_print)

        return lista

    def Expressao():

        exp1 = Conjuncao()
        exp2 = ExpressaoOpc(exp1)

        if exp2 in not None:
            return exp2
        else:
            return exp1


    def ExpressaoOpc(exp):

        node1 = None
        node2 = None

        if(token.type == "OR"):
            match("OR",vetorTokens)
            exp1 = Conjuncao()
            node1 = logicalOP(exp,||,exp1,None,tabSimbolos)
            node2 = ExpressaoOpc(node1)
        else:
            return None


    def Conjuncao():
        exp1 = Igualdade()
        exp2 = ConjuncaoOpc(exp1)

        if exp2 is not None:
            return exp2
        else:
            return exp1

    def ConjuncaoOpc(exp):

        if(token.type == "AND"):
            match("AND",vetorTokens)
            exp1 = Igualdade()
            node1 = logicalOP(exp, &&, exp1,None,tabSimbolos)
            node2 = ConjuncaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1


    def Igualdade():

        exp1 = Relacao()
        exp2 = IgualdadeOpc(exp1)

        if exp2 is not None:
            return exp2
        else:
            exp1


    def IgualdadeOpc(exp):

        node1 = None
        node2 = None


        if(token.type == "EQ":
            OpIgual()
            exp1 = Relacao()
            node1 = RelOp(exp,'==',exp1,None,tabSimbolos)
            node2 = IgualdadeOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        elif(token.type == "NE"):
            OpIgual()
            exp1 = Relacao()
            node1 = RelOp(exp,'!=',exp1,None,tabSimbolos)
            node2 = IgualdadeOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1
        else:
            return None


    def OpIgual():

        if(token.type == "EQ"):
            match("EQ",vetorTokens)
        elif(token.type == "NE"):
            match("NE",vetorTokens)


    def Relacao():

        exp1 = Adicao()
        exp2 = RelacaoOpc(exp1)

        if exp2 is not None:
            return exp2
        else:
            return exp1


    def RelacaoOpc(exp):

        node1 = None
        node2 = None

        if(token.type == "LT"):
            OpRel()
            exp2 = Adicao()
            node1 = RelOp(exp, '<', exp2,None,tabSimbolos)
            node2 = RelacaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        elif(token.type == "LE"):
            OpRel()
            exp2 = Adicao()
            node1 = RelOp(exp1, '<=', exp2,None,tabSimbolos)
            node2 = RelacaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        elif(token.type == "GT"):
            OpRel()
            exp2 = Adicao()
            node1 = RelOp(exp1, '>', exp2,None,tabSimbolos)
            node2 = RelacaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        elif(token.type == "GE"):
            OpRel()
            exp2 = Adicao()
            node1 = RelOp(exp1, '>=', exp2,None,tabSimbolos)
            node2 = RelacaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1
        else:
            return None


    def OpRel():

        if(token.type == "LT"):
            match("LT",vetorTokens)

        if(token.type == "LE"):
            match("LE",vetorTokens)

        if(token.type == "GT"):
            match("GT",vetorTokens)

        if(token.type == "GE"):
            match("GE",vetorTokens)


    def Adicao():
        exp1 = Termo()
        exp2 = AdicaoOpc(exp1)

        if exp2 is not None:
            return exp2
        else:
            return exp1


    def AdicaoOpc(exp):

        node1 = None
        node2 = None


        if(token.type == "PLUS"):

            OpAdicao()
            exp2 = Termo()
            node1 = ArithOp(exp,'+',exp2,None,tabSimbolos)
            node2 = AdicaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        elif(token.type == "MINUS"):

            OpAdicao()
            exp2 = Termo()
            node1 = ArithOp(exp,'-',exp2,None,tabSimbolos)
            node2 = AdicaoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        else:
            return None

    def OpAdicao():

        if(token.type == "PLUS"):
            match("PLUS",vetorTokens)
        elif(token.type == "MINUS"):
            match("MINUS",vetorTokens)
        }


    def Termo():

        exp1 = Fator()
        exp2 = TermoOpc(exp1)

        if exp2 is not None:
            return exp2
        else:
            return exp1


    def TermoOpc(exp):


        node1 = None
        node2 = None


        if(token.type == "MULT"):

            OpMult()
            exp2 = Fator()
            node1 = ArithOp(exp,'*',exp2,None,tabSimbolos)
            node2 = TermoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

        elif(token.type == "DIV"):

            OpMult()
            exp2 = Fator()
            node1 = ArithOp(exp,'/',exp2,None,tabSimbolos)
            node2 = TermoOpc(node1)

            if node2 is not None:
                return node2
            else:
                return node1

   def OpMult():

        if(token.type == "MULT"):
            match("MULT",vetorTokens)
        elif(token.type == "DIV"):
            match("DIV",vetorTokens)


    def Fator():

        if(token.type == "ID"):
            id_node = Id(token,None,int_type,tabSimbolos)
            match("ID",vetorTokens)
            return id_node

        if(token.type == "INTEGER_CONST"):
            num_node = Num(token,None,int_type,tabSimbolos)
            match("INTEGER_CONST",vetorTokens)
            return num_node

        if(token.type == "FLOAT_CONST"):
            float_node = Num(token,None,float_type,tabSimbolos)
            match("FLOAT_CONST",vetorTokens)
            return float_type

        if(token.type == "LBRACKET"):
            match("LBRACKET",vetorTokens)
            exp1 = Expressao()
            match("RBRACKET")
