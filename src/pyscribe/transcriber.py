from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing import TypedDict

    from elevenlabs import AsyncElevenLabs, ElevenLabs, SpeechToTextChunkResponseModel

    class ScribeArgs(TypedDict, total=False):
        model_id: str
        tag_audio_events: bool
        language_code: str


def _prep_convert_args(
    file_uri: str | Path,
    audio_events: bool,
    language: str | None,
) -> tuple[Path | None, ScribeArgs]:
    file = None if isinstance(file_uri, str) and file_uri.startswith("https://") else Path(file_uri)
    if file and not file.is_file():
        raise FileNotFoundError(file)

    kwargs: ScribeArgs = {
        "model_id": "scribe_v1",
        "tag_audio_events": audio_events,
    }
    if language:
        kwargs["language_code"] = language

    return file, kwargs


def transcribe(
    client: ElevenLabs,
    file_uri: str | Path,
    audio_events: bool = False,
    language: str | None = None,
) -> str:
    file, kwargs = _prep_convert_args(file_uri, audio_events, language)
    if not file:
        response = client.speech_to_text.convert(cloud_storage_url=cast(str, file_uri), **kwargs)
        return cast("SpeechToTextChunkResponseModel", response).text

    with file.open("rb") as audio_file:
        response = client.speech_to_text.convert(file=audio_file, **kwargs)
        return cast("SpeechToTextChunkResponseModel", response).text


async def atranscribe(
    client: AsyncElevenLabs,
    file_uri: str | Path,
    audio_events: bool = True,
    language: str | None = None,
) -> str:
    file, kwargs = _prep_convert_args(file_uri, audio_events, language)
    if not file:
        response = await client.speech_to_text.convert(cloud_storage_url=cast(str, file_uri), **kwargs)
        return cast("SpeechToTextChunkResponseModel", response).text

    content = await asyncio.get_running_loop().run_in_executor(None, file.read_bytes)
    response = await client.speech_to_text.convert(file=content, **kwargs)
    return cast("SpeechToTextChunkResponseModel", response).text
