"""System prompts for the Cross-Domain Learning Tutor.

This package contains system prompts for different components of the tutor:
- Expert tutor prompts for generating detailed explanations
- Field adapter prompts for translating between different areas of expertise
- Test generator prompts for creating adaptive assessments
"""

from .expert_tutor import get_expert_prompt
from .field_adapter import get_adapter_prompt
from .test_generator import get_test_generator_prompt

__all__ = [
    'get_expert_prompt',
    'get_adapter_prompt',
    'get_test_generator_prompt'
] 