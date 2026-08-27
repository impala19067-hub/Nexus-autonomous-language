"""
Sapphire Language Token Definitions
"""
from enum import Enum, auto

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    PROCESS_CMD = auto()   # e.g., $ ls -la or `git status`
    BOOLEAN = auto()
    NULL = auto()
    IDENTIFIER = auto()

    # Keywords
    FN = auto()
    LET = auto()
    CONST = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    IMPORT = auto()
    PARALLEL = auto()
    TRY = auto()
    CATCH = auto()
    STRUCT = auto()
    BREAK = auto()
    CONTINUE = auto()

    # Operators & Delimiters
    PLUS = auto()           # +
    MINUS = auto()          # -
    STAR = auto()           # *
    SLASH = auto()          # /
    PERCENT = auto()        # %
    PIPE = auto()           # |>
    ASSIGN = auto()         # =
    EQ = auto()             # ==
    NEQ = auto()            # !=
    LT = auto()             # <
    GT = auto()             # >
    LTE = auto()            # <=
    GTE = auto()            # >=
    AND = auto()            # && or and
    OR = auto()             # || or or
    NOT = auto()            # ! or not
    
    DOT = auto()            # .
    COMMA = auto()          # ,
    COLON = auto()          # :
    SEMICOLON = auto()      # ;
    AT = auto()             # @ (Decorators/Annotations)
    ARROW = auto()          # ->

    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]

    EOF = auto()

KEYWORDS = {
    "fn": TokenType.FN,
    "let": TokenType.LET,
    "const": TokenType.CONST,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "return": TokenType.RETURN,
    "import": TokenType.IMPORT,
    "parallel": TokenType.PARALLEL,
    "try": TokenType.TRY,
    "catch": TokenType.CATCH,
    "struct": TokenType.STRUCT,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
    "null": TokenType.NULL,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}

class Token:
    def __init__(self, type_: TokenType, value: any, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.column})"
