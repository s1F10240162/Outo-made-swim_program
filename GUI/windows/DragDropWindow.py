import logging
import os
import traceback
import threading
from module.send_message import send_slack_message
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, Qt, Slot
from GUI.utils.file_manager import FileManager
from GUI.components.dropArea import DropArea
from GUI.components.fileListWidget import FileListWidget
from GUI.components.loadingWidget import LoadingWidget
from GUI.components.completionWidget import CompletionWidget
from GUI.styles.stylesheet import MAIN_WINDOW
from dotenv import load_dotenv
load_dotenv()
INPUT_DATA_FOLDER = os.getenv("INPUT_DATA_FILE", "input_data_folder")

class DragDropWindow(QWidget):
    # 画面遷移用のシグナル
    switch_to_home = Signal()
    
    def __init__(self, result_folder_path, parent=None):
        super().__init__(parent)
        self.setObjectName("DragDropWindow")
        self.result_folder_path = result_folder_path  # 出力先パス
        self.input_folder_path = INPUT_DATA_FOLDER    # 入力先パス
        self.file_manager = FileManager(self.input_folder_path)  # 入力用フォルダにコピー

        # スタックウィジェットの作成（ドラッグドロップ画面、ローディング画面、完了画面の切り替え用）
        self.stacked_widget = QStackedWidget(self)
        
        # メインのドラッグドロップUI
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)

        # コンポーネントの作成
        self.drop_area = DropArea(self)
        self.file_list_widget = FileListWidget(self)
        
        # 戻るボタンの作成
        self.back_button = QPushButton("戻る")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setObjectName("SecondaryButton")
        self.back_button.clicked.connect(self.on_back_button_clicked)

        # ボタンレイアウト
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()

        # メインレイアウト設定
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.drop_area)
        main_layout.addWidget(self.file_list_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # ローディングウィジェット
        self.loading_widget = LoadingWidget()
        
        # 完了通知ウィジェット
        self.completion_widget = CompletionWidget()
        self.completion_widget.close_requested.connect(self.on_completion_close)
        
        # スタックウィジェットにページを追加
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.loading_widget)
        self.stacked_widget.addWidget(self.completion_widget)
        
        # 全体レイアウト
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # シグナル接続
        self.drop_area.filesDropped.connect(self.file_list_widget.add_files)
        self.file_list_widget.copyRequested.connect(self.on_copy_requested)

    def on_copy_requested(self, files):
        try:
            if not files:
                QMessageBox.warning(self, "警告", "コピーするファイルがありません")
                return
            copied_files = self.file_manager.copy_files(files)
            if not copied_files:
                QMessageBox.warning(self, "エラー", "ファイルのコピーに失敗しました")
                return
            self.file_list_widget.clear_files()
            self.stacked_widget.setCurrentIndex(1)
            self.process_thread = threading.Thread(target=self.run_processing)
            self.process_thread.daemon = True
            self.process_thread.start()
        except Exception as e:
            logging.error(f"on_copy_requestedでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"DragDropWindow on_copy_requestedでエラー: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", f"ファイルコピー処理中にエラーが発生しました: {e}")

    def run_processing(self):
        try:
            import main
            main.main(result_data_file=self.result_folder_path)
            from PySide6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(self, "show_completion", Qt.QueuedConnection)
        except Exception as e:
            logging.error(f"run_processingでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"DragDropWindow run_processingでエラー: {e}\n{traceback.format_exc()}")
            self.show_error(str(e))

    @Slot()
    def show_completion(self):
        """ 処理完了画面を表示する """
        self.stacked_widget.setCurrentIndex(2)
        try:
            import os
            import subprocess
            
            abs_path = os.path.abspath(self.result_folder_path)
            logging.info(f"[AutoOpen] Target result folder path: {abs_path}")
            
            if not os.path.exists(abs_path):
                logging.warning(f"[AutoOpen] Folder does not exist, creating it: {abs_path}")
                os.makedirs(abs_path, exist_ok=True)
                
            if os.path.exists(abs_path):
                try:
                    os.startfile(abs_path)
                    logging.info("[AutoOpen] Opened folder using os.startfile")
                except Exception as startfile_err:
                    logging.warning(f"[AutoOpen] os.startfile failed: {startfile_err}. Trying explorer fallback...")
                    subprocess.Popen(['explorer', abs_path], shell=True)
                    logging.info("[AutoOpen] Opened folder using explorer process fallback")
            else:
                logging.error(f"[AutoOpen] Cannot find or create result folder path: {abs_path}")
        except Exception as e:
            logging.error(f"エクスプローラーでフォルダを開く際にエラーが発生しました: {e}", exc_info=True)
    
    @Slot(str)
    def show_error(self, error_message):
        try:
            self.stacked_widget.setCurrentIndex(0)
            QMessageBox.critical(self, "エラー", f"処理中にエラーが発生しました:\n{error_message}")
        except Exception as e:
            logging.error(f"show_errorでエラー: {e}", exc_info=True)
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"DragDropWindow show_errorでエラー: {e}\n{traceback.format_exc()}")
    
    def on_completion_close(self):
        """ 完了画面の閉じるボタンがクリックされた時の処理 """
        self.stacked_widget.setCurrentIndex(0)  # メイン画面に戻る
        
    def on_back_button_clicked(self):
        """戻るボタンがクリックされたらシグナルを発行"""
        self.switch_to_home.emit()
