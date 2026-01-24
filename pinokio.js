module.exports = {
  version: "3.7",
  title: "API for TTS",
  description: "OpenAI-compatible TTS proxy for Ultimate TTS Studio.",
  menu: async (kernel, info) => {
    const installed = info.exists("app/env")
    const running = {
      install: info.running("install.js"),
      start: info.running("start.js"),
      update: info.running("update.js"),
      reset: info.running("reset.js")
    }

    if (running.install) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Installing",
        href: "install.js"
      }]
    }

    if (!installed) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.js"
      }]
    }

    if (running.start) {
      const local = info.local("start.js")
      if (local && local.url) {
        return [{
          default: true,
          icon: "fa-solid fa-rocket",
          text: "Open API",
          href: local.url
        }, {
          icon: "fa-solid fa-sliders",
          text: "Open Voice Manager",
          href: local.url + "/ui"
        }, {
          icon: "fa-solid fa-book",
          text: "Open Docs",
          href: local.url + "/docs"
        }, {
          icon: "fa-solid fa-terminal",
          text: "Terminal",
          href: "start.js"
        }]
      }
      return [{
        default: true,
        icon: "fa-solid fa-terminal",
        text: "Terminal",
        href: "start.js"
      }]
    }

    if (running.update) {
      return [{
        default: true,
        icon: "fa-solid fa-terminal",
        text: "Updating",
        href: "update.js"
      }]
    }

    if (running.reset) {
      return [{
        default: true,
        icon: "fa-solid fa-terminal",
        text: "Resetting",
        href: "reset.js"
      }]
    }

    return [{
      default: true,
      icon: "fa-solid fa-power-off",
      text: "Start",
      href: "start.js",
      params: {
        gradio_url: "http://127.0.0.1:7860/",
        tts_engine: "Chatterbox Turbo",
        audio_format: "mp3",
        gradio_api_name: "/generate_unified_tts"
      }
    }, {
      icon: "fa-solid fa-plug",
      text: "Install",
      href: "install.js"
    }, {
      icon: "fa-solid fa-rotate",
      text: "Update",
      href: "update.js"
    }, {
      icon: "fa-regular fa-circle-xmark",
      text: "Reset",
      href: "reset.js",
      confirm: "Are you sure you wish to reset the proxy environment?"
    }]
  }
}
