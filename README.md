# Rust Learning Tutor for Python Developers

An AI-powered tutor that helps Python developers learn Rust by adapting explanations and concepts to be more familiar to Python developers.

## Features

- Interactive web interface built with Streamlit
- Two-step AI pipeline:
  1. Generates detailed Rust explanations
  2. Adapts explanations for Python developers
- Draws parallels between Python and Rust concepts
- Provides code examples in both languages
- User feedback system

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

1. Enter your Rust-related question in the text area
2. Click "Get Explanation" to receive a Python-friendly explanation
3. Provide feedback on the explanation using the thumbs up/down buttons

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API access

## Note

This application uses the OpenAI API and will incur costs based on your API usage. Make sure to monitor your API usage and costs. 