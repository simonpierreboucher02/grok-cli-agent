# Grok Multi-Model Chat Agent

A Python CLI chat agent for **grok3**, **grok3mini**, and **grok4** models with the following characteristics:

## 📁 Project Structure

```
grok/
├── main.py              # CLI entry point with argument parsing
├── agent.py             # Core chat agent implementation
├── config.py            # Configuration management with dataclasses
├── utils.py             # Utilities for directories, logging, backups
├── export.py            # Multi-format conversation export (JSON/TXT/MD/HTML)
├── agents/              # Per-agent data storage (config, history, logs, exports)
│   └── {agent-id}/
│       ├── config.yaml  # Agent configuration
│       ├── history.json # Conversation history
│       ├── secrets.json # API keys (auto-generated, gitignored)
│       ├── backups/     # Automatic backups
│       ├── logs/        # Daily log files
│       ├── exports/     # Exported conversations
│       └── uploads/     # File uploads for inclusion
└── README.md
```

## 🚀 Features

- **Multi-Model Support**: Choose between Grok 3, Grok 3 Mini, and Grok 4
- **Persistent Conversations**: Automatic history saving with backups
- **File Inclusion**: Include programming files using `{filename}` syntax
- **Streaming & Non-Streaming**: Real-time response streaming support
- **Multi-Format Export**: Export conversations as JSON, TXT, Markdown, or HTML
- **Interactive CLI**: Rich command interface with colored output
- **Configuration Management**: Per-agent customizable settings
- **Secure API Key Storage**: Environment variables or encrypted local storage
- **Comprehensive Logging**: Detailed logging with rotation
- **Search & Statistics**: Search history and get conversation insights

## 📋 Prerequisites

```bash
pip install requests pyyaml colorama
```

## 🔑 API Key Setup

Set your Grok API key using one of these methods:

1. **Environment Variable** (Recommended):
   ```bash
   export GROK_API_KEY="your-api-key-here"
   ```

2. **Interactive Prompt**: The agent will ask for your key on first run and save it securely.

## 💻 Usage

### Basic Usage

```bash
# Start interactive chat with Grok 4
python main.py --model grok4 --agent-id my-agent

# Start chat with Grok 3 Mini
python main.py --model grok3mini --agent-id test-agent

# Start chat with Grok 3
python main.py --model grok3 --agent-id research-agent
```

### Management Commands

```bash
# List all agents
python main.py --list

# Show detailed agent information
python main.py --info my-agent --model grok4

# Configure agent interactively
python main.py --model grok4 --agent-id my-agent --config
```

### Export Conversations

```bash
# Export as HTML
python main.py --model grok4 --agent-id my-agent --export html

# Export as JSON
python main.py --model grok3mini --agent-id test --export json

# Export as Markdown
python main.py --model grok3 --agent-id research --export md
```

### Advanced Options

```bash
# Override temperature
python main.py --model grok4 --agent-id my-agent --temperature 0.7

# Disable streaming
python main.py --model grok4 --agent-id my-agent --no-stream
```

## 💬 Interactive Commands

Once in a chat session, use these commands:

- `/help` - Show available commands
- `/history [n]` - Show last n messages (default 5)  
- `/search <term>` - Search conversation history
- `/stats` - Show conversation statistics
- `/config` - Show current configuration
- `/export <format>` - Export conversation (json|txt|md|html)
- `/clear` - Clear conversation history (with confirmation)
- `/files` - List available files for inclusion
- `/info` - Show agent information
- `/quit` - Exit the chat

## 📄 File Inclusion

Include files in your messages using the `{filename}` syntax:

```
Can you review my code in {main.py} and suggest improvements?
```

**Supported file types:**
- Programming languages: `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, etc.
- Configuration files: `.json`, `.yaml`, `.toml`, `.ini`, etc.
- Documentation: `.md`, `.txt`, `.rst`, etc.
- Web files: `.html`, `.css`, `.scss`, etc.
- And many more...

**File search paths:**
- Current directory (`.`)
- Common project directories (`src/`, `lib/`, `scripts/`, etc.)
- Agent uploads directory (`agents/{agent-id}/uploads/`)

## ⚙️ Configuration

Each agent has its own configuration file (`agents/{agent-id}/config.yaml`):

```yaml
model: grok-4-latest
temperature: 0.0
max_tokens: 32768
max_history_size: 1000
stream: true
system_prompt: "You are a helpful assistant."
top_p: 1.0
created_at: "2024-01-01T00:00:00"
updated_at: "2024-01-01T00:00:00"
```

## 📊 Export Formats

### JSON Export
Complete conversation data with metadata, configuration, and statistics.

### Plain Text Export
Simple text format with timestamps, suitable for sharing or archiving.

### Markdown Export
Formatted Markdown with proper headers and structure.

### HTML Export
Beautiful, responsive HTML with modern styling, perfect for presentations or web sharing.

## 🔒 Security

- API keys are never logged or exposed
- Secrets are stored locally and added to `.gitignore`
- File inclusion has size limits (2MB per file)
- Only supported file types can be included
- Automatic backup creation before destructive operations

## 📝 Logging

Each agent maintains detailed logs in `agents/{agent-id}/logs/`:
- Daily log files with rotation
- Structured logging with timestamps
- Different log levels (INFO, WARNING, ERROR)
- Console output for warnings and errors

## 🗃️ Data Storage

Agent data is organized per agent:

```
agents/{agent-id}/
├── config.yaml      # Configuration settings
├── history.json     # Conversation messages
├── secrets.json     # API keys (gitignored)
├── backups/         # Automatic backups
│   ├── history_20240101_120000.json
│   └── ...
├── logs/            # Daily logs
│   ├── 2024-01-01.log
│   └── ...
├── exports/         # Exported conversations
│   ├── conversation_20240101_120000.html
│   └── ...
└── uploads/         # File uploads for inclusion
```

## 🛠️ Development

The codebase is modular and extensible:

- **`main.py`**: CLI interface and argument parsing
- **`agent.py`**: Core chat functionality and API integration
- **`config.py`**: Configuration management with dataclasses
- **`utils.py`**: Shared utilities for file operations, logging, etc.
- **`export.py`**: Multi-format conversation export functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This is a refactored and improved version of the original Grok agent implementations, providing a unified interface for all Grok models with enhanced features and better code organization.