# main.py
# バックグラウンド処理のメイン実行ファイル
# 最終的なエンドポイントはGUI/apps.pyのmain関数
# 役割: 競技種目ごとに選手データを取得し、タイム順にソートしてランキングを出力する。
# 変数:
#   - data: CSVから読み込んだ選手データ
#   - pl_lst: 選手データを格納するリスト
#   - category: 分類 ('male', 'female', 'mixed' のいずれか)
#   - sorted_dict: 競技別にソートされた選手データの辞書

from typing import NoReturn
import os
import logging
import traceback
from module.send_message import send_slack_message

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main(result_data_file=None, input_data_file=None, merged_csv_data_file=None, template_file=None) -> NoReturn:
    """
    メイン処理:
    1. CSV からプレイヤーデータを取得
    2. 指定されたカテゴリごとに選手をソート
    3. 結果をコンソールに出力
    戻り値:
        NoReturn: この関数は値を返しません
    例外:
        Exception: 処理中に発生した例外はログに記録され、処理を続行します
    """
    # 環境変数の取得（グローバル変数として管理）
    SLACK_TOKEN = os.getenv("SLACK_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
    APP_NAME = os.getenv("APP_NAME", "AquaProgrammer")
    input_data_file = os.getenv("INPUT_DATA_FILE", input_data_file)
    merged_csv_data_file = os.getenv("MERGED_CSV_DATA_FILE", merged_csv_data_file)
    result_data_file = os.getenv("RESULT_DATA_FILE", result_data_file)
    template_file = os.getenv("TEMPLATE_FILE", template_file)

    try:
        logger.info("Excelファイルの変換と結合を開始します")
        from scripts.ExcelToMergedCSV import main as ExcelToMergedCSV_main
        from scripts.write_ID import main as write_to_excel
        from scripts.fill_name import main as fill_name
        # 1. Excel→CSV→マージ
        ExcelToMergedCSV_main(input_data_file, merged_csv_data_file)
        # 2. IDデータの書き込み
        write_to_excel(result_data_file, input_data_file, merged_csv_data_file, template_file)
        # 3. 選手情報の補完
        fill_name(result_data_file, merged_csv_data_file)
        logger.info("処理が正常に完了しました")
        return True
    except FileNotFoundError as e:
        logger.error(f"ファイルが見つかりません: {e}")
        logger.error(traceback.format_exc())
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ファイルが見つかりません: {e}\n{traceback.format_exc()}")
        raise
    except PermissionError as e:
        logger.error(f"ファイルへのアクセス権限がありません: {e}")
        logger.error(traceback.format_exc())
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ファイルへのアクセス権限がありません: {e}\n{traceback.format_exc()}")
        raise
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        logger.error(traceback.format_exc())
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"予期しないエラーが発生しました: {e}\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    from GUI.apps import main as GUI_main
    # GUI_main()
    main()
