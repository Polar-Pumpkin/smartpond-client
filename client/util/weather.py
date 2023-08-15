import json
import os
from typing import Dict

skycon_map_path = os.path.join('config', 'skycon.json')
with open(skycon_map_path, 'r') as file:
    skycon_map = json.load(file)


def extract(payload) -> Dict[str, float]:
    context = payload['result']['realtime']
    skycon = context['skycon']
    return {
        '天气状态': float(skycon_map[skycon]) if not skycon.isdigit() else float(skycon),
        '风速': float(context['wind']['speed']),
        '气温': float(context['temperature']),
    }
