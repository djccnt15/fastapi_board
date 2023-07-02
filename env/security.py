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
        file_name: Path | str = 'encrypted.bin',
        public_key: Path | str = 'public.pem'
):
    encoded_data = data.encode('utf-8')
    with open(file_name, 'wb') as f:
        with open(public_key) as key:
            recipient_key = RSA.import_key(key.read())
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(encoded_data)
        for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext):
            f.write(x)


def decrypt_rsa(
        file_name: Path | str = 'encrypted.bin',
        private_key: Path | str = 'private.pem'
):
    with open(file_name, 'rb') as f:
        with open(private_key) as k:
            private = RSA.import_key(k.read())
        enc_session_key, nonce, tag, ciphertext = [f.read(x) for x in (private.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    return cipher_aes.decrypt_and_verify(ciphertext, tag).decode('utf-8')


if __name__ == '__main__':
    import json
    from ast import literal_eval

    from env.config import dir_config, get_config

    private_key = dir_config / 'private.pem'
    public_key = dir_config / 'public.pem'

    # # create RSA key
    # create_keys_rsa(private_key, public_key)

    # # encrypt key data
    # dir = get_config()['DIRS'].get('dir_config')
    # key = get_config()['DEFAULT'].get('key')
    # with open(Path(dir, key)) as f:
    #     key_json = json.load(f)
    # encrypt_rsa(str(key_json), dir_config / 'key.bin', public_key)

    # decrypt key data
    key = literal_eval(decrypt_rsa(dir_config / 'key.bin', private_key))
    print(key, type(key))