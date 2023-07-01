import json
from pathlib import Path
from configparser import ConfigParser

from addict import Dict

dir_config = Path('settings')


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(dir_config / 'config.ini')
    return config


mode = get_config()['DEFAULT'].get('mode')

auth_config = dir_config / get_config()['AUTH'].get('secret')

with open(auth_config) as f:
    auth_config = Dict(json.load(fp=f)).auth