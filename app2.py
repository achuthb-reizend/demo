from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/download')
def download_file():
    # VULNERABILITY: User input is used directly to access the file system
    # An attacker could send: /download?filename=../../../../etc/passwd
    filename = request.args.get('filename')
    
    file_path = os.path.join("uploads", filename)
    
    return send_file(file_path)

if __name__ == "__main__":
    app.run(debug=True)
