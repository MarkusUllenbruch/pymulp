from equation_handling import Var, Expression
import pytest

@pytest.fixture(autouse=True)
def reset_decision_variables():
    Var.decision_variables = {}

@pytest.fixture
def x1():
    return Var(name="x1")

@pytest.fixture
def x2():
    return Var(name="x2")




def test_add_x1(x1):
    assert Var.decision_variables == {"x1": x1}
    
    
def test_add_x2(x2):
    assert Var.decision_variables == {"x2": x2}
    
def test_add_x1_x2(x1, x2):
    assert Var.decision_variables == {"x1": x1, "x2": x2}
    
    
    
    
def test_x1_plus_x1(x1):
    res = x1 + x1
    assert res.variable_coeffs == {x1: 2.0}
    
def test_x1_minus_x1(x1):
    res = x1 - x1
    assert res.variable_coeffs == {x1: 0.0}
    
def test_minus_x1_minus_x1(x1):
    res = -x1 - x1
    assert res.variable_coeffs == {x1: -2.0}
    
def test_minus_x1_minus_5_x1(x1):
    res = -1.0*x1 - 5*x1
    assert res.variable_coeffs == {x1: -6.0}
    
def test_minus_minus_x1(x1):
    res = -(-x1)
    assert res.variable_coeffs == {x1: 1.0}
    
def test_minus_minus_minus_x1(x1):
    res = -(-(-x1))
    assert res.variable_coeffs == {x1: -1.0}
    
def test_zero_x1_plus_5_x1(x1):
    res = 0*x1 + 5*x1
    assert res.variable_coeffs == {x1: 5.0}
    
    
def test_5x_minus_20x(x1):
    res = 5*x1 - 20*x1
    assert res.variable_coeffs == {x1: -15.0}
    
    
def test_multiply_5x_minus_20x(x1):
    res = 10*(5*x1 - 20*x1)
    assert res.variable_coeffs == {x1: -150.0}
    
def test_multiply_5x_minus_20x_plus50x1(x1):
    res = 10*(5*x1 - 20*x1) + 50*x1
    assert res.variable_coeffs == {x1: -100.0}
    