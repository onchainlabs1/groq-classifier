import streamlit as st
from agents import answer
from ml_logic import classify_text, get_category_description
import time

# Set page configuration
st.set_page_config(
    page_title="AI Assistant & Text Classifier",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def add_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4B8BF5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5C5C5C;
        margin-bottom: 1.5rem;
    }
    .category-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .positive-box {
        background-color: #D6F5D6;
        border: 1px solid #4CAF50;
    }
    .negative-box {
        background-color: #F5D6D6;
        border: 1px solid #F44336;
    }
    .question-box {
        background-color: #D6E6F5;
        border: 1px solid #2196F3;
    }
    .informational-box {
        background-color: #E6D6F5;
        border: 1px solid #9C27B0;
    }
    .uncertain-box {
        background-color: #F5F5D6;
        border: 1px solid #FFC107;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    add_custom_css()
    
    # Header
    st.markdown('<h1 class="main-header">AI Assistant & Text Classifier</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Groq API and scikit-learn</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.groq.com/images/groq-logo.svg", width=200)
        st.markdown("### About")
        st.markdown("""
        This application combines:
        - **LLM Agent**: Uses Groq's llama3-70b-8192 model
        - **ML Classifier**: Uses scikit-learn to categorize text
        """)
        
        st.markdown("### Categories")
        st.markdown("""
        The classifier can identify:
        - 😊 **Positive** sentiment
        - 😠 **Negative** sentiment
        - ❓ **Questions** seeking information
        - ℹ️ **Informational** content
        """)
    
    # Text input field
    user_text = st.text_area("Enter your text or question:", height=150)
    
    # Split into two columns for buttons
    col1, col2 = st.columns(2)
    
    # Button to answer with the agent
    if col1.button("Answer with Agent 🤖", use_container_width=True):
        if user_text:
            with st.spinner("Generating response..."):
                # Add a slight delay to show the spinner
                time.sleep(0.5)
                result = answer(user_text)
                
                st.markdown("### 🤖 Agent Response:")
                st.write(result)
        else:
            st.warning("⚠️ Please enter a question first.")
    
    # Button to classify the text
    if col2.button("Classify Text 🔍", use_container_width=True):
        if user_text:
            with st.spinner("Analyzing text..."):
                # Add a slight delay to show the spinner
                time.sleep(0.5)
                category = classify_text(user_text)
                description = get_category_description(category)
                
                st.markdown("### 🔍 Classification Result:")
                
                # Format the output based on the category
                category_icon = {
                    "positive": "😊",
                    "negative": "😠",
                    "question": "❓",
                    "informational": "ℹ️",
                    "uncertain": "🤔"
                }.get(category, "🔍")
                
                category_class = {
                    "positive": "positive-box",
                    "negative": "negative-box",
                    "question": "question-box",
                    "informational": "informational-box",
                    "uncertain": "uncertain-box"
                }.get(category, "")
                
                st.markdown(f"""
                <div class="category-box {category_class}">
                    <h3>{category_icon} {category.upper()}</h3>
                    <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show example response based on category
                if category == "question":
                    st.markdown("### 🤖 Suggested Response:")
                    with st.spinner("Generating answer to question..."):
                        response = answer(user_text)
                        st.write(response)
        else:
            st.warning("⚠️ Please enter a text first.")
    
    # Instructions
    with st.expander("How to use this application"):
        st.markdown("""
        ### Instructions:
        1. **Answer with Agent**: Get detailed answers to your questions using a powerful language model
        2. **Classify Text**: Analyze what type of content your text represents
        
        ### Tips:
        - For best results with the agent, ask clear and specific questions
        - For classification, provide complete sentences or paragraphs
        - The classifier works best on English text
        
        ### Setup:
        Make sure to set up your `.env` file with your Groq API key:
        ```
        GROQ_API_KEY=your_key_here
        ```
        """)

if __name__ == "__main__":
    main() 