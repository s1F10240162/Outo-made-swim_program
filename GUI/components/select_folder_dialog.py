from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel
from PySide6.QtCore import Qt

class SelectFolderDialogWidget(QWidget):
    """
    保存先フォルダーを選択できるウィジェット
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        label = QLabel("保存先フォルダーを選択してください：")
        label.setStyleSheet("font-weight: 600; color: #475569; font-size: 14px;")
        
        self.path_edit = QLineEdit(self)
        self.path_edit.setReadOnly(True)
        self.path_edit.setMinimumHeight(40)
        
        # Load from .env if available, otherwise default to "result"
        import os
        from dotenv import load_dotenv
        load_dotenv()
        env_result = os.getenv("RESULT_DATA_FILE", "result")
        default_path = os.path.abspath(env_result)
        self.path_edit.setText(default_path)
        
        browse_btn = QPushButton("参照")
        browse_btn.setObjectName("SecondaryButton")
        browse_btn.setMinimumHeight(40)
        browse_btn.setFixedWidth(90)
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self.open_folder_dialog)
        
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)
        h_layout.addWidget(self.path_edit)
        h_layout.addWidget(browse_btn)
        
        layout.addWidget(label)
        layout.addLayout(h_layout)
        self.setLayout(layout)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "保存先フォルダーを選択")
        if folder_path:
            self.path_edit.setText(folder_path)

    def get_folder_path(self):
        return self.path_edit.text()
