#!/usr/bin/env python3
"""
Multi-format conversation export functionality (JSON/TXT/MD/HTML)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import asdict

def export_conversation(
    agent_id: str,
    model_name: str,
    messages: List[Dict[str, Any]], 
    config: Dict[str, Any],
    statistics: Dict[str, Any],
    export_dir: Path, 
    format_type: str
) -> str:
    """Export the conversation in the specified format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "json":
        return _export_json(agent_id, model_name, messages, config, statistics, export_dir, timestamp)
    elif format_type == "txt":
        return _export_txt(agent_id, model_name, messages, export_dir, timestamp)
    elif format_type == "md":
        return _export_markdown(agent_id, model_name, messages, export_dir, timestamp)
    elif format_type == "html":
        return _export_html(agent_id, model_name, messages, export_dir, timestamp)
    else:
        raise ValueError(f"Unsupported export format: {format_type}")

def _export_json(
    agent_id: str,
    model_name: str, 
    messages: List[Dict[str, Any]], 
    config: Dict[str, Any],
    statistics: Dict[str, Any],
    export_dir: Path, 
    timestamp: str
) -> str:
    """Export conversation to JSON format"""
    filename = f"conversation_{timestamp}.json"
    filepath = export_dir / filename
    
    export_data = {
        "agent_id": agent_id,
        "model": model_name,
        "exported_at": datetime.now().isoformat(),
        "config": config,
        "messages": messages,
        "statistics": statistics
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return str(filepath)

def _export_txt(
    agent_id: str,
    model_name: str,
    messages: List[Dict[str, Any]], 
    export_dir: Path, 
    timestamp: str
) -> str:
    """Export conversation to plain text format"""
    filename = f"conversation_{timestamp}.txt"
    filepath = export_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Conversation Export - Grok Multi-Model Chat Agent\n")
        f.write(f"Agent ID: {agent_id}\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Exported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for msg in messages:
            if msg.get("role") in ["user", "assistant"]:
                timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp_str}] {msg['role'].upper()}:\n")
                f.write(f"{msg['content']}\n\n")
    
    return str(filepath)

def _export_markdown(
    agent_id: str,
    model_name: str,
    messages: List[Dict[str, Any]], 
    export_dir: Path, 
    timestamp: str
) -> str:
    """Export conversation to Markdown format"""
    filename = f"conversation_{timestamp}.md"
    filepath = export_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# Conversation - Grok Multi-Model Chat Agent\n\n")
        f.write(f"**Agent ID:** {agent_id}  \n")
        f.write(f"**Model:** {model_name}  \n")
        f.write(f"**Exported at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
        
        for msg in messages:
            if msg.get("role") in ["user", "assistant"]:
                timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                role_emoji = "🧑" if msg["role"] == "user" else "🤖"
                f.write(f"## {role_emoji} {msg['role'].title()} - {timestamp_str}\n\n")
                f.write(f"{msg['content']}\n\n")
    
    return str(filepath)

def _export_html(
    agent_id: str,
    model_name: str,
    messages: List[Dict[str, Any]], 
    export_dir: Path, 
    timestamp: str
) -> str:
    """Export conversation to HTML format"""
    filename = f"conversation_{timestamp}.html"
    filepath = export_dir / filename
    
    # HTML template with styling
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversation - {model_name} - {agent_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
            margin: 5px 0;
        }}
        
        .conversation {{
            padding: 30px;
            max-height: 70vh;
            overflow-y: auto;
        }}
        
        .message {{
            margin-bottom: 25px;
            animation: fadeInUp 0.5s ease-out;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .message.user {{
            text-align: right;
        }}
        
        .message.assistant {{
            text-align: left;
        }}
        
        .message-content {{
            display: inline-block;
            max-width: 85%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 1.05em;
            line-height: 1.5;
            position: relative;
            word-wrap: break-word;
        }}
        
        .user .message-content {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }}
        
        .assistant .message-content {{
            background: #f8f9fa;
            color: #2d3748;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 5px;
        }}
        
        .timestamp {{
            font-size: 0.85em;
            color: #718096;
            margin: 5px 15px;
            font-style: italic;
        }}
        
        .message-content pre {{
            background: rgba(0, 0, 0, 0.05);
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            overflow-x: auto;
            font-size: 0.9em;
        }}
        
        .message-content code {{
            background: rgba(0, 0, 0, 0.05);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        .user .message-content pre,
        .user .message-content code {{
            background: rgba(255, 255, 255, 0.2);
        }}
        
        .footer {{
            background: #f7fafc;
            padding: 20px 30px;
            text-align: center;
            color: #718096;
            border-top: 1px solid #e2e8f0;
        }}
        
        .scroll-indicator {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            transform-origin: left;
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        /* Scrollbar styling */
        .conversation::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .conversation::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        .conversation::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }}
        
        .conversation::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                border-radius: 15px;
            }}
            
            .header {{
                padding: 25px 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .conversation {{
                padding: 20px;
            }}
            
            .message-content {{
                max-width: 95%;
                padding: 12px 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="scroll-indicator"></div>
    <div class="container">
        <div class="header">
            <h1>🤖 Grok Multi-Model Chat</h1>
            <p><strong>Agent:</strong> {agent_id}</p>
            <p><strong>Model:</strong> {model_name}</p>
            <p><strong>Exported:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="conversation">"""
    
    # Add messages
    for msg in messages:
        if msg.get("role") in ["user", "assistant"]:
            timestamp_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            role = msg["role"]
            content = msg["content"].replace("\n", "<br>").replace("```", "<pre>").replace("</pre>", "</pre>")
            
            # Simple code block formatting
            content = content.replace("`", "<code>").replace("</code>", "</code>")
            
            html_template += f"""
            <div class="message {role}">
                <div class="timestamp">{timestamp_str}</div>
                <div class="message-content">{content}</div>
            </div>"""
    
    # Close HTML
    html_template += f"""
        </div>
        
        <div class="footer">
            <p>Generated by Grok Multi-Model Chat Agent | Total Messages: {len([m for m in messages if m.get('role') in ['user', 'assistant']])}</p>
        </div>
    </div>
    
    <script>
        // Scroll progress indicator
        function updateScrollProgress() {{
            const conversation = document.querySelector('.conversation');
            const scrollIndicator = document.querySelector('.scroll-indicator');
            const scrollPercent = (conversation.scrollTop / (conversation.scrollHeight - conversation.clientHeight)) * 100;
            scrollIndicator.style.transform = `scaleX(${{scrollPercent / 100}})`;
        }}
        
        document.querySelector('.conversation').addEventListener('scroll', updateScrollProgress);
        
        // Auto-scroll to bottom on load
        window.addEventListener('load', function() {{
            const conversation = document.querySelector('.conversation');
            conversation.scrollTop = conversation.scrollHeight;
        }});
    </script>
</body>
</html>"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return str(filepath)

def get_export_formats() -> List[str]:
    """Get list of supported export formats"""
    return ["json", "txt", "md", "html"]

def validate_export_format(format_type: str) -> bool:
    """Validate if export format is supported"""
    return format_type.lower() in get_export_formats()