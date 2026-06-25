# event_utils.py
# 役割: 競技種目名の解析やイベント情報の管理を行う。
# 変数:
#   - event_name: 解析対象の競技種目名
#   - stroke: 泳法（例: 'fr', 'ba', 'fly'）
#   - distance: 距離（例: 50, 100, 200）

import logging
import os
import re
import traceback
from module.send_message import send_slack_message

# CSVファイルの列順に対応するイベント名をあらかじめ用意する
# 7列目～21列目(インデックス6～20)がこの順番である想定
EVENT_NAMES = [
    "100Ba", "100Fly", "200Fr", "100Br", "50Fr", "400Fr", "50Ba", "200IM", "200Ba", "50Fly", "200Br", "200Fly", "100Fr", "50Br", "400IM"
]

def parse_event_name(event_name: str) -> tuple[str, int]:
    try:
        match = re.match(r'(\d+)([A-Za-z]+)', event_name.strip())
        if not match:
            raise ValueError(f"イベント名 '{event_name}' をパースできません")
        dist_str, stroke_str = match.groups()
        distance = int(dist_str)
        stroke_map = {
            'Im':  'im',
            'Ba':  'ba',
            'Br':  'br',
            'Fly': 'fly',
            'Fr':  'fr'
        }
        stroke_str = stroke_str.capitalize()
        if stroke_str not in stroke_map:
            raise ValueError(f"未知の泳法 '{stroke_str}' を検出しました")
        stroke = stroke_map[stroke_str]
        return stroke, distance
    except Exception as e:
        logging.error(f"parse_event_nameでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"parse_event_nameでエラー: {e}\n{traceback.format_exc()}")
        raise
