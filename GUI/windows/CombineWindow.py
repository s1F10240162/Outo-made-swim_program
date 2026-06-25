# GUI/windows/CombineWindow.py
import os
import logging
import traceback
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel, QMessageBox, QAbstractItemView
from PySide6.QtCore import Qt, Signal, Slot
from module.merge_excel import merge_excel_files
from module.send_message import send_slack_message

logger = logging.getLogger(__name__)

EVENT_NAME_MAP = {
    "50fr.xlsx": "50m 自由形",
    "100fr.xlsx": "100m 自由形",
    "200fr.xlsx": "200m 自由形",
    "400fr.xlsx": "400m 自由形",
    "50ba.xlsx": "50m 背泳ぎ",
    "100ba.xlsx": "100m 背泳ぎ",
    "200ba.xlsx": "200m 背泳ぎ",
    "50br.xlsx": "50m 平泳ぎ",
    "100br.xlsx": "100m 平泳ぎ",
    "200br.xlsx": "200m 平泳ぎ",
    "50fly.xlsx": "50m バタフライ",
    "100fly.xlsx": "100m バタフライ",
    "200fly.xlsx": "200m バタフライ",
    "200im.xlsx": "200m 個人メドレー",
    "400im.xlsx": "400m 個人メドレー",
}

class CombineWindow(QWidget):
    switch_to_completion = Signal()
    
    def __init__(self, result_folder_path, parent=None):
        super().__init__(parent)
        self.result_folder_path = result_folder_path
        self.setObjectName("CombineWindow")
        
        # レイアウト
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # タイトル
        title_label = QLabel("印刷用結合ファイルの作成", self)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a;")
        
        # 説明文
        desc_label = QLabel("印刷したい種目を選択・並べ替えてください。\n(ドラッグ&ドロップまたは右側のボタンで順番を変更できます)", self)
        desc_label.setStyleSheet("font-size: 14px; color: #64748b; line-height: 1.4;")
        
        # リストと並べ替えボタンのレイアウト
        list_layout = QHBoxLayout()
        list_layout.setSpacing(15)
        
        # リストウィジェット
        self.list_widget = QListWidget(self)
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove) # ドラッグ&ドロップでの順序変更を許可
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # 並べ替えボタンのレイアウト
        btn_vertical_layout = QVBoxLayout()
        btn_vertical_layout.setSpacing(12)
        btn_vertical_layout.setAlignment(Qt.AlignTop)
        
        self.btn_up = QPushButton("▲ 上へ", self)
        self.btn_up.setCursor(Qt.PointingHandCursor)
        self.btn_up.setObjectName("SecondaryButton")
        self.btn_up.setMinimumHeight(45)
        self.btn_up.clicked.connect(self.move_item_up)
        
        self.btn_down = QPushButton("▼ 下へ", self)
        self.btn_down.setCursor(Qt.PointingHandCursor)
        self.btn_down.setObjectName("SecondaryButton")
        self.btn_down.setMinimumHeight(45)
        self.btn_down.clicked.connect(self.move_item_down)
        
        btn_vertical_layout.addWidget(self.btn_up)
        btn_vertical_layout.addWidget(self.btn_down)
        
        list_layout.addWidget(self.list_widget, 4)
        list_layout.addLayout(btn_vertical_layout, 1)
        
        # アクションボタンレイアウト
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.btn_back = QPushButton("戻る", self)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setMinimumHeight(48)
        self.btn_back.setObjectName("SecondaryButton")
        self.btn_back.clicked.connect(self.on_back_clicked)
        
        self.btn_combine = QPushButton("印刷用Excelを結合作成", self)
        self.btn_combine.setCursor(Qt.PointingHandCursor)
        self.btn_combine.setMinimumHeight(48)
        self.btn_combine.setObjectName("AccentButton")
        self.btn_combine.clicked.connect(self.combine_files)
        
        action_layout.addWidget(self.btn_back)
        action_layout.addWidget(self.btn_combine)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addLayout(list_layout)
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
        
        # ファイルリストを読み込む
        self.load_available_files()

    def load_available_files(self):
        """出力フォルダ内の利用可能なExcelファイル（個人成績）を読み込む"""
        self.list_widget.clear()
        if not os.path.exists(self.result_folder_path):
            return
            
        files = os.listdir(self.result_folder_path)
        # 結合ファイルや _id.xlsx は除外
        excel_files = [f for f in files if f.endswith(".xlsx") and not f.endswith("_id.xlsx") and f != "combined_program.xlsx" and not f.startswith("~$")]
        
        # 種目名をキーとした順番でソートして初期表示（50fr, 100fr, etc.）
        # ソート順を定義
        stroke_order = ["fly", "ba", "br", "fr", "im"]
        distance_order = [50, 100, 200, 400]
        
        def sort_key(filename):
            for stroke_idx, s in enumerate(stroke_order):
                for dist_idx, d in enumerate(distance_order):
                    if f"{d}{s}.xlsx" == filename:
                        return (stroke_idx, dist_idx)
            return (99, 99)
            
        sorted_files = sorted(excel_files, key=sort_key)
        
        for f in sorted_files:
            japanese_name = EVENT_NAME_MAP.get(f, f)
            item = QListWidgetItem(f"{japanese_name} ({f})")
            # ファイル名をカスタムデータとして保持
            item.setData(Qt.UserRole, f)
            self.list_widget.addItem(item)

    def move_item_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            current_item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, current_item)
            self.list_widget.setCurrentRow(current_row - 1)

    def move_item_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            current_item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, current_item)
            self.list_widget.setCurrentRow(current_row + 1)

    def on_back_clicked(self):
        self.switch_to_completion.emit()

    def combine_files(self):
        """リストの順番に従ってファイルを結合する"""
        try:
            count = self.list_widget.count()
            if count == 0:
                QMessageBox.warning(self, "警告", "結合する種目ファイルがありません。")
                return
                
            file_order = []
            for i in range(count):
                item = self.list_widget.item(i)
                filename = item.data(Qt.UserRole)
                file_order.append(filename)
                
            logger.info(f"ファイルの結合を開始します: {file_order}")
            
            # 結合を実行
            output_path = merge_excel_files(self.result_folder_path, file_order)
            
            # 成功メッセージ
            QMessageBox.information(
                self, 
                "成功", 
                f"印刷用プログラムの結合に成功しました！\n\nファイル名: combined_program.xlsx\n場所: {self.result_folder_path}"
            )
            self.switch_to_completion.emit()
            
        except Exception as e:
            logger.error(f"Excelの結合中にエラーが発生しました: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CombineWindow combine_filesでエラー: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", f"結合処理中にエラーが発生しました:\n{e}")
