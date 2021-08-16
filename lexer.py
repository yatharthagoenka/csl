from string_arrows import *
import string 

##########################
# CONSTANTS
##########################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


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

class ExpectedCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,'Expected Character',details)

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
TT_POW   = 'POW'
TT_LPAR  = 'LPAR'
TT_RPAR  = 'RPAR'
TT_EOF   = 'EOF'

# TT for variables
TT_EQ           = 'EQ'
TT_IDENTIFIER   = 'IDENTIFIER'
TT_KEYWORD      = 'KEYWORD'

# TT for booleans and comparisons
TT_EE = 'EQUAL_EQUAL'
TT_NE = 'NOT_EQUAL'
TT_LT = 'LESS_THAN'
TT_LTE = 'LESS_THAN_EQUAL'
TT_GT = 'GREATER_THAN'
TT_GTE = 'GREATER_THAN_EQUAL'

KEYWORDS = [
    'let',
    'and', 
    'or',
    'not'
]

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

    def matches(self,type_,value):
        return self.type == type_ and self.value == value

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
            elif self.cur_char in LETTERS:
                tokens.append(self.make_identifier())
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
            elif self.cur_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '(':
                tokens.append(Token(TT_LPAR, pos_start=self.pos))
                self.advance()
            elif self.cur_char == ')':
                tokens.append(Token(TT_RPAR, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '=':
                tokens.append(self.make_equals())
            elif self.cur_char == '<':
                tokens.append(self.make_less_than())
            elif self.cur_char == '>':
                tokens.append(self.make_greater_than())
            elif self.cur_char == '!':
                token, error = self.make_not_equals()
                if error: return[], error
                tokens.append(token)

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

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.cur_char != None and self.cur_char in LETTERS_DIGITS + '_':
            id_str += self.cur_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type,id_str,pos_start,self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.cur_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None
        else:
            self.advance()
            return None, ExpectedCharError(pos_start, self.pos, "'=' after '!'")

    def make_equals(self):
        tok_type  = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.cur_char == '=':
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start,pos_end=self.pos)

    def make_less_than(self):
        tok_type  = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.cur_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start,pos_end=self.pos)

    def make_greater_than(self):
        tok_type  = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.cur_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start,pos_end=self.pos)

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


class VarAccessNode:
    def __init__(self,var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    # value_node will be the value of the variable
    def __init__(self,var_name_tok,value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


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
        self.adv_count = 0      # How many times have we advanced in this parse result for expr

    def register_adv(self):
        self.adv_count += 1

    def register(self,res):
        self.adv_count += res.adv_count
        if res.error: self.error = res.error
        return res.node
        
    def success(self,node):
        self.node = node
        return self

    def failure(self,error):
        if not self.error or self.adv_count == 0:
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

    def atom(self):
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_INT,TT_FLOAT):
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_adv()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAR:
            res.register_adv()
            self.advance()
            exp = res.register(self.exp())
            if res.error: return res
            if self.cur_tok.type == TT_RPAR:
                res.register_adv()
                self.advance()
                return res.success(exp)
            else:
                return res.failure(InvalidSyntaxError(
                    self.cur_tok.pos_start,self.cur_tok.pos_end,
                    "Expected )\n"
                ))
                

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected INT, FLOAT, IDENTIFIER, '+', '-' or '('\n"
        ))
        # Here we returned error of +- too bcs there is no error handling for factor itself
        # it is only calling power, who is calling atom. Therefore, atom must reflect error of factor as well

    def power(self):
        return self.bin_op(self.atom,(TT_POW, ), self.factor)
    
    def factor(self):
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_PLUS,TT_MINUS):
            res.register_adv()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok,factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor,(TT_MUL,TT_DIV))

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.cur_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.cur_tok
            res.register_adv()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(EnvalidSyntaxError(
                self.cur_tok.pos_start ,self.cur_tok.pos_end,
                "Exprected int, float, identifier, '+', '-', '(' or 'not'"
            ))

        return res.success(node)

    def exp(self):
        res = ParseResult()

        if self.cur_tok.matches(TT_KEYWORD,'let'):
            res.register_adv()
            self.advance()

            if self.cur_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.cur_tok.pos_start, self.cur_tok.pos_end,
                    "Expected Identifier\n"
                ))
            
            var_name = self.cur_tok
            res.register_adv()
            self.advance()

            if self.cur_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.cur_tok.pos_start, self.cur_tok.pos_end,
                    "Expected '='\n"
                ))
            
            res.register_adv()
            self.advance()
            exp = res.register(self.exp())
            if res.error: return res
            return res.success(VarAssignNode(var_name,exp))

        node = res.register(self.bin_op(self.comp_expr,((TT_KEYWORD, "and"), (TT_KEYWORD, "or"))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.cur_tok.pos_start,self.cur_tok.pos_end,
                "Expected 'let',INT, FLOAT, IDENTIFIER, '+', '-' or '('\n"
            ))
        return res.success(node)

    # We define this func for easy use by both exp and term
    # where ops would stand for +- and */ respectively
    def bin_op(self,func_a,ops,func_b=None):
        if func_b==None:
            func_b = func_a

        res = ParseResult()
        # Register take in the parse result from the func call and return the node from it
        left = res.register(func_a())
        if res.error: return res

        while self.cur_tok.type in ops or (self.cur_tok.type, self.cur_tok.value) in ops:
            op_tok = self.cur_tok
            res.register_adv()
            self.advance()
            right = res.register(func_b())
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

    def pow_by(self,other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
    
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
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
        self.symbol_table = None

##########################
# SYMBOL TABLE : Keeps track of all var names and their values
##########################

# For every function, there would be a new symbol table to store its variables
# and once the func has run, this table could be discarded

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None      # Global variables

    # For getting var value
    def get(self, name):
        value = self.symbols.get(name, None)    # Get a value, if cant get, then default it to None
        # If None, check parent table for occurence, otherwise return as it is
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    # For setting var value
    def set(self,name,value):
        self.symbols[name] = value

    def remove(self,name):
        del self.symbols[name]


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

    def visit_VarAccessNode(self,node,context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        # Case where var isnt defined
        if not value:
            return res.failure(RTError(
                node.pos_start,node.pos_end,
                f"'{var_name}' is not defined\n",
                context
            ))

        # Value is copied and the position is now set to where the 
        # variable was accessed, not where it was assigned
        value = value.copy().set_pos(node.pos_start,node.pos_end)
        return res.success(value)


    def visit_VarAssignNode(self,node,context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node,context))

        if res.error: return res

        context.symbol_table.set(var_name,value)
        return res.success(value)


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
        elif node.op_tok.type == TT_POW:
            result,error = left.pow_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

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
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()
        
        if error:
            return res.failure()
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))


    
##########################
# RUN
##########################

global_symbol_table = SymbolTable()
global_symbol_table.set("null",Number(0))
global_symbol_table.set("true",Number(1))
global_symbol_table.set("false",Number(0))

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
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node,context)

    return result.value,result.error
