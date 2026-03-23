import json
import logging
import os
import re
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx
from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from gradio_client import Client, handle_file
from pydantic import BaseModel


DEFAULT_GRADIO_URL = "http://127.0.0.1:7860/"
DEFAULT_TTS_ENGINE = os.environ.get("DEFAULT_TTS_ENGINE", "Chatterbox Turbo")
DEFAULT_FORMAT = os.environ.get("DEFAULT_FORMAT", "mp3")
GRADIO_API_NAME = os.environ.get("GRADIO_API_NAME", "/generate_unified_tts")
CHATTERBOX_TURBO_REF_AUDIO = os.environ.get("CHATTERBOX_TURBO_REF_AUDIO", "")
AUTO_LOAD_ENGINE = os.environ.get("AUTO_LOAD_ENGINE", "true").lower() in ("1", "true", "yes", "on")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
DEFAULT_TRANSFORMER_URL = os.environ.get("TRANSFORMER_URL", "http://127.0.0.1:42026/")

GRADIO_URL = os.environ.get("GRADIO_URL", DEFAULT_GRADIO_URL)

ENGINE_ALIASES = {
    "Fish Speech": "Fish Speech S1",
    "Fish Speech S1": "Fish Speech S1",
    "Fish Speech S2 Pro": "Fish Speech S2 Pro",
}

KNOWN_ENGINES = [
    "ChatterboxTTS",
    "Chatterbox Multilingual",
    "Chatterbox Turbo",
    "Kokoro TTS",
    "Fish Speech S1",
    "Fish Speech S2 Pro",
    "IndexTTS",
    "IndexTTS2",
    "F5-TTS",
    "Higgs Audio",
    "VoxCPM",
    "KittenTTS",
    "Qwen Voice Design",
    "Qwen Voice Clone",
    "Qwen Custom Voice",
]

ENGINE_LOAD_API = {
    "ChatterboxTTS": "/handle_load_chatterbox",
    "Chatterbox Multilingual": "/handle_load_chatterbox_multilingual",
    "Chatterbox Turbo": "/handle_load_chatterbox_turbo",
    "Kokoro TTS": "/handle_load_kokoro",
    "Fish Speech S1": "/handle_load_fish",
    "Fish Speech S2 Pro": "/handle_load_fish_s2",
    "IndexTTS": "/handle_load_indextts",
    "IndexTTS2": "/handle_load_indextts2",
    "F5-TTS": "/handle_f5_load",
    "Higgs Audio": "/handle_load_higgs",
    "VoxCPM": "/handle_load_voxcpm",
    "KittenTTS": "/handle_load_kitten",
}

ENGINE_PARAM_PREFIX = {
    "ChatterboxTTS": "chatterbox_",
    "Chatterbox Multilingual": "chatterbox_mtl_",
    "Chatterbox Turbo": "chatterbox_turbo_",
    "Kokoro TTS": "kokoro_",
    "Fish Speech S1": "fish_",
    "Fish Speech S2 Pro": "fish_s2_",
    "IndexTTS": "indextts_",
    "IndexTTS2": "indextts2_",
    "F5-TTS": "f5_",
    "Higgs Audio": "higgs_",
    "VoxCPM": "voxcpm_",
    "KittenTTS": "kitten_",
    "Qwen Voice Design": "qwen_",
    "Qwen Voice Clone": "qwen_",
    "Qwen Custom Voice": "qwen_",
}

ENGINE_REF_PARAM = {
    "ChatterboxTTS": "chatterbox_ref_audio",
    "Chatterbox Multilingual": "chatterbox_mtl_ref_audio",
    "Chatterbox Turbo": "chatterbox_turbo_ref_audio",
    "Fish Speech S1": "fish_ref_audio",
    "Fish Speech S2 Pro": "fish_s2_ref_audio",
    "IndexTTS": "indextts_ref_audio",
    "IndexTTS2": "indextts2_ref_audio",
    "F5-TTS": "f5_ref_audio",
    "Higgs Audio": "higgs_ref_audio",
    "VoxCPM": "voxcpm_ref_audio",
    "Qwen Voice Clone": "qwen_ref_audio",
}

ENGINE_REF_TEXT_PARAM = {
    "Fish Speech S1": "fish_ref_text",
    "Fish Speech S2 Pro": "fish_s2_ref_text",
    "F5-TTS": "f5_ref_text",
    "Higgs Audio": "higgs_ref_text",
    "VoxCPM": "voxcpm_ref_text",
    "Qwen Voice Clone": "qwen_ref_text",
}

REQUIRED_REF_ENGINES = {"IndexTTS2"}

PARAM_CHOICES = {
    "indextts2_emotion_mode": ["audio_reference", "vector_control", "text_description"],
}

ENGINE_VOICE_PARAM = {
    "Kokoro TTS": "kokoro_voice",
    "KittenTTS": "kitten_voice",
    "Higgs Audio": "higgs_voice_preset",
    "Qwen Custom Voice": "qwen_speaker",
}

KITTEN_VOICES = [
    "expr-voice-2-m",
    "expr-voice-2-f",
    "expr-voice-3-m",
    "expr-voice-3-f",
    "expr-voice-4-m",
    "expr-voice-4-f",
    "expr-voice-5-m",
    "expr-voice-5-f",
]

FILE_PARAM_NAMES = {
    "audio_file",
    "files",
    "chatterbox_ref_audio",
    "chatterbox_mtl_ref_audio",
    "chatterbox_turbo_ref_audio",
    "fish_ref_audio",
    "fish_s2_ref_audio",
    "indextts_ref_audio",
    "indextts2_ref_audio",
    "indextts2_emotion_audio",
    "f5_ref_audio",
    "higgs_ref_audio",
    "voxcpm_ref_audio",
    "qwen_ref_audio",
}

LOADED_ENGINE: Optional[str] = None
DEFAULT_PARAMS: Optional[dict[str, Any]] = None
DEFAULT_PARAM_META: Optional[dict[str, dict[str, Any]]] = None
GRADIO_STATUS = {"connected": False, "message": "", "url": GRADIO_URL}

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("tts_proxy")

app = FastAPI()
security = HTTPBasic(auto_error=False)

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
ENV_FILE = APP_DIR.parent / "ENVIRONMENT"
VOICE_DIR = DATA_DIR / "voices"
VOICE_INDEX_FILE = DATA_DIR / "voices.json"
PRESET_FILE = DATA_DIR / "presets.json"
API_KEY_FILE = DATA_DIR / "api_key.txt"
TRANSFORMER_CONFIG_FILE = DATA_DIR / "transformer.json"
UI_INDEX = APP_DIR / "ui" / "index.html"


class OpenAITTSSpeechRequest(BaseModel):
    model: Optional[str] = None
    input: str
    voice: Optional[str] = None
    response_format: Optional[str] = None
    speed: Optional[float] = None
    reference_text: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    max_tokens: Optional[int] = None
    seed: Optional[int] = None
    transform: Optional[bool] = None


def admin_auth_enabled() -> bool:
    return bool(ADMIN_USERNAME and ADMIN_PASSWORD)


def require_admin(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    if not admin_auth_enabled():
        return
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Basic"},
        )
    user_ok = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    pass_ok = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    VOICE_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("Failed to parse %s", path)
        return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def read_env_value(key: str) -> Optional[str]:
    if not ENV_FILE.exists():
        return None
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        current_key, value = line.split("=", 1)
        if current_key.strip() == key:
            return value.strip()
    return None


def persist_env_value(key: str, value: str) -> None:
    lines: list[str] = []
    replaced = False
    if ENV_FILE.exists():
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            replaced = True
        else:
            new_lines.append(line)
    if not replaced:
        if new_lines and new_lines[-1].strip():
            new_lines.append("")
        new_lines.append(f"{key}={value}")
    ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def normalize_gradio_url(url: str, default_url: str = DEFAULT_GRADIO_URL) -> str:
    cleaned = url.strip()
    if not cleaned:
        return default_url
    if not re.match(r"^https?://", cleaned):
        cleaned = f"http://{cleaned}"
    if not cleaned.endswith("/"):
        cleaned = f"{cleaned}/"
    return cleaned


def normalize_service_url(url: str, default_url: str) -> str:
    return normalize_gradio_url(url, default_url=default_url)


def apply_gradio_env_override() -> None:
    global GRADIO_URL
    env_value = read_env_value("GRADIO_URL")
    if env_value:
        GRADIO_URL = normalize_gradio_url(env_value)
        os.environ["GRADIO_URL"] = GRADIO_URL


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-").lower()
    return cleaned or "voice"


def unique_slug(value: str, existing: set[str]) -> str:
    candidate = slugify(value)
    if candidate not in existing:
        return candidate
    index = 2
    while f"{candidate}-{index}" in existing:
        index += 1
    return f"{candidate}-{index}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_api_key() -> str:
    if not API_KEY_FILE.exists():
        return ""
    return API_KEY_FILE.read_text(encoding="utf-8").strip()


def write_api_key(value: str) -> None:
    API_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    API_KEY_FILE.write_text(value.strip() + "\n", encoding="utf-8")


def get_api_key() -> str:
    return read_api_key()


def require_api_key(request: Request) -> None:
    api_key = get_api_key()
    if not api_key:
        return
    auth_header = request.headers.get("authorization", "")
    token = ""
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    if not token:
        token = request.headers.get("x-api-key", "").strip()
    if token != api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


def load_voices() -> list[dict]:
    ensure_data_dirs()
    return load_json(VOICE_INDEX_FILE, [])


def save_voices(voices: list[dict]) -> None:
    save_json(VOICE_INDEX_FILE, voices)


def load_presets() -> list[dict]:
    ensure_data_dirs()
    return load_json(PRESET_FILE, [])


def save_presets(presets: list[dict]) -> None:
    save_json(PRESET_FILE, presets)


def default_transformer_config() -> dict[str, Any]:
    return {
        "enabled": False,
        "url": normalize_service_url(DEFAULT_TRANSFORMER_URL, DEFAULT_TRANSFORMER_URL),
        "mode": "balanced",
        "tone_profile": "warm",
        "target_engine": "Fish Speech S2 Pro",
        "fail_open": False,
    }


def load_transformer_config() -> dict[str, Any]:
    ensure_data_dirs()
    config = load_json(TRANSFORMER_CONFIG_FILE, default_transformer_config())
    merged = {**default_transformer_config(), **config}
    merged["url"] = normalize_service_url(merged.get("url", ""), DEFAULT_TRANSFORMER_URL)
    return merged


def save_transformer_config(config: dict[str, Any]) -> dict[str, Any]:
    merged = {**default_transformer_config(), **config}
    merged["url"] = normalize_service_url(merged.get("url", ""), DEFAULT_TRANSFORMER_URL)
    save_json(TRANSFORMER_CONFIG_FILE, merged)
    return merged


def fetch_transformer_health(config: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    cfg = config or load_transformer_config()
    try:
        response = httpx.get(f"{cfg['url'].rstrip('/')}/health", timeout=5.0)
        response.raise_for_status()
        payload = response.json()
        return {"connected": True, "message": payload.get("status", "ok"), "url": cfg["url"]}
    except Exception as exc:
        return {"connected": False, "message": str(exc), "url": cfg["url"]}


def call_transformer(text: str, config: dict[str, Any]) -> dict[str, Any]:
    try:
        response = httpx.post(
            f"{config['url'].rstrip('/')}/v1/text/transform",
            json={
                "text": text,
                "mode": config.get("mode") or "balanced",
                "tone_profile": config.get("tone_profile") or "warm",
            },
            timeout=15.0,
        )
        response.raise_for_status()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Transformer call failed: {exc}")
    payload = response.json()
    transformed = str(payload.get("transformed_text") or "").strip()
    if not transformed:
        raise HTTPException(status_code=502, detail="Transformer returned empty text")
    return {
        "text": text,
        "transformed_text": transformed,
        "mode": payload.get("mode") or config.get("mode"),
        "tone_profile": payload.get("tone_profile") or config.get("tone_profile"),
    }


def normalize_engine_name(engine: Optional[str]) -> Optional[str]:
    if not engine:
        return None
    cleaned = str(engine).strip()
    if not cleaned:
        return None
    return ENGINE_ALIASES.get(cleaned, cleaned)


def upstream_engine_name(engine: Optional[str]) -> Optional[str]:
    canonical = normalize_engine_name(engine)
    if canonical == "Fish Speech S1":
        return "Fish Speech"
    return canonical


def find_preset(name: str) -> Optional[dict]:
    target = name.strip()
    for preset in load_presets():
        if preset.get("name") == target:
            return normalize_preset_record(preset)
    return None


def preset_label(preset: dict) -> str:
    return str(preset.get("label") or preset.get("name") or "").strip()


def normalize_preset_record(preset: dict) -> dict:
    normalized = dict(preset)
    normalized["engine"] = normalize_engine_name(normalized.get("engine")) or normalized.get("engine")
    normalized["transform_enabled"] = bool(normalized.get("transform_enabled", False))
    return normalized


def find_preset_by_label(label: str, engine: Optional[str]) -> Optional[dict]:
    target = label.strip().lower()
    if not target:
        return None
    normalized_engine = normalize_engine_name(engine)
    matches = []
    for preset in load_presets():
        current = normalize_preset_record(preset)
        if preset_label(current).lower() == target:
            matches.append(current)
    if not matches:
        return None
    if normalized_engine:
        for preset in matches:
            if preset.get("engine") == normalized_engine:
                return preset
    if len(matches) == 1:
        return matches[0]
    return None


def find_voice(voice_id: str) -> Optional[dict]:
    for voice in load_voices():
        if voice.get("id") == voice_id:
            return voice
    return None


def resolve_voice_path(voice: dict) -> Path:
    return VOICE_DIR / voice["filename"]


def resolve_voice_reference(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    voice = find_voice(value)
    if voice:
        return str(resolve_voice_path(voice))
    if os.path.isfile(value):
        return value
    return None


def parse_param_string(param: str) -> dict:
    if not (param.startswith("@{") and param.endswith("}")):
        return {}
    content = param[2:-1]
    parts = [part.strip() for part in content.split(";") if part.strip()]
    parsed: dict[str, str] = {}
    for part in parts:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def normalize_param(param: Any) -> dict:
    if isinstance(param, dict):
        return param
    if isinstance(param, str):
        return parse_param_string(param)
    return {}


def normalize_meta_type(value: Any) -> Optional[str]:
    if isinstance(value, dict):
        return value.get("type")
    if isinstance(value, str):
        return value
    return None


def reset_gradio_cache() -> None:
    global DEFAULT_PARAMS, DEFAULT_PARAM_META, LOADED_ENGINE
    DEFAULT_PARAMS = None
    DEFAULT_PARAM_META = None
    LOADED_ENGINE = None


def extract_description(param: dict) -> str:
    type_field = param.get("type")
    if isinstance(type_field, dict):
        return str(type_field.get("description") or "")
    return ""


def extract_numeric_bounds(param: dict) -> tuple[Optional[float], Optional[float], Optional[float]]:
    def _to_float(value: Any) -> Optional[float]:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    min_value = _to_float(param.get("minimum") or param.get("min"))
    max_value = _to_float(param.get("maximum") or param.get("max"))
    step_value = _to_float(param.get("step"))

    if min_value is None or max_value is None:
        description = extract_description(param)
        match = re.search(r"between\s+(-?\d+(?:\.\d+)?)\s+and\s+(-?\d+(?:\.\d+)?)", description)
        if not match:
            match = re.search(r"from\s+(-?\d+(?:\.\d+)?)\s+to\s+(-?\d+(?:\.\d+)?)", description)
        if match:
            min_value = _to_float(match.group(1))
            max_value = _to_float(match.group(2))
    return min_value, max_value, step_value


def extract_choices(param: dict) -> list:
    for key in ("choices", "enum", "values"):
        choices = param.get(key)
        if isinstance(choices, list) and choices:
            return choices
    return []


def fetch_default_params() -> tuple[dict, dict, str, bool]:
    base_url = GRADIO_URL.rstrip("/")
    info_url = f"{base_url}/gradio_api/info?serialize=False"
    try:
        resp = httpx.get(info_url, timeout=10.0)
        resp.raise_for_status()
    except Exception as exc:
        message = f"Ultimate TTS is not reachable at {GRADIO_URL}. Start the backend and reconnect."
        logger.warning("Failed to fetch Gradio info: %s", exc)
        return {}, {}, message, False

    data = resp.json()
    endpoints = data.get("named_endpoints") or {}
    endpoint = endpoints.get(GRADIO_API_NAME)
    if not endpoint:
        message = f"Gradio endpoint {GRADIO_API_NAME} not found at {GRADIO_URL}."
        logger.warning("Endpoint %s not found in Gradio info", GRADIO_API_NAME)
        return {}, {}, message, False

    params = endpoint.get("parameters_info") or endpoint.get("parameters") or []
    defaults: dict[str, Any] = {}
    meta: dict[str, dict[str, Any]] = {}
    for raw_param in params:
        param = normalize_param(raw_param)
        if not param:
            continue
        name = param.get("name") or param.get("parameter_name") or param.get("label")
        if not name:
            continue
        value = param.get("default")
        if value is None:
            value = param.get("parameter_default")
        if value is None:
            value = param.get("value")
        if value is None:
            value = ""
        min_value, max_value, step_value = extract_numeric_bounds(param)
        defaults[name] = value
        meta[name] = {
            "label": param.get("label"),
            "choices": extract_choices(param),
            "python_type": normalize_meta_type(param.get("python_type")),
            "type": normalize_meta_type(param.get("type")),
            "component": param.get("component"),
            "raw_default": value,
            "description": extract_description(param),
            "min": min_value,
            "max": max_value,
            "step": step_value,
            "example": param.get("example_input"),
        }
    return defaults, meta, "Loaded from Ultimate TTS metadata.", True


def get_default_params(force_refresh: bool = False) -> dict:
    global DEFAULT_PARAMS, DEFAULT_PARAM_META, GRADIO_STATUS
    if force_refresh or DEFAULT_PARAMS is None or DEFAULT_PARAM_META is None or not DEFAULT_PARAMS:
        defaults, meta, message, connected = fetch_default_params()
        DEFAULT_PARAMS = defaults
        DEFAULT_PARAM_META = meta
        GRADIO_STATUS = {"connected": connected, "message": message, "url": GRADIO_URL}
    defaults = dict(DEFAULT_PARAMS or {})
    for key, value in list(defaults.items()):
        meta = (DEFAULT_PARAM_META or {}).get(key, {})
        component = meta.get("component")
        if value == "" and (
            key in FILE_PARAM_NAMES
            or key.endswith("_ref_audio")
            or key.endswith("_emotion_audio")
        ):
            defaults[key] = None
        if value == "" and component == "Checkbox":
            defaults[key] = False
        if value == "" and component in ("Slider", "Number"):
            defaults[key] = None
        if value == "":
            choices = meta.get("choices") or []
            if choices:
                defaults[key] = choices[0]
    return defaults


def get_engine_choices_from_meta() -> list[str]:
    get_default_params()
    meta = DEFAULT_PARAM_META or {}
    engine_meta = meta.get("tts_engine") or {}
    choices = engine_meta.get("choices") or []
    result: list[str] = []
    for choice in choices:
        normalized = normalize_engine_name(str(choice))
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def list_supported_engines() -> list[str]:
    engines: list[str] = []
    for engine in KNOWN_ENGINES:
        if engine not in engines:
            engines.append(engine)
    for choice in get_engine_choices_from_meta():
        if choice not in engines:
            engines.append(choice)
    if "Fish Speech" in engines:
        engines.remove("Fish Speech")
    return engines


def list_param_specs(engine: Optional[str] = None) -> list[dict]:
    defaults = get_default_params()
    meta = DEFAULT_PARAM_META or {}
    params: list[dict] = []
    normalized_engine = normalize_engine_name(engine) if engine else None
    prefix = ENGINE_PARAM_PREFIX.get(normalized_engine, "") if normalized_engine else ""
    for name, value in defaults.items():
        if name in ("text_input", "tts_engine"):
            continue
        if normalized_engine and prefix and not name.startswith(prefix) and name != "audio_format":
            continue
        info = meta.get(name, {})
        choices = info.get("choices") or PARAM_CHOICES.get(name)
        is_file = name in FILE_PARAM_NAMES or name.endswith("_ref_audio") or name.endswith("_emotion_audio")
        params.append(
            {
                "name": name,
                "default": value,
                "label": info.get("label"),
                "component": info.get("component"),
                "type": info.get("type"),
                "python_type": info.get("python_type"),
                "choices": choices,
                "is_file": is_file,
                "description": info.get("description"),
                "min": info.get("min"),
                "max": info.get("max"),
                "step": info.get("step"),
            }
        )
    return params


def fetch_kokoro_voice_choices() -> list[str]:
    try:
        client = Client(GRADIO_URL)
        voices = client.predict(api_name="/refresh_kokoro_voice_list")
        if isinstance(voices, list):
            return [str(v) for v in voices]
    except Exception as exc:
        logger.warning("Failed to fetch Kokoro voices: %s", exc)
    return []


def fetch_voice_choices(engine: str) -> dict:
    normalized_engine = normalize_engine_name(engine)

    def meta_choices(param_name: str) -> list[str]:
        get_default_params()
        meta = DEFAULT_PARAM_META or {}
        info = meta.get(param_name) or {}
        choices = info.get("choices") or []
        if isinstance(choices, list):
            return [str(choice) for choice in choices if str(choice).strip()]
        return []

    if normalized_engine == "Kokoro TTS":
        return {"param": ENGINE_VOICE_PARAM[normalized_engine], "choices": fetch_kokoro_voice_choices()}
    if normalized_engine in ENGINE_VOICE_PARAM:
        param = ENGINE_VOICE_PARAM[normalized_engine]
        choices = meta_choices(param)
        if choices:
            return {"param": param, "choices": choices}
    if normalized_engine == "KittenTTS":
        return {"param": ENGINE_VOICE_PARAM[normalized_engine], "choices": KITTEN_VOICES}
    if normalized_engine == "Higgs Audio":
        return {"param": ENGINE_VOICE_PARAM[normalized_engine], "choices": ["EMPTY"]}
    return {"param": "", "choices": []}


def get_output_format(req: OpenAITTSSpeechRequest) -> str:
    out_fmt = (req.response_format or DEFAULT_FORMAT).lower()
    if out_fmt not in ("mp3", "wav"):
        return DEFAULT_FORMAT
    return out_fmt


def resolve_output_format(req: OpenAITTSSpeechRequest, preset: Optional[dict]) -> str:
    if req.response_format:
        return get_output_format(req)
    if preset:
        preset_format = (preset.get("params") or {}).get("audio_format")
        if isinstance(preset_format, str) and preset_format.lower() in ("mp3", "wav"):
            return preset_format.lower()
    return DEFAULT_FORMAT


def resolve_engine(req: OpenAITTSSpeechRequest, preset: Optional[dict]) -> str:
    supported = list_supported_engines()
    requested_model = normalize_engine_name(req.model)
    if requested_model and requested_model in supported:
        return requested_model
    if preset:
        preset_engine = normalize_engine_name(preset.get("engine"))
        if preset_engine:
            return preset_engine
    requested_voice_engine = normalize_engine_name(req.voice)
    if requested_voice_engine and requested_voice_engine in supported:
        return requested_voice_engine
    default_engine = normalize_engine_name(DEFAULT_TTS_ENGINE)
    return default_engine if default_engine in supported else supported[0]


def collect_request_overrides(req: OpenAITTSSpeechRequest, engine: str) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    prefix = ENGINE_PARAM_PREFIX.get(engine)
    if not prefix:
        return overrides
    if req.reference_text is not None:
        ref_text_param = ENGINE_REF_TEXT_PARAM.get(engine)
        if ref_text_param:
            overrides[ref_text_param] = req.reference_text
    if req.temperature is not None:
        overrides[f"{prefix}temperature"] = req.temperature
    if req.top_p is not None:
        overrides[f"{prefix}top_p"] = req.top_p
    if req.repetition_penalty is not None:
        overrides[f"{prefix}repetition_penalty"] = req.repetition_penalty
    if req.max_tokens is not None:
        token_key = f"{prefix}max_tokens"
        if engine == "Fish Speech S2 Pro":
            token_key = "fish_s2_max_tokens"
        overrides[token_key] = req.max_tokens
    if req.seed is not None:
        overrides[f"{prefix}seed"] = req.seed
    return overrides


def should_transform_text(engine: str, preset: Optional[dict], req: OpenAITTSSpeechRequest) -> bool:
    config = load_transformer_config()
    if not config.get("enabled"):
        return False
    target_engine = normalize_engine_name(config.get("target_engine")) or "Fish Speech S2 Pro"
    if engine != target_engine:
        return False
    if req.transform is not None:
        return bool(req.transform)
    if preset and preset.get("transform_enabled"):
        return True
    return True


def build_params(req: OpenAITTSSpeechRequest, preset: Optional[dict], voice_sample: Optional[dict], engine: str) -> dict[str, Any]:
    params = get_default_params().copy()
    if preset and isinstance(preset.get("params"), dict):
        params.update(preset["params"])

    text_input = (req.input or "").strip()
    if not text_input:
        raise HTTPException(status_code=400, detail="Missing 'input' text")

    if should_transform_text(engine, preset, req):
        transformed = call_transformer(text_input, load_transformer_config())
        text_input = transformed["transformed_text"]

    params.update(
        {
            "text_input": text_input,
            "tts_engine": upstream_engine_name(engine),
            "audio_format": resolve_output_format(req, preset),
        }
    )

    ref_param = ENGINE_REF_PARAM.get(engine)
    ref_text_param = ENGINE_REF_TEXT_PARAM.get(engine)

    if voice_sample and ref_param:
        params[ref_param] = handle_file(str(resolve_voice_path(voice_sample)))

    if preset and preset.get("voice_id") and ref_param:
        voice = find_voice(preset["voice_id"])
        if voice:
            params[ref_param] = handle_file(str(resolve_voice_path(voice)))

    if req.reference_text is not None and ref_text_param:
        params[ref_text_param] = req.reference_text

    params.update(collect_request_overrides(req, engine))

    if req.voice and not preset and engine in ENGINE_VOICE_PARAM:
        voice_param = ENGINE_VOICE_PARAM[engine]
        params[voice_param] = req.voice

    for key, value in list(params.items()):
        if key in FILE_PARAM_NAMES or key.endswith("_ref_audio") or key.endswith("_emotion_audio"):
            resolved = resolve_voice_reference(value) if isinstance(value, str) else None
            if resolved:
                params[key] = handle_file(resolved)
            elif value in ("", None):
                params[key] = None

    if engine in REQUIRED_REF_ENGINES:
        required_ref_param = ENGINE_REF_PARAM.get(engine)
        if required_ref_param and not params.get(required_ref_param):
            raise HTTPException(
                status_code=400,
                detail=f"Reference audio is required for {engine}. Save a voice sample and attach it to the preset.",
            )

    if engine == "Chatterbox Turbo" and CHATTERBOX_TURBO_REF_AUDIO:
        if not os.path.isfile(CHATTERBOX_TURBO_REF_AUDIO):
            raise HTTPException(status_code=500, detail="CHATTERBOX_TURBO_REF_AUDIO path does not exist")
        params["chatterbox_turbo_ref_audio"] = handle_file(CHATTERBOX_TURBO_REF_AUDIO)

    return params


def call_ultimate_tts(engine: str, params: dict[str, Any]) -> tuple[bytes, str]:
    global LOADED_ENGINE
    try:
        client = Client(GRADIO_URL)
        load_api = ENGINE_LOAD_API.get(engine)
        if AUTO_LOAD_ENGINE and load_api and LOADED_ENGINE != engine:
            logger.info("Loading engine: %s", engine)
            client.predict(api_name=load_api)
            LOADED_ENGINE = engine
        result = client.predict(api_name=GRADIO_API_NAME, **params)
    except Exception as exc:
        safe_params = {}
        for key, value in params.items():
            if key in FILE_PARAM_NAMES or key.endswith("_ref_audio") or key.endswith("_emotion_audio"):
                safe_params[key] = "file"
            else:
                safe_params[key] = value
        logger.exception("Gradio call failed for engine %s with params %s", engine, safe_params)
        raise HTTPException(status_code=502, detail=f"Gradio call failed: {exc}")

    audio_path = result[0] if isinstance(result, (list, tuple)) else result
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=502, detail="No audio file returned")
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    out_fmt = str(params.get("audio_format") or DEFAULT_FORMAT).lower()
    media_type = "audio/mpeg" if out_fmt == "mp3" else "audio/wav"
    return audio_bytes, media_type


GRADIO_URL = normalize_gradio_url(GRADIO_URL)
apply_gradio_env_override()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", include_in_schema=False, dependencies=[Depends(require_admin)])
def root() -> Response:
    if UI_INDEX.exists():
        return FileResponse(UI_INDEX)
    return HTMLResponse("<h1>API for TTS</h1>")


@app.get("/ui", include_in_schema=False, dependencies=[Depends(require_admin)])
def ui() -> Response:
    if UI_INDEX.exists():
        return FileResponse(UI_INDEX)
    return HTMLResponse("<h1>Voice Manager UI not found.</h1>", status_code=404)


@app.get("/v1/tts/engines", dependencies=[Depends(require_admin)])
def engines() -> dict:
    return {"engines": list_supported_engines()}


@app.get("/v1/tts/params", dependencies=[Depends(require_admin)])
def params(engine: Optional[str] = Query(default=None)) -> dict:
    normalized = normalize_engine_name(engine) if engine else None
    if normalized and normalized not in list_supported_engines():
        normalized = None
    get_default_params()
    status = dict(GRADIO_STATUS)
    return {
        "params": list_param_specs(normalized),
        "message": status.get("message"),
        "connected": status.get("connected"),
        "gradio_url": status.get("url"),
    }


@app.get("/v1/tts/gradio", dependencies=[Depends(require_admin)])
def gradio_status() -> dict:
    get_default_params()
    status = dict(GRADIO_STATUS)
    return {
        "connected": status.get("connected"),
        "message": status.get("message"),
        "gradio_url": status.get("url"),
    }


@app.post("/v1/tts/gradio", dependencies=[Depends(require_admin)])
def set_gradio(payload: dict) -> dict:
    global GRADIO_URL
    url = str(payload.get("url", "")).strip()
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
    GRADIO_URL = normalize_gradio_url(url)
    os.environ["GRADIO_URL"] = GRADIO_URL
    persist_env_value("GRADIO_URL", GRADIO_URL)
    reset_gradio_cache()
    get_default_params(force_refresh=True)
    status = dict(GRADIO_STATUS)
    return {
        "status": "updated",
        "connected": status.get("connected"),
        "message": status.get("message"),
        "gradio_url": status.get("url"),
        "params": list_param_specs(),
    }


@app.post("/v1/tts/gradio/reload", dependencies=[Depends(require_admin)])
def reload_gradio() -> dict:
    global GRADIO_URL
    env_value = read_env_value("GRADIO_URL")
    GRADIO_URL = normalize_gradio_url(env_value or DEFAULT_GRADIO_URL)
    os.environ["GRADIO_URL"] = GRADIO_URL
    reset_gradio_cache()
    get_default_params(force_refresh=True)
    status = dict(GRADIO_STATUS)
    return {
        "status": "reloaded",
        "connected": status.get("connected"),
        "message": status.get("message"),
        "gradio_url": status.get("url"),
        "params": list_param_specs(),
    }


@app.get("/v1/tts/voice-choices", dependencies=[Depends(require_admin)])
def voice_choices(engine: str = Query(...)) -> dict:
    normalized = normalize_engine_name(engine)
    if not normalized or normalized not in list_supported_engines():
        raise HTTPException(status_code=400, detail="Unknown engine")
    return fetch_voice_choices(normalized)


@app.get("/v1/tts/voices", dependencies=[Depends(require_admin)])
def voices() -> dict:
    return {"voices": load_voices()}


@app.get("/v1/tts/api-key", dependencies=[Depends(require_admin)])
def api_key_status() -> dict:
    return {"api_key": get_api_key()}


@app.post("/v1/tts/api-key/generate", dependencies=[Depends(require_admin)])
def api_key_generate() -> dict:
    ensure_data_dirs()
    api_key = secrets.token_urlsafe(24)
    write_api_key(api_key)
    return {"api_key": api_key}


@app.post("/v1/tts/voices", dependencies=[Depends(require_admin)])
def create_voice(name: str = Form(default=""), file: UploadFile = File(...)) -> dict:
    ensure_data_dirs()
    voices = load_voices()
    existing = {voice["id"] for voice in voices}
    label = name.strip() or Path(file.filename or "voice").stem
    voice_id = unique_slug(label, existing)
    extension = Path(file.filename or "").suffix.lower() or ".wav"
    filename = f"{voice_id}{extension}"
    target_path = VOICE_DIR / filename
    with target_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    voice_data = {
        "id": voice_id,
        "label": label,
        "filename": filename,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    voices.append(voice_data)
    save_voices(voices)
    return {"voice": voice_data}


@app.put("/v1/tts/voices/{voice_id}", dependencies=[Depends(require_admin)])
def update_voice(voice_id: str, name: str = Form(default=""), file: Optional[UploadFile] = File(default=None)) -> dict:
    voices = load_voices()
    voice = next((v for v in voices if v.get("id") == voice_id), None)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    updated = False
    label = name.strip()
    if label:
        voice["label"] = label
        updated = True
    if file is not None:
        ensure_data_dirs()
        old_path = resolve_voice_path(voice)
        extension = Path(file.filename or "").suffix.lower() or Path(voice["filename"]).suffix or ".wav"
        filename = f"{voice_id}{extension}"
        target_path = VOICE_DIR / filename
        with target_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        if old_path.exists() and old_path != target_path:
            old_path.unlink()
        voice["filename"] = filename
        updated = True
    if not updated:
        raise HTTPException(status_code=400, detail="No changes provided")
    voice["updated_at"] = now_iso()
    save_voices(voices)
    return {"voice": voice}


@app.get("/v1/tts/voices/{voice_id}/file", dependencies=[Depends(require_admin)])
def voice_file(voice_id: str) -> Response:
    voice = find_voice(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    file_path = resolve_voice_path(voice)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Voice file not found")
    return FileResponse(file_path)


@app.delete("/v1/tts/voices/{voice_id}", dependencies=[Depends(require_admin)])
def delete_voice(voice_id: str) -> dict:
    voices = load_voices()
    presets = load_presets()
    if any(preset.get("voice_id") == voice_id for preset in presets):
        raise HTTPException(status_code=409, detail="Voice is used by a preset")
    voice = next((v for v in voices if v.get("id") == voice_id), None)
    remaining = [voice_record for voice_record in voices if voice_record.get("id") != voice_id]
    if len(remaining) == len(voices):
        raise HTTPException(status_code=404, detail="Voice not found")
    save_voices(remaining)
    if voice:
        file_path = resolve_voice_path(voice)
        if file_path.exists():
            file_path.unlink()
    return {"status": "deleted"}


@app.get("/v1/tts/presets", dependencies=[Depends(require_admin)])
def presets() -> dict:
    return {"presets": [normalize_preset_record(preset) for preset in load_presets()]}


@app.get("/v1/tts/presets/{preset_name}", dependencies=[Depends(require_admin)])
def preset(preset_name: str) -> dict:
    preset_data = find_preset(preset_name)
    if not preset_data:
        raise HTTPException(status_code=404, detail="Preset not found")
    return {"preset": preset_data}


@app.post("/v1/tts/presets", dependencies=[Depends(require_admin)])
def create_preset(payload: dict) -> dict:
    name = str(payload.get("name", "")).strip()
    label = str(payload.get("label", "")).strip()
    engine = normalize_engine_name(payload.get("engine"))
    if not name:
        raise HTTPException(status_code=400, detail="Preset name is required")
    if not engine or engine not in list_supported_engines():
        raise HTTPException(status_code=400, detail="Unknown engine")
    voice_id = payload.get("voice_id")
    if voice_id and not find_voice(voice_id):
        raise HTTPException(status_code=400, detail="Unknown voice_id")
    params = payload.get("params") or {}
    if not isinstance(params, dict):
        raise HTTPException(status_code=400, detail="Params must be an object")

    reference_text = str(payload.get("reference_text", "") or "").strip()
    ref_text_param = ENGINE_REF_TEXT_PARAM.get(engine)
    if reference_text and ref_text_param:
        params[ref_text_param] = reference_text

    overwrite = bool(payload.get("overwrite"))
    existing = find_preset(name)
    if existing and not overwrite:
        raise HTTPException(status_code=409, detail="Preset already exists")

    if not label:
        label = name

    presets_data = load_presets()
    presets_data = [preset_record for preset_record in presets_data if preset_record.get("name") != name]
    presets_data.append(
        {
            "name": name,
            "label": label,
            "engine": engine,
            "voice_id": voice_id,
            "params": params,
            "transform_enabled": bool(payload.get("transform_enabled", False)),
            "updated_at": now_iso(),
        }
    )
    save_presets(presets_data)
    return {"preset": find_preset(name)}


@app.delete("/v1/tts/presets/{preset_name}", dependencies=[Depends(require_admin)])
def delete_preset(preset_name: str) -> dict:
    presets_data = load_presets()
    remaining = [preset_record for preset_record in presets_data if preset_record.get("name") != preset_name]
    if len(remaining) == len(presets_data):
        raise HTTPException(status_code=404, detail="Preset not found")
    save_presets(remaining)
    return {"status": "deleted"}


@app.get("/v1/tts/transformer", dependencies=[Depends(require_admin)])
def transformer_status() -> dict:
    config = load_transformer_config()
    health = fetch_transformer_health(config)
    return {**config, **health}


@app.post("/v1/tts/transformer", dependencies=[Depends(require_admin)])
def update_transformer(payload: dict) -> dict:
    config = save_transformer_config(payload)
    health = fetch_transformer_health(config)
    return {**config, **health}


@app.post("/v1/tts/transformer/test", dependencies=[Depends(require_admin)])
def test_transformer(payload: dict) -> dict:
    text = str(payload.get("text", "") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    base_config = load_transformer_config()
    config = {
        **base_config,
        "mode": payload.get("mode", base_config.get("mode")),
        "tone_profile": payload.get("tone_profile", base_config.get("tone_profile")),
        "url": normalize_service_url(str(payload.get("url") or base_config.get("url") or DEFAULT_TRANSFORMER_URL), DEFAULT_TRANSFORMER_URL),
    }
    result = call_transformer(text, config)
    health = fetch_transformer_health(config)
    return {**result, **health}


@app.get("/v1/models")
def models(request: Request) -> dict:
    require_api_key(request)
    return {
        "object": "list",
        "data": [{"id": engine, "object": "model"} for engine in list_supported_engines()],
    }


@app.get("/v1/audio/models")
def audio_models(request: Request) -> dict:
    require_api_key(request)
    return models(request)


@app.get("/v1/audio/voices")
def audio_voices(request: Request) -> dict:
    require_api_key(request)
    presets_data = [normalize_preset_record(preset) for preset in load_presets()]
    voices_data = load_voices()
    seen = set()
    items = []
    for preset_record in presets_data:
        label = preset_label(preset_record)
        if not label or label in seen:
            continue
        seen.add(label)
        items.append({"id": label, "object": "voice"})
    for voice in voices_data:
        if voice["id"] in seen:
            continue
        seen.add(voice["id"])
        items.append({"id": voice["id"], "object": "voice"})
    return {"object": "list", "data": items}


@app.post("/v1/audio/speech")
def speech(req: OpenAITTSSpeechRequest, request: Request) -> Response:
    require_api_key(request)
    preset = find_preset(req.voice) if req.voice else None
    if not preset and req.voice:
        preset = find_preset_by_label(req.voice, req.model or DEFAULT_TTS_ENGINE)
    voice_sample = find_voice(req.voice) if req.voice and not preset else None
    engine = resolve_engine(req, preset)
    if preset and req.model and normalize_engine_name(preset.get("engine")) != normalize_engine_name(req.model):
        raise HTTPException(status_code=400, detail="Preset engine does not match model")

    params = build_params(req, preset, voice_sample, engine)
    audio_bytes, media_type = call_ultimate_tts(engine, params)
    return Response(content=audio_bytes, media_type=media_type)
