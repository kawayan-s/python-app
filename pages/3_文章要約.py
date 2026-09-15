import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("文章要約")
settings = sidebar_settings()
tool_header("📝 文章要約", "長文を目的に合わせた形式・分量で要約します。")

text = st.text_area("要約したい文章 *", height=300, placeholder="記事・議事録・論文などを貼り付け")

col1, col2, col3 = st.columns(3)
with col1:
    style = st.selectbox("形式", ["箇条書き", "段落", "1行 (TL;DR)", "エグゼクティブサマリー"])
with col2:
    length = st.selectbox("分量", ["短め", "標準", "詳しめ"])
with col3:
    keep_terms = st.checkbox("固有名詞・数値を保持", value=True)

if text:
    st.caption(f"入力文字数: {len(text):,}")

if st.button("要約する", type="primary", disabled=not text):
    system, prompt = prompts.summarize(
        text=text, style=style, length=length, keep_terms=keep_terms,
    )
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="要約結果", download_name="summary.md",
    )
