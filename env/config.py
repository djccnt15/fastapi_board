from pathlib import Path
from configparser import ConfigParser
from ast import literal_eval

from addict import Dict

from env.security import decrypt_rsa

dir_config = Path('env')


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(dir_config / 'config.ini')
    return config


mode = get_config()['DEFAULT'].get('mode')


def get_key(
        file_name: Path | str = dir_config / 'key.bin',
        private_key: Path | str = dir_config / 'private.pem'
):
    return Dict(literal_eval(decrypt_rsa(file_name, private_key)))