from string_arrows import *

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
        result += f'File {self.pos_start.fn}, Line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt,self.pos_start,self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,'Illegal Character',details)

class InvalidSyntaxError(Error):
    def __init__(self,pos_start,pos_end,details=''):
        super().__init__(pos_start,pos_end,'Invalid Syntax',details)

class RTError(Error):
    def __init__(self,pos_start,pos_end,details,context):
        super().__init__(pos_start,pos_end,'Runtime Error',details)
        self.context = context
    
    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt,self.pos_start,self.pos_end)

        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f' File {pos.fn}, line {str(pos.ln+1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        return 'Traceback (most recent call last):\n' + result


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
    
    def advance(self,cur_char=None):
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
TT_EOF   = 'EOF'

class Token:
    # This start and end pos is of the particular token at hand for pointing error precisely
    def __init__(self,type_,value=None,pos_start=None,pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end

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
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '(':
                tokens.append(Token(TT_LPAR, pos_start=self.pos))
                self.advance()
            elif self.cur_char == ')':
                tokens.append(Token(TT_RPAR, pos_start=self.pos))
                self.advance()
            
            # meaning we input an unrecognized char. Then we print an error
            else:
                pos_start = self.pos.copy()
                char = self.cur_char
                self.advance()
                return [],IllegalCharError(pos_start,self.pos,"'"+char+"'")
                    # Start was pos_start and end was cur pos bcs we advanced in between start and return

        tokens.append(Token(TT_EOF,pos_start=self.pos))
        return tokens,None

    def make_number(self):
        num_str = ''
        dot_count = 0       # to check for int or float
        pos_start = self.pos.copy()

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
            return Token(TT_INT,int(num_str),pos_start,self.pos)
        else:
            return Token(TT_FLOAT, float(num_str),pos_start,self.pos)


##########################
# NODES
##########################

# Tokens for numbers, ie INT and FLOAT
class NumberNode:
    def __init__(self,tok):
        self.tok = tok

        # For interpreter
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'{self.tok}'

# Tokens for binary operators, ie + - / *
class BinOpNode:
    def __init__(self,left_node,op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        # For interpreter
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node},{self.op_tok},{self.right_node})'

class UnaryOpNode:
    def __init__(self,op_tok,node):
        self.op_tok = op_tok
        self.node = node

        # For interpreter
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return f'{self.op_tok,self.node}'

##########################
# PARSE RESULT
##########################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self,res):
        if isinstance(res,ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self,node):
        self.node = node
        return self

    def failure(self,error):
        self.error = error
        return self


##########################
# PARSER
##########################

class Parser:
    # Taking a list of tokens in expression
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_ind = -1
        self.advance()

    def advance(self):
        self.tok_ind += 1
        if self.tok_ind < len(self.tokens):
            self.cur_tok = self.tokens[self.tok_ind]
        return self.cur_tok

    ######################################

    def parse(self):
        res = self.exp()
        # If there is no error but curr token is still not EOF, 
        # means there's code that hasnt been parsed, that leads to syntax error
        if not res.error and self.cur_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.cur_tok.pos_start, self.cur_tok.pos_end,
                "Expected + - / *\n"
            ))
        return res
    
    def factor(self):
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_PLUS,TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok,factor))

        elif tok.type in (TT_INT,TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAR:
            res.register(self.advance())
            exp = res.register(self.exp())
            if res.error: return res
            if self.cur_tok.type == TT_RPAR:
                res.register(self.advance())
                return res.success(exp)
            else:
                return res.failure(InvalidSyntaxError(
                    self.cur_tok.pos_start,self.cur_tok.pos_end,
                    "Expected )\n"
                ))
                

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float\n"
        ))

    def term(self):
        return self.bin_op(self.factor,(TT_MUL,TT_DIV))

    def exp(self):
        return self.bin_op(self.term,(TT_PLUS,TT_MINUS))

    # We define this func for easy use by both exp and term
    # where ops would stand for +- and */ respectively
    def bin_op(self,func,ops):
        res = ParseResult()
        # Register take in the parse result from the func call and return the node from it
        left = res.register(func())
        if res.error: return res

        while self.cur_tok.type in ops:
            op_tok = self.cur_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left,op_tok,right)
        
        return res.success(left)


##########################
# RUNTIME RESULT (for checking div by 0)
##########################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self,res):
        if res.error: self.error = res.error
        return res.value
    
    def success(self,value):
        self.value = value
        return self

    def failure(self,error):
        self.error = error
        return self

##########################
# VALUES
##########################

# for storing nos and operating them with other nos
class Number:
    def __init__(self,value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self,pos_start=None,pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self,context=None):
        self.context = context
        return self

    def added_to(self,other):
        if isinstance(other,Number):
            return Number(self.value + other.value).set_context(self.context),None     # No possible RT Error
    
    def subtracted_by(self,other):
        if isinstance(other,Number):
            return Number(self.value - other.value).set_context(self.context),None     # No possible RT Error
    
    def multiplied_by(self,other):
        if isinstance(other,Number):
            return Number(self.value * other.value).set_context(self.context),None     # No possible RT Error
    
    def divided_by(self,other):
        if isinstance(other,Number):
            if(other.value==0):
                return None,RTError(
                    other.pos_start,other.pos_end,
                    " Division by Zero\n",
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)


##########################
# CONTEXT (for tracing back an error to its core)
##########################

class Context:
    def __init__(self,display_name,parent=None,parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos


##########################
# INTERPRETER
##########################

class Interpreter:
    # Processes a node and visits all its child notes
    def visit(self,node,context):
        # this will automatically create visit_BinOpNode and such sort based on that node
        method_name = f'visit_{type(node).__name__}'

        method = getattr(self,method_name,self.no_visit_method)
        return method(node,context)

    def no_visit_method(self,node,context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ##############################

    def visit_NumberNode(self,node,context):
        # print("Found Number Node")
        # We directly called success as a single number can never give RT
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
        )

    def visit_BinOpNode(self,node,context):
        # print("Found Binary Op Node")

        # If a bin op is found, visit both left and right nodes for computation
        res = RTResult()
        left = res.register(self.visit(node.left_node,context))
        if res.error: return res
        right = res.register(self.visit(node.right_node,context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result,error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result,error = left.subtracted_by(right)
        elif node.op_tok.type == TT_MUL:
            result,error = left.multiplied_by(right)
        elif node.op_tok.type == TT_DIV:
            result,error = left.divided_by(right)
        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start,node.pos_end))

    def visit_UnaryOpNode(self,node,context):
        # print("Found Unary Op Node")
        # If a unary op is found, visit its child node for computation
        res = RTResult()
        number = res.register(self.visit(node.node,context))
        if res.error: return res

        error=None

        if node.op_tok.type == TT_MINUS:
            number,error = number.multiplied_by(Number(-1))
        
        if error:
            return res.failure()
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))


    
##########################
# RUN
##########################

def run(fn, text):
    # Generate Tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST (Abstract Syntax Tree)
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None,ast.error

    # Run Error (if no error obv)
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node,context)

    return result.value,result.error