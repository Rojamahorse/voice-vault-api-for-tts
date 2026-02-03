import json
import logging
import os
import re
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query, Request, Depends
from fastapi.responses import Response, HTMLResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import httpx
from gradio_client import Client, handle_file

DEFAULT_GRADIO_URL = "http://127.0.0.1:7860/"
GRADIO_URL = os.environ.get("GRADIO_URL", DEFAULT_GRADIO_URL)
DEFAULT_TTS_ENGINE = os.environ.get("DEFAULT_TTS_ENGINE", "Chatterbox Turbo")
DEFAULT_FORMAT = os.environ.get("DEFAULT_FORMAT", "mp3")
GRADIO_API_NAME = os.environ.get("GRADIO_API_NAME", "/generate_unified_tts")
CHATTERBOX_TURBO_REF_AUDIO = os.environ.get("CHATTERBOX_TURBO_REF_AUDIO", "")
AUTO_LOAD_ENGINE = os.environ.get("AUTO_LOAD_ENGINE", "true").lower() in (
    "1",
    "true",
    "yes",
    "on",
)
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

KNOWN_ENGINES = [
    "ChatterboxTTS",
    "Chatterbox Multilingual",
    "Chatterbox Turbo",
    "Kokoro TTS",
    "Fish Speech",
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
    "Fish Speech": "/handle_load_fish",
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
    "Fish Speech": "fish_",
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
    "Fish Speech": "fish_ref_audio",
    "IndexTTS": "indextts_ref_audio",
    "IndexTTS2": "indextts2_ref_audio",
    "F5-TTS": "f5_ref_audio",
    "Higgs Audio": "higgs_ref_audio",
    "VoxCPM": "voxcpm_ref_audio",
    "Qwen Voice Clone": "qwen_ref_audio",
}

REQUIRED_REF_ENGINES = {
    "IndexTTS2",
    "Qwen Voice Clone",
}

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

LOADED_ENGINE = None
DEFAULT_PARAMS = None
DEFAULT_PARAM_META = None
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
UI_INDEX = APP_DIR / "ui" / "index.html"

FILE_PARAM_NAMES = {
    "audio_file",
    "files",
    "chatterbox_ref_audio",
    "chatterbox_mtl_ref_audio",
    "chatterbox_turbo_ref_audio",
    "fish_ref_audio",
    "indextts_ref_audio",
    "indextts2_ref_audio",
    "indextts2_emotion_audio",
    "f5_ref_audio",
    "higgs_ref_audio",
    "voxcpm_ref_audio",
    "qwen_ref_audio",
}

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
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


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
    lines = []
    replaced = False
    if ENV_FILE.exists():
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    new_lines = []
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


def find_preset(name: str) -> Optional[dict]:
    name = name.strip()
    for preset in load_presets():
        if preset.get("name") == name:
            return preset
    return None


def preset_label(preset: dict) -> str:
    return str(preset.get("label") or preset.get("name") or "").strip()


def find_preset_by_label(label: str, engine: Optional[str]) -> Optional[dict]:
    target = label.strip().lower()
    if not target:
        return None
    presets = [preset for preset in load_presets() if preset_label(preset).lower() == target]
    if not presets:
        return None
    if engine:
        for preset in presets:
            if preset.get("engine") == engine:
                return preset
    if len(presets) == 1:
        return presets[0]
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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def normalize_gradio_url(url: str, default_url: str = DEFAULT_GRADIO_URL) -> str:
    cleaned = url.strip()
    if not cleaned:
        return default_url
    if not re.match(r"^https?://", cleaned):
        cleaned = f"http://{cleaned}"
    if not cleaned.endswith("/"):
        cleaned = f"{cleaned}/"
    return cleaned

GRADIO_URL = normalize_gradio_url(GRADIO_URL)
apply_gradio_env_override()

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

class OpenAITTSSpeechRequest(BaseModel):
    model: Optional[str] = None
    input: str
    voice: Optional[str] = None
    response_format: Optional[str] = None
    speed: Optional[float] = None


def resolve_engine(req: OpenAITTSSpeechRequest, preset: Optional[dict]) -> str:
    supported = list_supported_engines()
    if req.model and req.model in supported:
        return req.model
    if preset:
        return preset.get("engine", DEFAULT_TTS_ENGINE)
    if req.voice and req.voice in supported:
        return req.voice
    return DEFAULT_TTS_ENGINE


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
        if isinstance(preset_format, str):
            preset_format = preset_format.lower()
            if preset_format in ("mp3", "wav"):
                return preset_format
    return DEFAULT_FORMAT


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
        message = f"Gradio API not reachable at {GRADIO_URL}. Start the TTS service and click Reconnect."
        logger.warning("Failed to fetch Gradio info: %s", exc)
        return {}, {}, message, False

    data = resp.json()
    endpoints = data.get("named_endpoints") or {}
    endpoint = endpoints.get(GRADIO_API_NAME)
    if not endpoint:
        message = f"Gradio endpoint {GRADIO_API_NAME} not found at {GRADIO_URL}. Update GRADIO_API_NAME or target."
        logger.warning("Endpoint %s not found in Gradio info", GRADIO_API_NAME)
        return {}, {}, message, False

    params = endpoint.get("parameters_info") or endpoint.get("parameters") or []
    defaults = {}
    meta = {}
    for raw_param in params:
        param = normalize_param(raw_param)
        if not param:
            continue
        name = (
            param.get("name")
            or param.get("parameter_name")
            or param.get("label")
        )
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
    return defaults, meta, "Loaded from Gradio metadata.", True


def get_engine_choices_from_meta() -> list[str]:
    if DEFAULT_PARAM_META is None or not DEFAULT_PARAM_META:
        get_default_params()
    meta = DEFAULT_PARAM_META or {}
    engine_meta = meta.get("tts_engine") or {}
    choices = engine_meta.get("choices") or []
    if isinstance(choices, list):
        return [str(choice) for choice in choices if str(choice).strip()]
    return []


def list_supported_engines() -> list[str]:
    engines = list(KNOWN_ENGINES)
    for choice in get_engine_choices_from_meta():
        if choice not in engines:
            engines.append(choice)
    return engines


def coerce_value(value, python_type: Optional[str]):
    if value is None or python_type is None:
        return value
    if python_type == "float" and isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return value
    if python_type == "int" and isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return value
    if python_type == "bool" and isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("1", "true", "yes", "on"):
            return True
        if lowered in ("0", "false", "no", "off"):
            return False
    return value


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return False


def is_numeric_string(value: str) -> bool:
    return bool(re.match(r"^\s*-?\d+(\.\d+)?([eE][-+]?\d+)?\s*$", value))


def get_default_params(force_refresh: bool = False) -> dict:
    global DEFAULT_PARAMS, DEFAULT_PARAM_META, GRADIO_STATUS
    if force_refresh or DEFAULT_PARAMS is None or DEFAULT_PARAM_META is None or not DEFAULT_PARAMS:
        defaults, meta, message, connected = fetch_default_params()
        DEFAULT_PARAMS = defaults
        DEFAULT_PARAM_META = meta
        GRADIO_STATUS = {"connected": connected, "message": message, "url": GRADIO_URL}
    defaults = DEFAULT_PARAMS.copy()
    for key, value in defaults.items():
        if value == "" and (
            key in FILE_PARAM_NAMES
            or key.endswith("_ref_audio")
            or key.endswith("_emotion_audio")
        ):
            defaults[key] = None
        if value == "" and key.endswith("_language"):
            defaults[key] = "en"
        meta = DEFAULT_PARAM_META.get(key, {})
        component = meta.get("component")
        if value == "" and component == "Checkbox":
            defaults[key] = False
        if isinstance(defaults[key], str) and component == "Checkbox":
            lowered = defaults[key].strip().lower()
            if lowered in ("true", "1", "yes", "on"):
                defaults[key] = True
            elif lowered in ("false", "0", "no", "off", ""):
                defaults[key] = False
        if value == "" and component in ("Slider", "Number"):
            if "seed" in key:
                defaults[key] = None
            else:
                defaults[key] = None
        if value == "":
            choices = meta.get("choices") or []
            if choices:
                defaults[key] = choices[0]
        defaults[key] = coerce_value(defaults[key], meta.get("python_type"))
        if isinstance(defaults[key], str) and is_numeric_string(defaults[key]):
            if meta.get("type") == "number" or meta.get("component") in (
                "Slider",
                "Number",
            ):
                try:
                    defaults[key] = float(defaults[key])
                except ValueError:
                    logger.warning("Failed to coerce %s=%r", key, defaults[key])
        if isinstance(defaults[key], str) and is_numeric_string(defaults[key]):
            try:
                defaults[key] = float(defaults[key])
            except ValueError:
                logger.warning("Failed to coerce numeric string %s=%r", key, defaults[key])
        if meta.get("type") == "number" or meta.get("component") in ("Slider", "Number"):
            if isinstance(defaults[key], str):
                raw_default = meta.get("raw_default")
                if isinstance(raw_default, (int, float)):
                    defaults[key] = float(raw_default)
                elif is_numeric_string(raw_default if isinstance(raw_default, str) else ""):
                    defaults[key] = float(raw_default)
                else:
                    defaults[key] = None
    return defaults


def list_param_specs(engine: Optional[str] = None) -> list[dict]:
    defaults = get_default_params()
    meta = DEFAULT_PARAM_META or {}
    params: list[dict] = []
    prefix = ENGINE_PARAM_PREFIX.get(engine, "") if engine else ""
    for name, value in defaults.items():
        if name in ("text_input", "tts_engine"):
            continue
        if engine and prefix and not name.startswith(prefix) and name != "audio_format":
            continue
        info = meta.get(name, {})
        choices = info.get("choices") or PARAM_CHOICES.get(name)
        is_file = (
            name in FILE_PARAM_NAMES
            or name.endswith("_ref_audio")
            or name.endswith("_emotion_audio")
        )
        params.append({
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
        })
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
    def meta_choices(param_name: str) -> list[str]:
        if DEFAULT_PARAM_META is None or not DEFAULT_PARAM_META:
            get_default_params()
        meta = DEFAULT_PARAM_META or {}
        info = meta.get(param_name) or {}
        choices = info.get("choices") or []
        if isinstance(choices, list):
            return [str(choice) for choice in choices if str(choice).strip()]
        return []

    if engine == "Kokoro TTS":
        return {"param": ENGINE_VOICE_PARAM[engine], "choices": fetch_kokoro_voice_choices()}
    if engine in ENGINE_VOICE_PARAM:
        param = ENGINE_VOICE_PARAM[engine]
        choices = meta_choices(param)
        if choices:
            return {"param": param, "choices": choices}
    if engine == "KittenTTS":
        return {"param": ENGINE_VOICE_PARAM[engine], "choices": KITTEN_VOICES}
    if engine == "Higgs Audio":
        return {"param": ENGINE_VOICE_PARAM[engine], "choices": ["EMPTY"]}
    return {"param": "", "choices": []}


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
    engine = engine if engine in list_supported_engines() else None
    get_default_params()
    status = GRADIO_STATUS.copy()
    return {"params": list_param_specs(engine), "message": status.get("message"), "connected": status.get("connected"), "gradio_url": status.get("url")}


@app.get("/v1/tts/gradio", dependencies=[Depends(require_admin)])
def gradio_status() -> dict:
    get_default_params()
    status = GRADIO_STATUS.copy()
    return {"connected": status.get("connected"), "message": status.get("message"), "gradio_url": status.get("url")}


@app.post("/v1/tts/gradio", dependencies=[Depends(require_admin)])
def set_gradio(payload: dict) -> dict:
    global GRADIO_URL, GRADIO_STATUS
    url = str(payload.get("url", "")).strip()
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
    GRADIO_URL = normalize_gradio_url(url)
    os.environ["GRADIO_URL"] = GRADIO_URL
    persist_env_value("GRADIO_URL", GRADIO_URL)
    reset_gradio_cache()
    get_default_params(force_refresh=True)
    status = GRADIO_STATUS.copy()
    return {"status": "updated", "connected": status.get("connected"), "message": status.get("message"), "gradio_url": status.get("url"), "params": list_param_specs()}


@app.post("/v1/tts/gradio/reload", dependencies=[Depends(require_admin)])
def reload_gradio() -> dict:
    global GRADIO_URL
    env_value = read_env_value("GRADIO_URL")
    if env_value:
        GRADIO_URL = normalize_gradio_url(env_value)
    else:
        GRADIO_URL = normalize_gradio_url(DEFAULT_GRADIO_URL)
    os.environ["GRADIO_URL"] = GRADIO_URL
    reset_gradio_cache()
    get_default_params(force_refresh=True)
    status = GRADIO_STATUS.copy()
    return {"status": "reloaded", "connected": status.get("connected"), "message": status.get("message"), "gradio_url": status.get("url"), "params": list_param_specs()}


@app.get("/v1/tts/voice-choices", dependencies=[Depends(require_admin)])
def voice_choices(engine: str = Query(...)) -> dict:
    if engine not in list_supported_engines():
        raise HTTPException(status_code=400, detail="Unknown engine")
    return fetch_voice_choices(engine)


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
def create_voice(
    name: str = Form(default=""),
    file: UploadFile = File(...),
) -> dict:
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
    }
    voices.append(voice_data)
    save_voices(voices)
    return {"voice": voice_data}


@app.delete("/v1/tts/voices/{voice_id}", dependencies=[Depends(require_admin)])
def delete_voice(voice_id: str) -> dict:
    voices = load_voices()
    presets = load_presets()
    if any(preset.get("voice_id") == voice_id for preset in presets):
        raise HTTPException(status_code=409, detail="Voice is used by a preset")

    voice = next((v for v in voices if v.get("id") == voice_id), None)
    remaining = [voice for voice in voices if voice.get("id") != voice_id]
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
    return {"presets": load_presets()}


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
    engine = payload.get("engine")
    if not name:
        raise HTTPException(status_code=400, detail="Preset name is required")
    if engine not in list_supported_engines():
        raise HTTPException(status_code=400, detail="Unknown engine")
    voice_id = payload.get("voice_id")
    if voice_id and not find_voice(voice_id):
        raise HTTPException(status_code=400, detail="Unknown voice_id")
    params = payload.get("params") or {}
    if not isinstance(params, dict):
        raise HTTPException(status_code=400, detail="Params must be an object")

    overwrite = parse_bool(payload.get("overwrite"))
    existing = find_preset(name)
    if existing and not overwrite:
        raise HTTPException(status_code=409, detail="Preset already exists")

    if not label:
        label = name

    presets = load_presets()
    presets = [preset for preset in presets if preset.get("name") != name]
    presets.append({
        "name": name,
        "label": label,
        "engine": engine,
        "voice_id": voice_id,
        "params": params,
        "updated_at": now_iso(),
    })
    save_presets(presets)
    return {"preset": find_preset(name)}


@app.delete("/v1/tts/presets/{preset_name}", dependencies=[Depends(require_admin)])
def delete_preset(preset_name: str) -> dict:
    presets = load_presets()
    remaining = [preset for preset in presets if preset.get("name") != preset_name]
    if len(remaining) == len(presets):
        raise HTTPException(status_code=404, detail="Preset not found")
    save_presets(remaining)
    return {"status": "deleted"}


@app.get("/v1/models")
def models(request: Request) -> dict:
    require_api_key(request)
    engines = list_supported_engines()
    return {
        "object": "list",
        "data": [{"id": engine, "object": "model"} for engine in engines],
    }


@app.get("/v1/audio/models")
def audio_models(request: Request) -> dict:
    require_api_key(request)
    return models(request)


@app.get("/v1/audio/voices")
def audio_voices(request: Request) -> dict:
    require_api_key(request)
    presets = load_presets()
    voices = load_voices()
    seen = set()
    items = []
    for preset in presets:
        label = preset_label(preset)
        if not label or label in seen:
            continue
        seen.add(label)
        items.append({"id": label, "object": "voice"})
    for voice in voices:
        if voice["id"] in seen:
            continue
        seen.add(voice["id"])
        items.append({"id": voice["id"], "object": "voice"})
    return {
        "object": "list",
        "data": items,
    }


@app.post("/v1/audio/speech")
def speech(req: OpenAITTSSpeechRequest, request: Request) -> Response:
    require_api_key(request)
    text = (req.input or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'input' text")

    preset = find_preset(req.voice) if req.voice else None
    if not preset and req.voice:
        preset = find_preset_by_label(req.voice, req.model or DEFAULT_TTS_ENGINE)
    voice_sample = find_voice(req.voice) if req.voice and not preset else None
    tts_engine = resolve_engine(req, preset)
    if preset and req.model and preset.get("engine") != req.model:
        raise HTTPException(status_code=400, detail="Preset engine does not match model")

    out_fmt = resolve_output_format(req, preset)

    defaults = get_default_params()
    params = defaults.copy()
    if preset and isinstance(preset.get("params"), dict):
        params.update(preset["params"])
    params.update({
        "text_input": text,
        "tts_engine": tts_engine,
        "audio_format": out_fmt,
    })

    if voice_sample:
        ref_param = ENGINE_REF_PARAM.get(tts_engine)
        if ref_param:
            params[ref_param] = handle_file(str(resolve_voice_path(voice_sample)))

    if preset and preset.get("voice_id"):
        ref_param = ENGINE_REF_PARAM.get(tts_engine)
        if ref_param:
            voice = find_voice(preset["voice_id"])
            if voice:
                params[ref_param] = handle_file(str(resolve_voice_path(voice)))

    if req.voice and not preset and tts_engine in ENGINE_VOICE_PARAM:
        voice_param = ENGINE_VOICE_PARAM[tts_engine]
        if voice_param and req.voice:
            params[voice_param] = req.voice

    for key, value in list(params.items()):
        if (
            key in FILE_PARAM_NAMES
            or key.endswith("_ref_audio")
            or key.endswith("_emotion_audio")
        ):
            resolved = resolve_voice_reference(value) if isinstance(value, str) else None
            if resolved:
                params[key] = handle_file(resolved)
            elif value in ("", None):
                params[key] = None

    required_ref_param = ENGINE_REF_PARAM.get(tts_engine)
    if tts_engine in REQUIRED_REF_ENGINES and required_ref_param:
        if not params.get(required_ref_param):
            raise HTTPException(
                status_code=400,
                detail=f"Reference audio is required for {tts_engine}. Save a voice sample and attach it to the preset.",
            )

    if CHATTERBOX_TURBO_REF_AUDIO:
        if not os.path.isfile(CHATTERBOX_TURBO_REF_AUDIO):
            raise HTTPException(
                status_code=500,
                detail="CHATTERBOX_TURBO_REF_AUDIO path does not exist",
            )
        params["chatterbox_turbo_ref_audio"] = handle_file(
            CHATTERBOX_TURBO_REF_AUDIO
        )

    try:
        client = Client(GRADIO_URL)
        if AUTO_LOAD_ENGINE and ENGINE_LOAD_API.get(tts_engine):
            global LOADED_ENGINE
            if LOADED_ENGINE != tts_engine:
                logger.info("Loading engine: %s", tts_engine)
                client.predict(api_name=ENGINE_LOAD_API[tts_engine])
                LOADED_ENGINE = tts_engine
        result = client.predict(api_name=GRADIO_API_NAME, **params)
    except Exception as exc:
        safe_params = {}
        for key, value in params.items():
            if key in FILE_PARAM_NAMES or key.endswith("_ref_audio") or key.endswith("_emotion_audio"):
                safe_params[key] = "file"
            else:
                safe_params[key] = value
        logger.exception("Gradio call failed for engine %s with params %s", tts_engine, safe_params)
        raise HTTPException(status_code=502, detail=f"Gradio call failed: {exc}")

    audio_path = result[0] if isinstance(result, (list, tuple)) else result
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=502, detail="No audio file returned")

    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    media_type = "audio/mpeg" if out_fmt == "mp3" else "audio/wav"
    return Response(content=audio_bytes, media_type=media_type)
