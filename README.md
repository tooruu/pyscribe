# 🎵 _pyscribe_
A robust tool to transcribe audio (including music) files and URLs into text using **ElevenLabs Scribe** AI model.

## 📋 Requirements
- 64-bit operating system
- Python 3.8+ if not using standalone binary
- ElevenLabs API key

## 🚀 Installation

### Prebuilt standalone binary (Windows, macOS, Linux)
Get a standalone binary from [the latest release](https://github.com/tooruu/pyscribe/releases/latest).

### Run the tool directly with uv
```bash
uvx pyscribest "path/or/url.mp3"
```
### Install from [PyPI](https://pypi.org/project/pyscribest)
```bash
pip install pyscribest
```

## ⚡ Usage

> [!IMPORTANT]
> ### API key configuration
> Log in to your [ElevenLabs dashboard](https://elevenlabs.io/app/developers/api-keys) and create an API key with access to **Speech to Text** endpoint.
>
> The script looks for the API key in the following order:
> 1. `--key` command-line parameter
> 2. `ELEVENLABS_API_KEY` environment variable
> 3. System keyring (automatically saved if you use the `--key` parameter)

### Basic Transcription
Output is always written to `sys.stdout`
```bash
pyscribe "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3"
```
> [!NOTE]
> `python -m pyscribe` is available as an alternative if you installed with pip

### CLI Options
- `--full`: Insert audio event tags like `[laughter]`
- `--lang`: Specify an ISO-639-1 or ISO-639-3 [language code](https://elevenlabs.io/docs/overview/capabilities/speech-to-text#supported-languages) for improved performance, e.g. `de` or `deu` for German
- `--key`: ElevenLabs API key (this will be saved to your keyring for future use)

```bash
pyscribe --lang deu --full video.webm
```

## 🛠 Integration
**_pyscribe_** package provides both synchronous and asynchronous interfaces for seamless integration into any workflow

### Sync
```py
from elevenlabs import ElevenLabs
from pyscribe import transcribe

client = ElevenLabs(api_key="YOUR API KEY")
text = transcribe(client, "path/or/url.mp3")
print(text)
```

### Async
```py
from elevenlabs import AsyncElevenLabs
from pyscribe import atranscribe

client = AsyncElevenLabs(api_key="YOUR API KEY")
text = await atranscribe(client, "path/or/url.mp3")
print(text)
```
