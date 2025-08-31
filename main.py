#!/usr/bin/env python3
"""
Grok Multi-Model Chat Agent - CLI Entry Point
A Python CLI chat agent for grok3, grok3mini, and grok4 models

Usage:
    python main.py --model grok4 --agent-id my-agent
    python main.py --list
    python main.py --model grok3mini --agent-id test --export html
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from agent import GrokChatAgent
from config import AgentConfig, SUPPORTED_MODELS
from utils import setup_colorama, print_colored
from export import export_conversation

# Initialize colorama
Fore, Style = setup_colorama()

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Grok Multi-Model Chat Agent - Advanced AI Chat Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --model grok4 --agent-id my-agent              # Start interactive chat with Grok 4
  %(prog)s --model grok3mini --agent-id test              # Start interactive chat with Grok 3 Mini  
  %(prog)s --list                                         # List all available agents
  %(prog)s --model grok3 --agent-id my-agent --export html # Export conversation in HTML
  %(prog)s --model grok4 --agent-id my-agent --config     # Configure agent interactively

Supported Models:
  - grok3: Grok 3 model
  - grok3mini: Grok 3 Mini model  
  - grok4: Grok 4 model
        """
    )

    # Required arguments
    parser.add_argument(
        "--model", 
        choices=list(SUPPORTED_MODELS.keys()),
        help="Model to use for the chat session"
    )
    parser.add_argument(
        "--agent-id", 
        help="ID of the agent for the chat session"
    )

    # Optional arguments  
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List all available agents"
    )
    parser.add_argument(
        "--info", 
        metavar="ID", 
        help="Show detailed information for an agent"
    )
    parser.add_argument(
        "--config", 
        action="store_true", 
        help="Configure the agent interactively"
    )
    
    # Model parameters
    parser.add_argument(
        "--temperature", 
        type=float, 
        help="Override the temperature (0.0-2.0)"
    )
    parser.add_argument(
        "--no-stream", 
        action="store_true", 
        help="Disable streaming"
    )
    
    # Export options
    parser.add_argument(
        "--export", 
        choices=["json", "txt", "md", "html"], 
        help="Export format for the conversation"
    )

    return parser

def list_agents():
    """List all available agents across all models."""
    from utils import list_all_agents
    
    agents = list_all_agents()
    if not agents:
        print_colored(f"No agents found", Fore.YELLOW)
        return

    print_colored(f"\nAvailable Agents:", Fore.CYAN)
    print_colored(f"{'ID':<20} {'Model':<20} {'Messages':<10} {'Last Updated':<25}", Fore.WHITE)
    print("-" * 75)

    for agent in agents:
        updated = agent.get("updated_at", "Unknown")
        if updated != "Unknown":
            try:
                from datetime import datetime
                updated = datetime.fromisoformat(updated).strftime("%Y-%m-%d %H:%M")
            except:
                pass

        model = agent.get('model', 'unknown')
        print(f"{agent['id']:<20} {model:<20} {agent.get('message_count', 0):<10} {updated:<25}")

def show_agent_info(agent_id: str, model: Optional[str] = None):
    """Display detailed information about an agent."""
    from utils import show_detailed_agent_info
    show_detailed_agent_info(agent_id, model)

def create_agent_config_interactive(model: str) -> AgentConfig:
    """Interactive creation of the configuration."""
    print_colored(f"\nCreating Agent Configuration for {SUPPORTED_MODELS[model]['name']}", Fore.CYAN)
    print_colored(f"Press Enter to use default values\n", Fore.YELLOW)

    config = AgentConfig(model=SUPPORTED_MODELS[model]['model_name'])

    # Display the model being used
    print_colored(f"Model used: {SUPPORTED_MODELS[model]['name']} ({config.model})\n", Fore.GREEN)

    # Temperature
    temp_input = input(f"Temperature (0.0-2.0) [{config.temperature}]: ").strip()
    if temp_input:
        try:
            config.temperature = float(temp_input)
        except ValueError:
            print_colored("Invalid temperature, using default value", Fore.RED)

    # System prompt
    system_prompt = input(f"System prompt (optional): ").strip()
    if system_prompt:
        config.system_prompt = system_prompt

    # Max tokens for completion
    tokens_input = input(f"Max tokens for completion [{config.max_tokens}]: ").strip()
    if tokens_input:
        try:
            config.max_tokens = int(tokens_input)
        except ValueError:
            print_colored("Invalid number of tokens, using default value", Fore.RED)

    # Streaming
    stream_input = input(f"Enable streaming (y/n) [{'y' if config.stream else 'n'}]: ").strip().lower()
    if stream_input in ['n', 'no', 'false']:
        config.stream = False
    elif stream_input in ['y', 'yes', 'true']:
        config.stream = True

    return config

def interactive_chat(agent: GrokChatAgent):
    """Interactive chat session."""
    model_info = SUPPORTED_MODELS[agent.model_key]
    
    print_colored(f"\nStarting interactive chat with {model_info['name']}", Fore.GREEN)
    print_colored(f"Agent: {agent.agent_id}", Fore.YELLOW)
    print_colored(f"Type '/help' for commands, '/quit' to exit\n", Fore.GREEN)

    while True:
        try:
            user_input = input(f"{Fore.CYAN}You: {Style.RESET_ALL}").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith('/'):
                command_parts = user_input[1:].split()
                command = command_parts[0].lower()

                if command == 'help':
                    print_colored(f"\nAvailable Commands:", Fore.YELLOW)
                    print_colored(f"/help - Show this help message", Fore.WHITE)
                    print_colored(f"/history [n] - Show the last n messages (default 5)", Fore.WHITE)
                    print_colored(f"/search <term> - Search the conversation history", Fore.WHITE)
                    print_colored(f"/stats - Show conversation statistics", Fore.WHITE)
                    print_colored(f"/config - Show current configuration", Fore.WHITE)
                    print_colored(f"/export <json|txt|md|html> - Export the conversation", Fore.WHITE)
                    print_colored(f"/clear - Clear the conversation history", Fore.WHITE)
                    print_colored(f"/files - List available files for inclusion", Fore.WHITE)
                    print_colored(f"/info - Show agent information", Fore.WHITE)
                    print_colored(f"/quit - Exit the chat\n", Fore.WHITE)
                    print_colored(f"File Inclusion: Use {{filename}} in your messages to include file content.", Fore.CYAN)
                    print_colored(f"Supported: Programming files (.py, .js, etc.), config files, documentation\n", Fore.CYAN)

                elif command == 'history':
                    limit = 5
                    if len(command_parts) > 1:
                        try:
                            limit = int(command_parts[1])
                        except ValueError:
                            print_colored("Invalid number", Fore.RED)
                            continue

                    recent_messages = agent.messages[-limit:]
                    if not recent_messages:
                        print_colored("No messages in history", Fore.YELLOW)
                    else:
                        print_colored(f"\nLast {len(recent_messages)} messages:", Fore.YELLOW)
                        for msg in recent_messages:
                            from datetime import datetime
                            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
                            role_color = Fore.CYAN if msg["role"] == "user" else Fore.GREEN
                            content = msg['content'][:100] + ('...' if len(msg['content']) > 100 else '')
                            print(f"{Fore.WHITE}[{timestamp}] {role_color}{msg['role']}: {content}")
                    print()

                elif command == 'search':
                    if len(command_parts) < 2:
                        print_colored("Usage: /search <term>", Fore.RED)
                        continue

                    search_term = ' '.join(command_parts[1:])
                    results = agent.search_history(search_term)

                    if not results:
                        print_colored(f"No results found for '{search_term}'", Fore.YELLOW)
                    else:
                        print_colored(f"\nFound {len(results)} results for '{search_term}':", Fore.YELLOW)
                        for result in results:
                            msg = result["message"]
                            from datetime import datetime
                            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
                            role_color = Fore.CYAN if msg["role"] == "user" else Fore.GREEN
                            print(f"{Fore.WHITE}[{timestamp}] {role_color}{msg['role']}: {result['preview']}")
                    print()

                elif command == 'stats':
                    stats = agent.get_statistics()
                    print_colored(f"\nConversation Statistics:", Fore.YELLOW)
                    print_colored(f"Model: {agent.config.model}", Fore.WHITE)
                    print_colored(f"Total messages: {stats['total_messages']}", Fore.WHITE)
                    print_colored(f"User messages: {stats['user_messages']}", Fore.WHITE)
                    print_colored(f"Assistant messages: {stats['assistant_messages']}", Fore.WHITE)
                    print_colored(f"Total characters: {stats['total_characters']:,}", Fore.WHITE)
                    print_colored(f"Average message length: {stats['average_message_length']:,}", Fore.WHITE)
                    if stats['first_message']:
                        print_colored(f"First message: {stats['first_message']}", Fore.WHITE)
                        print_colored(f"Last message: {stats['last_message']}", Fore.WHITE)
                        print_colored(f"Duration: {stats['conversation_duration']}", Fore.WHITE)
                    print()

                elif command == 'config':
                    print_colored(f"\nCurrent Configuration:", Fore.YELLOW)
                    from dataclasses import asdict
                    config_dict = asdict(agent.config)
                    for key, value in config_dict.items():
                        if key not in ['created_at', 'updated_at']:
                            print_colored(f"{key}: {value}", Fore.WHITE)
                    print()

                elif command == 'export':
                    if len(command_parts) < 2:
                        print_colored("Usage: /export <json|txt|md|html>", Fore.RED)
                        continue

                    format_type = command_parts[1].lower()
                    if format_type not in ['json', 'txt', 'md', 'html']:
                        print_colored("Invalid format. Use: json, txt, md, or html", Fore.RED)
                        continue

                    try:
                        filepath = agent.export_conversation(format_type)
                        print_colored(f"Exported to: {filepath}", Fore.GREEN)
                    except Exception as e:
                        print_colored(f"Export failed: {e}", Fore.RED)

                elif command == 'clear':
                    confirm = input(f"{Fore.YELLOW}Clear conversation history? (y/N): {Style.RESET_ALL}").strip().lower()
                    if confirm in ['y', 'yes']:
                        agent.clear_history()
                        print_colored("Conversation history cleared", Fore.GREEN)

                elif command == 'files':
                    files = agent.list_files()
                    if not files:
                        print_colored("No supported files found for inclusion", Fore.YELLOW)
                    else:
                        print_colored(f"\nFiles available for inclusion:", Fore.YELLOW)
                        for file_info in files[:20]:  # Limit to 20 files
                            print_colored(f"{file_info}", Fore.WHITE)
                        if len(files) > 20:
                            print_colored(f"... and {len(files) - 20} more files", Fore.YELLOW)
                        print_colored(f"Use {{filename}} in your message to include file content\n", Fore.CYAN)

                elif command == 'info':
                    show_agent_info(agent.agent_id, agent.model_key)

                elif command in ['quit', 'exit', 'q']:
                    print_colored("Goodbye!", Fore.GREEN)
                    break

                else:
                    print_colored(f"Unknown command: {command}", Fore.RED)
                    print_colored("Type '/help' for available commands", Fore.YELLOW)

                continue

            # Regular message - send to API
            print(f"\n{Fore.GREEN}Assistant: {Style.RESET_ALL}", end="", flush=True)

            response_text = ""
            for chunk in agent.call_api(user_input):
                print(chunk, end="", flush=True)
                response_text += chunk

            print("\n")

        except KeyboardInterrupt:
            print_colored(f"\nUse '/quit' to exit gracefully", Fore.YELLOW)
        except Exception as e:
            print_colored(f"\nError: {e}", Fore.RED)

def main():
    """Main CLI interface."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle the list command
    if args.list:
        list_agents()
        return

    # Handle the info command
    if args.info:
        show_agent_info(args.info, args.model)
        return

    # Require model and agent-id for other operations
    if not args.model:
        parser.print_help()
        print_colored(f"\nError: --model is required", Fore.RED)
        return
        
    if not args.agent_id:
        parser.print_help()
        print_colored(f"\nError: --agent-id is required", Fore.RED)
        return

    try:
        # Initialize the agent
        agent = GrokChatAgent(args.agent_id, args.model)

        # Handle the config command
        if args.config:
            new_config = create_agent_config_interactive(args.model)
            agent.config = new_config
            agent.save_config()
            print_colored("Configuration saved", Fore.GREEN)
            return

        # Handle the export command
        if args.export:
            filepath = agent.export_conversation(args.export)
            print_colored(f"Exported to: {filepath}", Fore.GREEN)
            return

        # Apply command-line overrides
        overrides = {}
        if args.temperature is not None:
            overrides["temperature"] = args.temperature
        if args.no_stream:
            overrides["stream"] = False

        if overrides:
            from dataclasses import asdict
            agent.config = AgentConfig(**{**asdict(agent.config), **overrides})
            agent.save_config()

        # Start the interactive chat
        interactive_chat(agent)

    except KeyboardInterrupt:
        print_colored(f"\nInterrupted by user", Fore.YELLOW)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()