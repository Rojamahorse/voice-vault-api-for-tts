# API for TTS (OpenAI-compatible proxy)

This folder provides a small FastAPI proxy that wraps Ultimate TTS Studio's Gradio
endpoint and exposes it as an OpenAI-compatible Text-to-Speech API at
`/v1/audio/speech`. This makes it usable from OpenWebUI without modifying the
Ultimate-TTS-Studio.git folder.

## What this app does
- Starts a local HTTP proxy that translates OpenAI TTS requests into
  `/generate_unified_tts` calls.
- Returns raw audio bytes (`mp3` or `wav`) to the caller.
- Hosts a Voice Manager UI for saving voice samples and engine presets.

## How to use
1. Start Ultimate TTS Studio on this machine and make sure Gradio is running
   (default `http://127.0.0.1:7860/`).
2. In Pinokio, open `api-for-tts.git`, run `Install`, then `Start`.
3. Note the proxy URL shown in the terminal (for example `http://0.0.0.0:3000`).
   Use the LAN IP for remote access, e.g. `http://192.168.0.236:<proxy_port>`.
4. Optional: open the Voice Manager UI at `http://192.168.0.236:<proxy_port>/ui`
   and save voice samples and presets.
5. On the AMD server (OpenWebUI), set the TTS Base URL to:
   `http://192.168.0.236:<proxy_port>/v1`
6. Allow inbound traffic to the proxy port in Windows Firewall on the TTS machine.

Defaults:
- `DEFAULT_TTS_ENGINE` is set to `Chatterbox Turbo`.
- `DEFAULT_FORMAT` is set to `mp3`.
  - The proxy pulls the Gradio defaults for all other parameters.

Optional environment variables (set via `start.js` params):
- `GRADIO_URL` (default: `http://127.0.0.1:7860/`)
- `GRADIO_API_NAME` (default: `/generate_unified_tts`)
- `DEFAULT_TTS_ENGINE` (default: `Chatterbox Turbo`)
- `DEFAULT_FORMAT` (default: `mp3`)
- `CHATTERBOX_TURBO_REF_AUDIO` (optional absolute path to a reference audio file)
- `AUTO_LOAD_ENGINE` (default: `true`, auto-loads the engine via /handle_load_* before synthesis)
- `LOG_LEVEL` (default: `INFO`)

Privacy defaults (set in `start.js`):
- `HF_HUB_DISABLE_TELEMETRY=1`
- `GRADIO_ANALYTICS_ENABLED=False`
- `GRADIO_TELEMETRY=0`

OpenWebUI quick notes:
- Set TTS Base URL to `http://192.168.0.236:<proxy_port>/v1`.
- Set TTS Model to any engine from Ultimate TTS Studio.
- Set Voice to a saved preset name (optional).

## Voice Manager UI
The Voice Manager UI lives at `/ui` on the proxy. It lets you:
- Upload reference audio clips into a local vault.
- Build presets per engine (voice sample + parameter overrides).
- Copy the exact model and voice strings to use in OpenWebUI.

Preset behavior:
- `model` must match the preset engine.
- `voice` should be the preset name.
- Preset params override Gradio defaults, but request `response_format`
  still controls the output file format unless the request omits it.

Local data is stored under `app/data/` (ignored by git).

## API examples

### Curl
```bash
curl -X POST http://192.168.0.236:<proxy_port>/v1/audio/speech ^
  -H "Content-Type: application/json" ^
  -d "{\"input\":\"Hello from OpenWebUI\",\"model\":\"Chatterbox Turbo\",\"voice\":\"matt-chatterbox-turbo\",\"response_format\":\"mp3\"}" ^
  --output out.mp3
```

### JavaScript (Node.js)
```javascript
import fs from "fs";

const res = await fetch("http://192.168.0.236:<proxy_port>/v1/audio/speech", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    input: "Hello from OpenWebUI",
    model: "Chatterbox Turbo",
    voice: "matt-chatterbox-turbo",
    response_format: "mp3"
  })
});

const audio = Buffer.from(await res.arrayBuffer());
fs.writeFileSync("out.mp3", audio);
```

### Python
```python
import requests

resp = requests.post(
    "http://192.168.0.236:<proxy_port>/v1/audio/speech",
    json={
        "input": "Hello from OpenWebUI",
        "model": "Chatterbox Turbo",
        "voice": "matt-chatterbox-turbo",
        "response_format": "mp3",
    },
)
resp.raise_for_status()
with open("out.mp3", "wb") as f:
    f.write(resp.content)
```

---

API Info:

API documentation
http://127.0.0.1:7860/

API Recorder

55 API endpoints


Choose one of the following ways to interact with the API.

1. Install the python client (docs) if you don't already have it installed.

copy
$ pip install gradio_client
2. Find the API endpoint below corresponding to your desired function in the app. Copy the code snippet, replacing the placeholder values with your own input data. Or use the 
API Recorder

 to automatically generate your API requests.

api_name: /handle_load_chatterbox
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_chatterbox"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_20" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_chatterbox
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_chatterbox"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_20" Markdown component.

api_name: /handle_load_chatterbox_multilingual
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_chatterbox_multilingual"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_27" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_chatterbox_multilingual
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_chatterbox_multilingual"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_27" Markdown component.

api_name: /handle_load_chatterbox_turbo
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_chatterbox_turbo"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_34" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_chatterbox_turbo
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_chatterbox_turbo"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_34" Markdown component.

api_name: /handle_load_kokoro
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_kokoro"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_41" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_kokoro
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_kokoro"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_41" Markdown component.

api_name: /handle_load_fish
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_fish"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_48" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_fish
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_fish"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_48" Markdown component.

api_name: /handle_load_indextts
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_indextts"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_55" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_indextts
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_indextts"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_55" Markdown component.

api_name: /handle_load_indextts2
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_indextts2"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_62" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_indextts2
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_indextts2"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_62" Markdown component.

api_name: /handle_indextts2_emotion_mode_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		mode="audio_reference",
		api_name="/handle_indextts2_emotion_mode_change"
)
print(result)
Accepts 1 parameter:
mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "ðŸŽ­ Emotion Control Mode - Choose how to control emotional expression" Radio component.

Returns 1 element
api_name: /handle_speaker_1_emotion_mode_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		mode="audio_reference",
		api_name="/handle_speaker_1_emotion_mode_change"
)
print(result)
Accepts 1 parameter:
mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Emotion Reference Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“ Emotion Description" Textbox component.

api_name: /handle_speaker_2_emotion_mode_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		mode="audio_reference",
		api_name="/handle_speaker_2_emotion_mode_change"
)
print(result)
Accepts 1 parameter:
mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Emotion Reference Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“ Emotion Description" Textbox component.

api_name: /handle_speaker_3_emotion_mode_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		mode="audio_reference",
		api_name="/handle_speaker_3_emotion_mode_change"
)
print(result)
Accepts 1 parameter:
mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Emotion Reference Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“ Emotion Description" Textbox component.

api_name: /handle_speaker_4_emotion_mode_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		mode="audio_reference",
		api_name="/handle_speaker_4_emotion_mode_change"
)
print(result)
Accepts 1 parameter:
mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Emotion Reference Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“ Emotion Description" Textbox component.

api_name: /handle_speaker_5_emotion_mode_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		mode="audio_reference",
		api_name="/handle_speaker_5_emotion_mode_change"
)
print(result)
Accepts 1 parameter:
mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Emotion Reference Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“ Emotion Description" Textbox component.

api_name: /apply_indextts2_emotion_preset
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		preset_name="neutral",
		api_name="/apply_indextts2_emotion_preset"
)
print(result)
Accepts 1 parameter:
preset_name Literal['neutral', 'happy', 'sad', 'angry', 'excited', 'melancholic', 'surprised', 'afraid'] Required

The input value that is provided in the "ðŸŽ­ Emotion Presets - Quick emotion settings" Radio component.

Returns tuple of 8 elements
[0] float

The output value that appears in the "ðŸ˜Š Happy" Slider component.

[1] float

The output value that appears in the "ðŸ˜  Angry" Slider component.

[2] float

The output value that appears in the "ðŸ˜¢ Sad" Slider component.

[3] float

The output value that appears in the "ðŸ˜¨ Afraid" Slider component.

[4] float

The output value that appears in the "ðŸ¤¢ Disgusted" Slider component.

[5] float

The output value that appears in the "ðŸ˜” Melancholic" Slider component.

[6] float

The output value that appears in the "ðŸ˜² Surprised" Slider component.

[7] float

The output value that appears in the "ðŸ˜Œ Calm" Slider component.

api_name: /handle_load_higgs
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_higgs"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_70" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_higgs
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_higgs"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_70" Markdown component.

api_name: /handle_load_voxcpm
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_voxcpm"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_77" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_voxcpm
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_voxcpm"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_77" Markdown component.

api_name: /handle_load_kitten
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_load_kitten"
)
print(result)
Accepts 0 parameters:
Returns tuple of 3 elements
[0] str

The output value that appears in the "value_84" Markdown component.

[1] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_unload_kitten
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_unload_kitten"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_84" Markdown component.

api_name: /update_f5_model_status
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/update_f5_model_status"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_6" Markdown component.

api_name: /handle_f5_download
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		model_name="F5-TTS Base",
		api_name="/handle_f5_download"
)
print(result)
Accepts 1 parameter:
model_name Literal['F5-TTS Base', 'F5-TTS v1 Base', 'F5-TTS French', 'F5-TTS German', 'F5-TTS Japanese', 'F5-TTS Spanish'] Default: "F5-TTS Base"

The input value that is provided in the "ðŸŽ¯ Select Model" Dropdown component.

Returns tuple of 2 elements
[0] str

The output value that appears in the "ðŸ“Š Download Status" Textbox component.

[1] str

The output value that appears in the "value_6" Markdown component.

api_name: /handle_f5_load
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		model_name="F5-TTS Base",
		api_name="/handle_f5_load"
)
print(result)
Accepts 1 parameter:
model_name Literal['F5-TTS Base', 'F5-TTS v1 Base', 'F5-TTS French', 'F5-TTS German', 'F5-TTS Japanese', 'F5-TTS Spanish'] Default: "F5-TTS Base"

The input value that is provided in the "ðŸŽ¯ Select Model" Dropdown component.

Returns tuple of 4 elements
[0] str

The output value that appears in the "ðŸ“Š Download Status" Textbox component.

[1] str

The output value that appears in the "value_6" Markdown component.

[2] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ Select TTS Engine" Radio component.

[3] Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS']

The output value that appears in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

api_name: /handle_f5_unload
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_f5_unload"
)
print(result)
Accepts 0 parameters:
Returns tuple of 2 elements
[0] str

The output value that appears in the "ðŸ“Š Download Status" Textbox component.

[1] str

The output value that appears in the "value_6" Markdown component.

api_name: /handle_clear_temp_files
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_clear_temp_files"
)
print(result)
Accepts 0 parameters:
Returns tuple of 8 elements
[0] str

The output value that appears in the "value_92" Markdown component.

[1] filepath

The output value that appears in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component.

[2] filepath

The output value that appears in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component.

[3] filepath

The output value that appears in the "ðŸŽ¤ Speaker 1 Voice Sample" Audio component.

[4] filepath

The output value that appears in the "ðŸŽ¤ Speaker 2 Voice Sample" Audio component.

[5] filepath

The output value that appears in the "ðŸŽ¤ Speaker 3 Voice Sample" Audio component.

[6] filepath

The output value that appears in the "ðŸŽ¤ Speaker 4 Voice Sample" Audio component.

[7] filepath

The output value that appears in the "ðŸŽ¤ Speaker 5 Voice Sample" Audio component.

api_name: /generate_unified_tts
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		text_input="Hello! This is a demonstration of the ultimate TTS studio. You can choose between Chatterbox TTS. Fish Speech, VoxCPM, Index TTS and Index TTS 2, Higgs audio TTS and F5 TTS for custom voice cloning or Kitten TTS and Kokoro TTS for high-quality pre-trained voices and VibeVoice for podcast.",
		tts_engine="ChatterboxTTS",
		audio_format="wav",
		chatterbox_ref_audio=None,
		chatterbox_exaggeration=0.5,
		chatterbox_temperature=0.8,
		chatterbox_cfg_weight=0.5,
		chatterbox_chunk_size=300,
		chatterbox_seed=0,
		chatterbox_mtl_ref_audio=None,
		chatterbox_mtl_language="en",
		chatterbox_mtl_exaggeration=0.5,
		chatterbox_mtl_temperature=0.8,
		chatterbox_mtl_cfg_weight=0.5,
		chatterbox_mtl_repetition_penalty=2,
		chatterbox_mtl_min_p=0.05,
		chatterbox_mtl_top_p=1,
		chatterbox_mtl_chunk_size=300,
		chatterbox_mtl_seed=0,
		chatterbox_turbo_ref_audio=None,
		chatterbox_turbo_exaggeration=0.5,
		chatterbox_turbo_temperature=0.8,
		chatterbox_turbo_cfg_weight=0.5,
		chatterbox_turbo_repetition_penalty=1.2,
		chatterbox_turbo_min_p=0.05,
		chatterbox_turbo_top_p=1,
		chatterbox_turbo_chunk_size=300,
		chatterbox_turbo_seed=0,
		kokoro_voice="af_heart",
		kokoro_speed=1,
		fish_ref_audio=None,
		fish_ref_text=None,
		fish_temperature=0.8,
		fish_top_p=0.8,
		fish_repetition_penalty=1.1,
		fish_max_tokens=1024,
		fish_seed=None,
		indextts_ref_audio=None,
		indextts_temperature=0.8,
		indextts_seed=None,
		indextts2_ref_audio=None,
		indextts2_emotion_mode="audio_reference",
		indextts2_emotion_audio=None,
		indextts2_emotion_description="Hello!!",
		indextts2_emo_alpha=1,
		indextts2_happy=0,
		indextts2_angry=0,
		indextts2_sad=0,
		indextts2_afraid=0,
		indextts2_disgusted=0,
		indextts2_melancholic=0,
		indextts2_surprised=0,
		indextts2_calm=1,
		indextts2_temperature=0.8,
		indextts2_top_p=0.9,
		indextts2_top_k=50,
		indextts2_repetition_penalty=1.1,
		indextts2_max_mel_tokens=1500,
		indextts2_seed=None,
		indextts2_use_random=False,
		f5_ref_audio=None,
		f5_ref_text=None,
		f5_speed=1,
		f5_cross_fade=0.15,
		f5_remove_silence=False,
		f5_seed=0,
		higgs_ref_audio=None,
		higgs_ref_text=None,
		higgs_voice_preset="EMPTY",
		higgs_system_prompt="Hello!!",
		higgs_temperature=1,
		higgs_top_p=0.95,
		higgs_top_k=50,
		higgs_max_tokens=1024,
		higgs_ras_win_len=7,
		higgs_ras_win_max_num_repeat=2,
		kitten_voice="expr-voice-2-f",
		voxcpm_ref_audio=None,
		voxcpm_ref_text=None,
		voxcpm_cfg_value=2,
		voxcpm_inference_timesteps=10,
		voxcpm_normalize=True,
		voxcpm_denoise=True,
		voxcpm_retry_badcase=True,
		voxcpm_retry_badcase_max_times=3,
		voxcpm_retry_badcase_ratio_threshold=6,
		voxcpm_seed=-1,
		gain_db=0,
		enable_eq=False,
		eq_bass=0,
		eq_mid=0,
		eq_treble=0,
		enable_reverb=False,
		reverb_room=0.3,
		reverb_damping=0.5,
		reverb_wet=0.3,
		enable_echo=False,
		echo_delay=0.3,
		echo_decay=0.5,
		enable_pitch=False,
		pitch_semitones=0,
		api_name="/generate_unified_tts"
)
print(result)
Accepts 101 parameters:
text_input str Default: "Hello! This is a demonstration of the ultimate TTS studio. You can choose between Chatterbox TTS. Fish Speech, VoxCPM, Index TTS and Index TTS 2, Higgs audio TTS and F5 TTS for custom voice cloning or Kitten TTS and Kokoro TTS for high-quality pre-trained voices and VibeVoice for podcast."

The input value that is provided in the "ðŸ“ Text to synthesize" Textbox component.

tts_engine Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ Select TTS Engine" Radio component.

audio_format Literal['wav', 'mp3'] Default: "wav"

The input value that is provided in the "ðŸŽµ Audio Output Format" Radio component.

chatterbox_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

chatterbox_exaggeration float Default: 0.5

The input value that is provided in the "ðŸŽ­ Exaggeration" Slider component.

chatterbox_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

chatterbox_cfg_weight float Default: 0.5

The input value that is provided in the "âš¡ CFG Weight" Slider component.

chatterbox_chunk_size float Default: 300

The input value that is provided in the "ðŸ“„ Chunk Size" Slider component.

chatterbox_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

chatterbox_mtl_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

chatterbox_mtl_language Literal['ar', 'zh', 'da', 'nl', 'en', 'fi', 'fr', 'de', 'el', 'he', 'hi', 'it', 'ja', 'ko', 'ms', 'no', 'pl', 'pt', 'ru', 'es', 'sw', 'sv', 'tr'] Default: "en"

The input value that is provided in the "Select target language" Radio component.

chatterbox_mtl_exaggeration float Default: 0.5

The input value that is provided in the "ðŸŽ­ Exaggeration" Slider component.

chatterbox_mtl_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

chatterbox_mtl_cfg_weight float Default: 0.5

The input value that is provided in the "âš¡ CFG Weight" Slider component.

chatterbox_mtl_repetition_penalty float Default: 2

The input value that is provided in the "ðŸ” Repetition Penalty" Slider component.

chatterbox_mtl_min_p float Default: 0.05

The input value that is provided in the "ðŸ“Š Min P" Slider component.

chatterbox_mtl_top_p float Default: 1

The input value that is provided in the "ðŸŽ¯ Top P" Slider component.

chatterbox_mtl_chunk_size float Default: 300

The input value that is provided in the "ðŸ“„ Chunk Size" Slider component.

chatterbox_mtl_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

chatterbox_turbo_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

chatterbox_turbo_exaggeration float Default: 0.5

The input value that is provided in the "ðŸŽ­ Exaggeration" Slider component.

chatterbox_turbo_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

chatterbox_turbo_cfg_weight float Default: 0.5

The input value that is provided in the "âš¡ CFG Weight" Slider component.

chatterbox_turbo_repetition_penalty float Default: 1.2

The input value that is provided in the "ðŸ” Repetition Penalty" Slider component.

chatterbox_turbo_min_p float Default: 0.05

The input value that is provided in the "ðŸ“Š Min P" Slider component.

chatterbox_turbo_top_p float Default: 1

The input value that is provided in the "ðŸŽ¯ Top P" Slider component.

chatterbox_turbo_chunk_size float Default: 300

The input value that is provided in the "ðŸ“„ Chunk Size" Slider component.

chatterbox_turbo_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

kokoro_voice Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "af_heart"

The input value that is provided in the "" Radio component.

kokoro_speed float Default: 1

The input value that is provided in the "âš¡ Speech Speed" Slider component.

fish_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

fish_ref_text str | None Default: None

The input value that is provided in the "ðŸ—£ï¸ Reference Text (Optional)" Textbox component.

fish_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

fish_top_p float Default: 0.8

The input value that is provided in the "ðŸŽ­ Top P" Slider component.

fish_repetition_penalty float Default: 1.1

The input value that is provided in the "ðŸ”„ Repetition Penalty" Slider component.

fish_max_tokens float Default: 1024

The input value that is provided in the "ðŸ”¢ Max Tokens" Slider component.

fish_seed float | None Default: None

The input value that is provided in the "ðŸŽ² Seed (None=random)" Number component.

indextts_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

indextts_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

indextts_seed float | None Default: None

The input value that is provided in the "ðŸŽ² Seed" Number component.

indextts2_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio (Required) - Voice to clone (max 15s for optimal performance)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

indextts2_emotion_mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "ðŸŽ­ Emotion Control Mode - Choose how to control emotional expression" Radio component.

indextts2_emotion_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ­ Emotion Reference Audio - Audio expressing the desired emotion" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

indextts2_emotion_description str Required

The input value that is provided in the "ðŸ“ Emotion Description - Describe the desired emotion in natural language" Textbox component.

indextts2_emo_alpha float Default: 1

The input value that is provided in the "ðŸŽšï¸ Emotion Strength - Blend between speaker voice and emotion reference" Slider component.

indextts2_happy float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

indextts2_angry float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

indextts2_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

indextts2_afraid float Default: 0

The input value that is provided in the "ðŸ˜¨ Afraid" Slider component.

indextts2_disgusted float Default: 0

The input value that is provided in the "ðŸ¤¢ Disgusted" Slider component.

indextts2_melancholic float Default: 0

The input value that is provided in the "ðŸ˜” Melancholic" Slider component.

indextts2_surprised float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

indextts2_calm float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

indextts2_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature - Controls randomness in generation" Slider component.

indextts2_top_p float Default: 0.9

The input value that is provided in the "ðŸŽ¯ Top-p - Nucleus sampling parameter" Slider component.

indextts2_top_k float Default: 50

The input value that is provided in the "ðŸ” Top-k - Top-k sampling parameter" Slider component.

indextts2_repetition_penalty float Default: 1.1

The input value that is provided in the "ðŸ”„ Repetition Penalty - Penalty for repetitive content" Slider component.

indextts2_max_mel_tokens float Default: 1500

The input value that is provided in the "ðŸ“ Max Mel Tokens - Maximum length of generated audio" Slider component.

indextts2_seed float | None Default: None

The input value that is provided in the "ðŸŽ² Seed - Set seed for reproducible results" Number component.

indextts2_use_random bool Default: False

The input value that is provided in the "ðŸŽ² Random Sampling - Enable random sampling for variation" Checkbox component.

f5_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

f5_ref_text str | None Default: None

The input value that is provided in the "ðŸ“ Reference Text (Optional)" Textbox component.

f5_speed float Default: 1

The input value that is provided in the "âš¡ Speed" Slider component.

f5_cross_fade float Default: 0.15

The input value that is provided in the "ðŸ”„ Cross-fade Duration" Slider component.

f5_remove_silence bool Default: False

The input value that is provided in the "ðŸ”‡ Remove Silence" Checkbox component.

f5_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

higgs_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

higgs_ref_text str | None Default: None

The input value that is provided in the "ðŸ“ Reference Text (Optional)" Textbox component.

higgs_voice_preset Literal['EMPTY', 'broom_salesman', 'chadwick', 'en_man', 'en_woman', 'mabel', 'vex', 'zh_man_sichuan', 'EMPTY'] Default: "EMPTY"

The input value that is provided in the "ðŸ—£ï¸ Voice Preset" Dropdown component.

higgs_system_prompt str Required

The input value that is provided in the "ðŸ’¬ System Prompt (Optional)" Textbox component.

higgs_temperature float Default: 1

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

higgs_top_p float Default: 0.95

The input value that is provided in the "ðŸŽ¯ Top-P" Slider component.

higgs_top_k float Default: 50

The input value that is provided in the "ðŸ” Top-K" Slider component.

higgs_max_tokens float Default: 1024

The input value that is provided in the "ðŸ“ Max Tokens" Slider component.

higgs_ras_win_len float Default: 7

The input value that is provided in the "ðŸªŸ RAS Window Length" Slider component.

higgs_ras_win_max_num_repeat float Default: 2

The input value that is provided in the "ðŸ”„ RAS Max Repeats" Slider component.

kitten_voice Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-2-f"

The input value that is provided in the "ðŸ—£ï¸ Voice Selection" Radio component.

voxcpm_ref_audio filepath | None Default: None

The input value that is provided in the "ðŸŽ¤ Reference Audio (for voice cloning)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

voxcpm_ref_text str | None Default: None

The input value that is provided in the "ðŸ“ Reference Text (auto-transcribed)" Textbox component.

voxcpm_cfg_value float Default: 2

The input value that is provided in the "CFG Value" Slider component.

voxcpm_inference_timesteps float Default: 10

The input value that is provided in the "Inference Timesteps" Slider component.

voxcpm_normalize bool Default: True

The input value that is provided in the "Normalize" Checkbox component.

voxcpm_denoise bool Default: True

The input value that is provided in the "Denoise" Checkbox component.

voxcpm_retry_badcase bool Default: True

The input value that is provided in the "Retry Bad Cases" Checkbox component.

voxcpm_retry_badcase_max_times float Default: 3

The input value that is provided in the "Max Retry Times" Number component.

voxcpm_retry_badcase_ratio_threshold float Default: 6

The input value that is provided in the "Retry Ratio Threshold" Number component.

voxcpm_seed float Default: -1

The input value that is provided in the "Seed" Number component.

gain_db float Default: 0

The input value that is provided in the "ðŸŽšï¸ Master Gain (dB)" Slider component.

enable_eq bool Default: False

The input value that is provided in the "Enable 3-Band EQ" Checkbox component.

eq_bass float Default: 0

The input value that is provided in the "ðŸ”ˆ Bass" Slider component.

eq_mid float Default: 0

The input value that is provided in the "ðŸ”‰ Mid" Slider component.

eq_treble float Default: 0

The input value that is provided in the "ðŸ”Š Treble" Slider component.

enable_reverb bool Default: False

The input value that is provided in the "Enable Reverb" Checkbox component.

reverb_room float Default: 0.3

The input value that is provided in the "Room Size" Slider component.

reverb_damping float Default: 0.5

The input value that is provided in the "Damping" Slider component.

reverb_wet float Default: 0.3

The input value that is provided in the "Wet Mix" Slider component.

enable_echo bool Default: False

The input value that is provided in the "Enable Echo" Checkbox component.

echo_delay float Default: 0.3

The input value that is provided in the "Delay Time (s)" Slider component.

echo_decay float Default: 0.5

The input value that is provided in the "Decay Amount" Slider component.

enable_pitch bool Default: False

The input value that is provided in the "Enable Pitch Shift" Checkbox component.

pitch_semitones float Default: 0

The input value that is provided in the "Pitch (semitones)" Slider component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Generated Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“Š Status" Textbox component.

api_name: /handle_analyze_script
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		script_text="Hello!!",
		selected_engine="ChatterboxTTS",
		api_name="/handle_analyze_script"
)
print(result)
Accepts 2 parameters:
script_text str Required

The input value that is provided in the "ðŸ“ Conversation Script" Textbox component.

selected_engine Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ Select TTS Engine" Radio component.

Returns tuple of 6 elements
[0] str

The output value that appears in the "ðŸ” Detected Speakers" Textbox component.

[1] filepath

The output value that appears in the "ðŸŽ¤ Speaker 1 Voice Sample" Audio component.

[2] filepath

The output value that appears in the "ðŸŽ¤ Speaker 2 Voice Sample" Audio component.

[3] filepath

The output value that appears in the "ðŸŽ¤ Speaker 3 Voice Sample" Audio component.

[4] filepath

The output value that appears in the "ðŸŽ¤ Speaker 4 Voice Sample" Audio component.

[5] filepath

The output value that appears in the "ðŸŽ¤ Speaker 5 Voice Sample" Audio component.

api_name: /handle_example_script
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		selected_engine="ChatterboxTTS",
		api_name="/handle_example_script"
)
print(result)
Accepts 1 parameter:
selected_engine Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ Select TTS Engine" Radio component.

Returns tuple of 7 elements
[0] str

The output value that appears in the "ðŸ“ Conversation Script" Textbox component.

[1] str

The output value that appears in the "ðŸ” Detected Speakers" Textbox component.

[2] filepath

The output value that appears in the "ðŸŽ¤ Speaker 1 Voice Sample" Audio component.

[3] filepath

The output value that appears in the "ðŸŽ¤ Speaker 2 Voice Sample" Audio component.

[4] filepath

The output value that appears in the "ðŸŽ¤ Speaker 3 Voice Sample" Audio component.

[5] filepath

The output value that appears in the "ðŸŽ¤ Speaker 4 Voice Sample" Audio component.

[6] filepath

The output value that appears in the "ðŸŽ¤ Speaker 5 Voice Sample" Audio component.

api_name: /handle_clear_script
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_clear_script"
)
print(result)
Accepts 0 parameters:
Returns tuple of 7 elements
[0] str

The output value that appears in the "ðŸ“ Conversation Script" Textbox component.

[1] str

The output value that appears in the "ðŸ” Detected Speakers" Textbox component.

[2] filepath

The output value that appears in the "ðŸŽ¤ Speaker 1 Voice Sample" Audio component.

[3] filepath

The output value that appears in the "ðŸŽ¤ Speaker 2 Voice Sample" Audio component.

[4] filepath

The output value that appears in the "ðŸŽ¤ Speaker 3 Voice Sample" Audio component.

[5] filepath

The output value that appears in the "ðŸŽ¤ Speaker 4 Voice Sample" Audio component.

[6] filepath

The output value that appears in the "ðŸŽ¤ Speaker 5 Voice Sample" Audio component.

api_name: /lambda
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		script="Hello!!",
		pause=0.8,
		trans_pause=0.3,
		audio_fmt="wav",
		s1=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		s2=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		s3=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		s4=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		s5=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		kv1="af_heart",
		kv2="am_adam",
		kv3="bf_emma",
		kv4="bm_lewis",
		kv5="af_sarah",
		ktv1="expr-voice-2-f",
		ktv2="expr-voice-2-m",
		ktv3="expr-voice-3-f",
		ktv4="expr-voice-3-m",
		ktv5="expr-voice-4-f",
		engine="ChatterboxTTS",
		em1="audio_reference",
		ea1=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		ed1="Hello!!",
		h1=0,
		s1_sad=0,
		a1=0,
		af1=0,
		su1=0,
		c1=1,
		em2="audio_reference",
		ea2=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		ed2="Hello!!",
		h2=0,
		s2_sad=0,
		a2=0,
		af2=0,
		su2=0,
		c2=1,
		em3="audio_reference",
		ea3=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		ed3="Hello!!",
		h3=0,
		s3_sad=0,
		a3=0,
		af3=0,
		su3=0,
		c3=1,
		em4="audio_reference",
		ea4=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		ed4="Hello!!",
		h4=0,
		s4_sad=0,
		a4=0,
		af4=0,
		su4=0,
		c4=1,
		em5="audio_reference",
		ea5=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		ed5="Hello!!",
		h5=0,
		s5_sad=0,
		a5=0,
		af5=0,
		su5=0,
		c5=1,
		api_name="/lambda"
)
print(result)
Accepts 65 parameters:
script str Required

The input value that is provided in the "ðŸ“ Conversation Script" Textbox component.

pause float Default: 0.8

The input value that is provided in the "ðŸ”‡ Speaker Change Pause (s)" Slider component.

trans_pause float Default: 0.3

The input value that is provided in the "â¸ï¸ Same Speaker Pause (s)" Slider component.

audio_fmt Literal['wav', 'mp3'] Default: "wav"

The input value that is provided in the "ðŸŽµ Audio Output Format" Radio component.

s1 filepath Required

The input value that is provided in the "ðŸŽ¤ Speaker 1 Voice Sample" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

s2 filepath Required

The input value that is provided in the "ðŸŽ¤ Speaker 2 Voice Sample" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

s3 filepath Required

The input value that is provided in the "ðŸŽ¤ Speaker 3 Voice Sample" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

s4 filepath Required

The input value that is provided in the "ðŸŽ¤ Speaker 4 Voice Sample" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

s5 filepath Required

The input value that is provided in the "ðŸŽ¤ Speaker 5 Voice Sample" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

kv1 Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "af_heart"

The input value that is provided in the "" Radio component.

kv2 Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "am_adam"

The input value that is provided in the "" Radio component.

kv3 Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "bf_emma"

The input value that is provided in the "" Radio component.

kv4 Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "bm_lewis"

The input value that is provided in the "" Radio component.

kv5 Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "af_sarah"

The input value that is provided in the "" Radio component.

ktv1 Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-2-f"

The input value that is provided in the "" Radio component.

ktv2 Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-2-m"

The input value that is provided in the "" Radio component.

ktv3 Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-3-f"

The input value that is provided in the "" Radio component.

ktv4 Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-3-m"

The input value that is provided in the "" Radio component.

ktv5 Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-4-f"

The input value that is provided in the "" Radio component.

engine Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ Select TTS Engine" Radio component.

em1 Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

ea1 filepath Required

The input value that is provided in the "ðŸŽµ Emotion Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

ed1 str Required

The input value that is provided in the "ðŸ“ Emotion Description" Textbox component.

h1 float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

s1_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

a1 float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

af1 float Default: 0

The input value that is provided in the "ðŸ˜¨ Afraid" Slider component.

su1 float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

c1 float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

em2 Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

ea2 filepath Required

The input value that is provided in the "ðŸŽµ Emotion Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

ed2 str Required

The input value that is provided in the "ðŸ“ Emotion Description" Textbox component.

h2 float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

s2_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

a2 float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

af2 float Default: 0

The input value that is provided in the " 28 Afraid" Slider component.

su2 float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

c2 float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

em3 Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

ea3 filepath Required

The input value that is provided in the "ðŸŽµ Emotion Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

ed3 str Required

The input value that is provided in the "ðŸ“ Emotion Description" Textbox component.

h3 float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

s3_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

a3 float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

af3 float Default: 0

The input value that is provided in the "ðŸ˜¨ Afraid" Slider component.

su3 float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

c3 float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

em4 Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

ea4 filepath Required

The input value that is provided in the "ðŸŽµ Emotion Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

ed4 str Required

The input value that is provided in the "ðŸ“ Emotion Description" Textbox component.

h4 float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

s4_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

a4 float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

af4 float Default: 0

The input value that is provided in the "ðŸ˜¨ Afraid" Slider component.

su4 float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

c4 float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

em5 Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "Emotion Control Mode" Radio component.

ea5 filepath Required

The input value that is provided in the "ðŸŽµ Emotion Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

ed5 str Required

The input value that is provided in the "ðŸ“ Emotion Description" Textbox component.

h5 float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

s5_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

a5 float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

af5 float Default: 0

The input value that is provided in the "ðŸ˜¨ Afraid" Slider component.

su5 float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

c5 float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽµ Generated Audio" Audio component.

[1] str

The output value that appears in the "ðŸ“Š Conversation Summary" Textbox component.

api_name: /handle_voxcpm_transcription
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		audio_path=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		api_name="/handle_voxcpm_transcription"
)
print(result)
Accepts 1 parameter:
audio_path filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio (for voice cloning)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

Returns 1 element
str

The output value that appears in the "ðŸ“ Reference Text (auto-transcribed)" Textbox component.

api_name: /handle_tts_engine_change
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		selected_engine="ChatterboxTTS",
		api_name="/handle_tts_engine_change"
)
print(result)
Accepts 1 parameter:
selected_engine Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ Select TTS Engine" Radio component.

Returns tuple of 4 elements
[0] str

The output value that appears in the "ðŸ“Š Conversation Summary" Textbox component.

[1] str

The output value that appears in the "ðŸ“ Conversation Script" Textbox component.

[2] float

The output value that appears in the "ðŸ”‡ Speaker Change Pause (s)" Slider component.

[3] float

The output value that appears in the "â¸ï¸ Same Speaker Pause (s)" Slider component.

api_name: /switch_engine_tab
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		selected_engine="ChatterboxTTS",
		api_name="/switch_engine_tab"
)
print(result)
Accepts 1 parameter:
selected_engine Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'VoxCPM', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ Select TTS Engine" Radio component.

Returns 1 element
api_name: /handle_ebook_analysis
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		file_path=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf'),
		api_name="/handle_ebook_analysis"
)
print(result)
Accepts 1 parameter:
file_path filepath Required

The input value that is provided in the "ðŸ“ Upload eBook File" File component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

Returns tuple of 2 elements
[0] str

The output value that appears in the "value_283" Markdown component.

[1] list[Literal[]]

The output value that appears in the "ðŸ“‹ Select Chapters to Convert (leave empty for all)" Checkboxgroup component.

api_name: /handle_ebook_conversion
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		file_path=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf'),
		tts_engine_choice="ChatterboxTTS",
		selected_chapters=[],
		chunk_length=500,
		ebook_format="wav",
		cb_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		cb_exag=0.5,
		cb_temp=0.8,
		cb_cfg=0.5,
		cb_seed=0,
		cb_mtl_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		cb_mtl_lang="en",
		cb_mtl_exag=0.5,
		cb_mtl_temp=0.8,
		cb_mtl_cfg=0.5,
		cb_mtl_rep_pen=2,
		cb_mtl_min_p=0.05,
		cb_mtl_top_p=1,
		cb_mtl_seed=0,
		cb_turbo_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		cb_turbo_exag=0.5,
		cb_turbo_temp=0.8,
		cb_turbo_cfg=0.5,
		cb_turbo_rep_pen=1.2,
		cb_turbo_min_p=0.05,
		cb_turbo_top_p=1,
		cb_turbo_seed=0,
		kok_voice="af_heart",
		kok_speed=1,
		fish_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		fish_ref_text="Hello!!",
		fish_temp=0.8,
		fish_top_p=0.8,
		fish_rep_pen=1.1,
		fish_max_tok=1024,
		fish_seed_val=3,
		idx_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		idx_temp=0.8,
		idx_seed=3,
		indextts2_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		indextts2_emotion_mode="audio_reference",
		indextts2_emotion_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		indextts2_emotion_description="Hello!!",
		indextts2_emo_alpha=1,
		indextts2_happy=0,
		indextts2_angry=0,
		indextts2_sad=0,
		indextts2_afraid=0,
		indextts2_disgusted=0,
		indextts2_melancholic=0,
		indextts2_surprised=0,
		indextts2_calm=1,
		indextts2_temperature=0.8,
		indextts2_top_p=0.9,
		indextts2_top_k=50,
		indextts2_repetition_penalty=1.1,
		indextts2_max_mel_tokens=1500,
		indextts2_seed=3,
		indextts2_use_random=False,
		f5_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		f5_ref_text="Hello!!",
		f5_speed=1,
		f5_cross_fade=0.15,
		f5_remove_silence=False,
		f5_seed_val=0,
		higgs_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		higgs_ref_text="Hello!!",
		higgs_voice_preset="EMPTY",
		higgs_system_prompt="Hello!!",
		higgs_temperature=1,
		higgs_top_p=0.95,
		higgs_top_k=50,
		higgs_max_tokens=1024,
		higgs_ras_win_len=7,
		higgs_ras_win_max_num_repeat=2,
		kitten_voice_param="expr-voice-2-f",
		voxcpm_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		voxcpm_ref_text="Hello!!",
		voxcpm_cfg_value=2,
		voxcpm_inference_timesteps=10,
		voxcpm_normalize=True,
		voxcpm_denoise=True,
		voxcpm_retry_badcase=True,
		voxcpm_retry_badcase_max_times=3,
		voxcpm_retry_badcase_ratio_threshold=6,
		voxcpm_seed=-1,
		gain=0,
		eq_en=False,
		eq_b=0,
		eq_m=0,
		eq_t=0,
		rev_en=False,
		rev_room=0.3,
		rev_damp=0.5,
		rev_wet=0.3,
		echo_en=False,
		echo_del=0.3,
		echo_dec=0.5,
		pitch_en=False,
		pitch_semi=0,
		chunk_gap=1,
		chapter_gap=2,
		api_name="/handle_ebook_conversion"
)
print(result)
Accepts 102 parameters:
file_path filepath Required

The input value that is provided in the "ðŸ“ Upload eBook File" File component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

tts_engine_choice Literal['ChatterboxTTS', 'Chatterbox Multilingual', 'Chatterbox Turbo', 'Kokoro TTS', 'Fish Speech', 'IndexTTS', 'IndexTTS2', 'F5-TTS', 'Higgs Audio', 'KittenTTS'] Default: "ChatterboxTTS"

The input value that is provided in the "ðŸŽ¯ TTS Engine for Audiobook" Radio component.

selected_chapters list[Literal[]] Default: []

The input value that is provided in the "ðŸ“‹ Select Chapters to Convert (leave empty for all)" Checkboxgroup component.

chunk_length float Default: 500

The input value that is provided in the "ðŸ“„ Text Chunk Length" Slider component.

ebook_format Literal['wav', 'mp3'] Default: "wav"

The input value that is provided in the "ðŸŽµ Audiobook Format" Radio component.

cb_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

cb_exag float Default: 0.5

The input value that is provided in the "ðŸŽ­ Exaggeration" Slider component.

cb_temp float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

cb_cfg float Default: 0.5

The input value that is provided in the "âš¡ CFG Weight" Slider component.

cb_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

cb_mtl_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

cb_mtl_lang Literal['ar', 'zh', 'da', 'nl', 'en', 'fi', 'fr', 'de', 'el', 'he', 'hi', 'it', 'ja', 'ko', 'ms', 'no', 'pl', 'pt', 'ru', 'es', 'sw', 'sv', 'tr'] Default: "en"

The input value that is provided in the "Select target language" Radio component.

cb_mtl_exag float Default: 0.5

The input value that is provided in the "ðŸŽ­ Exaggeration" Slider component.

cb_mtl_temp float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

cb_mtl_cfg float Default: 0.5

The input value that is provided in the "âš¡ CFG Weight" Slider component.

cb_mtl_rep_pen float Default: 2

The input value that is provided in the "ðŸ” Repetition Penalty" Slider component.

cb_mtl_min_p float Default: 0.05

The input value that is provided in the "ðŸ“Š Min P" Slider component.

cb_mtl_top_p float Default: 1

The input value that is provided in the "ðŸŽ¯ Top P" Slider component.

cb_mtl_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

cb_turbo_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

cb_turbo_exag float Default: 0.5

The input value that is provided in the "ðŸŽ­ Exaggeration" Slider component.

cb_turbo_temp float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

cb_turbo_cfg float Default: 0.5

The input value that is provided in the "âš¡ CFG Weight" Slider component.

cb_turbo_rep_pen float Default: 1.2

The input value that is provided in the "ðŸ” Repetition Penalty" Slider component.

cb_turbo_min_p float Default: 0.05

The input value that is provided in the "ðŸ“Š Min P" Slider component.

cb_turbo_top_p float Default: 1

The input value that is provided in the "ðŸŽ¯ Top P" Slider component.

cb_turbo_seed float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

kok_voice Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "af_heart"

The input value that is provided in the "" Radio component.

kok_speed float Default: 1

The input value that is provided in the "âš¡ Speech Speed" Slider component.

fish_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

fish_ref_text str Required

The input value that is provided in the "ðŸ—£ï¸ Reference Text (Optional)" Textbox component.

fish_temp float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

fish_top_p float Default: 0.8

The input value that is provided in the "ðŸŽ­ Top P" Slider component.

fish_rep_pen float Default: 1.1

The input value that is provided in the "ðŸ”„ Repetition Penalty" Slider component.

fish_max_tok float Default: 1024

The input value that is provided in the "ðŸ”¢ Max Tokens" Slider component.

fish_seed_val float Required

The input value that is provided in the "ðŸŽ² Seed (None=random)" Number component.

idx_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

idx_temp float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

idx_seed float Required

The input value that is provided in the "ðŸŽ² Seed" Number component.

indextts2_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio (Required) - Voice to clone (max 15s for optimal performance)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

indextts2_emotion_mode Literal['audio_reference', 'vector_control', 'text_description'] Default: "audio_reference"

The input value that is provided in the "ðŸŽ­ Emotion Control Mode - Choose how to control emotional expression" Radio component.

indextts2_emotion_audio filepath Required

The input value that is provided in the "ðŸŽ­ Emotion Reference Audio - Audio expressing the desired emotion" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

indextts2_emotion_description str Required

The input value that is provided in the "ðŸ“ Emotion Description - Describe the desired emotion in natural language" Textbox component.

indextts2_emo_alpha float Default: 1

The input value that is provided in the "ðŸŽšï¸ Emotion Strength - Blend between speaker voice and emotion reference" Slider component.

indextts2_happy float Default: 0

The input value that is provided in the "ðŸ˜Š Happy" Slider component.

indextts2_angry float Default: 0

The input value that is provided in the "ðŸ˜  Angry" Slider component.

indextts2_sad float Default: 0

The input value that is provided in the "ðŸ˜¢ Sad" Slider component.

indextts2_afraid float Default: 0

The input value that is provided in the "ðŸ˜¨ Afraid" Slider component.

indextts2_disgusted float Default: 0

The input value that is provided in the "ðŸ¤¢ Disgusted" Slider component.

indextts2_melancholic float Default: 0

The input value that is provided in the "ðŸ˜” Melancholic" Slider component.

indextts2_surprised float Default: 0

The input value that is provided in the "ðŸ˜² Surprised" Slider component.

indextts2_calm float Default: 1

The input value that is provided in the "ðŸ˜Œ Calm" Slider component.

indextts2_temperature float Default: 0.8

The input value that is provided in the "ðŸŒ¡ï¸ Temperature - Controls randomness in generation" Slider component.

indextts2_top_p float Default: 0.9

The input value that is provided in the "ðŸŽ¯ Top-p - Nucleus sampling parameter" Slider component.

indextts2_top_k float Default: 50

The input value that is provided in the "ðŸ” Top-k - Top-k sampling parameter" Slider component.

indextts2_repetition_penalty float Default: 1.1

The input value that is provided in the "ðŸ”„ Repetition Penalty - Penalty for repetitive content" Slider component.

indextts2_max_mel_tokens float Default: 1500

The input value that is provided in the "ðŸ“ Max Mel Tokens - Maximum length of generated audio" Slider component.

indextts2_seed float Required

The input value that is provided in the "ðŸŽ² Seed - Set seed for reproducible results" Number component.

indextts2_use_random bool Default: False

The input value that is provided in the "ðŸŽ² Random Sampling - Enable random sampling for variation" Checkbox component.

f5_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

f5_ref_text str Required

The input value that is provided in the "ðŸ“ Reference Text (Optional)" Textbox component.

f5_speed float Default: 1

The input value that is provided in the "âš¡ Speed" Slider component.

f5_cross_fade float Default: 0.15

The input value that is provided in the "ðŸ”„ Cross-fade Duration" Slider component.

f5_remove_silence bool Default: False

The input value that is provided in the "ðŸ”‡ Remove Silence" Checkbox component.

f5_seed_val float Default: 0

The input value that is provided in the "ðŸŽ² Seed (0=random)" Number component.

higgs_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

higgs_ref_text str Required

The input value that is provided in the "ðŸ“ Reference Text (Optional)" Textbox component.

higgs_voice_preset Literal['EMPTY', 'broom_salesman', 'chadwick', 'en_man', 'en_woman', 'mabel', 'vex', 'zh_man_sichuan', 'EMPTY'] Default: "EMPTY"

The input value that is provided in the "ðŸ—£ï¸ Voice Preset" Dropdown component.

higgs_system_prompt str Required

The input value that is provided in the "ðŸ’¬ System Prompt (Optional)" Textbox component.

higgs_temperature float Default: 1

The input value that is provided in the "ðŸŒ¡ï¸ Temperature" Slider component.

higgs_top_p float Default: 0.95

The input value that is provided in the "ðŸŽ¯ Top-P" Slider component.

higgs_top_k float Default: 50

The input value that is provided in the "ðŸ” Top-K" Slider component.

higgs_max_tokens float Default: 1024

The input value that is provided in the "ðŸ“ Max Tokens" Slider component.

higgs_ras_win_len float Default: 7

The input value that is provided in the "ðŸªŸ RAS Window Length" Slider component.

higgs_ras_win_max_num_repeat float Default: 2

The input value that is provided in the "ðŸ”„ RAS Max Repeats" Slider component.

kitten_voice_param Literal['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'] Default: "expr-voice-2-f"

The input value that is provided in the "ðŸ—£ï¸ Voice Selection" Radio component.

voxcpm_ref_audio filepath Required

The input value that is provided in the "ðŸŽ¤ Reference Audio (for voice cloning)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

voxcpm_ref_text str Required

The input value that is provided in the "ðŸ“ Reference Text (auto-transcribed)" Textbox component.

voxcpm_cfg_value float Default: 2

The input value that is provided in the "CFG Value" Slider component.

voxcpm_inference_timesteps float Default: 10

The input value that is provided in the "Inference Timesteps" Slider component.

voxcpm_normalize bool Default: True

The input value that is provided in the "Normalize" Checkbox component.

voxcpm_denoise bool Default: True

The input value that is provided in the "Denoise" Checkbox component.

voxcpm_retry_badcase bool Default: True

The input value that is provided in the "Retry Bad Cases" Checkbox component.

voxcpm_retry_badcase_max_times float Default: 3

The input value that is provided in the "Max Retry Times" Number component.

voxcpm_retry_badcase_ratio_threshold float Default: 6

The input value that is provided in the "Retry Ratio Threshold" Number component.

voxcpm_seed float Default: -1

The input value that is provided in the "Seed" Number component.

gain float Default: 0

The input value that is provided in the "ðŸŽšï¸ Master Gain (dB)" Slider component.

eq_en bool Default: False

The input value that is provided in the "Enable 3-Band EQ" Checkbox component.

eq_b float Default: 0

The input value that is provided in the "ðŸ”ˆ Bass" Slider component.

eq_m float Default: 0

The input value that is provided in the "ðŸ”‰ Mid" Slider component.

eq_t float Default: 0

The input value that is provided in the "ðŸ”Š Treble" Slider component.

rev_en bool Default: False

The input value that is provided in the "Enable Reverb" Checkbox component.

rev_room float Default: 0.3

The input value that is provided in the "Room Size" Slider component.

rev_damp float Default: 0.5

The input value that is provided in the "Damping" Slider component.

rev_wet float Default: 0.3

The input value that is provided in the "Wet Mix" Slider component.

echo_en bool Default: False

The input value that is provided in the "Enable Echo" Checkbox component.

echo_del float Default: 0.3

The input value that is provided in the "Delay Time (s)" Slider component.

echo_dec float Default: 0.5

The input value that is provided in the "Decay Amount" Slider component.

pitch_en bool Default: False

The input value that is provided in the "Enable Pitch Shift" Checkbox component.

pitch_semi float Default: 0

The input value that is provided in the "Pitch (semitones)" Slider component.

chunk_gap float Default: 1

The input value that is provided in the "ðŸ”‡ Gap Between Chunks (seconds)" Slider component.

chapter_gap float Default: 2

The input value that is provided in the "ðŸ“– Gap Between Chapters (seconds)" Slider component.

Returns tuple of 3 elements
[0] filepath

The output value that appears in the "ðŸŽ§ Generated Audiobook" Audio component.

[1] filepath

The output value that appears in the "ðŸ“¥ Download Large Audiobook" File component.

[2] str

The output value that appears in the "ðŸ“Š eBook Conversion Status" Textbox component.

api_name: /handle_clear_ebook
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_clear_ebook"
)
print(result)
Accepts 0 parameters:
Returns tuple of 6 elements
[0] filepath

The output value that appears in the "ðŸ“ Upload eBook File" File component.

[1] str

The output value that appears in the "value_283" Markdown component.

[2] list[Literal[]]

The output value that appears in the "ðŸ“‹ Select Chapters to Convert (leave empty for all)" Checkboxgroup component.

[3] filepath

The output value that appears in the "ðŸŽ§ Generated Audiobook" Audio component.

[4] filepath

The output value that appears in the "ðŸ“¥ Download Large Audiobook" File component.

[5] str

The output value that appears in the "ðŸ“Š eBook Conversion Status" Textbox component.

api_name: /upload_and_refresh
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		files=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf'),
		voice_name="Hello!!",
		api_name="/upload_and_refresh"
)
print(result)
Accepts 2 parameters:
files filepath Required

The input value that is provided in the "ðŸ“ Upload Voice File (.pt)" File component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

voice_name str Required

The input value that is provided in the "ðŸ‘¤ Custom Voice Name" Textbox component.

Returns tuple of 10 elements
[0] str

The output value that appears in the "ðŸ“Š Upload Status" Textbox component.

[1] dict(headers: list[Any], data: list[list[Any]], metadata: dict(str, list[Any] | None) | None)

The output value that appears in the "value_464" Dataframe component.

[2] str

The output value that appears in the "ðŸ‘¤ Custom Voice Name" Textbox component.

[3] filepath

The output value that appears in the "ðŸ“ Upload Voice File (.pt)" File component.

[4] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[5] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[6] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[7] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[8] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[9] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

api_name: /refresh_kokoro_voice_list
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/refresh_kokoro_voice_list"
)
print(result)
Accepts 0 parameters:
Returns 1 element
Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

api_name: /refresh_all_kokoro_voices
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/refresh_all_kokoro_voices"
)
print(result)
Accepts 0 parameters:
Returns tuple of 5 elements
[0] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[1] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[2] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[3] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

[4] Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola']

The output value that appears in the "" Radio component.

api_name: /get_custom_voice_list
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/get_custom_voice_list"
)
print(result)
Accepts 0 parameters:
Returns 1 element
dict(headers: list[Any], data: list[list[Any]], metadata: dict(str, list[Any] | None) | None)

The output value that appears in the "value_464" Dataframe component.

api_name: /update_speaker_visibility
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		num_speakers=2,
		api_name="/update_speaker_visibility"
)
print(result)
Accepts 1 parameter:
num_speakers float Default: 2

The input value that is provided in the "ðŸŽ¤ Number of Speakers" Slider component.

Returns 1 element
api_name: /handle_vibevoice_load
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		selected_model_path=None,
		path="models/VibeVoice-1.5B",
		use_flash_attention=False,
		api_name="/handle_vibevoice_load"
)
print(result)
Accepts 3 parameters:
selected_model_path Literal[] Required

The input value that is provided in the "ðŸ“¦ Downloaded Models" Radio component.

path str Default: "models/VibeVoice-1.5B"

The input value that is provided in the "ðŸ“ Model Path" Textbox component.

use_flash_attention bool Default: False

The input value that is provided in the "âš¡ Use Flash Attention" Checkbox component.

Returns 1 element
str

The output value that appears in the "value_327" Markdown component.

api_name: /handle_vibevoice_unload
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/handle_vibevoice_unload"
)
print(result)
Accepts 0 parameters:
Returns 1 element
str

The output value that appears in the "value_327" Markdown component.

api_name: /handle_vibevoice_download
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		model_name="VibeVoice-1.5B",
		api_name="/handle_vibevoice_download"
)
print(result)
Accepts 1 parameter:
model_name Literal['VibeVoice-1.5B', 'VibeVoice-Large'] Default: "VibeVoice-1.5B"

The input value that is provided in the "Select Model to Download" Radio component.

Returns 1 element
str

The output value that appears in the "value_332" Markdown component.

api_name: /refresh_vibevoice_voices
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/refresh_vibevoice_voices"
)
print(result)
Accepts 0 parameters:
Returns tuple of 4 elements
[0] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_309" Radio component.

[1] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_312" Radio component.

[2] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_315" Radio component.

[3] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_318" Radio component.

api_name: /refresh_vibevoice_model_list
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		api_name="/refresh_vibevoice_model_list"
)
print(result)
Accepts 0 parameters:
Returns 1 element
Literal[]

The output value that appears in the "ðŸ“¦ Downloaded Models" Radio component.

api_name: /handle_add_custom_voice
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		audio_file=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf'),
		voice_name="Hello!!",
		api_name="/handle_add_custom_voice"
)
print(result)
Accepts 2 parameters:
audio_file filepath Required

The input value that is provided in the "ðŸ“ Upload Voice Sample" File component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

voice_name str Required

The input value that is provided in the "ðŸ·ï¸ Voice Name" Textbox component.

Returns tuple of 6 elements
[0] str

The output value that appears in the "value_351" Markdown component.

[1] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_309" Radio component.

[2] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_312" Radio component.

[3] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_315" Radio component.

[4] Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman']

The output value that appears in the "value_318" Radio component.

[5] str

The output value that appears in the "ðŸ·ï¸ Voice Name" Textbox component.

api_name: /handle_vibevoice_generation
copy
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		num_speakers=2,
		script="Hello!!",
		speaker_1="custom-santa",
		speaker_2="custom-santa",
		speaker_3="custom-santa",
		speaker_4="custom-santa",
		cfg_scale=1.3,
		seed=44,
		audio_format="wav",
		api_name="/handle_vibevoice_generation"
)
print(result)
Accepts 9 parameters:
num_speakers float Default: 2

The input value that is provided in the "ðŸŽ¤ Number of Speakers" Slider component.

script str Required

The input value that is provided in the "ðŸ“ Podcast Script" Textbox component.

speaker_1 Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman'] Required

The input value that is provided in the "parameter_309" Radio component.

speaker_2 Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman'] Required

The input value that is provided in the "parameter_312" Radio component.

speaker_3 Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman'] Required

The input value that is provided in the "parameter_315" Radio component.

speaker_4 Literal['custom-santa', 'en-Alice_woman', 'en-Carter_man', 'en-Frank_man', 'en-Mary_woman_bgm', 'en-Maya_woman', 'in-Samuel_man', 'zh-Anchen_man_bgm', 'zh-Bowen_man', 'zh-Xinran_woman'] Required

The input value that is provided in the "parameter_318" Radio component.

cfg_scale float Default: 1.3

The input value that is provided in the "ðŸŽ›ï¸ CFG Scale" Slider component.

seed float Default: 44

The input value that is provided in the "ðŸŽ² Seed (optional)" Number component.

audio_format Literal['wav', 'mp3'] Default: "wav"

The input value that is provided in the "ðŸŽµ Audio Format" Radio component.

Returns tuple of 2 elements
[0] filepath

The output value that appears in the "ðŸŽ§ Generated Podcast" Audio component.

[1] str

The output value that appears in the "ðŸ“Š Generation Status" Textbox component.
