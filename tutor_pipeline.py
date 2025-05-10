"""Cross-Domain Learning Tutor Pipeline.

This module implements a two-step pipeline for helping professionals learn new fields:
1. An expert model that generates detailed explanations in the target field
2. A field adapter model that makes the explanations more accessible to professionals
   from a different field.
"""

import os
from typing import Optional, List, Dict
from openai import OpenAI
from prompts import get_expert_prompt, get_adapter_prompt

class CrossDomainTutor:
    """A pipeline for generating field-adapted explanations.
    
    This class implements a two-step process:
    1. Generate a detailed explanation in the target field using GPT-4
    2. Adapt the explanation for professionals from a different field using GPT-4
    
    Attributes:
        client (OpenAI): The OpenAI client instance for making API calls.
        source_field (str): The field the user is proficient in.
        target_field (str): The field the user wants to learn about.
        conversation_history (List[Dict]): History of the conversation for context.
    """
    
    def __init__(self, source_field: str, target_field: str, api_key: Optional[str] = None):
        """Initialize the CrossDomainTutor.
        
        Args:
            source_field (str): The field the user is proficient in.
            target_field (str): The field the user wants to learn about.
            api_key (Optional[str]): OpenAI API key. If not provided, will be read from environment.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.source_field = source_field
        self.target_field = target_field
        self.conversation_history = []
        
    def get_explanation(self, query: str) -> str:
        """Process the user's query through the two-step pipeline.
        
        Args:
            query (str): The user's question or topic about the target field.
            
        Returns:
            str: A source-field-friendly explanation of the target field concept.
            
        Raises:
            ValueError: If the query is empty or None.
            Exception: If there's an error with the OpenAI API call.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
            
        # Add user query to conversation history
        self.conversation_history.append({"role": "user", "content": query})
            
        # Step 1: Generate target field explanation
        target_explanation = self._generate_target_explanation(query)
        
        # Step 2: Adapt for source field professionals
        adapted_explanation = self._adapt_for_source_field(target_explanation)
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": adapted_explanation})
        
        return adapted_explanation
    
    def _generate_target_explanation(self, query: str) -> str:
        """Generate a detailed explanation in the target field.
        
        Args:
            query (str): The user's question about the target field.
            
        Returns:
            str: A detailed explanation of the target field concept.
            
        Raises:
            Exception: If there's an error with the OpenAI API call.
        """
        recent_context = self.conversation_history[-4:] if self.conversation_history else []
        messages = [
            {"role": "system", "content": get_expert_prompt(self.target_field)},
            *recent_context,
            {"role": "user", "content": query}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _adapt_for_source_field(self, target_explanation: str) -> str:
        """Adapt the target field explanation for source field professionals.
        
        Args:
            target_explanation (str): The original target field explanation.
            
        Returns:
            str: A source-field-friendly version of the explanation.
            
        Raises:
            Exception: If there's an error with the OpenAI API call.
        """
        recent_context = self.conversation_history[-4:] if self.conversation_history else []
        messages = [
            {"role": "system", "content": get_adapter_prompt(self.source_field, self.target_field)},
            *recent_context,
            {"role": "user", "content": target_explanation}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content 