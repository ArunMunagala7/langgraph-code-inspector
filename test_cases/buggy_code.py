# Test Case: Buggy Code - Multiple Issues
# Expected Quality: D
# Expected Bugs: 5


def calculate_average(numbers):
    # Bug 1: No input validation
    # Bug 2: Division by zero if empty list
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    avg = total / len(numbers)  # ZeroDivisionError risk
    return avg

def find_max(lst):
    # Bug 3: No check for empty list
    max = lst[0]  # IndexError if empty
    for num in lst:
        if num > max:
            max = num
    return max

# Bug 4: Hardcoded password
password = "admin123"

def login(user, pwd):
    # Bug 5: Insecure comparison, no hashing
    if pwd == password:
        return True
    return False
