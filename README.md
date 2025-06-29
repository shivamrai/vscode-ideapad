# vscode-ideapad

A VS Code extension for local LLM interaction using [`llama.cpp`](https://github.com/ggerganov/llama.cpp), served via a Python FastAPI backend and integrated into a modern React-based webview interface.

This extension is meant for local, secure, offline inference workflows and serves as a hobby project. Future enhancements may include performance optimization via a Go backend.

---

```
vscode-ideapad/
├── packages/
│   ├── ideapad-extension/      # VS Code Extension Host (TypeScript)
│   │   ├── src/                # extension.ts and helpers
│   │   ├── package.json        # VS Code extension manifest
│   │   └── tsconfig.json
│   ├── ideapad-webview/        # Webview UI (React + Vite/webpack)
│   │   ├── public/
│   │   ├── src/
│   │   └── vite.config.ts
│   └── ideapad-backend/        # Python backend (FastAPI + llama-cpp-python)
│       ├── main.py
│       ├── requirements.txt
│       └── model_config.json
├── dist/                       # Compiled .vsix and build artifacts
├── scripts/                    # Build/packaging scripts
│   └── build-extension.sh
├── .vscode/                    # Launch/debug configs
│   └── launch.json
├── .gitignore
└── README.md
```
For backend testing run 
```
(vscode-ideapad) ➜  ideapad-backend git:(main) ✗ uvicorn main:app --reload
```
Use the following info to check service health.
```http://127.0.0.1:8000/api/chat/health```
Use the following to access backend paths
```http://localhost:8000/docs```

Happy Hacking :)
Download models for now from https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF in gguf format, star their project.
