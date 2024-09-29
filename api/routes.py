import os
from flask import Flask, request, jsonify
from .encryption_utils.encryptor import encrypt_file, decrypt_file

app = Flask(__name__)

# Route for encryption
@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'File and password are required'}), 400

    file = request.files['file']
    password = request.form['password']
    content = file.read()

    encrypted_content = encrypt_file(content, password)

    return encrypted_content, 200, {
        'Content-Disposition': f'attachment; filename="{file.filename}.enc"'
    }

# Route for decryption
@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Encrypted file and password are required'}), 400

    file = request.files['file']
    password = request.form['password']
    encrypted_content = file.read()

    try:
        decrypted_content = decrypt_file(encrypted_content, password)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # Remove the ".enc" extension from the original filename
    original_filename = file.filename.replace(".enc", "")

    return decrypted_content, 200, {
        'Content-Disposition': f'attachment; filename="{original_filename}"'
    }
