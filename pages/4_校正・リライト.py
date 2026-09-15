import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("校正・リライト")
settings = sidebar_settings()
tool_header("🔧 校正・リライト", "誤字脱字の修正や、自然な言い回しへの書き換えを行います。")

text = st.text_area("対象の文章 *", height=280)

col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox(
        "方針",
        [
            "誤字脱字・文法の校正のみ",
            "自然さ重視のリライト",
            "簡潔化",
            "詳細化・肉付け",
        ],
    )
with col2:
    tone = st.selectbox("仕上がりのトーン", ["元のまま", "丁寧・フォーマル", "カジュアル", "硬め・論文調"])

show_diff = st.checkbox("主な修正点も表示する", value=True)

if st.button("実行する", type="primary", disabled=not text):
    system, prompt = prompts.rewrite(
        text=text, mode=mode, tone=tone, show_diff=show_diff,
    )
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="結果", download_name="rewrite.md",
    )
