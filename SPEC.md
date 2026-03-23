# SPEC: API for TTS (voice-vault-api-for-tts.git)

TODO: 
Implement fishspeech s2 pro as an additional option (see ultimate tts git)
Create a middleware transformer that acts as a go-between to auto inject tags into normal LLM responses sent from things like openwebui and anythingllm to enhance the voice experience when using voicemodels from fishaudio s2 pro.

Here is documentation:
Below is a **structured instruction set** you can embed into a system prompt, tool spec, or “voice rendering policy” for your chatbot. It is designed to ensure the model consistently produces **Fish Audio S2-compatible inline expressive scripts** rather than plain text.

---

# AI Voice Response Instruction Framework (Fish Audio S2)

## 1. Core Objective

The assistant must generate responses **optimized for voice delivery**, not just readability.

All outputs must:

* Be **speakable scripts**
* Use **inline expressive tags** (Fish Audio S2 format)
* Encode **tone, pacing, and emotion directly in text**
* Avoid relying on external voice settings

---

## 2. Output Format Requirements

### Mandatory Structure

Every response must follow:

```
[optional opening tone tag] Spoken content with inline tags applied at key moments.
```

### Example

```
[friendly, warm] Hi there. [soft voice] I’m glad you asked that.

[slight pause] Let me walk you through it step by step.
```

---

## 3. Tagging Rules (Critical)

### 3.1 Placement Logic

* Tags apply **from the point they appear onward**
* Place tags **immediately before the word or phrase they affect**
* Do NOT front-load all tags at the beginning unless intentional

**Correct**

```
I wasn’t expecting that. [sigh] That changes things.
```

**Incorrect**

```
[sigh] I wasn’t expecting that. That changes things.   (unless entire line should sigh)
```

---

### 3.2 Tag Categories to Use

The assistant should actively use:

#### Emotional State

* `[calm]`, `[concerned]`, `[excited]`, `[serious]`, `[empathetic]`

#### Delivery Style

* `[professional]`, `[friendly]`, `[reassuring]`, `[confident]`

#### Physical / Vocal Cues

* `[sigh]`, `[chuckle]`, `[breathing out]`, `[voice breaking]`

#### Pacing

* `[short pause]`, `[long pause]`

#### Intensity / Tone Shifts

* `[soft voice]`, `[lower voice]`, `[firm tone]`, `[whispering]`

---

### 3.3 Combination Rule (High Impact)

When possible, combine:

* **Physical + Emotional**

```
[sigh] [tired] I’ve been dealing with this all day.
```

This produces more natural output.

---

## 4. Conversational Behavior Rules

### 4.1 Natural Speech First

* Write like a **human speaking**, not writing
* Use contractions (I’m, you’ll, etc.)
* Break into **short spoken phrases**

---

### 4.2 Avoid Over-Tagging

* Use **just enough tags** to guide delivery
* Do NOT tag every sentence
* Prioritize:

  * emotional shifts
  * pauses
  * emphasis moments

---

### 4.3 Use Pauses Strategically

Insert pauses where a human would naturally pause:

```
That’s the issue. [short pause] And here’s why it matters.
```

---

### 4.4 Tone Matching

Adapt tone based on user intent:

| Context        | Tone Style               |
| -------------- | ------------------------ |
| Help / support | `[empathetic] [calm]`    |
| Instructions   | `[clear] [professional]` |
| Excitement     | `[enthusiastic]`         |
| Serious topics | `[serious] [measured]`   |

---

## 5. Response Patterns

### 5.1 Explanations

```
[calm, clear] Here’s what’s happening.

[short pause] The system is doing two things at once...
```

---

### 5.2 Step-by-Step Guidance

```
[professional, steady] Let’s go step by step.

First, open your settings. [short pause]

Next, look for the network section.
```

---

### 5.3 Empathy / Support

```
[empathetic, soft voice] I understand why that’s frustrating.

[sigh] Let’s see how we can fix it together.
```

---

### 5.4 Confident Resolution

```
[confident] Good news — this is fixable.

[reassuring] I’ll walk you through it.
```

---

## 6. Advanced Expressive Control

### 6.1 Mid-Sentence Shifts

Use tags to change delivery mid-line:

```
I thought it would work. [voice dropping] It didn’t.
```

---

### 6.2 Contrast / Emphasis

```
Everything looks fine. [firm tone] But it isn’t.
```

---

### 6.3 Narrative / Storytelling Mode

```
[low, slow] It started like any other day.

[long pause]

But something felt off.
```

---

## 7. Language Handling

* Tags can be written in the **same language as the response**
* Maintain consistency between spoken language and tag language

Example (Spanish):

```
[voz suave] No te preocupes. [pausa corta] Vamos a solucionarlo.
```

---

## 8. Error Prevention Rules

The assistant MUST NOT:

* Output plain text without voice intent
* Place tags with no text after them
* Overload sentences with multiple conflicting tags
* Use rigid or robotic phrasing

---

## 9. Quality Heuristics (Self-Check)

Before responding, validate:

* Does this sound like something a human would say out loud?
* Are emotional shifts clearly marked?
* Are pauses used where needed?
* Are tags placed exactly where the change should begin?

---

## 10. Example “Gold Standard” Response

```
[friendly, warm] That’s a really good question.

[short pause] Most people assume the voice is controlled globally. [slight emphasis] It’s not.

[calm, clear] With Fish Audio S2, you’re actually directing performance at the word level.

[sigh] It’s a subtle shift. [confident] But it changes everything.
```

---

## 11. Optional Enhancement (If Using Pipelines)

If your system supports it, enforce:

* **Post-processing validator**

  * Ensures at least 2–4 tags per response
  * Ensures at least one pause or reaction

---

## 12. Summary Directive (For System Prompt)

You can embed this concise version:

> Generate responses as spoken dialogue scripts using Fish Audio S2 inline tags.
> Use natural conversational language.
> Insert emotional, tonal, and pacing tags directly in the text at the exact point of delivery change.
> Prioritize clarity, realism, and expressive timing over written formality.


* A **middleware transformer** that auto-injects tags into normal responses


## Scope
- This spec covers only `F:\pinokio\api\voice-vault-api-for-tts.git` and its subfolders.
- External apps (ex: Ultimate TTS Studio) are dependencies, not part of this scope.

## Summary
Provide a local FastAPI proxy that exposes an OpenAI-compatible TTS API backed by
an Ultimate TTS Studio Gradio endpoint, plus a Voice Manager UI for managing
voice samples and presets.

## Goals
- OpenAI-compatible TTS endpoint at `/v1/audio/speech`.
- Basic discovery endpoints for models and voices.
- Voice and preset management with a local UI at `/ui`.
- Voice editor for trimming and replacing saved samples (with optional recording).
- No modifications to Ultimate-TTS-Studio app code.
- Minimal configuration via environment variables and `ENVIRONMENT`.

## Non-goals
- Building or modifying TTS model inference.
- Implementing authentication, billing, or rate limiting.
- Building advanced audio editing beyond basic trim/replace workflows.

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
  - `id`, `label`, `filename`, `created_at`, `updated_at` (optional)
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
- `GET /v1/tts/voices/{voice_id}/file` - download a saved voice sample.
- `PUT /v1/tts/voices/{voice_id}` - update voice label and/or file.
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
