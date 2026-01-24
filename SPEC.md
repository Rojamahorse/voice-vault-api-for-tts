# SPEC: API for TTS (api-for-tts.git)

## Scope
- This spec covers only `F:\pinokio\api\api-for-tts.git` and its subfolders.
- External apps (ex: Ultimate TTS Studio) are dependencies, not part of this scope.

## Summary
Provide a local FastAPI proxy that exposes an OpenAI-compatible TTS API backed by
an Ultimate TTS Studio Gradio endpoint, plus a Voice Manager UI for managing
voice samples and presets.

## Goals
- OpenAI-compatible TTS endpoint at `/v1/audio/speech`.
- Basic discovery endpoints for models and voices.
- Voice and preset management with a local UI at `/ui`.
- No modifications to Ultimate-TTS-Studio app code.
- Minimal configuration via environment variables and `ENVIRONMENT`.

## Non-goals
- Building or modifying TTS model inference.
- Implementing authentication, billing, or rate limiting.
- Building audio editing features beyond the current UI scope.

## User Flows
- As a user, I set a Gradio target URL, load engines, and confirm connectivity.
- As a user, I upload voice samples and build presets tied to engines.
- As a user, I copy model and voice values into clients such as OpenWebUI.

## Architecture
- `app/tts_proxy.py`
  - FastAPI server, OpenAI TTS proxy, Gradio metadata loader.
  - Reads and writes local data under `app/data`.
- `app/ui/index.html`
  - Voice Manager UI for samples, presets, and the cheat sheet.
- `app/data/`
  - `voices.json`, `presets.json`, voice files under `voices/`.
- Root scripts (`install.js`, `start.js`, `reset.js`, `update.js`)
  - Pinokio launcher for install/start/update/reset.

## Configuration
- `ENVIRONMENT` file in project root (Pinokio-managed)
  - `GRADIO_URL` (default: `http://127.0.0.1:7860/`)
  - `GRADIO_API_NAME` (default: `/generate_unified_tts`)
  - `DEFAULT_TTS_ENGINE` (default: `Chatterbox Turbo`)
  - `DEFAULT_FORMAT` (default: `mp3`)
  - `CHATTERBOX_TURBO_REF_AUDIO` (optional absolute path)
  - `AUTO_LOAD_ENGINE` (default: `true`)
  - `LOG_LEVEL` (default: `INFO`)

## Data Model
- Voice
  - `id`, `label`, `filename`, `created_at`
- Preset
  - `name`, `label`, `engine`, `voice_id`, `params`, `updated_at`

## API Surface (local)
- `GET /health` - basic health check.
- `GET /ui` - Voice Manager UI.
- `GET /v1/tts/engines` - supported engines list.
- `GET /v1/tts/params?engine=...` - Gradio params and defaults.
- `GET /v1/tts/gradio` - current Gradio status and URL.
- `POST /v1/tts/gradio` - set Gradio URL.
- `POST /v1/tts/gradio/reload` - reload Gradio metadata.
- `GET /v1/tts/voice-choices?engine=...` - engine-specific voice choices.
- `GET /v1/tts/voices` - list saved voices.
- `GET /v1/tts/api-key` - returns stored API key (blank if unset).
- `POST /v1/tts/api-key/generate` - generates and persists an API key.
- `POST /v1/tts/voices` - create a voice sample.
- `DELETE /v1/tts/voices/{voice_id}` - delete a voice sample.
- `GET /v1/tts/presets` - list presets.
- `GET /v1/tts/presets/{preset_name}` - get preset details.
- `POST /v1/tts/presets` - create or update a preset.
- `DELETE /v1/tts/presets/{preset_name}` - delete a preset.
- `GET /v1/models`, `GET /v1/audio/models` - OpenAI-compatible model list.
- `GET /v1/audio/voices` - OpenAI-compatible voice list.
- `POST /v1/audio/speech` - OpenAI-compatible TTS endpoint.

## Security
- If an API key is set, OpenAI-compatible endpoints require
  `Authorization: Bearer <key>` (or `X-API-Key`).
- If the API key is blank, endpoints are open (default).

## Backlog and Assessments (from TODO)
Deferred or assessment-only items that may influence design choices:
- Add an API key generator for security/public access.
- Add a Gradio-style audio editor/player for trimming samples and editing saved
  voice samples (not delete-only).
- Assess multi-source support (multiple Gradio targets at once), including a
  possible source library or bookmark list.
- Assess compatibility with other Gradio apps and more dynamic source switching
  (examples: Chattered, ChatterCraft-Pinokio).
- Improve compatibility with menu systems by making models/voices available as
  selectable lists (not only copy/paste).

## UI/UX Acceptance Criteria (priority order)
P0
- Each field in the cheat sheet has a copy-to-clipboard action with clear
  feedback (visual or status text).

P1
- Parameter reset buttons align to a consistent left column regardless of label
  length, so reset placement is stable across rows.
- When a slider has a numeric input, the numeric input appears directly to the
  right of the slider, shares the same row, and has a minimum width that avoids
  jitter (at least 3 digits).

P2
- Cheat sheet includes at least two additional endpoint examples that match the
  actual API surface and help menu systems populate select lists (for example,
  models and voices endpoints).

P3
- Cheat sheet title is generic (not OpenWebUI-specific).
- Read-only fields may stack under related controls on narrow layouts and retain
  a consistent visual size.

## Documentation Requirements
- `README.md` stays as the user guide.
- `SPEC.md` (this file) defines scope, architecture, and acceptance criteria
  for this folder only.

## Open Questions
- Which additional API examples should appear in the cheat sheet? 
  ANSWER: You are the expert, don't over do it but Whatever is practical / commonly used by applications/users of TTS apps
- Should the copy-to-clipboard action be icon-only or icon with text?
  Icon only is fine, what are the typical ui standards for this? Use those.
- Is multi-source targeting expected to be parallel (multi-select) or exclusive
  (one active target at a time)? For UI purposes, setting presets or viewing parameters, one at a time is fine but would be nice if they could be up and running/operational at the same time. 
