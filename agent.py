#!/usr/bin/env python3
"""
Core chat agent implementation for Grok Multi-Model Chat Agent
Supports grok3, grok3mini, and grok4 models
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Generator, List, Dict, Any
from dataclasses import asdict
from requests.exceptions import RequestException, HTTPError, Timeout

from config import AgentConfig, SUPPORTED_MODELS, SUPPORTED_EXTENSIONS
from utils import (
    setup_agent_directories, setup_logging, create_backup, load_json_file, 
    save_json_file, load_yaml_file, save_yaml_file, get_api_key, save_api_key,
    load_api_key, is_supported_file, get_search_paths, list_available_files,
    setup_colorama, print_colored
)
from export import export_conversation

# Setup colorama
Fore, Style = setup_colorama()

class GrokChatAgent:
    """Unified chat agent for Grok models with persistence and streaming support"""

    def __init__(self, agent_id: str, model_key: str):
        if model_key not in SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model_key}. Supported models: {list(SUPPORTED_MODELS.keys())}")
            
        self.agent_id = agent_id
        self.model_key = model_key
        self.model_info = SUPPORTED_MODELS[model_key]
        
        # Create directory structure
        self.base_dir = setup_agent_directories(agent_id)
        
        # Setup logging
        self.logger = setup_logging(agent_id, self.base_dir)
        
        # Load or create configuration
        self.config = self._load_config()
        
        # Load conversation history
        self.messages = self._load_history()
        
        # Configure API key
        self.api_key = self._get_api_key()
        
        self.logger.info(f"Grok Chat Agent initialized: {agent_id} using {self.model_info['name']}")

    def _load_config(self) -> AgentConfig:
        """Load the agent's configuration from config.yaml"""
        config_file = self.base_dir / "config.yaml"
        
        if config_file.exists():
            config_data = load_yaml_file(config_file)
            if config_data:
                try:
                    return AgentConfig(**config_data)
                except Exception as e:
                    self.logger.error(f"Error loading config: {e}")
        
        # Create default config for this model
        config = AgentConfig(
            model=self.model_info['model_name'],
            max_tokens=self.model_info['max_tokens']
        )
        self.save_config(config)
        return config

    def save_config(self, config: Optional[AgentConfig] = None):
        """Save the agent's configuration to config.yaml"""
        if config is None:
            config = self.config
        
        config.update_timestamp()
        config_file = self.base_dir / "config.yaml"
        
        if not save_yaml_file(config_file, config.to_dict()):
            self.logger.error("Failed to save configuration")

    def _get_api_key(self) -> str:
        """Retrieve the API key from environment variables, secrets file, or prompt user"""
        # Try environment variable first
        api_key = os.getenv('GROK_API_KEY')
        if api_key:
            self.logger.info("API key loaded from environment variable")
            return api_key
        
        # Try secrets file
        api_key = load_api_key(self.base_dir)
        if api_key:
            self.logger.info("API key loaded from secrets file")
            return api_key
        
        # Prompt user for API key
        print_colored(f"API key for {self.model_info['name']} not found.", Fore.YELLOW)
        print_colored("You can set the GROK_API_KEY environment variable or enter it now.", Fore.YELLOW)
        
        api_key = input(f"{Fore.CYAN}Enter the API key for Grok models: {Style.RESET_ALL}").strip()
        
        if not api_key:
            raise ValueError("An API key is required")
        
        # Save the key
        if save_api_key(api_key, self.base_dir):
            self.logger.info(f"API key saved for user (length: {len(api_key)})")
        
        return api_key

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load conversation history from history.json"""
        history_file = self.base_dir / "history.json"
        return load_json_file(history_file, [])

    def _save_history(self):
        """Save conversation history to history.json with automatic backups"""
        history_file = self.base_dir / "history.json"
        
        if not save_json_file(history_file, self.messages, create_backup_file=True):
            self.logger.error("Failed to save conversation history")

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to the conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.messages.append(message)
        
        # Truncate history if necessary
        if len(self.messages) > self.config.max_history_size:
            removed = self.messages[:-self.config.max_history_size]
            self.messages = self.messages[-self.config.max_history_size:]
            self.logger.info(f"History truncated: {len(removed)} old messages removed")
        
        self._save_history()

    def _process_file_inclusions(self, content: str) -> str:
        """Replace {filename} patterns with the content of the files"""
        def replace_file(match):
            filename = match.group(1)
            search_paths = get_search_paths(self.base_dir)
            
            for search_path in search_paths:
                file_path = search_path / filename
                if file_path.exists() and file_path.is_file():
                    
                    # Check if the file is supported
                    if not is_supported_file(file_path):
                        self.logger.warning(f"Unsupported file type: {filename}")
                        return f"[WARNING: Unsupported file type {filename}]"
                    
                    try:
                        # Check file size (limit to 2MB)
                        max_size = 2 * 1024 * 1024  # 2MB
                        if file_path.stat().st_size > max_size:
                            self.logger.error(f"File {filename} too large (>2MB)")
                            return f"[ERROR: File {filename} too large (max 2MB)]"
                        
                        # Try UTF-8 first
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()
                        except UnicodeDecodeError:
                            # Fall back to latin-1
                            with open(file_path, 'r', encoding='latin-1') as f:
                                file_content = f.read()
                        
                        # Add a header with file information
                        file_info = f"// File: {filename} ({file_path.suffix})\n"
                        if file_path.suffix.lower() in ['.py', '.r']:
                            file_info = f"# File: {filename} ({file_path.suffix})\n"
                        elif file_path.suffix.lower() in ['.html', '.xml']:
                            file_info = f"<!-- File: {filename} ({file_path.suffix}) -->\n"
                        elif file_path.suffix.lower() in ['.css', '.scss', '.sass']:
                            file_info = f"/* File: {filename} ({file_path.suffix}) */\n"
                        elif file_path.suffix.lower() in ['.sql']:
                            file_info = f"-- File: {filename} ({file_path.suffix})\n"
                        
                        full_content = file_info + file_content
                        
                        self.logger.info(f"File included: {filename} ({len(file_content)} characters)")
                        return full_content
                    
                    except Exception as e:
                        self.logger.error(f"Error reading file {filename}: {e}")
                        return f"[ERROR: Unable to read {filename}: {e}]"
            
            self.logger.warning(f"File not found: {filename}")
            return f"[ERROR: File {filename} not found]"
        
        return re.sub(r'\{([^}]+)\}', replace_file, content)

    def _build_api_payload(self, new_message: str, override_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build the API request payload"""
        # Process file inclusions
        processed_message = self._process_file_inclusions(new_message)
        
        # Build messages in API format
        messages = []
        
        # Add system prompt if configured
        if self.config.system_prompt:
            messages.append({
                "role": "system",
                "content": self.config.system_prompt
            })
        
        # Add conversation history
        for msg in self.messages:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add the new user message
        messages.append({
            "role": "user",
            "content": processed_message
        })
        
        # Apply any configuration overrides
        config = asdict(self.config)
        if override_config:
            config.update(override_config)
        
        # Build the payload - only include parameters supported by Grok API
        payload = {
            "model": config["model"],
            "messages": messages,
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "stream": config["stream"]
        }
        
        return payload

    def _make_api_request(self, payload: Dict[str, Any]) -> requests.Response:
        """Make the API request with error and retry handling"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        timeout = self.model_info['timeout']
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Sending API request to {self.model_info['name']} (attempt {attempt + 1}/{max_retries})")
                
                response = requests.post(
                    self.model_info['api_url'],
                    headers=headers,
                    json=payload,
                    stream=payload.get("stream", True),
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    self.logger.info("API request successful")
                    return response
                elif response.status_code == 401:
                    raise ValueError("Invalid API key")
                elif response.status_code == 403:
                    raise ValueError("API access forbidden")
                elif response.status_code == 429:
                    # Rate limit reached - wait and retry
                    delay = base_delay * (2 ** attempt)
                    self.logger.warning(f"Rate limit reached, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                elif response.status_code >= 500:
                    # Server error - retry
                    delay = base_delay * (2 ** attempt)
                    self.logger.warning(f"Server error {response.status_code}, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    # Log the error response body for debugging
                    try:
                        error_body = response.text
                        self.logger.error(f"API Error {response.status_code}: {error_body}")
                    except:
                        self.logger.error(f"API Error {response.status_code}: Unable to read response body")
                    response.raise_for_status()
            
            except Timeout as e:
                self.logger.warning(f"Request timed out after {timeout}s (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    raise Exception(f"Request timed out after {timeout}s.") from e
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"Retrying in {delay}s...")
                time.sleep(delay)
            except RequestException as e:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"Request failed ({e}), retrying in {delay}s...")
                time.sleep(delay)
        
        raise Exception(f"API request failed after {max_retries} attempts")

    def _parse_streaming_response(self, response: requests.Response) -> Generator[str, None, None]:
        """Parse the streaming response from server-side events"""
        assistant_message = ""
        
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line or line.strip() == "":
                    continue
                
                try:
                    # Handle server-side event formats
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        
                        if data_str == "[DONE]":
                            break
                        
                        data = json.loads(data_str)
                        
                        # Extract content
                        choices = data.get("choices", [])
                        if choices:
                            choice = choices[0]
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")
                            
                            if content:
                                assistant_message += content
                                yield content
                            
                            finish_reason = choice.get("finish_reason")
                            if finish_reason == "stop":
                                break
                
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid JSON in stream: {e}")
                    continue
                except Exception as e:
                    self.logger.warning(f"Error processing stream line: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error parsing streaming response: {e}")
        
        # Add the assistant's message to history if content was received
        if assistant_message.strip():
            self.add_message("assistant", assistant_message)

    def _parse_non_streaming_response(self, response: requests.Response) -> str:
        """Parse the non-streaming response from the API"""
        try:
            data = response.json()
            
            # Extract the message content
            choices = data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                content = message.get("content", "")
                
                if content:
                    self.add_message("assistant", content)
                    return content
            
            return "No response content received"
        
        except Exception as e:
            self.logger.error(f"Error parsing non-streaming response: {e}")
            return f"Error parsing response: {e}"

    def call_api(self, new_message: str, override_config: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """Call the Grok API with the new message"""
        try:
            # Add the user's message to history
            self.add_message("user", new_message)
            
            # Build the API payload
            payload = self._build_api_payload(new_message, override_config)
            
            self.logger.info(f"Calling API at {self.model_info['api_url']}")
            self.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Display model information to the user
            timeout_mins = self.model_info['timeout'] // 60
            print_colored(f"🤖 Using {self.model_info['name']} (timeout: {timeout_mins}min)...", Fore.YELLOW)
            
            # Make the request
            response = self._make_api_request(payload)
            
            # Handle streaming vs non-streaming
            if payload.get("stream", True):
                yield from self._parse_streaming_response(response)
            else:
                result = self._parse_non_streaming_response(response)
                yield result
        
        except Exception as e:
            error_msg = f"API call failed: {e}"
            self.logger.error(error_msg)
            yield error_msg

    def clear_history(self):
        """Clear the conversation history"""
        create_backup(
            self.base_dir / "history.json",
            self.base_dir / "backups"
        )
        self.messages.clear()
        self._save_history()
        self.logger.info("Conversation history cleared")

    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        if not self.messages:
            return {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "total_characters": 0,
                "average_message_length": 0,
                "first_message": None,
                "last_message": None,
                "conversation_duration": None
            }
        
        user_msgs = [m for m in self.messages if m["role"] == "user"]
        assistant_msgs = [m for m in self.messages if m["role"] == "assistant"]
        
        total_chars = sum(len(m["content"]) for m in self.messages)
        avg_length = total_chars // len(self.messages) if self.messages else 0
        
        first_time = datetime.fromisoformat(self.messages[0]["timestamp"])
        last_time = datetime.fromisoformat(self.messages[-1]["timestamp"])
        duration = last_time - first_time
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "total_characters": total_chars,
            "average_message_length": avg_length,
            "first_message": first_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_message": last_time.strftime("%Y-%m-%d %H:%M:%S"),
            "conversation_duration": str(duration).split('.')[0] if duration.total_seconds() > 0 else "0:00:00"
        }

    def export_conversation(self, format_type: str) -> str:
        """Export the conversation in the specified format"""
        export_dir = self.base_dir / "exports"
        export_dir.mkdir(exist_ok=True)
        
        filepath = export_conversation(
            agent_id=self.agent_id,
            model_name=self.model_info['name'],
            messages=self.messages,
            config=asdict(self.config),
            statistics=self.get_statistics(),
            export_dir=export_dir,
            format_type=format_type
        )
        
        self.logger.info(f"Conversation exported to {filepath}")
        return filepath

    def search_history(self, term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search the conversation history for a term"""
        results = []
        term_lower = term.lower()
        
        for i, msg in enumerate(self.messages):
            if term_lower in msg["content"].lower():
                results.append({
                    "index": i,
                    "message": msg,
                    "preview": msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                })
            
            if len(results) >= limit:
                break
        
        return results

    def list_files(self) -> List[str]:
        """List available files for inclusion"""
        return list_available_files(self.base_dir)