"""
SESSION 4 - Task 3: Custom Calculator Tool Integration with LangChain's Tool Class
Objective: Create custom arithmetic calculator functions in Python (add, subtract, 
multiply, divide, power) and integrate with LangChain using the Tool class.
"""

import sys
import re
import math

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from langchain_core.tools import Tool

# ==============================================================================
# CORE ARITHMETIC FUNCTIONS
# ==============================================================================
def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Returns the difference of two numbers."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Returns the quotient of two numbers, preventing division by zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

def power(a: float, b: float) -> float:
    """Returns a raised to the power of b."""
    return a ** b

# ==============================================================================
# UNIFIED CUSTOM CALCULATOR PARSER
# ==============================================================================
def custom_calculator_engine(query_or_expr: str) -> str:
    """
    Parses and evaluates expressions using custom arithmetic functions.
    Supports queries like: 'add 15 and 25', '15*3', 'divide 100 by 4', '12 + 8 * 2'.
    """
    clean = query_or_expr.lower().strip()
    
    # Word pattern recognition for billing: "3 plates of ... at 320 each with 5% tax"
    bill_match = re.search(r'(\d+)\s*(?:plates?|items?|portions?|orders?).*?(?:at|@)\s*(\d+).*?(\d+)%\s*tax', clean)
    if bill_match:
        qty = float(bill_match.group(1))
        unit_price = float(bill_match.group(2))
        tax_pct = float(bill_match.group(3))
        total = (qty * unit_price) * (1 + tax_pct / 100.0)
        return f"({qty} * {unit_price}) + {tax_pct}% tax = {total:.2f}"

    # Word pattern recognition for explicit functional calls
    add_match = re.search(r'(?:add|sum of)\s+([0-9.]+)\s+(?:and|\+)\s+([0-9.]+)', clean)
    if add_match:
        res = add(float(add_match.group(1)), float(add_match.group(2)))
        return f"{add_match.group(1)} + {add_match.group(2)} = {res}"

    sub_match = re.search(r'(?:subtract)\s+([0-9.]+)\s+(?:from)\s+([0-9.]+)', clean)
    if sub_match:
        res = subtract(float(sub_match.group(2)), float(sub_match.group(1)))
        return f"{sub_match.group(2)} - {sub_match.group(1)} = {res}"

    mul_match = re.search(r'(?:multiply)\s+([0-9.]+)\s+(?:by|and|\*)\s+([0-9.]+)', clean)
    if mul_match:
        res = multiply(float(mul_match.group(1)), float(mul_match.group(2)))
        return f"{mul_match.group(1)} * {mul_match.group(2)} = {res}"

    div_match = re.search(r'(?:divide)\s+([0-9.]+)\s+(?:by|\/)\s+([0-9.]+)', clean)
    if div_match:
        try:
            res = divide(float(div_match.group(1)), float(div_match.group(2)))
            return f"{div_match.group(1)} / {div_match.group(2)} = {res}"
        except ZeroDivisionError as e:
            return str(e)

    # General arithmetic evaluation
    clean = re.sub(r'\btimes\b|\bx\b', '*', clean)
    clean = re.sub(r'\bplus\b', '+', clean)
    clean = re.sub(r'\bminus\b', '-', clean)
    clean = re.sub(r'\bdivided by\b|\bover\b', '/', clean)
    
    expr = re.sub(r'[^0-9+\-*/().^ ]', '', clean).replace('^', '**').strip()
    if not expr:
        return "Invalid arithmetic expression."
    try:
        scope = {
            "add": add, "sub": subtract, "mul": multiply, "div": divide, "pow": power,
            "math": math
        }
        val = eval(expr, {"__builtins__": None}, scope)
        return f"{expr} = {val}"
    except Exception as e:
        return f"Calculation error: {e}"

# ==============================================================================
# REGISTER WITH LANGCHAIN TOOL CLASS
# ==============================================================================
def get_custom_calculator_tool() -> Tool:
    """Creates a LangChain Tool instance for custom arithmetic."""
    return Tool(
        name="CustomCalculator",
        func=custom_calculator_engine,
        description=(
            "Use this tool to perform arithmetic calculations: addition, subtraction, "
            "multiplication, division, and exponents. Input should be an expression or sentence like '15*3' or 'add 20 and 5'."
        )
    )

def main():
    print("=" * 65)
    print("   SESSION 4 - TASK 3: CUSTOM CALCULATOR TOOL REGISTRATION")
    print("=" * 65)
    
    calc_tool = get_custom_calculator_tool()
    print(f"Tool Name        : {calc_tool.name}")
    print(f"Tool Description : {calc_tool.description}")
    print("-" * 65)
    
    test_queries = [
        "15*3",
        "add 120 and 45",
        "divide 100 by 4",
        "subtract 30 from 100",
        "(50 + 25) * 2 / 5"
    ]
    
    for q in test_queries:
        result = calc_tool.run(q)
        print(f"Input : '{q}'")
        print(f"Output: {result}")
        print("-" * 65)

if __name__ == "__main__":
    main()
