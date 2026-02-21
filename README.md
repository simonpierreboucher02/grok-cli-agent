<div align="center">

# 🧠 Grok CLI Agent

### Multi-Model CLI Chat Agent for Grok 3, Grok 3 Mini & Grok 4

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![X.AI](https://img.shields.io/badge/X.AI-Grok-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-blueviolet?style=for-the-badge)](https://github.com/simonpierreboucher02/grok-cli-agent/releases)

<br/>

[![Models](https://img.shields.io/badge/Models-Grok%203%20%7C%20Grok%203%20Mini%20%7C%20Grok%204-green?style=flat-square&logo=x&logoColor=white)](https://x.ai/grok)
[![Streaming](https://img.shields.io/badge/Streaming-Real--time-blue?style=flat-square)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![Exports](https://img.shields.io/badge/Exports-JSON%20%7C%20TXT%20%7C%20MD%20%7C%20HTML-orange?style=flat-square)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![Multi--Agent](https://img.shields.io/badge/Multi--Agent-Persistent%20Sessions-red?style=flat-square)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![File Inclusion](https://img.shields.io/badge/File%20Inclusion-%7Bfilename%7D%20Syntax-teal?style=flat-square)](https://github.com/simonpierreboucher02/grok-cli-agent)

<br/>

[![OS: Linux](https://img.shields.io/badge/OS-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![OS: macOS](https://img.shields.io/badge/OS-macOS-000000?style=flat-square&logo=apple&logoColor=white)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![OS: Windows](https://img.shields.io/badge/OS-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![Shell](https://img.shields.io/badge/Shell-Bash%20%7C%20Zsh%20%7C%20PowerShell-4EAA25?style=flat-square&logo=gnubash&logoColor=white)](https://github.com/simonpierreboucher02/grok-cli-agent)

<br/>

[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-informational?style=flat-square)](https://peps.python.org/pep-0008/)
[![Dependencies](https://img.shields.io/badge/Dependencies-Minimal%20%283%20core%29-success?style=flat-square)](requirements.txt)
[![Storage](https://img.shields.io/badge/Storage-Local%20JSON-lightgrey?style=flat-square&logo=json&logoColor=white)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![Config](https://img.shields.io/badge/Config-YAML--based-ff69b4?style=flat-square&logo=yaml&logoColor=white)](https://github.com/simonpierreboucher02/grok-cli-agent)
[![API](https://img.shields.io/badge/API-X.AI%20REST-000000?style=flat-square&logo=x&logoColor=white)](https://x.ai)

<br/>

> **A powerful Python CLI agent for X.AI's Grok models — persistent conversations, file injection, streaming, multi-format exports, and per-agent YAML configuration.**

<br/>

[✨ Features](#-features) •
[📐 Architecture](#-architecture) •
[⚙️ Installation](#-installation) •
[🔑 API Key Setup](#-api-key-setup) •
[🚀 Usage](#-usage) •
[💬 Commands](#-interactive-commands) •
[📎 File Inclusion](#-file-inclusion) •
[⚙️ Configuration](#-configuration) •
[📊 Export Formats](#-export-formats) •
[📝 Logging](#-logging) •
[🗃️ Data Storage](#-data-storage) •
[🤝 Contributing](#-contributing) •
[👨‍💻 Authors](#-authors) •
[📄 License](#-license)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI & Models
- **Multi-Model Support** — Grok 3, Grok 3 Mini, Grok 4
- **Real-time Streaming** — Token-by-token API responses
- **Non-Streaming Mode** — Full response at once (`--no-stream`)
- **Configurable Temperature** — Fine-tune creativity (0.0–2.0)
- **Max Tokens Control** — Up to 32,768 tokens per response
- **Top-P Sampling** — Nucleus sampling support

</td>
<td width="50%">

### 💾 Persistence & Agents
- **Persistent Conversations** — History survives restarts
- **Multi-Agent Sessions** — Isolated per `--agent-id`
- **Automatic Backups** — History backed up on every session
- **Per-Agent YAML Config** — Each agent has its own settings
- **Agent Listing** — `--list` shows all agents with stats
- **Agent Info View** — `--info` shows detailed agent metadata

</td>
</tr>
<tr>
<td width="50%">

### 📁 File & Context
- **File Injection** — `{filename}` syntax embeds files into prompts
- **Broad File Support** — Python, JS, TS, Go, Rust, JSON, YAML, MD, HTML, CSS, and more
- **File Discovery** — `/files` command lists injectable files
- **Context-Aware** — Inject multiple files in one message

</td>
<td width="50%">

### 📤 Export & Reporting
- **JSON Export** — Full metadata, timestamps, and stats
- **TXT Export** — Clean plain-text transcript
- **Markdown Export** — GitHub-compatible documentation
- **HTML Export** — Responsive, styled conversation view
- **In-session Export** — `/export <format>` without quitting
- **CLI Export** — `--export` flag for scripted pipelines

</td>
</tr>
<tr>
<td width="50%">

### 🎨 UX & CLI
- **Colored Terminal** — Role-based color coding with Colorama
- **Interactive REPL** — Full command system inside chat
- **Conversation Search** — `/search <term>` across history
- **Stats Dashboard** — `/stats` shows messages, chars, duration
- **History Review** — `/history [n]` shows recent messages
- **Graceful Exit** — `/quit` with clean session save

</td>
<td width="50%">

### 🔒 Security & Config
- **Secure API Key Handling** — Env variable or encrypted secrets file
- **Isolated Agent Storage** — Per-agent directories, no cross-contamination
- **Daily Log Rotation** — Logs rotate automatically
- **Input Validation** — Type-safe argument parsing
- **Error Recovery** — Graceful handling of API and I/O errors

</td>
</tr>
</table>

---

## 📐 Architecture

```
grok-cli-agent/
├── main.py            ← CLI entry point (argparse, interactive REPL)
├── agent.py           ← GrokChatAgent class (API calls, history, search)
├── config.py          ← AgentConfig dataclass + SUPPORTED_MODELS registry
├── export.py          ← Multi-format export engine (JSON/TXT/MD/HTML)
├── utils.py           ← Colorama setup, agent listing, file discovery
├── requirements.txt   ← Minimal dependencies (requests, PyYAML, colorama)
└── agents/            ← Auto-created per-agent data directories
    └── {agent-id}/
        ├── config.yaml      ← Agent-specific model settings
        ├── history.json     ← Full conversation history
        ├── secrets.json     ← Encrypted API key (if stored locally)
        ├── backups/         ← Automatic history snapshots
        ├── logs/            ← Daily-rotated session logs
        ├── exports/         ← All exported conversation files
        └── uploads/         ← Files staged for injection
```

### Data Flow

```
User Input
    │
    ▼
main.py (parse args / REPL)
    │
    ├─── File Injection {filename} ──────► utils.py (file discovery)
    │
    ▼
agent.py (GrokChatAgent.call_api)
    │
    ├─── config.py (AgentConfig / model registry)
    │
    ▼
X.AI REST API  ─── streaming chunks ───► REPL output
    │
    ▼
history.json (persistent) + logs/
    │
    ▼
export.py (on demand) ──► JSON / TXT / MD / HTML
```

---

## ⚙️ Installation

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| pip | latest recommended |
| X.AI API Key | Required |

### Step 1 — Clone

```bash
git clone https://github.com/simonpierreboucher02/grok-cli-agent.git
cd grok-cli-agent
```

### Step 2 — Virtual Environment (recommended)

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | ≥ 2.31.0 | HTTP calls to X.AI API |
| `PyYAML` | ≥ 6.0.1 | Per-agent YAML config |
| `colorama` | ≥ 0.4.6 | Cross-platform terminal colors |

---

## 🔑 API Key Setup

### Option 1 — Environment Variable (recommended)

```bash
# Linux / macOS
export GROK_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GROK_API_KEY="your-api-key-here"

# Persistent (add to ~/.bashrc or ~/.zshrc)
echo 'export GROK_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 2 — Interactive Prompt

Run the agent without setting the env variable. It will prompt you on first launch and store the key in `agents/{agent-id}/secrets.json`.

---

## 🚀 Usage

### Start an Interactive Chat

```bash
# Grok 4 — most capable
python main.py --model grok4 --agent-id my-agent

# Grok 3 Mini — fast & lightweight
python main.py --model grok3mini --agent-id quick-chat

# Grok 3 — balanced performance
python main.py --model grok3 --agent-id research-agent
```

### Manage Agents

```bash
# List all agents with message counts and last activity
python main.py --list

# Show detailed info for a specific agent
python main.py --info my-agent --model grok4

# Interactively configure an agent
python main.py --model grok4 --agent-id my-agent --config
```

### Export Conversations

```bash
# Export as HTML (styled, shareable)
python main.py --model grok4 --agent-id my-agent --export html

# Export as JSON (full metadata)
python main.py --model grok3mini --agent-id quick-chat --export json

# Export as Markdown (GitHub-compatible)
python main.py --model grok3 --agent-id research-agent --export md

# Export as plain text
python main.py --model grok4 --agent-id my-agent --export txt
```

### Advanced Options

```bash
# Override temperature for this session
python main.py --model grok4 --agent-id my-agent --temperature 0.3

# Disable streaming (wait for full response)
python main.py --model grok4 --agent-id my-agent --no-stream

# Combine options
python main.py --model grok3 --agent-id analysis --temperature 0.1 --no-stream
```

### CLI Reference

```
usage: main.py [-h] [--model {grok3,grok3mini,grok4}] [--agent-id ID]
               [--list] [--info ID] [--config]
               [--temperature FLOAT] [--no-stream]
               [--export {json,txt,md,html}]

Arguments:
  --model       Model to use: grok3 | grok3mini | grok4
  --agent-id    Agent session identifier (persistent)
  --list        List all available agents
  --info        Show detailed info for an agent
  --config      Configure agent interactively
  --temperature Override temperature (0.0–2.0)
  --no-stream   Disable real-time streaming
  --export      Export format: json | txt | md | html
```

---

## 💬 Interactive Commands

Once inside a chat session, the following slash commands are available:

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/history [n]` | Display last `n` messages (default: 5) |
| `/search <term>` | Full-text search through conversation history |
| `/stats` | Show conversation statistics (messages, chars, duration) |
| `/config` | Display current agent configuration |
| `/export <format>` | Export conversation without leaving chat |
| `/clear` | Clear conversation history (with confirmation) |
| `/files` | List all files available for `{filename}` injection |
| `/info` | Show agent metadata and session info |
| `/quit` | Exit the chat session gracefully |

### Example Session

```
You: /stats

Conversation Statistics:
Model: grok-4
Total messages: 14
User messages: 7
Assistant messages: 7
Total characters: 8,342
Average message length: 596
First message: 2025-08-20 09:15:23
Last message: 2025-08-20 09:47:11
Duration: 31 minutes, 48 seconds

You: /search python

Found 3 results for 'python':
[09:17:01] user: Can you review {main.py} and suggest...
[09:22:45] assistant: Looking at the Python code, I notice...
[09:31:12] user: What Python version is required?

You: /export html
Exported to: agents/my-agent/exports/conversation_20250820_094820.html
```

---

## 📎 File Inclusion

Inject file contents directly into your messages using the `{filename}` syntax.

### Basic Usage

```
You: Review this code: {main.py}
You: Compare these configs: {config.yaml} and {settings.json}
You: Debug this: {src/api/handler.py}
```

### Supported File Types

| Category | Extensions |
|----------|-----------|
| Python | `.py`, `.pyi` |
| JavaScript / TypeScript | `.js`, `.ts`, `.jsx`, `.tsx` |
| Systems | `.go`, `.rs`, `.c`, `.cpp`, `.h` |
| JVM | `.java`, `.kt`, `.scala` |
| Data / Config | `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.env` |
| Markup | `.html`, `.css`, `.xml`, `.svg` |
| Documentation | `.md`, `.rst`, `.txt` |
| Shell | `.sh`, `.bash`, `.zsh`, `.ps1` |

### Tips

- Use `/files` to discover all injectable files in your working directory
- Inject multiple files in one message
- Large files are injected fully — keep context limits in mind
- Relative paths are resolved from the current working directory

---

## ⚙️ Configuration

Each agent stores its configuration in `agents/{agent-id}/config.yaml`:

```yaml
model: grok-4
temperature: 0.7
max_tokens: 32768
max_history_size: 1000
stream: true
system_prompt: "You are a helpful assistant."
top_p: 1.0
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | — | X.AI model identifier |
| `temperature` | float | `0.7` | Creativity (0.0 = deterministic, 2.0 = very creative) |
| `max_tokens` | int | `32768` | Maximum tokens per response |
| `max_history_size` | int | `1000` | Max messages kept in history |
| `stream` | bool | `true` | Enable real-time token streaming |
| `system_prompt` | string | `"You are a helpful assistant."` | Agent persona/instructions |
| `top_p` | float | `1.0` | Nucleus sampling threshold |

### Supported Models

| Key | Model ID | Best For |
|-----|----------|---------|
| `grok3` | `grok-3` | Balanced general use |
| `grok3mini` | `grok-3-mini` | Fast, cost-efficient tasks |
| `grok4` | `grok-4` | Complex reasoning, long context |

---

## 📊 Export Formats

| Format | Flag | Output | Best For |
|--------|------|--------|---------|
| JSON | `--export json` | Full metadata, messages, stats as structured JSON | Programmatic processing, archiving |
| TXT | `--export txt` | Plain-text timestamped transcript | Reading, printing |
| Markdown | `--export md` | GitHub-flavored Markdown with headers | Documentation, sharing on GitHub |
| HTML | `--export html` | Responsive, styled, self-contained HTML page | Sharing with non-technical users |

Exports are saved to: `agents/{agent-id}/exports/conversation_{timestamp}.{ext}`

---

## 📝 Logging

Logs are stored per-agent in `agents/{agent-id}/logs/`:

```
agents/my-agent/logs/
├── agent_20250820.log
├── agent_20250821.log
└── agent_20250822.log
```

- **Daily rotation** — new log file each day
- **Log levels** — `INFO`, `WARNING`, `ERROR`
- **Tracked events** — API requests, responses, errors, config changes, exports
- **Timestamps** — ISO 8601 format on every line

---

## 🗃️ Data Storage

All data is stored locally under `agents/`:

```
agents/
└── {agent-id}/
    ├── config.yaml        ← YAML agent configuration
    ├── history.json       ← Full conversation history (messages + metadata)
    ├── secrets.json       ← API key (if stored locally)
    ├── backups/           ← Auto-snapshots of history.json
    │   └── history_backup_{timestamp}.json
    ├── logs/              ← Daily-rotated session logs
    │   └── agent_{date}.log
    ├── exports/           ← All exported conversation files
    │   ├── conversation_{timestamp}.html
    │   ├── conversation_{timestamp}.json
    │   └── conversation_{timestamp}.md
    └── uploads/           ← Files staged for injection
```

> **Privacy note:** All data stays on your local machine. Nothing is sent to any server except the X.AI API for model inference.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a branch** — `git checkout -b feature/your-feature-name`
3. **Implement** your feature or fix
4. **Test** your changes thoroughly
5. **Commit** with a clear message — `git commit -m "feat: add XYZ"`
6. **Push** — `git push origin feature/your-feature-name`
7. **Open a Pull Request** against `main`

### Ideas for Contributions

- [ ] Additional export formats (PDF, DOCX)
- [ ] Plugin system for custom commands
- [ ] Conversation branching
- [ ] Web UI companion
- [ ] Token usage tracking per message
- [ ] Prompt templates / personas library

---

## 👨‍💻 Authors

<table>
<tr>
<td align="center" width="50%">

### Simon-Pierre Boucher
**Creator & Lead Developer**

[![Email](https://img.shields.io/badge/Email-spbou4%40protonmail.com-6D4AFF?style=for-the-badge&logo=protonmail&logoColor=white)](mailto:spbou4@protonmail.com)
[![Website](https://img.shields.io/badge/Website-www.spboucher.ai-0A66C2?style=for-the-badge&logo=safari&logoColor=white)](https://www.spboucher.ai)
[![GitHub](https://img.shields.io/badge/GitHub-simonpierreboucher02-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/simonpierreboucher02)

*Python developer, AI systems architect, and real estate technology innovator.*

</td>
<td align="center" width="50%">

### Claude (Anthropic)
**AI Co-Author & Documentation**

[![Anthropic](https://img.shields.io/badge/Anthropic-Claude-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Model](https://img.shields.io/badge/Model-Claude%20Sonnet%204.6-orange?style=for-the-badge)](https://anthropic.com/claude)

*AI assistant that helped architect, document, and refine this project.*
*Powered by Claude Code — Anthropic's official CLI for Claude.*

</td>
</tr>
</table>

---

## 📄 License

```
MIT License

Copyright (c) 2025 Simon-Pierre Boucher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Built with Python 🐍 + X.AI Grok 🤖 + Claude Code ✨**

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Powered by Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?style=flat-square&logo=x&logoColor=white)](https://x.ai/grok)
[![Docs by Claude](https://img.shields.io/badge/Docs%20by-Claude%20Code-CC785C?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com/claude-code)

*© 2025 Simon-Pierre Boucher — [spbou4@protonmail.com](mailto:spbou4@protonmail.com) — [www.spboucher.ai](https://www.spboucher.ai)*

</div>
