# get_ID.py
# 役割: 競技ごとに選手リストを作成し、選手IDを取得する。
# 変数:
#   - data: CSVから読み込んだ選手データ
#   - players: すべての選手データ
#   - sorted_dict: 競技別にソートされた選手データの辞書
#   - player_id_list: 取得した選手IDのリスト

import os
import logging
from typing import List, Tuple, Dict, Optional, Any
from dotenv import load_dotenv
from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row
from module.player_sort_utils import group_and_sort_all_events
from module.player_data import PlayerData
import traceback
from module.send_message import send_slack_message

# ロガーの設定
logger = logging.getLogger(__name__)

load_dotenv()
INPUT_DATA_FILE = os.getenv("INPUT_DATA_FILE", "input_data_folder")
MERGED_CSV_DATA_FILE = os.path.join(INPUT_DATA_FILE, os.getenv("MERGED_CSV_DATA_FILE", "merged_output.csv"))

def get_player_id(csv_path: str, event: Tuple[str, int], category: str = "mixed") -> List[str]:
    """
    指定したイベントに参加する選手のIDを取得する。

    引数:
        - csv_path: 読み込み対象のCSVファイルのパス
        - event: イベントを示すタプル (stroke, distance) 例: ("fr", 50)
        - category: 集計するカテゴリ ("male", "female", "mixed" など)

    戻り値:
        - 指定イベントに該当する選手のIDリスト
        
    例外:
        - FileNotFoundError: CSVファイルが存在しない場合
        - ValueError: イベント情報やカテゴリが正しくない場合
    """
    try:
        # CSVデータの読み込み
        data = read_csv_data(csv_path)
        if len(data) <= 1:  # ヘッダーのみ、またはデータなし
            logger.warning(f"CSVファイルにデータがありません: {csv_path}")
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルにデータがありません: {csv_path}")
            return []

        # 選手データの作成
        header = data[0]
        players = []
        for row in data[1:]:  # ヘッダーをスキップ
            try:
                row_dict = dict(zip(header, row))
                player = create_player_from_row(row_dict)
                players.append(player)
            except ValueError as e:
                logger.warning(f"選手データの作成に失敗しました: {e}")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手データの作成に失敗しました: {e}")
                continue

        # 選手をグループ化してソート
        sorted_dict = group_and_sort_all_events(players, category)
        sorted_players = sorted_dict.get(event, [])
        
        player_ids = [player.id for player in sorted_players]
        logger.info(f"イベント {event} の選手IDを {len(player_ids)}件 取得しました")
        return player_ids

    except FileNotFoundError as e:
        logger.error(f"CSVファイルが見つかりません: {csv_path} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルが見つかりません: {csv_path} - {e}")
        raise
    except ValueError as e:
        logger.error(f"イベントまたはカテゴリの指定が不正です: {event}, {category} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"イベントまたはカテゴリの指定が不正です: {event}, {category} - {e}")
        raise ValueError(f"イベントまたはカテゴリの指定が不正です: {event}, {category}")
    except Exception as e:
        logger.error(f"選手ID取得中に予期しないエラーが発生しました: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手ID取得中に予期しないエラーが発生しました: {e}\n{traceback.format_exc()}")
        raise

def get_player_info_by_id(player_id_list: List[str], csv_path: str) -> List[Tuple[str, str, str]]:
    """
    指定されたIDリストに対応する選手の名前と性別を取得する。

    引数:
        - player_id_list: 検索対象のプレイヤーIDのリスト
        - csv_path: 読み込み対象のCSVファイルのパス（全選手データが必要）

    戻り値:
        - 指定IDに該当する選手の (ID, 名前, 性別) のリスト
        
    例外:
        - FileNotFoundError: CSVファイルが存在しない場合
    """
    try:
        # CSVデータの読み込み
        data = read_csv_data(csv_path)
        if len(data) <= 1:  # ヘッダーのみ、またはデータなし
            logger.warning(f"CSVファイルにデータがありません: {csv_path}")
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルにデータがありません: {csv_path}")
            return []

        # 選手データをID別の辞書に格納
        header = data[0]
        players: Dict[str, PlayerData] = {}
        for row in data[1:]:
            try:
                row_dict = dict(zip(header, row))
                player = create_player_from_row(row_dict)
                players[player.id] = player
            except ValueError as e:
                logger.warning(f"選手データの作成に失敗しました: {e}")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手データの作成に失敗しました: {e}")
                continue

        # 指定されたIDに対応する選手情報を取得
        result = []
        for pid in player_id_list:
            if pid in players:
                result.append((pid, players[pid].name, players[pid].sex))
            else:
                logger.warning(f"選手ID '{pid}' に対応する選手が見つかりません")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手ID '{pid}' に対応する選手が見つかりません")
        
        logger.info(f"選手情報を {len(result)}/{len(player_id_list)} 件取得しました")
        return result

    except FileNotFoundError as e:
        logger.error(f"CSVファイルが見つかりません: {csv_path} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルが見つかりません: {csv_path} - {e}")
        raise
    except Exception as e:
        logger.error(f"選手情報取得中に予期しないエラーが発生しました: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手情報取得中に予期しないエラーが発生しました: {e}\n{traceback.format_exc()}")
        raise

def get_players_by_event(csv_path: str, event: Tuple[str, int], category: str = "mixed") -> List[PlayerData]:
    """
    指定したイベントに参加する選手のリストを取得する。

    引数:
        - csv_path: 読み込み対象のCSVファイルのパス
        - event: イベントを示すタプル (stroke, distance) 例: ("fr", 50)
        - category: 集計するカテゴリ ("male", "female", "mixed" など)

    戻り値:
        - 指定イベントに該当する選手オブジェクトのリスト
        
    例外:
        - FileNotFoundError: CSVファイルが存在しない場合
        - ValueError: イベント情報やカテゴリが正しくない場合
    """
    try:
        # CSVデータの読み込み
        data = read_csv_data(csv_path)
        if len(data) <= 1:  # ヘッダーのみ、またはデータなし
            logger.warning(f"CSVファイルにデータがありません: {csv_path}")
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルにデータがありません: {csv_path}")
            return []

        # 選手データの作成
        header = data[0]
        players = []
        for row in data[1:]:  # ヘッダーをスキップ
            try:
                row_dict = dict(zip(header, row))
                player = create_player_from_row(row_dict)
                players.append(player)
            except ValueError as e:
                logger.warning(f"選手データの作成に失敗しました: {e}")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手データの作成に失敗しました: {e}")
                continue

        # 選手をグループ化してソート
        sorted_dict = group_and_sort_all_events(players, category)
        sorted_players = sorted_dict.get(event, [])
        
        logger.info(f"イベント {event} の選手を {len(sorted_players)}件 取得しました")
        return sorted_players

    except FileNotFoundError as e:
        logger.error(f"CSVファイルが見つかりません: {csv_path} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルが見つかりません: {csv_path} - {e}")
        raise
    except ValueError as e:
        logger.error(f"イベントまたはカテゴリの指定が不正です: {event}, {category} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"イベントまたはカテゴリの指定が不正です: {event}, {category} - {e}")
        raise ValueError(f"イベントまたはカテゴリの指定が不正です: {event}, {category}")
    except Exception as e:
        logger.error(f"選手取得中に予期しないエラーが発生しました: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"選手取得中に予期しないエラーが発生しました: {e}\n{traceback.format_exc()}")
        raise
