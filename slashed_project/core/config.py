import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "fullscreen": True,
            "volume": 100,
            "resolution": {
                "width": 2560,
                "height": 1600
            },
            "aspect-ratio": "16:10"
        }
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)