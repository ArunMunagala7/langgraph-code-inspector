# Test Case: Missing Edge Cases
# Expected Quality: C+
# Expected Bugs: 4


def reverse_string(s):
    # Missing: None check, empty string check
    return s[::-1]

def get_first_element(arr):
    # Missing: empty array check
    return arr[0]

def divide(a, b):
    # Missing: division by zero check
    return a / b

def parse_json(json_string):
    import json
    # Missing: error handling for invalid JSON
    return json.loads(json_string)

def access_dict(d, key):
    # Missing: key existence check
    return d[key]
