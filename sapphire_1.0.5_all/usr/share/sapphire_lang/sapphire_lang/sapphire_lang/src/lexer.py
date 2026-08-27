"""
Sapphire Language Lexer / Scanner
"""
from src.tokens import Token, TokenType, KEYWORDS

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at Line {line}, Column {column}: {message}")
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source: str):
        self.source = source[1:] if source.startswith("\ufeff") else source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            ch = self.advance()
            self.scan_token(ch)

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        self.column += 1
        return ch

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def scan_token(self, ch: str):
        if ch in (' ', '\r', '\t'):
            return
        elif ch == '\n':
            self.line += 1
            self.column = 1
            return
        elif ch == '/':
            if self.match('/'):
                # Line comment
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            elif self.match('*'):
                # Block comment
                while not self.is_at_end():
                    if self.peek() == '*' and self.peek_next() == '/':
                        self.advance()
                        self.advance()
                        break
                    if self.peek() == '\n':
                        self.line += 1
                        self.column = 1
                    self.advance()
            else:
                self.add_token(TokenType.SLASH, "/")
        elif ch == '+':
            self.add_token(TokenType.PLUS, "+")
        elif ch == '-':
            if self.match('>'):
                self.add_token(TokenType.ARROW, "->")
            else:
                self.add_token(TokenType.MINUS, "-")
        elif ch == '*':
            self.add_token(TokenType.STAR, "*")
        elif ch == '%':
            self.add_token(TokenType.PERCENT, "%")
        elif ch == '|':
            if self.match('>'):
                self.add_token(TokenType.PIPE, "|>")
            elif self.match('|'):
                self.add_token(TokenType.OR, "||")
            else:
                self.add_token(TokenType.PIPE, "|")
        elif ch == '&':
            if self.match('&'):
                self.add_token(TokenType.AND, "&&")
            else:
                raise LexerError("Unexpected character '&'", self.line, self.column)
        elif ch == '=':
            if self.match('='):
                self.add_token(TokenType.EQ, "==")
            else:
                self.add_token(TokenType.ASSIGN, "=")
        elif ch == '!':
            if self.match('='):
                self.add_token(TokenType.NEQ, "!=")
            else:
                self.add_token(TokenType.NOT, "!")
        elif ch == '<':
            if self.match('='):
                self.add_token(TokenType.LTE, "<=")
            else:
                self.add_token(TokenType.LT, "<")
        elif ch == '>':
            if self.match('='):
                self.add_token(TokenType.GTE, ">=")
            else:
                self.add_token(TokenType.GT, ">")
        elif ch == '(':
            self.add_token(TokenType.LPAREN, "(")
        elif ch == ')':
            self.add_token(TokenType.RPAREN, ")")
        elif ch == '{':
            self.add_token(TokenType.LBRACE, "{")
        elif ch == '}':
            self.add_token(TokenType.RBRACE, "}")
        elif ch == '[':
            self.add_token(TokenType.LBRACKET, "[")
        elif ch == ']':
            self.add_token(TokenType.RBRACKET, "]")
        elif ch == ',':
            self.add_token(TokenType.COMMA, ",")
        elif ch == '.':
            self.add_token(TokenType.DOT, ".")
        elif ch == ':':
            self.add_token(TokenType.COLON, ":")
        elif ch == ';':
            self.add_token(TokenType.SEMICOLON, ";")
        elif ch == '@':
            self.add_token(TokenType.AT, "@")
        elif ch == '"':
            self.scan_string()
        elif ch == '`':
            self.scan_backtick_process()
        elif ch == '$':
            self.scan_dollar_process()
        elif ch.isdigit():
            self.scan_number()
        elif ch.isalpha() or ch == '_':
            self.scan_identifier()
        else:
            raise LexerError(f"Unexpected character '{ch}'", self.line, self.column)

    def add_token(self, type_: TokenType, value: any):
        self.tokens.append(Token(type_, value, self.line, self.column))

    def scan_string(self):
        # Check for triple quote """
        if self.peek() == '"' and self.peek_next() == '"':
            self.advance()
            self.advance()
            # Multiline triple-quoted string
            val_chars = []
            while not self.is_at_end():
                if self.peek() == '"' and self.peek_next() == '"':
                    # Check third quote
                    if self.current + 2 < len(self.source) and self.source[self.current + 2] == '"':
                        self.advance()
                        self.advance()
                        self.advance()
                        break
                ch = self.advance()
                if ch == '\n':
                    self.line += 1
                    self.column = 1
                val_chars.append(ch)
            self.add_token(TokenType.STRING, "".join(val_chars))
            return

        # Normal single line or escaped string
        val_chars = []
        while self.peek() != '"' and not self.is_at_end():
            ch = self.advance()
            if ch == '\\':
                escaped = self.advance()
                if escaped == 'n': val_chars.append('\n')
                elif escaped == 't': val_chars.append('\t')
                elif escaped == 'r': val_chars.append('\r')
                elif escaped == '"': val_chars.append('"')
                elif escaped == '\\': val_chars.append('\\')
                else: val_chars.append(escaped)
            else:
                if ch == '\n':
                    self.line += 1
                    self.column = 1
                val_chars.append(ch)

        if self.is_at_end():
            raise LexerError("Unterminated string literal", self.line, self.column)
        self.advance() # consume closing '"'
        self.add_token(TokenType.STRING, "".join(val_chars))

    def scan_backtick_process(self):
        # Process literal: `command arg1 arg2`
        val_chars = []
        while self.peek() != '`' and not self.is_at_end():
            ch = self.advance()
            if ch == '\n':
                self.line += 1
                self.column = 1
            val_chars.append(ch)
        if self.is_at_end():
            raise LexerError("Unterminated process literal", self.line, self.column)
        self.advance() # consume closing '`'
        self.add_token(TokenType.PROCESS_CMD, "".join(val_chars).strip())

    def scan_dollar_process(self):
        # Process literal starting with $, e.g., $ ls -la or $ git status
        # Reads until end of line or pipe '|>' or semicolon ';'
        val_chars = []
        while not self.is_at_end() and self.peek() not in ('\n', ';', '\r'):
            if self.peek() == '|' and self.peek_next() == '>':
                break
            val_chars.append(self.advance())
        cmd_str = "".join(val_chars).strip()
        self.add_token(TokenType.PROCESS_CMD, cmd_str)

    def scan_number(self):
        is_float = False
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            is_float = True
            self.advance() # consume '.'
            while self.peek().isdigit():
                self.advance()
        num_str = self.source[self.start:self.current]
        value = float(num_str) if is_float else int(num_str)
        self.add_token(TokenType.NUMBER, value)

    def scan_identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        if token_type == TokenType.BOOLEAN:
            value = True if text == "true" else False
        elif token_type == TokenType.NULL:
            value = None
        else:
            value = text
        self.add_token(token_type, value)
