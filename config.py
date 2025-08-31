#!/usr/bin/env python3
"""
Configuration management with dataclasses for Grok Multi-Model Chat Agent
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime

# Supported models configuration
SUPPORTED_MODELS = {
    'grok3': {
        'name': 'Grok 3',
        'model_name': 'grok-3-latest',
        'api_url': 'https://api.x.ai/v1/chat/completions',
        'max_tokens': 32768,
        'timeout': 300
    },
    'grok3mini': {
        'name': 'Grok 3 Mini',
        'model_name': 'grok-3-mini-latest', 
        'api_url': 'https://api.x.ai/v1/chat/completions',
        'max_tokens': 32768,
        'timeout': 300
    },
    'grok4': {
        'name': 'Grok 4',
        'model_name': 'grok-4-latest',
        'api_url': 'https://api.x.ai/v1/chat/completions',
        'max_tokens': 32768,
        'timeout': 300
    }
}

# Supported file extensions for inclusion
SUPPORTED_EXTENSIONS = {
    # Programming languages
    '.py', '.r', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc', '.cxx',
    '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
    '.clj', '.hs', '.ml', '.fs', '.vb', '.pl', '.pm', '.sh', '.bash', '.zsh', '.fish',
    '.ps1', '.bat', '.cmd', '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.xml', '.xsl', '.xslt', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    '.properties', '.env', '.dockerfile', '.docker', '.makefile', '.cmake', '.gradle',
    '.sbt', '.pom', '.lock', '.mod', '.sum',

    # Data and markup
    '.md', '.markdown', '.rst', '.tex', '.latex', '.csv', '.tsv', '.jsonl', '.ndjson',
    '.svg', '.rss', '.atom', '.plist',

    # Configuration and infrastructure
    '.tf', '.tfvars', '.hcl', '.nomad', '.consul', '.vault', '.k8s', '.kubectl',
    '.helm', '.kustomize', '.ansible', '.inventory', '.playbook',

    # Documentation and text
    '.txt', '.log', '.out', '.err', '.trace', '.debug', '.info', '.warn', '.error',
    '.readme', '.license', '.changelog', '.authors', '.contributors', '.todo',

    # Notebooks and scripts
    '.ipynb', '.rmd', '.qmd', '.jl', '.m', '.octave', '.R', '.Rmd',

    # Web and API
    '.graphql', '.gql', '.rest', '.http', '.api', '.postman', '.insomnia',

    # Other useful formats
    '.editorconfig', '.gitignore', '.gitattributes', '.dockerignore', '.eslintrc',
    '.prettierrc', '.babelrc', '.webpack', '.rollup', '.vite', '.parcel'
}

@dataclass
class AgentConfig:
    """Configuration parameters for the Grok Chat Agent"""
    model: str = "grok-4-latest"
    temperature: float = 0.0
    max_tokens: Optional[int] = 32768
    max_history_size: int = 1000
    stream: bool = True
    system_prompt: Optional[str] = "You are a helpful assistant."
    top_p: float = 1.0
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        """Post-initialization setup"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        """Create configuration from dictionary"""
        return cls(**data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now().isoformat()

    def get_model_info(self, model_key: str) -> Dict[str, Any]:
        """Get model information for the specified model key"""
        return SUPPORTED_MODELS.get(model_key, SUPPORTED_MODELS['grok4'])

    def validate(self) -> bool:
        """Validate configuration parameters"""
        if not (0.0 <= self.temperature <= 2.0):
            return False
        if self.max_tokens is not None and self.max_tokens <= 0:
            return False
        if self.max_history_size <= 0:
            return False
        if not (0.0 <= self.top_p <= 1.0):
            return False
        return True