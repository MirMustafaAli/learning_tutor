"""Programming Language Tutor Pipeline.

This module implements a two-step pipeline for helping developers learn new programming languages:
1. An expert model that generates detailed explanations in the target language
2. A language adapter model that makes the explanations more accessible to developers
   familiar with a different language.
"""

import os
from typing import Optional, Tuple
from openai import OpenAI
from prompts import get_expert_prompt, get_adapter_prompt

class LanguageTutorPipeline:
    """A pipeline for generating language-adapted programming explanations.
    
    This class implements a two-step process:
    1. Generate a detailed explanation in the target language using GPT-4
    2. Adapt the explanation for developers familiar with a different language using GPT-4
    
    Attributes:
        client (OpenAI): The OpenAI client instance for making API calls.
        source_language (str): The programming language the user is proficient in.
        target_language (str): The programming language the user wants to learn.
    """
    
    def __init__(self, source_language: str, target_language: str, api_key: Optional[str] = None):
        """Initialize the LanguageTutorPipeline.
        
        Args:
            source_language (str): The programming language the user is proficient in.
            target_language (str): The programming language the user wants to learn.
            api_key (Optional[str]): OpenAI API key. If not provided, will be read from environment.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.source_language = source_language
        self.target_language = target_language
        
    def get_explanation(self, query: str) -> str:
        """Process the user's query through the two-step pipeline.
        
        Args:
            query (str): The user's question about the target language.
            
        Returns:
            str: A source-language-friendly explanation of the target language concept.
            
        Raises:
            ValueError: If the query is empty or None.
            Exception: If there's an error with the OpenAI API call.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
            
        # Step 1: Generate target language explanation
        target_explanation = self._generate_target_explanation(query)
        
        # Step 2: Adapt for source language developers
        adapted_explanation = self._adapt_for_source_language(target_explanation)
        
        return adapted_explanation
    
    def _generate_target_explanation(self, query: str) -> str:
        """Generate a detailed explanation in the target language.
        
        Args:
            query (str): The user's question about the target language.
            
        Returns:
            str: A detailed explanation of the target language concept.
            
        Raises:
            Exception: If there's an error with the OpenAI API call.
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": get_expert_prompt(self.target_language)},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _adapt_for_source_language(self, target_explanation: str) -> str:
        """Adapt the target language explanation for source language developers.
        
        Args:
            target_explanation (str): The original target language explanation.
            
        Returns:
            str: A source-language-friendly version of the explanation.
            
        Raises:
            Exception: If there's an error with the OpenAI API call.
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": get_adapter_prompt(self.source_language, self.target_language)},
                {"role": "user", "content": target_explanation}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content 