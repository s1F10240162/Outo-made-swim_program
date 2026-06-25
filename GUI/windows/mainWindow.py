import os
import logging
import traceback
from module.send_message import send_slack_message
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Qt
from GUI.styles.stylesheet import MAIN_WINDOW
from GUI.windows.DragDropWindow import DragDropWindow
from dotenv import load_dotenv

# 環境変数から設定を読み込む
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "AquaProgrammer")  # デフォルト値として"AquaProgrammer"を設定

class MainWindow(QMainWindow):
    """
    アプリケーションのメインウィンドウ。
    QStackedWidgetを使用して異なる画面間をシームレスに切り替えます。
    """
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(700, 550)
        self.resize(800, 600)
        self.setStyleSheet(MAIN_WINDOW)

        # スタックウィジェットのセットアップ
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 画面インスタンスはMainWindow生成後に作成される
        self.home_page = None
        self.drag_drop_page = None
        
    def setup_pages(self, home_page):
        self.home_page = home_page
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.setCurrentIndex(0)
        self.drag_drop_page = None

    def switch_to_home(self):
        try:
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            logging.error(f"MainWindow switch_to_homeでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"MainWindow switch_to_homeでエラー: {e}\n{traceback.format_exc()}")

    def switch_to_drag_drop(self, result_folder_path):
        try:
            # 既存のDragDropWindowがあれば削除
            if self.drag_drop_page:
                self.stacked_widget.removeWidget(self.drag_drop_page)
                self.drag_drop_page.deleteLater()
            # 新しいDragDropWindowを生成し、保存先パスを渡す
            self.drag_drop_page = DragDropWindow(result_folder_path)
            self.drag_drop_page.switch_to_home.connect(self.switch_to_home)
            self.stacked_widget.addWidget(self.drag_drop_page)
            self.stacked_widget.setCurrentWidget(self.drag_drop_page)
        except Exception as e:
            logging.error(f"MainWindow switch_to_drag_dropでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"MainWindow switch_to_drag_dropでエラー: {e}\n{traceback.format_exc()}")