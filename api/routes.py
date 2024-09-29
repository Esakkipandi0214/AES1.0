import os
import logging
from flask import Flask, request, jsonify
from .encryption_utils.encryptor import encrypt_file, decrypt_file

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        if 'file' not in request.files or 'password' not in request.form:
            return jsonify({'error': 'File and password are required'}), 400

        file = request.files['file']
        password = request.form['password']
        content = file.read()

        encrypted_content = encrypt_file(content, password)

        return encrypted_content, 200, {
            'Content-Disposition': f'attachment; filename="{file.filename}.enc"'
        }
    except Exception as e:
        logging.error(f"Error in encrypt: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        if 'file' not in request.files or 'password' not in request.form:
            return jsonify({'error': 'Encrypted file and password are required'}), 400

        file = request.files['file']
        password = request.form['password']
        encrypted_content = file.read()

        decrypted_content = decrypt_file(encrypted_content, password)
        original_filename = file.filename.replace(".enc", "")

        return decrypted_content, 200, {
            'Content-Disposition': f'attachment; filename="{original_filename}"'
        }
    except Exception as e:
        logging.error(f"Error in decrypt: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
