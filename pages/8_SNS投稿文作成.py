import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("SNS投稿文作成")
settings = sidebar_settings()
tool_header("📣 SNS投稿文作成", "素材から各プラットフォーム向けの投稿文を作成します。")

material = st.text_area("素材 *", height=180, placeholder="告知したいこと、記事リンクの要約、伝えたいメッセージなど")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox(
        "プラットフォーム",
        ["X (Twitter)", "Instagram", "LinkedIn", "Facebook", "スレッド(連投)"],
    )
    count = st.slider("案の数", 1, 8, 3)
with col2:
    tone = st.selectbox("トーン", ["親しみやすい", "プロフェッショナル", "熱量高め", "淡々と情報提供"])
    hashtags = st.checkbox("ハッシュタグを付ける", value=True)
    emoji = st.checkbox("絵文字を使う", value=True)

if st.button("生成する", type="primary", disabled=not material):
    system, prompt = prompts.social(
        material=material, platform=platform, count=count,
        tone=tone, hashtags=hashtags, emoji=emoji,
    )
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="投稿文案", download_name="social.md",
    )
