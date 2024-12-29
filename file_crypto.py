import os
import sys
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from threading import Timer

def encrypt_file(input_file, password):
    """Encrypt the input file and save as .enc"""
    key = password.encode('utf-8')[:32]  # Ensure key is 32 bytes
    iv = os.urandom(16)  # Random IV
    encrypted_file = input_file + ".enc"

    with open(input_file, "rb") as f:
        plaintext = f.read()

    # Pad plaintext for AES block alignment
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length] * padding_length)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(encrypted_file, "wb") as f:
        f.write(iv + ciphertext)

    print(f"File encrypted as {encrypted_file}")

def decrypt_file(encrypted_file, password, auto_delete_time=900):
    """Decrypt the input file and save as original file"""
    key = password.encode('utf-8')[:32]  # Ensure key is 32 bytes
    decrypted_file = encrypted_file.replace(".enc", "")

    with open(encrypted_file, "rb") as f:
        iv = f.read(16)  # First 16 bytes are the IV
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    padding_length = plaintext_padded[-1]
    plaintext = plaintext_padded[:-padding_length]

    with open(decrypted_file, "wb") as f:
        f.write(plaintext)

    print(f"File decrypted as {decrypted_file}")
    
    # Schedule deletion of the decrypted file
    def delete_file():
        try:
            os.remove(decrypted_file)
            print(f"Decrypted file {decrypted_file} has been deleted after {auto_delete_time // 60} minutes.")
        except Exception as e:
            print(f"Error deleting file: {e}")
    
    Timer(auto_delete_time, delete_file).start()

def main():
    if len(sys.argv) < 3:
        print("Usage: file_crypto.py <encrypt|decrypt> <file> <password>")
        sys.exit(1)

    operation = sys.argv[1].lower()
    input_file = sys.argv[2]
    password = sys.argv[3]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    if operation == "encrypt":
        encrypt_file(input_file, password)
    elif operation == "decrypt":
        decrypt_file(input_file, password)
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)

if __name__ == "__main__":
    main()