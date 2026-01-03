import os
import subprocess
import flask

app = flask.Flask(__name__)

# --- 1. SECRET SCANNING TRIGGER ---
# GitHub's "Generic Secret" scanner should pick this up.
TEST_API_KEY = "xoxb-123456789012-1234567890123-4567890abcdef1234567890a" 

@app.route("/run-scan")
def scan_directory():
    # --- 2. CODEQL TRIGGER (Command Injection & Path Traversal) ---
    # We take input from the URL and pass it directly to a shell command.
    # CodeQL tracks the "taint" from request.args to subprocess.check_output.
    user_dir = flask.request.args.get("folder")
    
    # VULNERABILITY: An attacker could pass "; rm -rf /" or "../../etc/passwd"
    command = "ls -la " + user_dir
    output = subprocess.check_output(command, shell=True)
    
    return output

if __name__ == "__main__":
    app.run()
