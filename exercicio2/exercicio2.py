from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
import secrets
import struct

HEADER_SIZE = 48
IDENTIFIER = b'\x12\x34'  
VERSION = 1              
ALGORITHM = 1            
MODE = 1                 
RESERVED = b'\x00' * 11  

def create_header(iv: bytes, fingerprint: bytes) -> bytes:
    """Cria o cabeçalho para o arquivo criptografado."""
    header = IDENTIFIER
    header += bytes([VERSION])
    header += bytes([ALGORITHM])
    header += bytes([MODE])
    header += iv
    header += fingerprint
    header += RESERVED
    return header

def calculate_fingerprint(data: bytes) -> bytes:
    """Calcula o fingerprint do dado."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()[:16]  # Usando apenas os primeiros 16 bytes do hash


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

    # Calcula o fingerprint do texto cifrado
    fingerprint = calculate_fingerprint(ciphertext)

    # Cria o cabeçalho e escreve no arquivo de saída
    with open(output_file, 'wb') as f:
        header = create_header(iv, fingerprint)
        f.write(header)
        f.write(ciphertext)

def decrypt_file(input_file: str, output_file: str, key: bytes):
    """Descriptografa o arquivo especificado."""
    with open(input_file, 'rb') as f:
        header = f.read(HEADER_SIZE)
        iv = header[8:24]
        fingerprint = header[24:40]
        ciphertext = f.read()

    # Verifica a integridade do arquivo
    calculated_fingerprint = calculate_fingerprint(ciphertext)
    if calculated_fingerprint != fingerprint:
        raise ValueError("A integridade do arquivo foi comprometida!")

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

def corrupt_file(file_path: str):
    """Corrompe o arquivo especificado."""
    with open(file_path, 'r+b') as f:
        f.seek(10)  # Move o cursor para a posição 10
        f.write(b'\x00')  # Escreve um byte nulo para corromper o arquivo

# Chave de 16 bytes
key = b'0123456789abcdef'  

# Criptografar
encrypt_file('input_file.txt', 'encrypted.enc', key)

# Corromper o arquivo
corrupt_file('input_file.txt')

# Descriptografar
try:
    decrypt_file('encrypted.enc', 'decrypted.txt', key)
except ValueError as e:
    print(e)
