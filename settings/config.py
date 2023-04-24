from pathlib import Path
from configparser import ConfigParser

config = ConfigParser()
config.read(Path('settings', 'config.ini'))
mode = config['DEFAULT'].get('mode')