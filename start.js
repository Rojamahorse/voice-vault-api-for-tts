module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        env: {
          "GRADIO_URL": "{{args.gradio_url ? args.gradio_url : 'http://127.0.0.1:7860/'}}",
          "DEFAULT_TTS_ENGINE": "{{args.tts_engine ? args.tts_engine : 'Chatterbox Turbo'}}",
          "DEFAULT_FORMAT": "{{args.audio_format ? args.audio_format : 'mp3'}}",
          "GRADIO_API_NAME": "{{args.gradio_api_name ? args.gradio_api_name : '/generate_unified_tts'}}",
          "CHATTERBOX_TURBO_REF_AUDIO": "{{args.chatterbox_turbo_ref_audio ? args.chatterbox_turbo_ref_audio : ''}}",
          "HF_HUB_DISABLE_TELEMETRY": "1",
          "GRADIO_ANALYTICS_ENABLED": "False",
          "GRADIO_TELEMETRY": "0"
        },
        path: "app",
        message: [
          "python -m uvicorn tts_proxy:app --host 0.0.0.0 --port {{port}}"
        ],
        on: [{
          "event": "/(http:\/\/[0-9.:]+)/",
          "done": true
        }]
      }
    },
    {
      method: "local.set",
      params: {
        url: "{{input.event[1]}}"
      }
    }
  ]
}
