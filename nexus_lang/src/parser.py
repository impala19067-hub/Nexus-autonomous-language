"""
Nexus Language Recursive Descent / Pratt Parser
"""
from src.tokens import Token, TokenType
from src.ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignmentNode, FunctionDefNode, IfNode,
    WhileNode, ForNode, ParallelBlockNode, TryCatchNode, StructDefNode,
    ReturnNode, ExpressionStmtNode, DecoratorNode, NumberLiteralNode,
    StringLiteralNode, ProcessCmdNode, BooleanLiteralNode, NullLiteralNode,
    IdentifierNode, ArrayLiteralNode, MapLiteralNode, BinaryOpNode,
    UnaryOpNode, CallNode, PipeNode, MemberAccessNode, IndexAccessNode,
    LambdaNode
)

class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"ParserError at Line {token.line}, Column {token.column} near '{token.value}': {message}")
        self.token = token

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> ProgramNode:
        statements = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type_: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, type_: TokenType, message: str) -> Token:
        if self.check(type_):
            return self.advance()
        raise ParserError(message, self.peek())

    # --- Declarations & Statements ---

    def declaration(self):
        try:
            if self.match(TokenType.AT):
                return self.decorator_declaration()
            if self.match(TokenType.LET):
                return self.var_declaration(is_const=False)
            if self.match(TokenType.CONST):
                return self.var_declaration(is_const=True)
            if self.match(TokenType.FN):
                return self.function_declaration()
            if self.match(TokenType.STRUCT):
                return self.struct_declaration()
            return self.statement()
        except ParserError as err:
            self.synchronize()
            raise err

    def decorator_declaration(self):
        name_token = self.consume(TokenType.IDENTIFIER, "Expected decorator name after '@'")
        args = []
        if self.match(TokenType.LPAREN):
            if not self.check(TokenType.RPAREN):
                while True:
                    args.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RPAREN, "Expected ')' after decorator arguments")
        target = self.declaration()
        return DecoratorNode(name_token.value, args, target)

    def var_declaration(self, is_const: bool):
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        type_ann = None
        if self.match(TokenType.COLON):
            type_token = self.consume(TokenType.IDENTIFIER, "Expected type annotation after ':'")
            type_ann = type_token.value

        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()

        self.match(TokenType.SEMICOLON)
        return VarDeclNode(name_token.value, initializer, is_const=is_const, type_annotation=type_ann)

    def function_declaration(self):
        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        params = []
        if not self.check(TokenType.RPAREN):
            while True:
                p_name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
                if self.match(TokenType.COLON):
                    self.consume(TokenType.IDENTIFIER, "Expected type after ':'")
                params.append(p_name)
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")

        return_type = None
        if self.match(TokenType.ARROW):
            return_type = self.consume(TokenType.IDENTIFIER, "Expected return type after '->'").value

        body = self.block_statement()
        return FunctionDefNode(name_token.value, params, body, return_type)

    def struct_declaration(self):
        name_token = self.consume(TokenType.IDENTIFIER, "Expected struct name")
        self.consume(TokenType.LBRACE, "Expected '{' before struct body")
        fields = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            f_name = self.consume(TokenType.IDENTIFIER, "Expected field name").value
            self.consume(TokenType.COLON, "Expected ':' after field name")
            f_type = self.consume(TokenType.IDENTIFIER, "Expected field type").value
            fields.append((f_name, f_type))
            self.match(TokenType.COMMA)
            self.match(TokenType.SEMICOLON)
        self.consume(TokenType.RBRACE, "Expected '}' after struct fields")
        return StructDefNode(name_token.value, fields)

    def statement(self):
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.PARALLEL):
            return self.parallel_statement()
        if self.match(TokenType.TRY):
            return self.try_catch_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.check(TokenType.LBRACE):
            return ExpressionStmtNode(self.block_statement())

        expr = self.expression()
        self.match(TokenType.SEMICOLON)
        return ExpressionStmtNode(expr)

    def block_statement(self) -> list:
        self.consume(TokenType.LBRACE, "Expected '{' before block")
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        return statements

    def if_statement(self):
        condition = self.expression()
        then_branch = self.block_statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            if self.check(TokenType.IF):
                self.advance()
                else_branch = [self.if_statement()]
            else:
                else_branch = self.block_statement()
        return IfNode(condition, then_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        body = self.block_statement()
        return WhileNode(condition, body)

    def for_statement(self):
        var_name = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'for'").value
        self.consume(TokenType.IN, "Expected 'in' after variable name")
        iterable = self.expression()
        body = self.block_statement()
        return ForNode(var_name, iterable, body)

    def parallel_statement(self):
        body = self.block_statement()
        return ParallelBlockNode(body)

    def try_catch_statement(self):
        try_body = self.block_statement()
        self.consume(TokenType.CATCH, "Expected 'catch' after try block")
        catch_var = "err"
        if self.match(TokenType.LPAREN):
            catch_var = self.consume(TokenType.IDENTIFIER, "Expected catch variable name").value
            self.consume(TokenType.RPAREN, "Expected ')' after catch variable")
        catch_body = self.block_statement()
        return TryCatchNode(try_body, catch_var, catch_body)

    def return_statement(self):
        expr = None
        if not self.check(TokenType.SEMICOLON) and not self.check(TokenType.RBRACE):
            expr = self.expression()
        self.match(TokenType.SEMICOLON)
        return ReturnNode(expr)

    # --- Expressions ---

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.pipe()

        if self.match(TokenType.ASSIGN):
            value = self.assignment()
            if isinstance(expr, (IdentifierNode, MemberAccessNode, IndexAccessNode)):
                return AssignmentNode(expr, value)
            raise ParserError("Invalid assignment target", self.previous())

        return expr

    def pipe(self):
        expr = self.logical_or()

        while self.match(TokenType.PIPE):
            right = self.logical_or()
            expr = PipeNode(expr, right)

        return expr

    def logical_or(self):
        expr = self.logical_and()

        while self.match(TokenType.OR):
            operator = self.previous().value
            right = self.logical_and()
            expr = BinaryOpNode(expr, operator, right)

        return expr

    def logical_and(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous().value
            right = self.equality()
            expr = BinaryOpNode(expr, operator, right)

        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.EQ, TokenType.NEQ):
            operator = self.previous().value
            right = self.comparison()
            expr = BinaryOpNode(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            operator = self.previous().value
            right = self.term()
            expr = BinaryOpNode(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().value
            right = self.factor()
            expr = BinaryOpNode(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.previous().value
            right = self.unary()
            expr = BinaryOpNode(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous().value
            right = self.unary()
            return UnaryOpNode(operator, right)

        return self.call_or_access()

    def call_or_access(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                member_name = self.consume(TokenType.IDENTIFIER, "Expected property name after '.'").value
                expr = MemberAccessNode(expr, member_name)
            elif self.match(TokenType.LBRACKET):
                index_expr = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexAccessNode(expr, index_expr)
            elif self.match(TokenType.ARROW):
                # Lambda shorthand: param -> body
                if isinstance(expr, IdentifierNode):
                    body = self.expression()
                    expr = LambdaNode([expr.name], body)
                else:
                    break
            else:
                break

        return expr

    def finish_call(self, callee: ASTNode) -> CallNode:
        arguments = []
        if not self.check(TokenType.RPAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        return CallNode(callee, arguments)

    def primary(self):
        if self.match(TokenType.BOOLEAN):
            return BooleanLiteralNode(self.previous().value)
        if self.match(TokenType.NULL):
            return NullLiteralNode()
        if self.match(TokenType.NUMBER):
            return NumberLiteralNode(self.previous().value)
        if self.match(TokenType.STRING):
            return StringLiteralNode(self.previous().value)
        if self.match(TokenType.PROCESS_CMD):
            return ProcessCmdNode(self.previous().value)

        if self.match(TokenType.IDENTIFIER):
            # Check for multi-param lambda: (x, y) => body or param => body
            id_name = self.previous().value
            return IdentifierNode(id_name)

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        if self.match(TokenType.LBRACKET):
            # Array literal
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACKET, "Expected ']' after array elements")
            return ArrayLiteralNode(elements)

        if self.match(TokenType.LBRACE):
            # Map literal {"key": val}
            pairs = []
            if not self.check(TokenType.RBRACE):
                while True:
                    key = self.expression()
                    self.consume(TokenType.COLON, "Expected ':' after map key")
                    val = self.expression()
                    pairs.append((key, val))
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACE, "Expected '}' after map pairs")
            return MapLiteralNode(pairs)

        raise ParserError(f"Unexpected token '{self.peek().value}'", self.peek())

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in (TokenType.FN, TokenType.LET, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.RETURN):
                return
            self.advance()
