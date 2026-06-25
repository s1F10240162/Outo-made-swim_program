import os
import logging
import traceback
from module.send_message import send_slack_message
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from GUI.styles.stylesheet import MAIN_WINDOW
from GUI.components.select_folder_dialog import SelectFolderDialogWidget
from dotenv import load_dotenv

# 環境変数から設定を読み込む
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "AquaProgrammer")  # デフォルト値として"AquaProgrammer"を設定

class HomeWindow(QWidget):
    # 画面遷移用のシグナル（保存先パスを渡せるように変更）
    switch_to_drag_drop = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomeWindow")

        # レイアウト設定
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(25)

        # タイトルラベル
        title_label = QLabel(APP_NAME)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""        
            font-size: 42px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 5px;
        """)
        
        # サブタイトルラベル
        subtitle_label = QLabel("水泳競技プログラム自動作成支援ツール")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""        
            font-size: 16px;
            font-weight: 500;
            color: #64748b;
            margin-bottom: 30px;
        """)

        # ボタン作成
        start_button = QPushButton("プログラム製作を開始する")
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setMinimumHeight(52)
        start_button.setStyleSheet("""        
            QPushButton {
                font-size: 16px;
                border-radius: 8px;
            }
        """)
        
        # ボタンクリック時のイベント接続
        start_button.clicked.connect(self.on_start_button_clicked)

        # フォルダー選択ウィジェットの追加
        self.folder_selector = SelectFolderDialogWidget(self)

        # レイアウトにウィジェットを追加
        layout.addStretch(1)  # 上部に余白を作る
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(self.folder_selector)  # フォルダー選択を追加
        layout.addStretch(1)  # 中央に余白を作る
        layout.addWidget(start_button)
        layout.addStretch(2)  # 下部に余白を作る
        
        self.setLayout(layout)

    def on_start_button_clicked(self):
        try:
            folder = self.get_selected_folder()
            self.switch_to_drag_drop.emit(folder)
        except Exception as e:
            logging.error(f"HomeWindow on_start_button_clickedでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"HomeWindow on_start_button_clickedでエラー: {e}\n{traceback.format_exc()}")

    def get_selected_folder(self):
        try:
            return self.folder_selector.get_folder_path()
        except Exception as e:
            logging.error(f"HomeWindow get_selected_folderでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"HomeWindow get_selected_folderでエラー: {e}\n{traceback.format_exc()}")
            return ""