"""AI ライティングツール — ホーム画面。

個人用。Python + Streamlit + Gemini API。データベース・認証なし。
起動: streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from lib.ui import APP_ICON, APP_TITLE, sidebar_settings

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

settings = sidebar_settings()

st.title(f"{APP_ICON} {APP_TITLE}")
st.write(
    "ブログ執筆・メール返信・要約など、ライティング作業をまとめて助ける個人用ツールです。"
    "左のメニューからツールを選んでください。"
)

if not settings.api_key:
    st.info(
        "はじめに、サイドバーで **Gemini API キー** を設定してください。"
        "キーは [Google AI Studio](https://aistudio.google.com/apikey) で無料取得できます。",
        icon="🔑",
    )

st.divider()

TOOLS = [
    ("✏️ ブログ記事作成", "テーマとキーワードから記事の構成・本文を生成", "pages/1_ブログ記事作成.py"),
    ("📧 メール作成・返信", "受信メールへの返信文や新規メールを作成", "pages/2_メール作成・返信.py"),
    ("📝 文章要約", "長文を箇条書き / 段落 / TL;DR で要約", "pages/3_文章要約.py"),
    ("🔧 校正・リライト", "誤字脱字の修正、自然な言い回しへの書き換え", "pages/4_校正・リライト.py"),
    ("🎭 トーン変換", "フォーマル⇔カジュアルなど文体を変換", "pages/5_トーン変換.py"),
    ("💡 タイトル・コピー生成", "記事タイトルや広告コピーの案出し", "pages/6_タイトル・コピー生成.py"),
    ("🌐 翻訳", "ニュアンスを保った自然な翻訳", "pages/7_翻訳.py"),
    ("📣 SNS投稿文作成", "X / Instagram / LinkedIn 向けの投稿文", "pages/8_SNS投稿文作成.py"),
]

cols = st.columns(2)
for i, (name, desc, path) in enumerate(TOOLS):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(name)
            st.write(desc)
            st.page_link(path, label="開く →")

st.divider()
st.caption(
    f"モデル: `{settings.model}` / 入力テキストは Google の Gemini API に送信されます。"
    " 機密情報の取り扱いにご注意ください。"
)
