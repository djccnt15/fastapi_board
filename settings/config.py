from pathlib import Path
from configparser import ConfigParser

dir_config = Path('settings')


def get_config():
    config = ConfigParser()
    config.read(dir_config / 'config.ini')
    return config


mode = get_config()['DEFAULT'].get('mode')