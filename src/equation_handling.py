from enum import Enum # Remote Änderung by other Dev
from typing import Dict

class VarType(Enum):
    CONTINUOUS = "continuous"
    BINARY = "binary"
    INTEGER = "integer"

class Var:
    decision_variables: Dict[str, float] = {}

    def __init__(self,
                 name: str,
                 lower_bound: float=0.0,
                 upper_bound: float=None,
                 vartype: VarType = VarType.CONTINUOUS) -> None:
        
        
        
        if name in Var.decision_variables:
            raise ValueError(f"Var object with name -{name}- already exists!")
        Var.decision_variables[name] = self
        
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.vartype = vartype
        
        if vartype == VarType.BINARY:
            self.lower_bound = 0
            self.upper_bound = 1
            

    def __repr__(self) -> str:
        return f"Var(name={self.name}, lower_bound={self.lower_bound}, upper_bound={self.upper_bound})"

    def __str__(self) -> str:
        return self.name

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Expression(variable_coeffs={self: other})
        raise TypeError(f"Unsupported operand type for *: {type(self)} and {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __add__(self, other):
        if isinstance(other, Var):
            return Expression({self: 1.0}) + Expression({other: 1.0})
        if isinstance(other, Expression):
            return Expression({self: 1.0}) + other
        if isinstance(other, (int, float)):
            return Expression(variable_coeffs={self: 1.0}, constant=other)
        raise TypeError(f"Unsupported operand type for +: {type(self)} and {type(other)}")
        
    def __radd__(self, other):
        return self.__add__(other)
        
    def __sub__(self, other):
        if isinstance(other, Var):
            return Expression({self: 1.0}) + Expression({other: -1.0})
        if isinstance(other, Expression):
            return Expression({self: 1.0}) - other
        if isinstance(other, (int, float)):
            return Expression(variable_coeffs={self: 1.0}, constant=other)
        raise TypeError(f"Unsupported operand type for -: {type(self)} and {type(other)}")
        
    def __rsub__(self, other):
        return (-self).__add__(other)
        
    def __neg__(self):
        return Expression({self: -1.0})
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Expression(variable_coeffs={self: 1/other})
        raise TypeError(f"Unsupported operand type for /: {type(self)} and {type(other)}")



class Expression:
    def __init__(self, variable_coeffs: Dict[Var, float], constant=0.0):
        
        self.variable_coeffs = variable_coeffs
        self.constant = constant
        
    def __neg__(self):
        self.variable_coeffs = {var: -1.0*coeff for var, coeff in self.variable_coeffs.items()}
        self.constant *= -1.0
        return self

    def __repr__(self):
        return f"Expression({self.variable_coeffs})"

    def __str__(self):
        expression = []
        for variable, coeff in self.variable_coeffs.items():
            expression.append(f"{coeff}*{variable}")
        return " + ".join(expression)

    def __add__(self, other):
        if isinstance(other, Var):
            return self + Expression({other: 1.0})
        if isinstance(other, Expression):
            variable_coeffs_ = self.variable_coeffs.copy()
            for variable, coeff in other.variable_coeffs.items():
                if variable in variable_coeffs_.keys():
                    variable_coeffs_[variable] += coeff
                else:
                    variable_coeffs_[variable] = coeff
            return Expression(variable_coeffs=variable_coeffs_, constant=self.constant+other.constant)
        if isinstance(other, (int, float)):
            self.constant += other
            return self
        raise TypeError(f"Unsupported operand type for +: {type(self)} and {type(other)}")
        
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Var):
            return self + Expression({other: -1.0})
        if isinstance(other, (int, float)):
            self.constant -= other
            return self
        if isinstance(other, Expression):
            variable_coeffs_ = self.variable_coeffs.copy()
            for variable, coeff in other.variable_coeffs.items():
                if variable in variable_coeffs_.keys():
                    variable_coeffs_[variable] -= coeff
                else:
                    variable_coeffs_[variable] = -coeff
                    
            return Expression(variable_coeffs=variable_coeffs_,
                              constant=self.constant - other.constant)
        raise TypeError(f"Unsupported operand type for -: {type(self)} and {type(other)}")
        
    def __rsub__(self, other):
        return (-self).__add__(other)
        
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self.variable_coeffs = {var: coeff*other for var, coeff in self.variable_coeffs.items()}
            self.constant *= other
            return self
        raise TypeError(f"Unsupported operand type for *: {type(self)} and {type(other)}")
        
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            self.variable_coeffs = {var: coeff/other for var, coeff in self.variable_coeffs.items()}
            self.constant /= other
            return self
        raise TypeError(f"Unsupported operand type for /: {type(self)} and {type(other)}") 
    

    
class Model:
    def __init__(self):
        self.constraints = {}
        self.obj = None
        self.minmax = None
    
    def addConstraint(self,
                      lhs: Expression,
                      sense: str,
                      rhs: float,
                      name: str) -> None:
        self.constraints[name] = (lhs, sense, rhs)
    
    def setObjective(self,
                     obj: Expression,
                     sense: str) -> None:
        self.obj = obj
        self.minmax = sense
    
    def write_lp_file(self):
        pass
    
    def solve(self):
        pass
    
    
    
if __name__ == "__main__":
    x = Var(name="x", lower_bound=0.0, upper_bound=5.0, vartype=VarType.CONTINUOUS)
    y = Var(name="y", lower_bound=0.0, upper_bound=2.0, vartype=VarType.CONTINUOUS)
