import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("タイトル・コピー生成")
settings = sidebar_settings()
tool_header("💡 タイトル・コピー生成", "記事タイトルや広告コピーの案を複数出します。")

text = st.text_area("内容 / 素材 *", height=200, placeholder="記事の要旨、商品説明、伝えたいことなど")

col1, col2, col3 = st.columns(3)
with col1:
    platform = st.selectbox(
        "用途",
        ["ブログ記事タイトル", "YouTube 動画タイトル", "広告コピー", "メール件名", "プレスリリース見出し"],
    )
with col2:
    count = st.slider("案の数", 3, 15, 7)
with col3:
    tone = st.selectbox("トーン", ["キャッチー", "堅実・誠実", "好奇心をそそる", "ベネフィット訴求"])

if st.button("案を出す", type="primary", disabled=not text):
    system, prompt = prompts.headlines(text=text, platform=platform, count=count, tone=tone)
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="タイトル案", download_name="headlines.md",
    )
