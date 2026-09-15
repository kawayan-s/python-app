# ✍️ AI ライティングツール

個人用の AI ライティング支援ツール。ブログ執筆・メール返信・要約などを 1 つの Streamlit アプリにまとめています。
データベース・ログイン認証はなし。

技術スタック: **Python / Streamlit / Gemini API（google-genai）**

## 収録ツール

| ツール | 内容 |
| --- | --- |
| ✏️ ブログ記事作成 | テーマ・キーワードから構成／本文を生成 |
| 📧 メール作成・返信 | 受信メールへの返信、新規メールの下書き |
| 📝 文章要約 | 箇条書き / 段落 / TL;DR など形式を選んで要約 |
| 🔧 校正・リライト | 誤字脱字修正、自然な言い回しへの書き換え |
| 🎭 トーン変換 | フォーマル⇔カジュアルなど文体を変換 |
| 💡 タイトル・コピー生成 | 記事タイトル・広告コピーの案出し |
| 🌐 翻訳 | ニュアンスを保った自然な翻訳 |
| 📣 SNS投稿文作成 | X / Instagram / LinkedIn 向け投稿文 |

## セットアップ

```powershell
# 1. 依存関係のインストール
pip install -r requirements.txt

# 2. Gemini API キーを取得
#    https://aistudio.google.com/apikey

# 3. 起動
streamlit run app.py
```

API キーはブラウザのサイドバーに直接入力できます。毎回入力したくない場合は次のいずれか:

- 環境変数: `$env:GEMINI_API_KEY = "xxxx"` してから `streamlit run app.py`
- `.streamlit/secrets.toml`（`.streamlit/secrets.toml.example` をコピー）

## 構成

```
app.py                  ホーム画面
pages/                  各ツール（Streamlit マルチページ）
lib/
  gemini_client.py      Gemini API ラッパー（ストリーミング対応）
  prompts.py            ツールごとのプロンプト定義
  ui.py                 サイドバー・生成処理などの共通 UI
```

新しいツールを追加するには `lib/prompts.py` に関数を足し、`pages/` に 1 ファイル追加するだけです。

## 注意

入力したテキストは Google の Gemini API に送信されます。機密情報の取り扱いにご注意ください。
