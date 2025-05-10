"""Cross-Domain Learning Tutor Pipeline.

This module implements a two-step pipeline for helping professionals learn new fields
through explanations adapted to their current area of expertise.
"""

import json
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from prompts import get_expert_prompt, get_adapter_prompt, get_test_generator_prompt

class CrossDomainTutor:
    """A tutor that helps professionals learn new fields through adapted explanations."""
    
    def __init__(self, source_field: str, target_field: str):
        """Initialize the tutor.
        
        Args:
            source_field (str): The field the user is proficient in.
            target_field (str): The field the user wants to learn about.
        """
        self.source_field = source_field
        self.target_field = target_field
        self.client = OpenAI()
        self.conversation_history: List[Dict[str, str]] = []
        self.test_history: List[Dict] = []
        self.current_difficulty = 1
        
    def get_explanation(self, query: str) -> str:
        """Get an explanation adapted to the user's field of expertise.
        
        Args:
            query (str): The user's question about the target field.
            
        Returns:
            str: An explanation adapted to the user's field.
        """
        # Step 1: Generate detailed explanation in target field
        target_explanation = self._generate_target_explanation(query)
        
        # Step 2: Adapt the explanation for the source field
        adapted_explanation = self._adapt_for_source_field(target_explanation)
        
        # Update conversation history
        self.conversation_history.append({
            "role": "user",
            "content": query
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": adapted_explanation
        })
        
        return adapted_explanation
    
    def generate_test(self) -> Dict:
        """Generate a test with 5 MCQs at the current difficulty level.
        
        Returns:
            Dict: A dictionary containing the test questions and metadata.
        """
        # Get the test generator prompt
        prompt = get_test_generator_prompt(
            self.source_field,
            self.target_field,
            self.current_difficulty
        )
        
        # Generate the test
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Generate a test with 5 MCQs."}
            ],
            temperature=0.7
        )
        
        # Parse the response
        try:
            test_data = json.loads(response.choices[0].message.content)
            self.test_history.append(test_data)
            return test_data
        except json.JSONDecodeError:
            raise ValueError("Failed to generate a valid test format")
    
    def evaluate_test(self, test_data: Dict, user_answers: Dict[str, str]) -> Tuple[float, bool]:
        """Evaluate a test and determine if difficulty should increase.
        
        Args:
            test_data (Dict): The test data containing questions and correct answers.
            user_answers (Dict[str, str]): Dictionary mapping question indices to user's answers.
            
        Returns:
            Tuple[float, bool]: (score as percentage, whether to increase difficulty)
        """
        correct_count = 0
        total_questions = len(test_data["questions"])
        
        for i, question in enumerate(test_data["questions"]):
            if user_answers.get(str(i)) == question["correct_answer"]:
                correct_count += 1
        
        score = (correct_count / total_questions) * 100
        
        # Increase difficulty if score is 80% or higher
        should_increase = score >= 80
        if should_increase and self.current_difficulty < 5:
            self.current_difficulty += 1
        
        return score, should_increase
    
    def _generate_target_explanation(self, query: str) -> str:
        """Generate a detailed explanation in the target field.
        
        Args:
            query (str): The user's question.
            
        Returns:
            str: A detailed explanation in the target field.
        """
        # Get recent context
        recent_context = self.conversation_history[-4:] if self.conversation_history else []
        
        # Generate the explanation
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": get_expert_prompt(self.target_field)},
                *[{"role": msg["role"], "content": msg["content"]} for msg in recent_context],
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _adapt_for_source_field(self, target_explanation: str) -> str:
        """Adapt an explanation for the source field.
        
        Args:
            target_explanation (str): The explanation in the target field.
            
        Returns:
            str: An explanation adapted for the source field.
        """
        # Get recent context
        recent_context = self.conversation_history[-4:] if self.conversation_history else []
        
        # Adapt the explanation
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": get_adapter_prompt(self.source_field, self.target_field)},
                *[{"role": msg["role"], "content": msg["content"]} for msg in recent_context],
                {"role": "user", "content": f"Please adapt this explanation for someone with {self.source_field} background:\n\n{target_explanation}"}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content 