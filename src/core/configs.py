import datetime as dt
from pathlib import Path

import yaml
from addict import Dict
from starlette.config import Config

KST = dt.timezone(offset=dt.timedelta(hours=9), name="KST")
RESOURCES = Path("resources")

sys_config = Config(env_file=".env")
env = sys_config(key="env")

if env == "container":
    with open(RESOURCES / "config_container.yaml", encoding="utf-8") as f:
        config = Dict(yaml.load(f, Loader=yaml.SafeLoader))
else:
    with open(RESOURCES / "config.yaml", encoding="utf-8") as f:
        config = Dict(yaml.load(f, Loader=yaml.SafeLoader))
