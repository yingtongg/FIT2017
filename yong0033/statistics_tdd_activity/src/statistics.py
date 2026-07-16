def sum(data):
    total = 0
    for value in data:
        total += value
    return total

def mean(data):
    total = 0
    count = 0
    for value in data:
        total += value
        count += 1
    return total / count if count != 0 else 0

def minimum(data):
    if not data:
        raise ValueError("minimum() arg is an empty sequence")
    min_val = data[0]
    for value in data:
        if value < min_val:
            min_val = value
    return min_val

def maximum(data):
    if not data:
        raise ValueError("maximum() arg is an empty sequence")
    max_val = data[0]
    for value in data:
        if value > max_val:
            max_val = value
    return max_val




