import streamlit as st

from lib import prompts
from lib.ui import page_setup, run_generation, sidebar_settings, tool_header

page_setup("メール作成・返信")
settings = sidebar_settings()
tool_header("📧 メール作成・返信", "受信メールへの返信、または新規メールの下書きを作成します。")

mode = st.radio("モード", ["返信", "新規作成"], horizontal=True)

received = ""
if mode == "返信":
    received = st.text_area("受信したメール本文 *", height=200, placeholder="ここに相手からのメールを貼り付け")

intent = st.text_area(
    "このメールで伝えたいこと / 目的 *",
    height=100,
    placeholder="例: 日程を来週火曜に変更したい。遅れたことを詫びる。",
)
points = st.text_area("必ず盛り込む要点", height=80, placeholder="箇条書きで可")

col1, col2 = st.columns(2)
with col1:
    relation = st.text_input("相手との関係", placeholder="例: 取引先の担当者 / 社内の上司 / 初めて連絡する相手")
with col2:
    tone = st.selectbox("トーン", ["丁寧（ビジネス標準）", "ややカジュアル", "非常に丁寧・かしこまり", "簡潔・端的"])

ready = bool(intent) and (mode == "新規作成" or bool(received))
if st.button("生成する", type="primary", disabled=not ready):
    system, prompt = prompts.email(
        mode=mode, received=received, intent=intent,
        points=points, relation=relation, tone=tone,
    )
    run_generation(
        settings, prompt, system_instruction=system,
        output_label="生成されたメール", download_name="email.md",
    )
