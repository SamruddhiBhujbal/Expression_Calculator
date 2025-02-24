import re

def tokenize(expression):
    return re.findall(r"\d+\.?\d*|//|\*\*|\S", expression)

def apply_op(op, b, a):
    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "%": lambda x, y: x % y,
        "//": lambda x, y: x // y,
        "**": lambda x, y: x ** y
    }
    return ops[op](a, b)

def evaluate(tokens):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "//": 2, "**": 3}
    values = []
    ops = []
    
    try:
        for token in tokens:
            if token.replace(".", "").lstrip("-").isdigit():
                values.append(float(token))
            elif token in precedence:
                while ops and ops[-1] != "(" and precedence.get(ops[-1], 0) >= precedence[token]:
                    values.append(apply_op(ops.pop(), values.pop(), values.pop()))
                ops.append(token)
            elif token == "(":
                ops.append(token)
            elif token == ")":
                while ops and ops[-1] != '(':
                    values.append(apply_op(ops.pop(), values.pop(), values.pop()))
                if not ops:
                    raise ValueError("Mismatched Parentheses.")
                ops.pop()
            else:
                raise ValueError(f"Invalid token: {token}")
        while ops:
            if ops[-1] == "(":
                raise ValueError("Mismatched Parentheses.")
            values.append(apply_op(ops.pop(), values.pop(), values.pop()))
        return values[0]
    except IndexError:
        raise ValueError("Invalid expression: not enough operands.")

def calculator(expression):
    try:
        tokens = tokenize(expression)
        result = evaluate(tokens)
        print(f"{expression} = {result}")
        return result
    except ValueError as e:
        print(f"Error: {str(e)}")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

