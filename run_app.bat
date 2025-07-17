@echo off

REM このファイルは src/gui に置く想定

REM バッチファイルのある場所に移動
cd /d %~dp0

REM 仮想環境がなければ作成し、初回はsrc/gui/requirements.txtをインストール
if not exist .venv (
    python -m venv .venv
    call .venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    echo.
    echo 仮想環境と必要なライブラリのインストールが完了しました。
    echo もう一度、この run_app.bat をダブルクリックしてアプリを起動してください。
    pause
    exit /b
)

REM 仮想環境を有効化
call .venv\Scripts\activate

REM src/gui/requirements.txt の内容を毎回反映
pip install --upgrade pip
pip install -r requirements.txt

REM Streamlitアプリを起動
streamlit run app.py
pause
exit /b