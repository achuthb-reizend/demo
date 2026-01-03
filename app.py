import sqlite3
import os

# --- 1. SECRET SCANNING TRIGGER ---
# GitHub recognizes this dummy AWS pattern. 
# WARNING: Never push real keys. This is a fake testing string.
AWS_ACCESS_KEY = "AKIAIM7343O4MEXAMPLE" 
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def find_user(username):
    # --- 2. CODEQL TRIGGER (SQL Injection) ---
    # User input is directly concatenated into the SQL string.
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    
    query = "SELECT * FROM accounts WHERE user = '" + username + "';"
    cursor.execute(query)
    
    return cursor.fetchone()

if __name__ == "__main__":
    print(find_user("admin"))
