from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal

class CompletionWidget(QWidget):
    """処理完了通知を表示するコンポーネント"""
    
    close_requested = Signal()  # 閉じるボタンが押された時に発火するシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 外側のレイアウト
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        
        # カード型のフレームを作成
        card = QFrame(self)
        card.setObjectName("CardFrame")
        card.setFixedSize(420, 200)
        
        # カード内部のレイアウト
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)
        
        # 完了メッセージ
        self.message_label = QLabel("プログラムの作成が完了しました", card)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            font-size: 20px;
            color: #0f172a;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        
        # 閉じるボタン
        self.close_button = QPushButton("閉じる", card)
        self.close_button.setObjectName("SecondaryButton")
        self.close_button.setMinimumHeight(45)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self._on_close_clicked)
        
        # カードレイアウトにウィジェットを追加
        card_layout.addWidget(self.message_label)
        card_layout.addWidget(self.close_button)
        
        # 外側レイアウトにカードを追加
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)
    
    def _on_close_clicked(self):
        """閉じるボタンがクリックされた時の処理"""
        self.close_requested.emit()