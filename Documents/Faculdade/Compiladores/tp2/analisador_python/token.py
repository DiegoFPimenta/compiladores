class Token(object):

    def __init__(self, type, lexema, numLinha):
        self.type = type
        self.lexema = lexema
        self.numLinha = None
        self.value = None

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER_CONST, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {lexema})'.format(
            type= tokenNames[self.type],
            lexema=self.lexema
        )

    def __repr__(self):
        #return self.__str__()
        return str(self.type)

    def __convertTo__(self):
        return
