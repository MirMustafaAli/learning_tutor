"""Programming Language Tutor Streamlit Application.

This module implements a Streamlit web interface for the Programming Language Tutor,
allowing developers to learn new programming languages through explanations adapted
to their current language proficiency.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from tutor_pipeline import LanguageTutorPipeline

def initialize_app(source_language: str, target_language: str) -> LanguageTutorPipeline:
    """Initialize the application and its dependencies.
    
    Args:
        source_language (str): The programming language the user is proficient in.
        target_language (str): The programming language the user wants to learn.
        
    Returns:
        LanguageTutorPipeline: An initialized pipeline instance.
        
    Raises:
        ValueError: If the OpenAI API key is not found in environment variables.
    """
    # Load environment variables
    load_dotenv()
    
    # Verify API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize the pipeline
    return LanguageTutorPipeline(source_language, target_language)

def main():
    """Main application entry point."""
    # Set up the Streamlit page
    st.set_page_config(
        page_title="Programming Language Tutor",
        page_icon="👨‍💻",
        layout="wide"
    )
    
    st.title("👨‍💻 Programming Language Tutor")
    st.markdown("""
    This tutor helps you learn new programming languages by adapting explanations
    to your current language proficiency.
    """)
    
    # Language selection
    col1, col2 = st.columns(2)
    with col1:
        source_language = st.text_input(
            "I am proficient in",
            placeholder="e.g., Python, JavaScript, Java",
            help="Enter the programming language you are most comfortable with"
        )
    with col2:
        target_language = st.text_input(
            "I want to learn",
            placeholder="e.g., Rust, Go, TypeScript",
            help="Enter the programming language you want to learn"
        )
    
    # User input
    user_query = st.text_area(
        f"What would you like to learn about {target_language}?",
        placeholder=f"Example: How do I handle errors in {target_language}?",
        height=100
    )
    
    if st.button("Get Explanation"):
        if not source_language or not target_language:
            st.warning("Please specify both your proficient language and the language you want to learn!")
        elif not user_query:
            st.warning("Please enter a question!")
        else:
            with st.spinner("Generating explanation..."):
                try:
                    # Initialize the pipeline with selected languages
                    tutor = initialize_app(source_language, target_language)
                    
                    # Get the explanation
                    explanation = tutor.get_explanation(user_query)
                    
                    # Display the explanation
                    st.markdown("### Explanation")
                    st.markdown(explanation)
                    
                    # Add a feedback section
                    st.markdown("### Was this helpful?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👍 Yes"):
                            st.success("Thank you for your feedback!")
                    with col2:
                        if st.button("👎 No"):
                            st.info("We'll try to improve our explanations!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 