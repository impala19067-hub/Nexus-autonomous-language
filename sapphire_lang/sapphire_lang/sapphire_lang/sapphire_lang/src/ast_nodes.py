"""
Sapphire Language Abstract Syntax Tree (AST) Nodes
"""

class ASTNode:
    pass

# --- Expressions ---

class NumberLiteralNode(ASTNode):
    def __init__(self, value: float | int):
        self.value = value

class StringLiteralNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

class ProcessCmdNode(ASTNode):
    def __init__(self, command: str):
        self.command = command

class BooleanLiteralNode(ASTNode):
    def __init__(self, value: bool):
        self.value = value

class NullLiteralNode(ASTNode):
    def __init__(self):
        self.value = None

class IdentifierNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

class ArrayLiteralNode(ASTNode):
    def __init__(self, elements: list[ASTNode]):
        self.elements = elements

class MapLiteralNode(ASTNode):
    def __init__(self, pairs: list[tuple[ASTNode, ASTNode]]):
        self.pairs = pairs

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, operator: str, operand: ASTNode):
        self.operator = operator
        self.operand = operand

class CallNode(ASTNode):
    def __init__(self, callee: ASTNode, arguments: list[ASTNode]):
        self.callee = callee
        self.arguments = arguments

class PipeNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

class MemberAccessNode(ASTNode):
    def __init__(self, object_node: ASTNode, member_name: str):
        self.object_node = object_node
        self.member_name = member_name

class IndexAccessNode(ASTNode):
    def __init__(self, object_node: ASTNode, index_node: ASTNode):
        self.object_node = object_node
        self.index_node = index_node

class LambdaNode(ASTNode):
    def __init__(self, params: list[str], body: ASTNode):
        self.params = params
        self.body = body

# --- Statements ---

class ProgramNode(ASTNode):
    def __init__(self, statements: list[ASTNode]):
        self.statements = statements

class VarDeclNode(ASTNode):
    def __init__(self, name: str, initializer: ASTNode, is_const: bool = False, type_annotation: str = None):
        self.name = name
        self.initializer = initializer
        self.is_const = is_const
        self.type_annotation = type_annotation

class AssignmentNode(ASTNode):
    def __init__(self, target: ASTNode, value: ASTNode):
        self.target = target
        self.value = value

class FunctionDefNode(ASTNode):
    def __init__(self, name: str, params: list[str], body: list[ASTNode], return_type: str = None):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: list[ASTNode], else_branch: list[ASTNode] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: list[ASTNode]):
        self.condition = condition
        self.body = body

class ForNode(ASTNode):
    def __init__(self, var_name: str, iterable: ASTNode, body: list[ASTNode]):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

class ParallelBlockNode(ASTNode):
    def __init__(self, statements: list[ASTNode]):
        self.statements = statements

class TryCatchNode(ASTNode):
    def __init__(self, try_body: list[ASTNode], catch_var: str, catch_body: list[ASTNode]):
        self.try_body = try_body
        self.catch_var = catch_var
        self.catch_body = catch_body

class StructDefNode(ASTNode):
    def __init__(self, name: str, fields: list[tuple[str, str]]):
        self.name = name
        self.fields = fields # List of (field_name, field_type)

class ReturnNode(ASTNode):
    def __init__(self, value: ASTNode = None):
        self.value = value

class ExpressionStmtNode(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

class DecoratorNode(ASTNode):
    def __init__(self, name: str, args: list[ASTNode], target: ASTNode):
        self.name = name
        self.args = args
        self.target = target
