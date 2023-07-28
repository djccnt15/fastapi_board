from pathlib import Path
from configparser import ConfigParser
from ast import literal_eval

from addict import Dict

from env.security import rsa_from_file, decrypt_rsa

dir_config = Path('env')


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(dir_config / 'config.ini')
    return config


mode = get_config()['DEFAULT'].get('mode')


def get_key(
        file_name: Path | str = dir_config / get_config()['DEFAULT'].get('key'),
        private_key: Path | str = dir_config / get_config()['DEFAULT'].get('private_key')
):
    enc_session_key, nonce, tag, ciphertext = rsa_from_file(private_key, file_name)
    return Dict(literal_eval(decrypt_rsa(enc_session_key, nonce, tag, ciphertext, private_key)))