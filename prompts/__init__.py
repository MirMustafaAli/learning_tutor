"""Prompts package for the Programming Language Tutor.

This package contains system prompts used by the Programming Language Tutor pipeline.
"""

from .expert_tutor import get_expert_prompt
from .language_adapter import get_adapter_prompt

__all__ = ['get_expert_prompt', 'get_adapter_prompt'] 