import os
from flask import Flask, request, jsonify, send_file
from .encryption_utils.encryptor import encrypt_file, decrypt_file

app = Flask(__name__)

@app.route('/api/')
def home():
    return jsonify({"message": "Hello from Flask!"})

# Route for encryption
@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'File and password are required'}), 400

    file = request.files['file']
    password = request.form['password']

    try:
        content = file.read()
        encrypted_content = encrypt_file(content, password)

        # Save encrypted content to a temporary file
        temp_filename = f"{file.filename}.enc"
        with open(temp_filename, 'wb') as temp_file:
            temp_file.write(encrypted_content)

        return send_file(temp_filename, as_attachment=True, attachment_filename=temp_filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for decryption
@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Encrypted file and password are required'}), 400

    file = request.files['file']
    password = request.form['password']

    try:
        encrypted_content = file.read()
        decrypted_content = decrypt_file(encrypted_content, password)

        # Save decrypted content to a temporary file
        original_filename = file.filename.replace(".enc", "")
        with open(original_filename, 'wb') as temp_file:
            temp_file.write(decrypted_content)

        return send_file(original_filename, as_attachment=True, attachment_filename=original_filename)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
