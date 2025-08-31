#!/usr/bin/env python3
"""
Utilities for directories, logging, backups, and general helper functions
"""

import os
import json
import yaml
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

try:
    from colorama import Fore, Style, init as colorama_init
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    
    # Fallback classes if colorama is not available
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

def setup_colorama() -> Tuple[object, object]:
    """Setup colorama and return Fore, Style classes"""
    if HAS_COLORAMA:
        colorama_init(autoreset=True)
    return Fore, Style

def print_colored(message: str, color: str = ""):
    """Print colored message"""
    print(f"{color}{message}{Style.RESET_ALL}" if color else message)

def ensure_directory(path: Path) -> None:
    """Ensure directory exists, create if it doesn't"""
    path.mkdir(parents=True, exist_ok=True)

def setup_agent_directories(agent_id: str) -> Path:
    """Setup directory structure for an agent"""
    base_dir = Path(f"agents/{agent_id}")
    directories = [
        base_dir,
        base_dir / "backups",
        base_dir / "logs", 
        base_dir / "exports",
        base_dir / "uploads"
    ]
    
    for directory in directories:
        ensure_directory(directory)
    
    return base_dir

def setup_logging(agent_id: str, base_dir: Path) -> logging.Logger:
    """Configure logging for an agent"""
    log_file = base_dir / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # Create logger
    logger = logging.getLogger(f"GrokAgent_{agent_id}")
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.WARNING)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def create_backup(file_path: Path, backup_dir: Path, max_backups: int = 10) -> None:
    """Create a rolling backup of a file"""
    if not file_path.exists():
        return
    
    ensure_directory(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
    
    try:
        shutil.copy2(file_path, backup_file)
        
        # Keep only the last max_backups backups
        backups = sorted(backup_dir.glob(f"{file_path.stem}_*{file_path.suffix}"))
        while len(backups) > max_backups:
            oldest = backups.pop(0)
            oldest.unlink()
            
    except Exception as e:
        print_colored(f"Error creating backup: {e}", Fore.RED)

def load_json_file(file_path: Path, default: Any = None) -> Any:
    """Load JSON file with error handling"""
    if not file_path.exists():
        return default or []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print_colored(f"Error loading {file_path}: {e}", Fore.RED)
        return default or []

def save_json_file(file_path: Path, data: Any, create_backup_file: bool = True) -> bool:
    """Save JSON file with optional backup"""
    try:
        if create_backup_file and file_path.exists():
            create_backup(file_path, file_path.parent / "backups")
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print_colored(f"Error saving {file_path}: {e}", Fore.RED)
        return False

def load_yaml_file(file_path: Path, default: Any = None) -> Any:
    """Load YAML file with error handling"""
    if not file_path.exists():
        return default
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print_colored(f"Error loading {file_path}: {e}", Fore.RED)
        return default

def save_yaml_file(file_path: Path, data: Any) -> bool:
    """Save YAML file with error handling"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print_colored(f"Error saving {file_path}: {e}", Fore.RED)
        return False

def get_api_key() -> str:
    """Retrieve the API key from environment variables or prompt user"""
    # First, try the environment variable
    api_key = os.getenv('GROK_API_KEY')
    if api_key:
        return api_key
    
    # Prompt the user to enter the API key
    print_colored("API key for Grok models not found.", Fore.YELLOW)
    print_colored("You can set the GROK_API_KEY environment variable or enter it now.", Fore.YELLOW)
    
    api_key = input(f"{Fore.CYAN}Enter the API key for Grok models: {Style.RESET_ALL}").strip()
    
    if not api_key:
        raise ValueError("An API key is required")
    
    return api_key

def save_api_key(api_key: str, base_dir: Path) -> bool:
    """Save API key to secrets file and update .gitignore"""
    secrets_file = base_dir / "secrets.json"
    secrets = {
        "provider": "grok",
        "keys": {
            "default": api_key
        }
    }
    
    try:
        with open(secrets_file, 'w') as f:
            json.dump(secrets, f, indent=2)
        
        # Add to .gitignore
        gitignore_file = Path('.gitignore')
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()
        else:
            gitignore_content = ""
        
        if 'secrets.json' not in gitignore_content:
            with open(gitignore_file, 'a') as f:
                f.write('\n# API keys\n**/secrets.json\nsecrets.json\n')
        
        masked_key = f"{api_key[:4]}...{api_key[-2:]}" if len(api_key) > 6 else "***"
        print_colored(f"API key saved ({masked_key})", Fore.GREEN)
        return True
        
    except Exception as e:
        print_colored(f"Error saving API key: {e}", Fore.RED)
        print_colored("Warning: Unable to save the API key to file", Fore.RED)
        return False

def load_api_key(base_dir: Path) -> Optional[str]:
    """Load API key from secrets file"""
    secrets_file = base_dir / "secrets.json"
    if secrets_file.exists():
        try:
            with open(secrets_file, 'r') as f:
                secrets = json.load(f)
                return secrets.get('keys', {}).get('default')
        except Exception as e:
            print_colored(f"Error reading secrets file: {e}", Fore.RED)
    return None

def is_supported_file(file_path: Path) -> bool:
    """Check if the file extension is supported for inclusion"""
    from config import SUPPORTED_EXTENSIONS
    
    if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
        return True
    
    # Check for known files without extensions
    known_files = {
        'makefile', 'dockerfile', 'readme', 'license', 'changelog'
    }
    
    return file_path.name.lower() in known_files

def get_search_paths(base_dir: Path) -> List[Path]:
    """Get standard search paths for file inclusion"""
    return [
        Path('.'),
        Path('src'), Path('lib'),
        Path('scripts'), Path('data'),
        Path('documents'), Path('files'),
        Path('config'), Path('configs'),
        base_dir / 'uploads'
    ]

def list_available_files(base_dir: Path) -> List[str]:
    """List available files for inclusion"""
    files = []
    search_paths = get_search_paths(base_dir)
    
    for search_path in search_paths:
        if search_path.exists():
            for file_path in search_path.rglob("*"):
                if (file_path.is_file() and
                    not file_path.name.startswith('.') and
                    is_supported_file(file_path)):
                    
                    size = file_path.stat().st_size
                    size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                    files.append(f"{file_path} ({size_str}) [{file_path.suffix}]")
    
    return sorted(files)

def list_all_agents() -> List[Dict[str, Any]]:
    """List all available agents across all models"""
    agents_dir = Path("agents")
    agents = []
    
    if not agents_dir.exists():
        return agents
    
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir():
            metadata_file = agent_dir / "metadata.json"
            config_file = agent_dir / "config.yaml"
            history_file = agent_dir / "history.json"
            
            # Basic info
            agent_info = {
                "id": agent_dir.name,
                "path": str(agent_dir),
                "exists": True
            }
            
            # Load metadata if available
            if metadata_file.exists():
                try:
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                        agent_info.update(metadata)
                except:
                    pass
            
            # Load config info
            if config_file.exists():
                try:
                    with open(config_file) as f:
                        config = yaml.safe_load(f)
                        agent_info["model"] = config.get("model", "unknown")
                        agent_info["created_at"] = config.get("created_at")
                        agent_info["updated_at"] = config.get("updated_at")
                except:
                    pass
            
            # History info
            if history_file.exists():
                try:
                    with open(history_file) as f:
                        history = json.load(f)
                        agent_info["message_count"] = len(history)
                        agent_info["history_size"] = history_file.stat().st_size
                except:
                    agent_info["message_count"] = 0
                    agent_info["history_size"] = 0
            else:
                agent_info["message_count"] = 0
                agent_info["history_size"] = 0
            
            agents.append(agent_info)
    
    return sorted(agents, key=lambda x: x.get("updated_at", ""))

def show_detailed_agent_info(agent_id: str, model: Optional[str] = None):
    """Display detailed information about an agent"""
    agent_dir = Path(f"agents/{agent_id}")
    
    if not agent_dir.exists():
        print_colored(f"Agent '{agent_id}' not found", Fore.RED)
        return
    
    print_colored(f"\n{'='*50}", Fore.CYAN)
    print_colored(f"Agent Information: {agent_id}", Fore.YELLOW)
    print_colored(f"{'='*50}", Fore.CYAN)
    
    # Load and display configuration
    config_file = agent_dir / "config.yaml"
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = yaml.safe_load(f)
            
            model_name = config.get('model', 'unknown')
            
            print_colored(f"\nConfiguration:", Fore.GREEN)
            print_colored(f"  Model: {model_name}", Fore.WHITE)
            print_colored(f"  Temperature: {config.get('temperature', 0.0)}", Fore.WHITE)
            print_colored(f"  Max Tokens: {config.get('max_tokens', 32768)}", Fore.WHITE)
            print_colored(f"  Streaming: {config.get('stream', True)}", Fore.WHITE)
            print_colored(f"  Created at: {config.get('created_at', 'Unknown')}", Fore.WHITE)
            print_colored(f"  Updated at: {config.get('updated_at', 'Unknown')}", Fore.WHITE)
        
        except Exception as e:
            print_colored(f"Error loading configuration: {e}", Fore.RED)
    
    # Display history stats
    history_file = agent_dir / "history.json"
    if history_file.exists():
        try:
            with open(history_file) as f:
                history = json.load(f)
            
            user_msgs = len([m for m in history if m.get("role") == "user"])
            assistant_msgs = len([m for m in history if m.get("role") == "assistant"])
            total_chars = sum(len(m.get("content", "")) for m in history)
            
            print_colored(f"\nConversation History:", Fore.GREEN)
            print_colored(f"  Total messages: {len(history)}", Fore.WHITE)
            print_colored(f"  User messages: {user_msgs}", Fore.WHITE)
            print_colored(f"  Assistant messages: {assistant_msgs}", Fore.WHITE)
            print_colored(f"  Total characters: {total_chars:,}", Fore.WHITE)
            print_colored(f"  File size: {history_file.stat().st_size:,} bytes", Fore.WHITE)
            
            if history:
                first_msg = datetime.fromisoformat(history[0]["timestamp"])
                last_msg = datetime.fromisoformat(history[-1]["timestamp"])
                print_colored(f"  First message: {first_msg.strftime('%Y-%m-%d %H:%M:%S')}", Fore.WHITE)
                print_colored(f"  Last message: {last_msg.strftime('%Y-%m-%d %H:%M:%S')}", Fore.WHITE)
        
        except Exception as e:
            print_colored(f"Error loading history: {e}", Fore.RED)
    else:
        print_colored(f"\nNo conversation history found", Fore.YELLOW)
    
    # Display directory structure
    print_colored(f"\nDirectory Structure:", Fore.GREEN)
    for item in sorted(agent_dir.rglob("*")):
        if item.is_file():
            size = item.stat().st_size
            size_str = f"{size:,}" if size < 1024 else f"{size/1024:.1f}K"
            rel_path = item.relative_to(agent_dir)
            print_colored(f"  {rel_path} ({size_str} bytes)", Fore.WHITE)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f} GB"

def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string with ellipsis if too long"""
    return text[:max_length] + "..." if len(text) > max_length else text