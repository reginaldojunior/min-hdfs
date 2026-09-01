import sys
import os
from flask import Flask, request, send_from_directory

app = Flask(__name__)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
STORAGE_DIR = f"storage_{PORT}"

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

@app.route('/upload/<filename>', methods=['POST'])
def upload(filename):
    with open(os.path.join(STORAGE_DIR, filename), "wb") as f:
        f.write(request.data)
    return f"Parte {filename} salva no Nó {PORT}", 201

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    # Retorna o pedaço binário do arquivo
    return send_from_directory(STORAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)