# Test Case: Security Vulnerabilities
# Expected Quality: F
# Expected Bugs: 6


import os

# Security Issue 1: Hardcoded credentials
DB_PASSWORD = "password123"
API_KEY = "sk_live_abc123xyz"

def execute_command(user_input):
    # Security Issue 2: Command injection vulnerability
    os.system(f"echo {user_input}")

def run_sql_query(user_id):
    import sqlite3
    # Security Issue 3: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def save_file(filename, content):
    # Security Issue 4: Path traversal vulnerability
    with open(filename, 'w') as f:
        f.write(content)

def eval_expression(expr):
    # Security Issue 5: Code injection via eval
    return eval(expr)

# Security Issue 6: Insecure random for security purposes
import random
def generate_token():
    return random.randint(1000, 9999)
