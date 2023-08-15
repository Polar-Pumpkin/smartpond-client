import json
import os
from typing import Dict

skycon_map_path = os.path.join('config', 'skycon.json')
with open(skycon_map_path, 'r') as file:
    skycon_map = json.load(file)


def extract(payload) -> Dict[str, float]:
    context = payload['result']['realtime']
    return {
        '天气状态': skycon_map[context['skycon']],
        '风速': context['wind']['speed'],
        '气温': context['temperature'],
    }