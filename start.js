module.exports = {
  daemon: true,
  run: [
    {
      method: "local.set",
      params: {
        proxy_port: "{{envs.PROXY_PORT ? envs.PROXY_PORT : (args.proxy_port ? args.proxy_port : '42025')}}"
      }
    },
    {
      method: "shell.run",
      params: {
        venv: "env",
        env: {
          "GRADIO_URL": "{{envs.GRADIO_URL ? envs.GRADIO_URL : (args.gradio_url ? args.gradio_url : 'http://127.0.0.1:7860/')}}",
          "DEFAULT_TTS_ENGINE": "{{envs.DEFAULT_TTS_ENGINE ? envs.DEFAULT_TTS_ENGINE : (args.tts_engine ? args.tts_engine : 'Chatterbox Turbo')}}",
          "DEFAULT_FORMAT": "{{envs.DEFAULT_FORMAT ? envs.DEFAULT_FORMAT : (args.audio_format ? args.audio_format : 'mp3')}}",
          "GRADIO_API_NAME": "{{envs.GRADIO_API_NAME ? envs.GRADIO_API_NAME : (args.gradio_api_name ? args.gradio_api_name : '/generate_unified_tts')}}",
          "CHATTERBOX_TURBO_REF_AUDIO": "{{envs.CHATTERBOX_TURBO_REF_AUDIO ? envs.CHATTERBOX_TURBO_REF_AUDIO : (args.chatterbox_turbo_ref_audio ? args.chatterbox_turbo_ref_audio : '')}}",
          "AUTO_LOAD_ENGINE": "{{envs.AUTO_LOAD_ENGINE ? envs.AUTO_LOAD_ENGINE : 'true'}}",
          "LOG_LEVEL": "{{envs.LOG_LEVEL ? envs.LOG_LEVEL : 'INFO'}}",
          "ADMIN_USERNAME": "{{envs.ADMIN_USERNAME ? envs.ADMIN_USERNAME : ''}}",
          "ADMIN_PASSWORD": "{{envs.ADMIN_PASSWORD ? envs.ADMIN_PASSWORD : ''}}",
          "HF_HUB_DISABLE_TELEMETRY": "1",
          "GRADIO_ANALYTICS_ENABLED": "False",
          "GRADIO_TELEMETRY": "0"
        },
        path: "app",
        message: [
          "python -m uvicorn tts_proxy:app --host 0.0.0.0 --port {{local.proxy_port}}"
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
