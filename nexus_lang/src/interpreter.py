"""
Nexus Language Interpreter / Runtime Evaluator
"""
import concurrent.futures
from src.ast_nodes import (
    ProgramNode, VarDeclNode, AssignmentNode, FunctionDefNode, IfNode,
    WhileNode, ForNode, ParallelBlockNode, TryCatchNode, StructDefNode,
    ReturnNode, ExpressionStmtNode, DecoratorNode, NumberLiteralNode,
    StringLiteralNode, ProcessCmdNode, BooleanLiteralNode, NullLiteralNode,
    IdentifierNode, ArrayLiteralNode, MapLiteralNode, BinaryOpNode,
    UnaryOpNode, CallNode, PipeNode, MemberAccessNode, IndexAccessNode,
    LambdaNode
)
from src.environment import Environment, EnvironmentError
from src.stdlib import STDLIB

class ReturnException(Exception):
    def __init__(self, value: any):
        self.value = value

class RuntimeError(Exception):
    def __init__(self, message: str):
        super().__init__(f"RuntimeError: {message}")

class NexusFunction:
    def __init__(self, decl: FunctionDefNode, closure: Environment):
        self.decl = decl
        self.closure = closure

    def call(self, interpreter: 'Interpreter', args: list) -> any:
        env = Environment(self.closure)
        for i, param in enumerate(self.decl.params):
            arg_val = args[i] if i < len(args) else None
            env.define(param, arg_val)

        try:
            for stmt in self.decl.body:
                interpreter.evaluate_statement(stmt, env)
        except ReturnException as ret:
            return ret.value
        return None

class NativeFunction:
    def __init__(self, py_func):
        self.py_func = py_func

    def call(self, interpreter: 'Interpreter', args: list) -> any:
        return self.py_func(*args)

class ProcessResult(str):
    """Wrapper class for process command output that behaves as string with extra methods."""
    def __new__(cls, stdout: str, exit_code: int = 0, stderr: str = ""):
        obj = super().__new__(cls, stdout)
        obj.exit_code = exit_code
        obj.stderr = stderr
        obj.success = (exit_code == 0)
        return obj

    def lines(self) -> list[str]:
        return [l for l in self.splitlines() if l.strip()]

    def is_empty(self) -> bool:
        return len(self.strip()) == 0

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self._setup_globals()

    def _setup_globals(self):
        # Register Built-in Stdlib Modules
        for name, module_cls in STDLIB.items():
            self.global_env.define(name, module_cls)

        # Register Built-in Global Functions
        self.global_env.define("print", NativeFunction(lambda *args: print(*[self._stringify(a) for a in args])))
        self.global_env.define("len", NativeFunction(lambda val: len(val) if hasattr(val, '__len__') else 0))
        self.global_env.define("range", NativeFunction(lambda *args: list(range(*args))))
        self.global_env.define("type", NativeFunction(lambda val: type(val).__name__))

    def interpret(self, program: ProgramNode, env: Environment = None) -> any:
        if env is None:
            env = self.global_env

        last_val = None
        for stmt in program.statements:
            last_val = self.evaluate_statement(stmt, env)
        return last_val

    def execute(self, program: ProgramNode, env: Environment = None) -> any:
        return self.interpret(program, env)

    def evaluate_statement(self, stmt: any, env: Environment) -> any:
        if isinstance(stmt, VarDeclNode):
            val = self.evaluate(stmt.initializer, env) if stmt.initializer else None
            env.define(stmt.name, val, is_const=stmt.is_const)
            return val

        elif isinstance(stmt, FunctionDefNode):
            fn = NexusFunction(stmt, env)
            env.define(stmt.name, fn)
            return fn

        elif isinstance(stmt, ExpressionStmtNode):
            return self.evaluate(stmt.expression, env)

        elif isinstance(stmt, IfNode):
            cond = self.evaluate(stmt.condition, env)
            if self._is_truthy(cond):
                for s in stmt.then_branch:
                    self.evaluate_statement(s, env)
            elif stmt.else_branch:
                for s in stmt.else_branch:
                    self.evaluate_statement(s, env)
            return None

        elif isinstance(stmt, WhileNode):
            while self._is_truthy(self.evaluate(stmt.condition, env)):
                for s in stmt.body:
                    self.evaluate_statement(s, env)
            return None

        elif isinstance(stmt, ForNode):
            iterable = self.evaluate(stmt.iterable, env)
            if not hasattr(iterable, '__iter__'):
                raise RuntimeError(f"Type '{type(iterable).__name__}' is not iterable")

            for item in iterable:
                loop_env = Environment(env)
                loop_env.define(stmt.var_name, item)
                for s in stmt.body:
                    self.evaluate_statement(s, loop_env)
            return None

        elif isinstance(stmt, ParallelBlockNode):
            # Concurrent execution of statements using ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for s in stmt.statements:
                    futures.append(executor.submit(self.evaluate_statement, s, Environment(env)))
                concurrent.futures.wait(futures)
            return None

        elif isinstance(stmt, TryCatchNode):
            try:
                for s in stmt.try_body:
                    self.evaluate_statement(s, env)
            except Exception as e:
                catch_env = Environment(env)
                catch_env.define(stmt.catch_var, str(e))
                for s in stmt.catch_body:
                    self.evaluate_statement(s, catch_env)
            return None

        elif isinstance(stmt, ReturnNode):
            val = self.evaluate(stmt.value, env) if stmt.value else None
            raise ReturnException(val)

        elif isinstance(stmt, StructDefNode):
            env.define(stmt.name, stmt)
            return stmt

        elif isinstance(stmt, DecoratorNode):
            # Evaluate target
            return self.evaluate_statement(stmt.target, env)

        return self.evaluate(stmt, env)

    def evaluate(self, expr: any, env: Environment) -> any:
        if isinstance(expr, NumberLiteralNode):
            return expr.value

        elif isinstance(expr, StringLiteralNode):
            # Handle String Interpolation: "Hello {expr}"
            val = expr.value
            if "{" in val and "}" in val:
                import re
                from src.lexer import Lexer
                from src.parser import Parser
                def _replace(match):
                    inner_code = match.group(1).strip()
                    try:
                        sub_lexer = Lexer(inner_code)
                        sub_parser = Parser(sub_lexer.tokenize())
                        ast_expr = sub_parser.expression()
                        res = self.evaluate(ast_expr, env)
                        return self._stringify(res)
                    except Exception:
                        return match.group(0)
                val = re.sub(r'\{([^}]+)\}', _replace, val)
            return val

        elif isinstance(expr, ProcessCmdNode):
            # Execute OS command natively
            res = STDLIB["os"].exec(expr.command)
            return ProcessResult(res["stdout"], res["exit_code"], res["stderr"])

        elif isinstance(expr, BooleanLiteralNode):
            return expr.value

        elif isinstance(expr, NullLiteralNode):
            return None

        elif isinstance(expr, IdentifierNode):
            return env.get(expr.name)

        elif isinstance(expr, ArrayLiteralNode):
            return [self.evaluate(elem, env) for elem in expr.elements]

        elif isinstance(expr, MapLiteralNode):
            res = {}
            for k_node, v_node in expr.pairs:
                k = self.evaluate(k_node, env)
                v = self.evaluate(v_node, env)
                res[str(k)] = v
            return res

        elif isinstance(expr, BinaryOpNode):
            left = self.evaluate(expr.left, env)
            right = self.evaluate(expr.right, env)
            op = expr.operator

            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return self._stringify(left) + self._stringify(right)
                return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right if right != 0 else 0
            elif op == '%': return left % right
            elif op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '>': return left > right
            elif op == '<=': return left <= right
            elif op == '>=': return left >= right
            elif op in ('&&', 'and'): return self._is_truthy(left) and self._is_truthy(right)
            elif op in ('||', 'or'): return self._is_truthy(left) or self._is_truthy(right)

        elif isinstance(expr, UnaryOpNode):
            val = self.evaluate(expr.operand, env)
            if expr.operator in ('!', 'not'):
                return not self._is_truthy(val)
            elif expr.operator == '-':
                return -val

        elif isinstance(expr, PipeNode):
            # Piping: left |> right
            left_val = self.evaluate(expr.left, env)

            # If right is a CallNode (e.g. |> lines() or |> filter(fn))
            if isinstance(expr.right, CallNode):
                if isinstance(expr.right.callee, IdentifierNode):
                    method_name = expr.right.callee.name
                    # Check if method exists on left_val or via MemberAccessNode logic
                    try:
                        mem_node = MemberAccessNode(expr.left, method_name)
                        method_fn = self.evaluate(mem_node, env)
                        call_args = [self.evaluate(arg, env) for arg in expr.right.arguments]
                        return self._invoke_callable(method_fn, call_args, env)
                    except Exception:
                        pass
                
                args = [left_val] + [self.evaluate(arg, env) for arg in expr.right.arguments]
                callee = self.evaluate(expr.right.callee, env)
                return self._invoke_callable(callee, args, env)

            elif isinstance(expr.right, IdentifierNode):
                method_name = expr.right.name
                try:
                    mem_node = MemberAccessNode(expr.left, method_name)
                    method_fn = self.evaluate(mem_node, env)
                    return self._invoke_callable(method_fn, [], env)
                except Exception:
                    pass
                callee = env.get(expr.right.name)
                return self._invoke_callable(callee, [left_val], env)

            elif isinstance(expr.right, LambdaNode):
                return self._invoke_lambda(expr.right, [left_val], env)
            else:
                right_val = self.evaluate(expr.right, env)
                if callable(right_val) or hasattr(right_val, 'call'):
                    return self._invoke_callable(right_val, [left_val], env)
                return right_val

        elif isinstance(expr, CallNode):
            callee = self.evaluate(expr.callee, env)
            args = [self.evaluate(arg, env) for arg in expr.arguments]
            return self._invoke_callable(callee, args, env)

        elif isinstance(expr, MemberAccessNode):
            obj = self.evaluate(expr.object_node, env)
            member = expr.member_name

            # Method access on objects/modules/strings/lists/maps
            if hasattr(obj, member):
                attr = getattr(obj, member)
                if callable(attr):
                    return NativeFunction(attr)
                return attr

            if isinstance(obj, dict):
                if member in obj:
                    return obj[member]
                elif member == "keys":
                    return NativeFunction(lambda: list(obj.keys()))
                elif member == "values":
                    return NativeFunction(lambda: list(obj.values()))

            if isinstance(obj, list):
                if member == "length" or member == "len":
                    return len(obj)
                elif member == "push":
                    return NativeFunction(lambda val: obj.append(val))
                elif member == "pop":
                    return NativeFunction(lambda: obj.pop() if obj else None)
                elif member == "join":
                    return NativeFunction(lambda sep="": sep.join([str(x) for x in obj]))
                elif member == "filter":
                    return NativeFunction(lambda fn: [x for x in obj if self._invoke_callable(fn, [x], env)])
                elif member == "map":
                    return NativeFunction(lambda fn: [self._invoke_callable(fn, [x], env) for x in obj])
                elif member == "is_empty":
                    return len(obj) == 0

            if isinstance(obj, str):
                if member == "lines":
                    return NativeFunction(lambda: [l for l in obj.splitlines() if l.strip()])
                elif member == "contains":
                    return NativeFunction(lambda sub: sub in obj)
                elif member == "to_upper":
                    return NativeFunction(lambda: obj.upper())
                elif member == "to_lower":
                    return NativeFunction(lambda: obj.lower())
                elif member == "trim":
                    return NativeFunction(lambda: obj.strip())
                elif member == "is_empty":
                    return len(obj.strip()) == 0

            raise RuntimeError(f"Property or method '{member}' not found on target {type(obj).__name__}")

        elif isinstance(expr, IndexAccessNode):
            obj = self.evaluate(expr.object_node, env)
            idx = self.evaluate(expr.index_node, env)
            try:
                return obj[idx]
            except Exception as e:
                raise RuntimeError(f"Index error accessing '{idx}': {e}")

        elif isinstance(expr, AssignmentNode):
            val = self.evaluate(expr.value, env)
            if isinstance(expr.target, IdentifierNode):
                env.assign(expr.target.name, val)
            elif isinstance(expr.target, IndexAccessNode):
                obj = self.evaluate(expr.target.object_node, env)
                idx = self.evaluate(expr.target.index_node, env)
                obj[idx] = val
            elif isinstance(expr.target, MemberAccessNode):
                obj = self.evaluate(expr.target.object_node, env)
                setattr(obj, expr.target.member_name, val)
            return val

        elif isinstance(expr, LambdaNode):
            return expr

        raise RuntimeError(f"Unknown AST node type: {type(expr).__name__}")

    def _invoke_callable(self, callee: any, args: list, env: Environment) -> any:
        if isinstance(callee, NexusFunction):
            return callee.call(self, args)
        elif isinstance(callee, NativeFunction):
            return callee.call(self, args)
        elif isinstance(callee, LambdaNode):
            return self._invoke_lambda(callee, args, env)
        elif callable(callee):
            return callee(*args)
        elif hasattr(callee, '__call__'):
            return callee(*args)
        raise RuntimeError(f"Target '{callee}' is not callable")

    def _invoke_lambda(self, lambda_node: LambdaNode, args: list, env: Environment) -> any:
        l_env = Environment(env)
        for i, param in enumerate(lambda_node.params):
            arg_val = args[i] if i < len(args) else None
            l_env.define(param, arg_val)
        return self.evaluate(lambda_node.body, l_env)

    def _is_truthy(self, val: any) -> bool:
        if val is None or val is False:
            return False
        if isinstance(val, (int, float)) and val == 0:
            return False
        if isinstance(val, (str, list, dict)) and len(val) == 0:
            return False
        return True

    def _stringify(self, val: any) -> str:
        if val is None: return "null"
        if val is True: return "true"
        if val is False: return "false"
        if isinstance(val, dict):
            import json
            return json.dumps(val, default=str)
        return str(val)
