from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_keys_rsa(
        private_key: Path | str = 'private.pem',
        public_key: Path | str = 'public.pem',
        length: int = 2048
):
    key = RSA.generate(length)

    private = key.export_key()
    with open(private_key, 'wb') as f:
        f.write(private)

    public = key.publickey().export_key()
    with open(public_key, 'wb') as f:
        f.write(public)


def encrypt_rsa(
        data: str,
        public_key: Path | str = 'public.pem'
):
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    with open(public_key) as key:
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(key.read()))
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode('utf-8'))

    return enc_session_key, cipher_aes.nonce, tag, ciphertext


def rsa_to_file(
        enc_session_key: bytes,
        nonce: bytes,
        tag: bytes,
        ciphertext: bytes,
        file_name: Path | str = 'encrypted.bin'
):
    with open(file_name, 'wb') as f:
        for x in (enc_session_key, nonce, tag, ciphertext):
            f.write(x)


def rsa_from_file(
        private_key: Path | str = 'private.pem',
        file_name: Path | str = 'encrypted.bin'
):
    with open(private_key) as k:
        private = RSA.import_key(k.read())

    with open(file_name, 'rb') as f:
        enc_session_key, nonce, tag, ciphertext = [f.read(x) for x in (private.size_in_bytes(), 16, 16, -1)]

    return enc_session_key, nonce, tag, ciphertext


def decrypt_rsa(
        enc_session_key: bytes,
        nonce: bytes,
        tag: bytes,
        ciphertext: bytes,
        private_key: Path | str = 'private.pem'
):
    with open(private_key) as k:
        private = RSA.import_key(k.read())

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    return cipher_aes.decrypt_and_verify(ciphertext, tag).decode('utf-8')


if __name__ == '__main__':
    import json
    from ast import literal_eval

    from conf.config import dir_config, get_config

    private_key = dir_config / get_config()['DEFAULT'].get('private_key')
    public_key = dir_config / get_config()['DEFAULT'].get('public_key')
    key = get_config()['DEFAULT'].get('key')

    # create RSA key
    create_keys_rsa(private_key, public_key)

    # encrypt key data
    with open(dir_config / 'key.json') as f:
        key_json = json.load(f)
    enc_session_key, nonce, tag, ciphertext = encrypt_rsa(str(key_json), public_key)
    rsa_to_file(enc_session_key, nonce, tag, ciphertext, dir_config / key)

    # decrypt key data
    enc_session_key, nonce, tag, ciphertext = rsa_from_file(private_key, dir_config / key)
    key = literal_eval(decrypt_rsa(enc_session_key, nonce, tag, ciphertext, private_key))
    print(key, type(key))