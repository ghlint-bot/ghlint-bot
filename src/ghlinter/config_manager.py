import json
from ghlinter.utils import load_json_file

__CONFIG_FILE_LOCATION = 'config.json'
__CONFIGS: json = {}

def load() -> None:
    __CONFIGS = load_json_file(__CONFIG_FILE_LOCATION)

def bot_name() -> str:
    return __CONFIGS['bot_name']

def issues() -> json:
    return __CONFIGS['issues']