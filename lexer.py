##########################
# CONSTANTS
##########################

DIGITS = '0123456789'

##########################
# LEXER
##########################

class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\n File {self.pos_start.fn}, Line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,'Illegal Character',details)


##########################
# POSITION
# To keep track of the line and col at which error occurs for better user exp
##########################

class Position:
    def __init__(self,ind,ln,col,fn,ftxt):
        self.ind = ind
        self.ln = ln
        self.col = col 
        self.fn = fn            # File name
        self.ftxt = ftxt        # File Text
    
    def advance(self,cur_char):
        self.ind += 1
        self.col += 1

        if cur_char == '\n':
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.ind,self.ln,self.col,self.fn,self.ftxt)


##########################
# TOKENS
##########################

# TT stands for Token Type
TT_INT   = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS  = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL   = 'MUL'
TT_DIV   = 'DIV'
TT_LPAR  = 'LPAR'
TT_RPAR  = 'RPAR'

class Token:
    def __init__(self,type_,value=None):
        self.type = type_
        self.value = value

    # repr is used to convert Class object to string for showing output
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


##########################
# LEXER
##########################

class Lexer:
    def __init__(self,fn,text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1,fn,text)         # Used to store starting index of text input
        # pos=-1 bcs advance method will immediately set increment to 0 at first run
        self.cur_char = None   # Used to store char at the index
        self.advance()
    
    # for updating the index and char as we keep on reading the text
    def advance(self):
        self.pos.advance(self.cur_char)
        self.cur_char = self.text[self.pos.ind] if self.pos.ind < len(self.text) else None
        # Char can only be updated to new if index<len, if not then char is None

    def make_tokens(self):
        tokens = []

        while self.cur_char != None:
            if self.cur_char in ' \t':
                self.advance()
            elif self.cur_char in DIGITS:
                tokens.append(self.make_number())
            elif self.cur_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.cur_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.cur_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.cur_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.cur_char == '(':
                tokens.append(Token(TT_LPAR))
                self.advance()
            elif self.cur_char == ')':
                tokens.append(Token(TT_RPAR))
                self.advance()
            
            # meaning we input an unrecognized char. Then we print an error
            else:
                pos_start = self.pos.copy()
                char = self.cur_char
                self.advance()
                return [],IllegalCharError(pos_start,self.pos,"'"+char+"'")
                    # Start was pos_start and end was cur pos bcs we advanced in between start and return

        return tokens,None

    def make_number(self):
        num_str = ''
        dot_count = 0       # to check for int or float

        while self.cur_char != None and self.cur_char in DIGITS + '.':
            if self.cur_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.cur_char
            self.advance()
        
        # if dot=1, means float, else int
        if dot_count == 0:
            return Token(TT_INT,int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


##########################
# RUN
##########################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error