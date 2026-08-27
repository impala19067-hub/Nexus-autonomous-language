"""
Sapphire Language Environment & Scope Manager
"""

class EnvironmentError(Exception):
    pass

class Environment:
    def __init__(self, enclosing: 'Environment' = None):
        self.enclosing = enclosing
        self.values = {}
        self.constants = set()

    def define(self, name: str, value: any, is_const: bool = False):
        if name in self.values and name in self.constants:
            raise EnvironmentError(f"Cannot reassign constant variable '{name}'")
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def get(self, name: str) -> any:
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise EnvironmentError(f"Undefined variable '{name}'")

    def assign(self, name: str, value: any):
        if name in self.values:
            if name in self.constants:
                raise EnvironmentError(f"Cannot mutate constant variable '{name}'")
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise EnvironmentError(f"Undefined variable '{name}'")
