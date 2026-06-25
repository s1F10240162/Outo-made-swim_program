from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PySide6.QtCore import Qt

class LoadingWidget(QWidget):
    """処理中のローディング表示を行うコンポーネント"""
    
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
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)
        
        # 処理中メッセージ
        self.message_label = QLabel("処理中です。しばらくお待ちください...", card)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 5px;
        """)
        
        # プログレスバー
        self.progress_bar = QProgressBar(card)
        self.progress_bar.setRange(0, 0)  # 不定のプログレス表示
        self.progress_bar.setFixedSize(320, 16)
        
        # カードレイアウトにウィジェットを追加
        card_layout.addWidget(self.message_label)
        card_layout.addWidget(self.progress_bar)
        
        # 外側レイアウトにカードを追加
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)