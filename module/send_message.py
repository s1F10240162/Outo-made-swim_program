import requests
import logging
import os
import traceback

# 環境変数の取得（グローバル変数として管理）
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

# ロギング設定（デバッグ時に役立つ）
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_slack_notification(webhook_url, message):
    """
    Slack通知を送信する関数。
    
    :param webhook_url: SlackのWebhook URL
    :param message: 送信するメッセージ内容
    """
    try:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Slack通知エラー: {str(e)}", exc_info=True)
        raise

def send_slack_message(system_name: str, text: str):
    """
    Slackにメッセージを送信する関数。
    :param system_name: 通知元のシステム名
    :param text: 送信するメッセージ内容
    """
    try:
        if not SLACK_TOKEN or not SLACK_CHANNEL:
            logging.warning("Slack トークンまたはチャンネルが未設定")
            return

        # システム名を先頭に付加する
        full_text = f"[{system_name}] {text}"

        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {SLACK_TOKEN}",
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {"channel": SLACK_CHANNEL, "text": full_text}

        try:
            response = requests.post(url, headers=headers, json=data)
            # response.raise_for_status()
            # logging.info(f"Slack 通知成功: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Slack 通知失敗: {e}", exc_info=True)
            # ここで例外を再送出しない（通知失敗は致命的でないため）
    except Exception as e:
        logging.error(f"send_slack_message関数内で予期しないエラー: {e}", exc_info=True)
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    # 環境変数からトークンとチャンネルを取得
    send_slack_message("TestSystem", "テストメッセージ")