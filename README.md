# Data Visualization App

This is a data visualization application built using Streamlit. The application allows users to upload CSV or Excel files, filter the data, and create different types of plots, such as line charts, bar charts, scatter plots, histograms, and heatmaps. Users can also customize graph titles, axis labels, and other visual elements, and save their settings for later use.

# データ可視化アプリ

これは、Streamlitを使用して構築されたデータ可視化アプリケーションです。このアプリケーションを使用すると、CSVまたはExcelファイルをアップロードしてデータをフィルタリングし、折れ線グラフ、棒グラフ、散布図、ヒストグラム、ヒートマップなど、さまざまな種類のグラフを作成できます。ユーザーはグラフのタイトル、軸ラベル、その他の視覚要素をカスタマイズし、設定を保存して後で使用することも可能です。

## Features / 機能

- **File Upload / ファイルのアップロード**: Upload your CSV or Excel files for data visualization. / データの可視化のためにCSVまたはExcelファイルをアップロードします。
- **Sample Data / サンプルデータ**: Use built-in sample datasets (simple or time series) to explore functionality without uploading your own files. / 独自のファイルをアップロードせずに、組み込みのサンプルデータセット（単純データまたは時系列データ）を使用して機能を探索します。
- **Data Filtering / データフィルタリング**: Apply filters to visualize specific portions of your dataset. / データセットの特定の部分を可視化するためのフィルタを適用します。
- **Graph Selection / グラフ選択**: Choose between various types of graphs, including: / 次のグラフの種類から選択できます：
  - Line charts (with dual y-axes support) / 折れ線グラフ（2つのY軸サポートあり）
  - Bar charts / 棒グラフ
  - Scatter plots / 散布図
  - Histograms / ヒストグラム
  - Heatmaps / ヒートマップ
- **Graph Customization / グラフのカスタマイズ**: Customize graph titles, axis labels, font sizes, and more. / グラフのタイトル、軸ラベル、フォントサイズなどをカスタマイズできます。
- **Save User Settings / ユーザー設定の保存**: Save your customized settings for use during future sessions. / カスタマイズした設定を保存し、将来のセッションで使用できます。
- **Download Options / ダウンロードオプション**: Download the generated graphs as HTML files or the filtered data as CSV. / 生成されたグラフをHTMLファイルとして、またはフィルタリングされたデータをCSVファイルとしてダウンロードできます。

## Installation / インストール

To install and run this application locally, follow these steps: / このアプリケーションをローカルにインストールして実行するには、以下の手順に従ってください：

### Prerequisites / 前提条件

- Python 3.7 or higher / Python 3.7以上
- pip (Python package installer) / pip（Pythonパッケージインストーラー）

### Clone the Repository / リポジトリをクローン

```bash
$ git clone https://github.com/stemtazoo/DataVisulalizationApp
$ cd data-visualization-app
```

### Install Dependencies / 依存関係のインストール

You can install the required dependencies using `pip` and the `requirements.txt` file: / 必要な依存関係は`pip`と`requirements.txt`ファイルを使用してインストールできます：

```bash
$ pip install -r requirements.txt
```

### Run the Application / アプリケーションの実行

To run the application locally, use the following command: / アプリケーションをローカルで実行するには、次のコマンドを使用します：

```bash
$ streamlit run app.py
```

This command will start a local server, and you can access the application in your browser at `http://localhost:8501/`. / このコマンドでローカルサーバーが起動し、ブラウザで`http://localhost:8501/`にアクセスできます。

## Usage / 使い方

1. **Upload a File / ファイルのアップロード**: Click on "Upload File" to upload your CSV or Excel file. / "Upload File"をクリックしてCSVまたはExcelファイルをアップロードします。
2. **Use Sample Data / サンプルデータの使用**: If you don't have your own data, select between "Simple Data" or "Time Series Data" as sample data. / 独自のデータがない場合は、"Simple Data"または"Time Series Data"をサンプルデータとして選択します。
3. **Data Preview and Filtering / データのプレビューとフィルタリング**: Filter the data and preview it using the "Data Preview" section. / データをフィルタリングし、「データプレビュー」セクションでプレビューします。
4. **Graph Generation / グラフの生成**:
   - Choose the type of graph you want. / 作成したいグラフの種類を選択します。
   - Select X-axis and Y-axis columns from the data. / データからX軸とY軸の列を選択します。
   - If using a line chart, optionally enable a secondary y-axis. / 折れ線グラフを使用する場合は、必要に応じて第2軸を有効にします。
5. **Customization / カスタマイズ**: Customize the graph title and axis labels as needed. / 必要に応じてグラフのタイトルや軸ラベルをカスタマイズします。
6. **Download Your Results / 結果のダウンロード**: Download the generated graph or filtered data for further use. / 生成されたグラフやフィルタリングされたデータをダウンロードして利用します。

## Project Structure / プロジェクト構成

```
├── app.py                    # Main application script / メインアプリケーションスクリプト
├── config/                   # Configurations / 各種設定ファイル
│   ├── config.json           # Default configuration settings / デフォルト設定
│   └── user_settings.json    # User-specific settings saved between sessions / セッション間で保存されるユーザー固有の設定
├── modules/                  # Python modules for various functionalities / 各種機能のPythonモジュール
│   ├── data_processing.py
│   ├── data_visualization_app.py
│   ├── file_loader.py
│   ├── filters.py
│   ├── helpers.py
│   ├── plot.py
│   ├── sample_data.py
│   ├── state_manager.py
│   ├── ui_components.py
│   └── utils.py
├── requirements.txt          # Python dependencies / Python依存関係
├── README.md                 # Project documentation (this file) / プロジェクトドキュメント（このファイル）
└── run_app.bat               # Windows batch file for quick app start / アプリの迅速な起動用Windowsバッチファイル
```

## Configuration / 設定

The application uses `config.json` for default settings, which include parameters like titles, tab names, etc. The user's custom settings are saved in `user_settings.json` and automatically loaded when the application starts. / このアプリケーションは、タイトル、タブ名などのパラメータを含むデフォルト設定に`config.json`を使用します。ユーザーのカスタム設定は`user_settings.json`に保存され、アプリケーション起動時に自動的にロードされます。

## Contributing / コントリビューション

Contributions are welcome! To contribute: / コントリビューションは歓迎です！コントリビューションを行うには：

1. Fork the repository. / リポジトリをフォークします。
2. Create a new branch (`git checkout -b feature-branch`). / 新しいブランチを作成します (`git checkout -b feature-branch`)。
3. Make your changes and commit them (`git commit -am 'Add some feature'`). / 変更を加えてコミットします (`git commit -am 'Add some feature'`)。
4. Push to the branch (`git push origin feature-branch`). / ブランチにプッシュします (`git push origin feature-branch`)。
5. Open a Pull Request. / プルリクエストを作成します。

## License / ライセンス

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details. / このプロジェクトはMITライセンスの下でライセンスされています。詳細については[LICENSE](LICENSE)ファイルを参照してください。

## Contact / 連絡先

If you have questions, feel free to reach out: / 質問がある場合は、お気軽にご連絡ください：

- Author: [stemtazoo] / 著者: [stemtazoo]
- Email: [stem.sci.tech.eng.math.2013@gmail.com] / メール: [stem.sci.tech.eng.math.2013@gmail.com]

## Download Link / ダウンロードリンク

You can download the project from GitHub at the following link: / プロジェクトは以下のリンクからGitHubでダウンロードできます：

[Data Visualization App GitHub Repository](https://github.com/stemtazoo/DataVisulalizationApp)  


