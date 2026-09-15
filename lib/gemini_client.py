"""Gemini API の薄いラッパー。

新しい google-genai SDK を利用する。
API キーは呼び出し側から明示的に渡す（環境変数 / st.secrets / サイドバー入力）。
"""

from __future__ import annotations

import logging
from typing import Iterator

from google import genai
from google.genai import types
from google.genai.errors import APIError

logger = logging.getLogger("gemini_client")

# サイドバーで選択できるモデル。先頭がデフォルト。
# 2.5系は新規ユーザー向けに提供終了（404 NOT_FOUND、API側で 3.6-flash を案内）したため 3.6系に更新。
AVAILABLE_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


class GeminiError(RuntimeError):
    """UI 側で扱いやすいようにラップした例外。"""


# HTTP ステータス別の、ユーザー向けの短い対処ヒント。
_ERROR_HINTS = {
    400: "API キーが正しいか、入力内容が長すぎないかを確認してください。",
    401: "API キーが正しいか確認してください。",
    403: "API キーの権限、または対象モデルの利用可否を確認してください。",
    404: "指定したモデルが見つかりません。モデル名を確認してください。",
    429: "レート制限に達しました。少し待ってから再試行してください。",
}


def _as_gemini_error(e: APIError) -> "GeminiError":
    """APIError を、画面表示して安全なメッセージに変換する。

    `str(e)` はレスポンス本文（将来 URL・リクエスト詳細を含みうる）を吐くため
    画面には出さず、完全な内容はコンソールログにのみ残す。画面には構造化
    フィールド（HTTP コード・ステータス）と定型ヒントだけを出す。
    """
    logger.warning("Gemini API error: %s", e, exc_info=e)
    code = getattr(e, "code", None)
    status = getattr(e, "status", None) or ""
    label = " ".join(str(x) for x in (code, status) if x) or "詳細不明"
    hint = _ERROR_HINTS.get(code, "キー・ネットワーク・レート制限を確認してください。")
    return GeminiError(f"Gemini API の呼び出しに失敗しました（{label}）。{hint}")


def get_client(api_key: str) -> genai.Client:
    if not api_key:
        raise GeminiError("Gemini API キーが設定されていません。")
    return genai.Client(api_key=api_key)


def _config(system_instruction: str | None, temperature: float) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction or None,
    )


def generate(
    client: genai.Client,
    model: str,
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.7,
) -> str:
    """一括生成。全文を文字列で返す。"""
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=_config(system_instruction, temperature),
        )
    except APIError as e:  # 認証エラー・レート制限など
        raise _as_gemini_error(e) from e
    return response.text or ""


def generate_stream(
    client: genai.Client,
    model: str,
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.7,
) -> Iterator[str]:
    """ストリーミング生成。テキストチャンクを順に yield する。"""
    try:
        stream = client.models.generate_content_stream(
            model=model,
            contents=prompt,
            config=_config(system_instruction, temperature),
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
    except APIError as e:
        raise _as_gemini_error(e) from e
