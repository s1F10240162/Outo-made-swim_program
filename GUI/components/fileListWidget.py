from PySide6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class FileListWidget(QWidget):
    """ファイルリストを表示・管理するコンポーネント"""
    
    copyRequested = Signal(list)  # コピー実行が要求された時に発火するシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # ファイルリスト表示部分
        self.file_list = QListWidget(self)
        
        # OKボタン
        self.ok_button = QPushButton("OK (コピー実行)", self)
        self.ok_button.setMinimumHeight(45)
        self.ok_button.clicked.connect(self._handle_copy_request)
        
        # レイアウト設定
        layout = QVBoxLayout()
        layout.addWidget(self.file_list)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
    
    def add_files(self, files):
        """ファイルリストに新しいファイルを追加（重複は除外）"""
        existing_files = {self.file_list.item(i).text() for i in range(self.file_list.count())}
        
        for file in files:
            if file not in existing_files:
                self.file_list.addItem(file)
    
    def get_files(self):
        """現在のファイルリストを取得"""
        return [self.file_list.item(i).text() for i in range(self.file_list.count())]
    
    def clear_files(self):
        """ファイルリストをクリア"""
        self.file_list.clear()
    
    def _handle_copy_request(self):
        """コピー実行ボタン押下時の処理"""
        files = self.get_files()
        self.copyRequested.emit(files)