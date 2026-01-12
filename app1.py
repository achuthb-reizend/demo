import sqlite3
import os
import pickle
import subprocess
import hashlib
import base64

# --- 1. SECRET SCANNING TRIGGERS ---
# Fake credentials for testing scanners
AWS_ACCESS_KEY = "AKIAIM7343O4MEXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCfakekeyforsecuritytestingonly
-----END RSA PRIVATE KEY-----"""

# --- 2. WEAK CRYPTOGRAPHY ---
def hash_password(password):
    # MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()

# --- 3. SQL INJECTION ---
def find_user(username):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()

    # Vulnerable string concatenation
    query = "SELECT * FROM accounts WHERE user = '" + username + "';"
    cursor.execute(query)

    return cursor.fetchone()

# --- 4. COMMAND INJECTION ---
def ping_host(host):
    # User input directly passed to shell
    os.system("ping -c 1 " + host)

# --- 5. INSECURE DESERIALIZATION ---
def load_session(data):
    # Arbitrary code execution risk
    return pickle.loads(base64.b64decode(data))

# --- 6. HARDCODED CREDENTIALS ---
def connect_admin():
    username = "admin"
    password = "admin123"  # hardcoded password
    return username, password

# --- 7. PATH TRAVERSAL ---
def read_file(filename):
    # No validation on path
    with open(filename, "r") as f:
        return f.read()

# --- 8. UNSAFE SUBPROCESS ---
def run_command(cmd):
    subprocess.Popen(cmd, shell=True)

if __name__ == "__main__":
    print(find_user("admin' OR '1'='1"))
    ping_host("8.8.8.8; rm -rf /tmp/test")
