import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("トーン変換")
settings = sidebar_settings()
tool_header("🎭 トーン変換", "内容はそのままに、文章の語調・文体だけを変換します。")

text = st.text_area("変換したい文章 *", height=240)

target = st.selectbox(
    "変換後のトーン",
    [
        "フォーマル・ビジネス",
        "カジュアル・フレンドリー",
        "丁寧でやわらかい",
        "簡潔・きびきび",
        "熱量高め・説得的",
        "落ち着いた・中立的",
        "です・ます → だ・である",
        "だ・である → です・ます",
    ],
)
keep_length = st.checkbox("元の分量を保つ", value=True)

if st.button("変換する", type="primary", disabled=not text):
    system, prompt = prompts.tone_shift(text=text, target=target, keep_length=keep_length)
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="変換結果", download_name="tone.md",
    )
