"""
API Documentation and Examples

This file contains examples of how to use the main components 
of the application programmatically.
"""

import os
from dotenv import load_dotenv
from agents import answer
from ml_logic import classify_text, get_category_description

# Load environment variables
load_dotenv()

def example_using_agent():
    """Example of using the LLM agent"""
    print("=== Using the LLM Agent ===")
    
    questions = [
        "What is machine learning?",
        "How does the Groq API work?",
        "Explain the difference between classification and regression"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        try:
            response = answer(question)
            print(f"Response: {response[:100]}...")  # Just show the first 100 chars
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n")


def example_using_classifier():
    """Example of using the text classifier"""
    print("=== Using the Text Classifier ===")
    
    texts = [
        "I love this product, it's amazing!",
        "This is terrible quality, don't buy it",
        "When will my order arrive?",
        "The store opens at 9am and closes at 6pm"
    ]
    
    for text in texts:
        print(f"\nText: {text}")
        try:
            category = classify_text(text)
            description = get_category_description(category)
            print(f"Category: {category}")
            print(f"Description: {description}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n")


def run_api_examples():
    """Run all API examples"""
    print("\n" + "="*50)
    print("GROQ CLASSIFIER API EXAMPLES")
    print("="*50 + "\n")
    
    print("This script demonstrates how to use the components of this application programmatically.\n")
    
    # Check if Groq API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY environment variable not set.")
        print("The agent examples will fail. Please set this in your .env file.\n")
    
    # Run the classifier example (doesn't need API key)
    example_using_classifier()
    
    # Only run the agent example if API key is set
    if os.getenv("GROQ_API_KEY"):
        example_using_agent()
    
    print("="*50)
    print("API examples completed")
    print("="*50 + "\n")


if __name__ == "__main__":
    run_api_examples() 