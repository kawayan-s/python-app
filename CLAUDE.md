# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

個人用の AI ライティング支援ツール（ブログ執筆、メール返信、要約など）を 1 つにまとめた Streamlit アプリ。データベース・ログイン認証はなし。技術スタック: Python / Streamlit / Gemini API (`google-genai`)。

## Commands

```powershell
# 依存関係のインストール
pip install -r requirements.txt

# 起動
streamlit run app.py

# API キーを毎回入力したくない場合（PowerShell）
$env:GEMINI_API_KEY = "xxxx"; streamlit run app.py
```

Lint/test の仕組みは存在しない（テストスイートなし）。動作確認は実際に `streamlit run app.py` を起動し、ブラウザで対象ページを操作して行う。

## Architecture

Streamlit のマルチページアプリ構成。`app.py` がホーム画面兼エントリポイントで、`pages/` 配下の各ファイルが 1 ツールに対応する（Streamlit の命名規則 `<番号>_<ページ名>.py` によりサイドバーのメニュー順・表示名が決まる）。

すべてのページは同じ3層構造に従う:

1. **`lib/ui.py`** — 共通 UI 部品。`sidebar_settings()` が API キー・モデル・temperature をサイドバーに描画して `Settings` を返し、各ページはこれを毎回呼ぶ。`run_generation()` が Gemini 呼び出し〜ストリーミング表示〜ダウンロードボタンまでを一括して行う共通処理で、新しいページを書くときは基本この関数を呼ぶだけでよい。
2. **`lib/prompts.py`** — ツールごとのプロンプト生成関数（`blog()`, `email()`, `summarize()` など）。すべて `(system_instruction, user_prompt) -> tuple[str, str]` の形で返す。UI ロジックを一切含まず、フォーム入力から素直に文字列を組み立てるだけの純粋関数。
3. **`lib/gemini_client.py`** — `google-genai` SDK の薄いラッパー。`generate()`（一括）と `generate_stream()`（ストリーミング、UI が使うのはこちら）を提供し、`APIError` を `GeminiError` に変換して UI 側で扱いやすくする。

API キーの解決順序は `lib/ui.py` の `_initial_api_key()` にあり、`st.session_state` → 環境変数 (`GEMINI_API_KEY`/`GOOGLE_API_KEY`) → `st.secrets` の順で探索する。サイドバーで入力した値は `st.session_state["api_key"]` に保存され、以降のページ遷移でも保持される。

## 新しいツールを追加する手順

既存の8ページはすべて同じ構成に従っている（`pages/3_文章要約.py` が最小構成の参考実装）。新規ツールもこの型を崩さずに追加する。

1. **`lib/prompts.py`** に関数を追加する。キーワード引数のみを受け取り、`(system_instruction, user_prompt)` の `tuple[str, str]` を返す。UIコードは書かない。共通の書き出しトーンを使う場合は `SYSTEM_BASE` を再利用・拡張する（`email()` の例のように文字列連結で足す）。
2. **`pages/<番号>_<ページ名>.py`** を追加する。番号はサイドバーの表示順、ファイル名がそのままメニュー表示名になる。中身は以下の順で固定:
   ```python
   import streamlit as st
   from lib import prompts
   from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

   page_setup("ページ名")
   settings = sidebar_settings()
   tool_header("<絵文字> ページ名", "1行の説明文")

   # 入力フォーム（st.text_input / st.text_area / st.selectbox / st.slider / st.checkbox）
   # 必須項目のラベル末尾には " *" を付ける

   if st.button("生成する", type="primary", disabled=not <必須項目>):
       system, prompt = prompts.<関数名>(...)
       run_generation(
           settings, prompt, system_instruction=system,
           output_label="<結果の見出し>", download_name="<ファイル名>.md",
       )
   ```
3. `app.py` の `TOOLS` リストにも `(表示名, 説明, ページパス)` を追加してホーム画面のカードに載せる。

**守るべき規約**:
- ボタンラベルは常に「生成する」（要約のみ「要約する」のように動詞化する例外あり）、`type="primary"`、必須入力が空なら `disabled=True`。
- 結果の描画・ダウンロードは自前で書かず必ず `run_generation()` に任せる（ストリーミング表示・空応答時の警告・ダウンロードボタン・プレーンテキスト表示をまとめて処理してくれる）。
- `download_name` は英語のスネークケース（`blog.md`, `summary.md` など）。

## Notes

- 入力テキストはすべて Google の Gemini API に送信される。機密情報の取り扱いに注意。
- `AVAILABLE_MODELS`（`lib/gemini_client.py`）の先頭がサイドバーのデフォルトモデルになる。モデルを追加・変更する際はここを編集する。
- APIキーの実体（`.env`、`.streamlit/secrets.toml`）は `.gitignore` 済み。サンプルは `.env.example` / `.streamlit/secrets.toml.example` を参照。誤ってコミットしないよう注意。
