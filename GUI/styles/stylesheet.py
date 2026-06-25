"""
アプリケーション全体で使用するスタイルシートを定義するモジュール
"""

# アプリケーション全体のグローバルスタイル（QSS）
APPLICATION_STYLE = """
    /* グローバル設定 */
    QWidget {
        font-family: "Segoe UI", "Helvetica Neue", "Arial", "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
        color: #2c3e50;
        font-size: 14px;
    }
    
    /* ウィンドウ背景 */
    QMainWindow, QWidget#HomeWindow, QWidget#DragDropWindow, QWidget#CombineWindow {
        background-color: #f4f7f9;
    }
    
    /* カード/コンテナ風背景 */
    QFrame#CardFrame {
        background-color: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
    }
    
    /* 入力フォーム (QLineEdit) */
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        color: #334155;
        selection-background-color: #0077ff;
    }
    
    QLineEdit:focus {
        border: 2px solid #0077ff;
        background-color: #ffffff;
    }
    
    QLineEdit:read-only {
        background-color: #f8fafc;
        color: #64748b;
        border: 1px solid #e2e8f0;
    }
    
    /* リストウィジェット */
    QListWidget {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 6px;
        outline: 0;
    }
    
    QListWidget::item {
        padding: 10px 14px;
        margin: 2px 0px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
        border-radius: 6px;
    }
    
    QListWidget::item:hover {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    QListWidget::item:selected {
        background-color: #e0f2fe;
        color: #0369a1;
        font-weight: bold;
    }
    
    /* プログレスバー */
    QProgressBar {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        text-align: center;
        background-color: #e2e8f0;
        height: 20px;
        font-weight: bold;
    }
    
    QProgressBar::chunk {
        background-color: #0077ff;
        border-radius: 9px;
    }
    
    /* デフォルトボタン (Primary) */
    QPushButton {
        background-color: #0077ff;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }
    
    QPushButton:hover {
        background-color: #0066dd;
    }
    
    QPushButton:pressed {
        background-color: #0055bb;
    }
    
    QPushButton:disabled {
        background-color: #cbd5e1;
        color: #94a3b8;
    }
    
    /* セカンダリボタン (戻る、閉じるなど) */
    QPushButton#SecondaryButton {
        background-color: #64748b;
        color: #ffffff;
    }
    
    QPushButton#SecondaryButton:hover {
        background-color: #475569;
    }
    
    QPushButton#SecondaryButton:pressed {
        background-color: #334155;
    }
    
    /* アクセントボタン (一括結合、成功など) */
    QPushButton#AccentButton {
        background-color: #10b981;
        color: #ffffff;
    }
    
    QPushButton#AccentButton:hover {
        background-color: #059669;
    }
    
    QPushButton#AccentButton:pressed {
        background-color: #047857;
    }
"""

# ドロップエリア用スタイル
DROP_AREA_DEFAULT = """
    QLabel {
        border: 2px dashed #94a3b8;
        border-radius: 8px;
        background-color: #ffffff;
        padding: 25px;
        font-size: 15px;
        font-weight: bold;
        color: #64748b;
    }
"""

DROP_AREA_ACTIVE = """
    QLabel {
        border: 2px solid #0077ff;
        border-radius: 8px;
        background-color: #eff6ff;
        padding: 25px;
        font-size: 15px;
        font-weight: bold;
        color: #0077ff;
    }
"""

# 後方互換性および既存参照のためのダミー定義
MAIN_WINDOW = APPLICATION_STYLE
FILE_LIST_WIDGET = ""
BUTTON_DEFAULT = ""

def get_application_style():
    """アプリケーション全体のスタイルシートを返します"""
    return APPLICATION_STYLE