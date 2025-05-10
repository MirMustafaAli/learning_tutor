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
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_test' not in st.session_state:
        st.session_state.current_test = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Create tabs for different modes
    chat_tab, test_tab = st.tabs(["💬 Chat", "📝 Test Your Knowledge"])
    
    with chat_tab:
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
    
    with test_tab:
        if not source_field or not target_field:
            st.warning("Please specify both your field of expertise and the field you want to explore!")
        else:
            # Initialize tutor
            tutor = initialize_app(source_field, target_field)
            
            # Generate new test if none exists
            if st.session_state.current_test is None:
                if st.button("Generate New Test"):
                    with st.spinner("Generating test..."):
                        try:
                            st.session_state.current_test = tutor.generate_test()
                            st.session_state.user_answers = {}
                            st.session_state.show_results = False
                        except Exception as e:
                            st.error(f"Failed to generate test: {str(e)}")
            
            # Display current test
            if st.session_state.current_test:
                st.markdown(f"### Test (Difficulty Level: {st.session_state.current_test['difficulty_level']})")
                
                for i, question in enumerate(st.session_state.current_test["questions"]):
                    st.markdown(f"**Question {i+1}:** {question['question']}")
                    
                    # Display options as radio buttons
                    options = list(question["options"].items())
                    selected = st.radio(
                        f"Select your answer for Question {i+1}",
                        options=[opt[0] for opt in options],
                        format_func=lambda x: f"{x}: {question['options'][x]}",
                        key=f"q{i}"
                    )
                    if selected:
                        st.session_state.user_answers[str(i)] = selected
                
                # Submit button
                if st.button("Submit Test"):
                    if len(st.session_state.user_answers) == len(st.session_state.current_test["questions"]):
                        score, should_increase = tutor.evaluate_test(
                            st.session_state.current_test,
                            st.session_state.user_answers
                        )
                        
                        st.session_state.show_results = True
                        
                        # Display results
                        st.markdown("### Test Results")
                        st.markdown(f"**Score:** {score:.1f}%")
                        
                        if should_increase:
                            st.success("Great job! The next test will be more challenging.")
                        else:
                            st.info("Keep practicing! You can try another test at the same difficulty level.")
                        
                        # Display explanations
                        st.markdown("### Detailed Explanations")
                        for i, question in enumerate(st.session_state.current_test["questions"]):
                            with st.expander(f"Question {i+1} Explanation"):
                                st.markdown(f"**Correct Answer:** {question['correct_answer']}")
                                st.markdown(f"**Explanation:** {question['explanation']}")
                                st.markdown(f"**Connection to {source_field}:** {question['source_field_connection']}")
                        
                        # Option to generate new test
                        if st.button("Generate New Test"):
                            st.session_state.current_test = None
                            st.session_state.user_answers = {}
                            st.session_state.show_results = False
                            st.experimental_rerun()
                    else:
                        st.warning("Please answer all questions before submitting!")

if __name__ == "__main__":
    main() 