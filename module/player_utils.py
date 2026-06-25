# player_utils.py
# 役割: CSVの行データを解析し、選手データオブジェクトを作成する。
# 変数:
#   - row: CSVの1行分のデータ
#   - player: 解析後のPlayerDataオブジェクト

import logging
import os
import traceback
from module.send_message import send_slack_message
from module.player_data import PlayerData
from module.event_utils import EVENT_NAMES, parse_event_name

def create_player_from_row(row_dict: dict[str, str]) -> PlayerData:
    try:
        player = PlayerData(
            id=str(row_dict.get("ID") or row_dict.get("No") or row_dict.get("Unnamed: 0") or "").strip(),
            name=str(row_dict.get("氏名") or "").strip(),
            hurigana=str(row_dict.get("ﾌﾘｶﾞﾅ") or "").replace("\u3000", " ").strip(),
            team=str(row_dict.get("学校名") or "").strip(),
            grade=str(row_dict.get("学年") or "").strip(),
            sex=str(row_dict.get("性別") or "").strip()
        )
        for ev_name in EVENT_NAMES:
            if ev_name in row_dict:
                record = str(row_dict[ev_name]).strip()
                if not record or record == "nan" or record == "0" or record == "0.0" or record == "0:00.00":
                    continue
                stroke, distance = parse_event_name(ev_name)
                player.set_time(stroke, distance, record)
        return player
    except Exception as e:
        logging.error(f"create_player_from_rowでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"create_player_from_rowでエラー: {e}\n{traceback.format_exc()}")
        raise
