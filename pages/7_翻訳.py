import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("翻訳")
settings = sidebar_settings()
tool_header("🌐 翻訳", "原文のニュアンスを保った自然な翻訳を行います。")

text = st.text_area("原文 *", height=240)

col1, col2 = st.columns(2)
with col1:
    target_lang = st.selectbox(
        "翻訳先の言語",
        ["英語", "日本語", "中国語（簡体字）", "韓国語", "フランス語", "ドイツ語", "スペイン語"],
    )
with col2:
    tone = st.selectbox("トーン", ["原文に合わせる", "フォーマル", "カジュアル", "ビジネス"])

glossary = st.text_input("用語・固有名詞の指定", placeholder="例: 弊社=our company, 製品名はそのまま")

if st.button("翻訳する", type="primary", disabled=not text):
    system, prompt = prompts.translate(
        text=text, target_lang=target_lang, tone=tone, glossary=glossary,
    )
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="翻訳結果", download_name="translation.md",
    )
