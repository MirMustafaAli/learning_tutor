"""Cross-Domain Learning Tutor Streamlit Application.

This module implements a Streamlit web interface for the Cross-Domain Learning Tutor,
allowing professionals to learn new fields through explanations adapted to their
current area of expertise.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from tutor_pipeline import CrossDomainTutor

def initialize_app(source_field: str, target_field: str) -> CrossDomainTutor:
    """Initialize the application and its dependencies.
    
    Args:
        source_field (str): The field the user is proficient in.
        target_field (str): The field the user wants to learn about.
        
    Returns:
        CrossDomainTutor: An initialized tutor instance.
        
    Raises:
        ValueError: If the OpenAI API key is not found in environment variables.
    """
    # Load environment variables
    load_dotenv()
    
    # Verify API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize the tutor
    return CrossDomainTutor(source_field, target_field)

def main():
    """Main application entry point."""
    # Set up the Streamlit page
    st.set_page_config(
        page_title="Cross-Domain Learning Tutor",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Cross-Domain Learning Tutor")
    st.markdown("""
    This tutor helps you explore new fields by adapting explanations to your current expertise.
    Whether you're a programmer learning biology, a mathematician exploring art, or any other
    combination, we'll help bridge the gap between your knowledge and new concepts.
    """)
    
    # Field selection
    col1, col2 = st.columns(2)
    with col1:
        source_field = st.text_input(
            "I have expertise in",
            placeholder="e.g., Software Engineering, Physics, Psychology",
            help="Enter your field of expertise"
        )
    with col2:
        target_field = st.text_input(
            "I want to explore",
            placeholder="e.g., Quantum Computing, Neuroscience, Design",
            help="Enter the field you want to learn about"
        )
    
    # Initialize session state for conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(f"What would you like to know about {target_field}?"):
        if not source_field or not target_field:
            st.warning("Please specify both your field of expertise and the field you want to explore!")
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get tutor response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Initialize the tutor with selected fields
                        tutor = initialize_app(source_field, target_field)
                        
                        # Get the explanation
                        response = tutor.get_explanation(prompt)
                        
                        # Display the response
                        st.markdown(response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            
            # Add feedback section
            st.markdown("### Was this helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes", key="yes_button"):
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 No", key="no_button"):
                    st.info("We'll try to improve our explanations!")

if __name__ == "__main__":
    main() 