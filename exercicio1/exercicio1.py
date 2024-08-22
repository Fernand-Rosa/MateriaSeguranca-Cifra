from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
import struct

HEADER_SIZE = 32
IDENTIFIER = b'\x12\x34'  
VERSION = 1              
ALGORITHM = 1            
MODE = 1                 
RESERVED = b'\x00' * 11  

def create_header(iv: bytes) -> bytes:
    """Cria o cabeçalho para o arquivo criptografado."""
    header = IDENTIFIER
    header += bytes([VERSION])
    header += bytes([ALGORITHM])
    header += bytes([MODE])
    header += iv
    header += RESERVED
    return header

def encrypt_file(input_file: str, output_file: str, key: bytes):
    """Criptografa o arquivo especificado."""
    iv = secrets.token_bytes(16)
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Adiciona padding ao texto em claro
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Criptografa o texto em claro
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Cria o cabeçalho e escreve no arquivo de saída
    with open(output_file, 'wb') as f:
        header = create_header(iv)
        f.write(header)
        f.write(ciphertext)

def decrypt_file(input_file: str, output_file: str, key: bytes):
    """Descriptografa o arquivo especificado."""
    with open(input_file, 'rb') as f:
        header = f.read(HEADER_SIZE)
        iv = header[8:24]
        ciphertext = f.read()

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()

    # Descriptografa o texto cifrado
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove o padding do texto
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Salva o texto descriptografado no arquivo de saída
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Chave de 16 bytes
key = b'0123456789abcdef'  

# Criptografar
encrypt_file('arquivo.txt', 'encrypted.enc', key)

# Descriptografar
decrypt_file('encrypted.enc', 'decrypted.txt', key)
