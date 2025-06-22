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
INFO:     Will watch for changes in these directories: ['/Volumes/Dock SSD/vscode-ideapad/packages/ideapad-backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [31202] using StatReload
INFO:     Started server process [31204]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60699 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:60702 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60742 - "GET /api/chat/health HTTP/1.1" 200 OK
INFO:     127.0.0.1:60746 - "GET /api/chat/health HTTP/1.1" 200 OK
INFO:     127.0.0.1:60778 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:60778 - "GET /openapi.json HTTP/1.1" 200 OK
```