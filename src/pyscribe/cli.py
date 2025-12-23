from __future__ import annotations

import argparse
import os
import sys
from io import TextIOWrapper

from elevenlabs import ElevenLabs

from pyscribe.auth import get_keyring_api_key, set_keyring_api_key
from pyscribe.transcriber import transcribe


class Args(argparse.Namespace):
    path: str
    key: str | None
    lang: str | None
    full: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="pyscribe",
        description="Transcribe music files into lyrics using ElevenLabs Scribe.",
    )
    parser.add_argument(
        "path",
        help="File path or HTTPS URL to transcribe",
    )
    parser.add_argument(
        "--key",
        help="ElevenLabs API key",
        default=os.getenv("ELEVENLABS_API_KEY"),
    )
    parser.add_argument(
        "--lang",
        help="ISO-639-1 or ISO-639-3 language code for better performance",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Insert audio event tags like [laughter]",
    )
    return parser.parse_args(namespace=Args())


def main() -> None:
    if sys.platform == "win32" and isinstance(sys.stdout, TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args()

    api_key = args.key or get_keyring_api_key()

    if not api_key:
        raise ValueError("API key is required. Set ELEVENLABS_API_KEY env var or use --key.")

    client = ElevenLabs(api_key=api_key)
    lyrics = transcribe(client, args.path, args.full, args.lang)
    print(lyrics)

    if args.key:
        set_keyring_api_key(api_key)


if __name__ == "__main__":
    main()
