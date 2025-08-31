# 🧠 Grok Multi-Model CLI Chat Agent  

**👨‍💻 Author: Simon-Pierre Boucher**  

<div align="center">  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)  
![XAI](https://img.shields.io/badge/X.AI-Grok-green?logo=x&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-yellow)  
![Version](https://img.shields.io/badge/Version-1.0.0-purple)  

**A Python CLI agent for Grok models (Grok 3, Grok 3 Mini, Grok 4)**  
*Persistent conversations, file inclusion, multi-format exports, and modular design*  

[✨ Features](#-features) • [⚙️ Installation](#-installation) • [🚀 Usage](#-usage) • [💬 Commands](#-interactive-commands) • [📎 File Inclusion](#-file-inclusion) • [⚙️ Configuration](#-configuration) • [📊 Export Formats](#-export-formats) • [📝 Logging](#-logging) • [🗃️ Data Storage](#-data-storage) • [🤝 Contributing](#-contributing) • [📄 License](#-license)  

</div>  

---

## ✨ Features  

- 🔹 **Multi-Model Support**: Grok 3, Grok 3 Mini, Grok 4  
- 💬 **Persistent Conversations**: History with backups  
- 📁 **File Inclusion**: `{filename}` syntax  
- 🌊 **Streaming & Non-Streaming**: Real-time API responses  
- 📤 **Multi-format Export**: JSON, TXT, Markdown, HTML  
- 🎨 **Interactive CLI**: Colored, intuitive commands  
- ⚙️ **Per-Agent Config**: YAML-based customization  
- 🔑 **Secure API Key Handling**  
- 📝 **Detailed Logging & Stats**  

---

## ⚙️ Installation  

Clone the repository:  
```bash
git clone https://github.com/simonpierreboucher02/grok-cli-agent.git
cd grok-cli-agent
```

Create and activate a virtual environment (recommended):  
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Setup  

Set your Grok API key:  

**Option 1: Env variable (recommended)**  
```bash
export GROK_API_KEY="your-api-key-here"
```  

**Option 2: Interactive Prompt**  
The agent will ask for your key on first run and save it securely.  

---

## 🚀 Usage  

### Start interactive chat  
```bash
python main.py --model grok4 --agent-id my-agent
python main.py --model grok3mini --agent-id test-agent
python main.py --model grok3 --agent-id research-agent
```  

### Manage agents  
```bash
python main.py --list
python main.py --info my-agent --model grok4
python main.py --model grok4 --agent-id my-agent --config
```  

### Export conversations  
```bash
python main.py --model grok4 --agent-id my-agent --export html
python main.py --model grok3mini --agent-id test --export json
python main.py --model grok3 --agent-id research --export md
```  

### Advanced options  
```bash
python main.py --model grok4 --agent-id my-agent --temperature 0.7
python main.py --model grok4 --agent-id my-agent --no-stream
```  

---

## 💬 Interactive Commands  

- `/help` → Show commands  
- `/history [n]` → Show last n messages  
- `/search <term>` → Search history  
- `/stats` → Show conversation stats  
- `/config` → Current config  
- `/export <format>` → Export chat  
- `/clear` → Clear history  
- `/files` → List files  
- `/info` → Show agent info  
- `/quit` → Exit chat  

---

## 📎 File Inclusion  

```
Review code: {main.py}  
Analyze configs: {config.yaml} {settings.json}  
```  

Supported: `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.json`, `.yaml`, `.md`, `.txt`, `.html`, `.css`, etc.  

---

## ⚙️ Configuration  

Each agent stores config in `agents/{agent-id}/config.yaml`:  

```yaml
model: grok4
temperature: 0.7
max_tokens: 32768
max_history_size: 1000
stream: true
system_prompt: "You are a helpful assistant."
top_p: 1.0
```  

---

## 📊 Export Formats  

- **JSON** → Full metadata & stats  
- **TXT** → Plain text logs  
- **Markdown** → GitHub-compatible docs  
- **HTML** → Responsive styled output  

---

## 📝 Logging  

Logs are stored per agent in `agents/{agent-id}/logs/`:  
- Daily rotated logs  
- INFO, WARNING, ERROR levels  
- Detailed request/response tracking  

---

## 🗃️ Data Storage  

```
agents/{agent-id}/
├── config.yaml
├── history.json
├── secrets.json
├── backups/
├── logs/
├── exports/
└── uploads/
```  

---

## 🤝 Contributing  

1. Fork repo  
2. Create feature branch  
3. Implement feature/fix  
4. Add tests if needed  
5. Submit PR  

---

## 📄 License  

MIT License — professional & educational use.  

---

**2025-08-29**  
*Université Laval*  
