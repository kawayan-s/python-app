"""各ページで共有する Streamlit UI パーツ。"""

from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st

from lib.gemini_client import (
    AVAILABLE_MODELS,
    GeminiError,
    generate_stream,
    get_client,
)

APP_TITLE = "AI ライティングツール"
APP_ICON = "✍️"


@dataclass
class Settings:
    api_key: str
    model: str
    temperature: float


def _initial_api_key() -> str:
    """環境変数 → st.secrets → セッション の順で API キーを探す。"""
    if st.session_state.get("api_key"):
        return st.session_state["api_key"]
    env = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if env:
        return env
    try:
        return st.secrets.get("GEMINI_API_KEY", "")  # type: ignore[no-any-return]
    except Exception:
        return ""


def page_setup(page_title: str) -> None:
    st.set_page_config(
        page_title=f"{page_title} | {APP_TITLE}",
        page_icon=APP_ICON,
        layout="wide",
    )


def sidebar_settings() -> Settings:
    """サイドバーに設定 UI を描画し、現在の設定を返す。"""
    with st.sidebar:
        st.subheader("⚙️ 設定")

        default_key = _initial_api_key()
        api_key = st.text_input(
            "Gemini API キー",
            value=default_key,
            type="password",
            help="Google AI Studio (aistudio.google.com/apikey) で取得できます。"
            " 環境変数 GEMINI_API_KEY でも設定可能です。",
        )
        if api_key:
            st.session_state["api_key"] = api_key

        model = st.selectbox("モデル", AVAILABLE_MODELS, index=0)
        temperature = st.slider(
            "創造性 (temperature)",
            min_value=0.0,
            max_value=1.5,
            value=0.7,
            step=0.1,
            help="低いほど堅実・一貫的、高いほど多様・創造的な文章になります。",
        )

        if not api_key:
            st.warning("API キーを入力すると利用できます。")
        st.caption("入力内容は Google の Gemini API に送信されます。")

    return Settings(api_key=api_key, model=model, temperature=temperature)


def run_generation(
    settings: Settings,
    prompt: str,
    *,
    system_instruction: str | None = None,
    output_label: str = "生成結果",
    download_name: str = "output.md",
) -> str | None:
    """プロンプトを実行し、結果をストリーミング表示・ダウンロード可能にする。

    生成テキストを返す（失敗時は None）。
    """
    if not settings.api_key:
        st.error("サイドバーで Gemini API キーを設定してください。")
        return None

    try:
        client = get_client(settings.api_key)
    except GeminiError as e:
        st.error(str(e))
        return None

    st.markdown(f"#### {output_label}")
    placeholder = st.empty()
    collected: list[str] = []

    try:
        for chunk in generate_stream(
            client,
            settings.model,
            prompt,
            system_instruction=system_instruction,
            temperature=settings.temperature,
        ):
            collected.append(chunk)
            placeholder.markdown("".join(collected))
    except GeminiError as e:
        st.error(str(e))
        return None

    text = "".join(collected).strip()
    if not text:
        st.warning("結果が空でした。入力内容を変えて再試行してください。")
        return None

    st.download_button(
        "⬇️ ダウンロード",
        data=text,
        file_name=download_name,
        mime="text/markdown",
    )
    with st.expander("プレーンテキストで表示 / コピー"):
        st.code(text, language=None)
    return text


def tool_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
