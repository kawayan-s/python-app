import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("ブログ記事作成")
settings = sidebar_settings()
tool_header("✏️ ブログ記事作成", "テーマ・キーワードから記事の構成や本文を生成します。")

topic = st.text_input("記事のテーマ *", placeholder="例: 在宅ワークで集中力を保つ方法")
col1, col2 = st.columns(2)
with col1:
    audience = st.text_input("想定読者", placeholder="例: リモートワーク歴の浅い会社員")
    tone = st.selectbox(
        "トーン",
        ["丁寧・解説的", "カジュアル・親しみやすい", "専門的・硬め", "熱量高め・説得的"],
    )
with col2:
    keywords = st.text_input("含めたいキーワード（カンマ区切り）", placeholder="ポモドーロ, 通知オフ, 朝ルーティン")
    length = st.selectbox("分量", ["1000〜1500字", "2000〜3000字", "4000字以上", "800字以内（コンパクト）"])

notes = st.text_area("補足・盛り込みたい情報", height=120, placeholder="自分の体験、参照したいデータ、結論の方向性など")
outline_only = st.checkbox("構成（見出し）だけ生成する")

if st.button("生成する", type="primary", disabled=not topic):
    system, prompt = prompts.blog(
        topic=topic,
        keywords=keywords,
        audience=audience,
        tone=tone,
        length=length,
        outline_only=outline_only,
        notes=notes,
    )
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="生成された記事", download_name="blog.md",
    )
