# AI Assistant and Text Classifier

This project combines an LLM agent using the Groq API with a scikit-learn-based text classifier.

## Features

- **LLM Agent**: Answers general questions using the llama3-70b-8192 model via Groq API
- **Text Classifier**: Analyzes sentiment by classifying texts as positive or negative
- **Streamlit Interface**: User-friendly interface to interact with both features

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following content:
   ```
   GROQ_API_KEY=your_key_here
   ```
   Replace `your_key_here` with your Groq API key.

## Running the Application

To start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## Project Structure

- `agents.py`: Contains the LLM agent implementation using LangChain and Groq
- `ml_logic.py`: Implements the text classifier using scikit-learn
- `app.py`: Streamlit interface to interact with the agent and classifier
- `requirements.txt`: Project dependencies list

## Requirements

- Python 3.8+
- Internet connection to access the Groq API 