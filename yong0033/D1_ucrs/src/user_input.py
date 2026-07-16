# src/user_input.py
"""
User Input module
"""

def is_int(val):
    try:
        int(val)
        return True
    except (TypeError, ValueError):
        return False

def is_float(val):
    try:
        float(val)
        return True
    except (TypeError, ValueError):
        return False

def read_string(prompt):
    return input(prompt)

def read_integer(prompt):
    line = read_string(prompt)
    while not is_int(line):
        print("Please enter a whole number.")
        line = read_string(prompt)
    return int(line)

def read_float(prompt):
    line = read_string(prompt)
    while not is_float(line):
        print("Please enter a decimal number.")
        line = read_string(prompt)
    return float(line)

def read_integer_range(prompt, min_val, max_val):
    num = read_integer(prompt)
    while num < min_val or num > max_val:
        print(f"Please enter a value between {min_val} and {max_val}")
        num = read_integer(prompt)
    return num

def read_float_range(prompt, min_val, max_val):
    num = read_float(prompt)
    while num < min_val or num > max_val:
        print(f"Please enter a value between {min_val} and {max_val}")
        num = read_float(prompt)
    return num

def read_bool(prompt):
    """
    Read boolean 'y'/'n'. Returns True for 'y', False for 'n'.
    """
    line = read_string(prompt).strip().lower()
    while line not in ("y", "n"):
        print("Please enter 'y' or 'n'")
        line = read_string(prompt).strip().lower()
    return line == "y"
