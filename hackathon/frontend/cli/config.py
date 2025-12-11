# cli/config.py

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".gateway"
CONFIG_FILE = CONFIG_DIR / "config.json"


def save_api_key(api_key: str):
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": api_key}, f)


def load_api_key() -> str | None:
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("api_key")
    except:
        return None
