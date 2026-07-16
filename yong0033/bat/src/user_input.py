'''
Author: Charlotte Pierce

Assignment code for FIT2107 Software Quality and Testing.
Not to be shared or distributed without permission.
'''


def is_int(val):
    '''
    Verify if a value is a valid integer.
    '''
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float(val):
    '''
    Verify if a value is a valid float.
    '''
    try:
        float(val)
        return True
    except ValueError:
        return False


def read_string(prompt):
    '''
    Read a string value from the user.
    '''
    return input(prompt)


def read_integer(prompt):
    '''
    Read an integer value from the user until valid.
    '''
    line = read_string(prompt)
    while not is_int(line):
        print("Please enter a whole number.")
        line = read_string(prompt)
    return int(line)


def read_float(prompt):
    '''
    Read a float value from the user until valid.
    '''
    line = read_string(prompt)
    while not is_float(line):
        print("Please enter a decimal number.")
        line = read_string(prompt)
    return float(line)


def read_integer_range(prompt, min_val, max_val):
    '''
    Read an integer within a range until valid.
    '''
    num = read_integer(prompt)
    while num < min_val or num > max_val:
        print(f"Please enter a value between {min_val} and {max_val}")
        num = read_integer(prompt)
    return num


def read_float_range(prompt, min_val, max_val):
    '''
    Read a float within a range until valid.
    '''
    num = read_float(prompt)
    while num < min_val or num > max_val:
        print(f"Please enter a value between {min_val} and {max_val}")
        num = read_float(prompt)
    return num


def read_bool(prompt):
    '''
    Read a boolean value ('y' or 'n') until valid.
    '''
    line = read_string(prompt).lower()
    while line not in ('y', 'n'):
        print("Please enter 'y' or 'n'")
        line = read_string(prompt).lower()
    return line
