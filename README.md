# 水泳競技プログラム作成自動化システム

このプロジェクトは、水泳競技大会における競技プログラムの作成を自動化するシステムです。  
手動での競技プログラム作成に多くの時間がかかるという課題を解決し、効率的な運用をサポートします。

---

## プロジェクトの目的

- **競技プログラムの作成時間を短縮**  
  手作業で行われていた競技プログラム作成を自動化し、作成にかかる負担を軽減します。
- **ヒューマンエラーの削減**  
  自動処理により、データ入力や選手情報の管理におけるミスを減らします。
- **標準化されたフォーマットの提供**  
  統一された形式の競技プログラムを提供し、運営の効率化に貢献します。

---

## システム概要

このシステムは、水泳大会のエントリーシートを集約し、競技ごとに選手をタイム順に並べ替え、
ID付きの競技プログラムを自動生成します。選手情報はCSVで管理され、最終的な競技プログラムは
Excel形式で出力されます。

GUIアプリ（PySide6）として提供しており、PyInstallerによりWindowsの実行ファイル（.exe）としても配布できます。

---

## ディレクトリ構成

```
root/
  ├── .env                       # 環境設定ファイル
  ├── template.xlsx              # 出力用テンプレートファイル
  ├── main.py                    # バックエンド処理のエントリーポイント
  ├── input_data_folder/         # 入力データフォルダ（個人情報のためgit管理外）
  │   └── [学校名].xlsx          # 各学校のエントリーシート
  ├── result_output_folder/      # 出力結果フォルダ（個人情報のためgit管理外）
  │   └── [距離][種目].xlsx      # 生成された種目別競技プログラム
  ├── scripts/                   # 処理スクリプト
  │   ├── ExcelToMergedCSV.py    # Excel→CSV変換・結合
  │   ├── get_ID.py              # 選手ID取得
  │   ├── write_ID.py            # Excel書き込み
  │   └── fill_name.py           # 選手情報補完
  ├── module/                    # ユーティリティモジュール
  │   ├── csv_utils.py           # CSV操作
  │   ├── player_data.py         # 選手データモデル
  │   ├── player_sort_utils.py   # ソート処理
  │   ├── calc_time.py           # タイム計算
  │   ├── player_utils.py        # 選手ユーティリティ
  │   └── merge_excel.py         # 種目別Excelの結合処理（実装中）
  └── GUI/                       # GUI関連ファイル
      ├── apps.py                # GUIアプリ起動エントリーポイント
      ├── styles/
      │   └── stylesheet.py      # スタイル定義
      ├── components/            # 共通UIコンポーネント
      │   ├── completionWidget.py
      │   ├── fileListWidget.py
      │   ├── loadingWidget.py
      │   └── select_folder_dialog.py
      └── windows/               # ウィンドウ定義
          ├── mainWindow.py      # メインウィンドウ（画面切り替え管理）
          ├── HomeWindow.py      # ホーム画面（保存先フォルダ選択）
          ├── DragDropWindow.py  # エントリーシートD&D画面
          └── CombineWindow.py   # 印刷用ファイル結合画面（実装中・未接続）
```

---

## 機能

1. **Excel→CSV変換・結合**  
   複数のExcelエントリーシートから必要な情報を抽出し、CSVに変換後、一つのCSVファイルに結合します。

2. **データの正規化**  
   選手名、記録時間などのデータを正規化し、一貫した形式に変換します。

3. **競技別の選手ソート**  
   各競技種目（自由形、平泳ぎ、背泳ぎ、バタフライ、個人メドレー）と距離（50m、100m、200m、400m）ごとに
   選手をタイム順にソートします。重複エントリーの除外処理も行います。

4. **ID割り当て**  
   選手ごとに一意のIDを割り当て、プログラム間の参照を容易にします。

5. **テンプレートベースの出力**  
   事前に定義されたExcelテンプレートに基づいて、種目別の競技プログラムを自動生成します。

6. **保存先フォルダの指定**  
   ホーム画面から出力先フォルダを自由に指定できます。

7. **印刷用ファイルの結合（実装中）**  
   種目別Excelファイルを選択・並べ替えして、印刷用の一括プログラムとして出力する機能を実装中です。

8. **エラーハンドリング**  
   ファイルの存在確認や形式チェック、処理中のエラー対応など堅牢な例外処理を実装しています。エラーはSlack通知にも対応しています。

---

## 処理工程

1. **データ収集・前処理**
   - `input_data_folder` 内のExcelエントリーシートを読み込みます。
   - 「個人エントリー」シートから必要な情報を抽出し、CSVに変換します。
   - 全CSVファイルを結合して `merged_output.csv` を生成します。

2. **データ処理**
   - 結合CSVから選手オブジェクトを生成します。
   - 重複エントリーを除外します。
   - 競技種目・距離ごとにグループ化します。
   - タイム順にソートして選手リストを作成します。

3. **出力生成**
   - 各競技種目・距離に対応するExcelファイルを生成します。
   - テンプレートを基に、選手IDを適切なセルに配置します。
   - 完成したファイルを指定の `result_output_folder` に保存します。

---

## 画面遷移

```
HomeWindow（起動画面・保存先フォルダ選択）
    ↓ プログラム製作を開始する
DragDropWindow（エントリーシートをD&Dで投入・処理実行）
    ↓ 処理完了
CompletionWidget（完了画面）
```

---

## 実行方法

### Pythonから実行する場合

1. 各学校のエントリーシート（Excel）を `input_data_folder` に配置します。
2. メインプログラムを実行します。

```sh
python main.py
```

3. 処理が完了すると、指定フォルダに各競技種目のExcelファイルが生成されます。

### exeから実行する場合

配布パッケージ内の `AquaProgrammer.exe` をダブルクリックして起動します。Python環境は不要です。

---

## 環境設定（.env）

```
# アプリ名（ウィンドウタイトルやSlack通知に使用）
APP_NAME = AquaProgrammer

# 出力結果の保存先フォルダ（デフォルト）
RESULT_DATA_FILE = result_output_folder

# 入力データの保存先フォルダ
INPUT_DATA_FILE = input_data_folder

# マージ結果の保存先ファイル
MERGED_CSV_DATA_FILE = merged_output.csv

# テンプレートファイル
TEMPLATE_FILE = template.xlsx
```

---

## 作業ルール
- 機能実装の時は必ずブランチを分けて実装する
- 修正の時は、'modify/修正内容'
- 新機能の場合は、'feature/新機能名'
- 新たに関数を作成した場合、その関数の機能について説明をコメントにて書く

```python
# 関数定義例
def calculate_time(time_str: str) -> float:
    """
    時間文字列（'1:23.45'形式）を秒数に変換する

    引数:
        time_str: 変換する時間文字列

    戻り値:
        変換された秒数（float）
    """
    # 処理内容
    return seconds
```

---
## Gitの使い方

```sh
# 1. リポジトリをクローン（初回のみ）
git clone https://github.com/kanade3256/Outo-made-swim_program.git
cd Outo-made-swim_program

# 2. 最新の変更を取得して main を最新にする
git checkout main  # または git switch main
git pull origin main  # 最新の変更を取得（fetch + merge）

# 3. 作業ブランチを作成
BRANCH_NAME="feature/新機能名"
git switch -c $BRANCH_NAME  # 新しいブランチを作成して切り替え

# 4. コードを編集し、変更をコミット
git add .
git commit -m "機能の説明をここに記述"

# 5. 作業ブランチをリモートにプッシュ
git push -u origin $BRANCH_NAME

# 6. GitHub上でプルリクエストを作成
```

---

## エラーハンドリング

システムは以下のようなエラー状況に対応しています：
- ファイルが見つからない場合
- ファイルへのアクセス権限がない場合
- ファイルの形式が不正な場合
- データの形式や内容に問題がある場合

エラーが発生した場合は、コンソールにメッセージが表示され、詳細なログが `app.log` に記録されます。  
また、`.env` にSlack Webhook URLを設定することで、エラー発生時にSlackへ通知されます。
