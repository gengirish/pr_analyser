"""File utility functions."""

import json
import os
from pathlib import Path
from typing import Any, Dict


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def save_json(data: Any, filepath: str, indent: int = 2):
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filepath: Output file path
        indent: JSON indentation
    """
    # Ensure directory exists
    ensure_directory(os.path.dirname(filepath) or '.')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_json(filepath: str) -> Any:
    """
    Load data from a JSON file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_text(content: str, filepath: str):
    """
    Save text content to a file.
    
    Args:
        content: Text content
        filepath: Output file path
    """
    # Ensure directory exists
    ensure_directory(os.path.dirname(filepath) or '.')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def load_text(filepath: str) -> str:
    """
    Load text content from a file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Text content
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
