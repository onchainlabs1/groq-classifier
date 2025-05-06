import streamlit as st
from agents import answer
from ml_logic import classify_text

def main():
    st.title("AI Assistant and Text Classifier")
    
    # Text input field
    user_text = st.text_area("Enter your text or question:", height=150)
    
    # Split into two columns for buttons
    col1, col2 = st.columns(2)
    
    result = None
    
    # Button to answer with the agent
    if col1.button("Answer with Agent"):
        with st.spinner("Generating response..."):
            if user_text:
                result = answer(user_text)
                st.subheader("Agent Response:")
                st.write(result)
            else:
                st.warning("Please enter a question first.")
    
    # Button to classify the text
    if col2.button("Classify Text"):
        with st.spinner("Classifying text..."):
            if user_text:
                category = classify_text(user_text)
                st.subheader("Classification:")
                
                # Color the category according to the result
                if category == "positive":
                    st.success(f"The text was classified as: {category.upper()}")
                elif category == "negative":
                    st.error(f"The text was classified as: {category.upper()}")
                else:
                    st.info(f"Classification: {category}")
            else:
                st.warning("Please enter a text first.")
    
    # Instructions section
    with st.expander("How to use"):
        st.markdown("""
        ### Instructions:
        1. **Answer with Agent**: Use this option to get answers to general questions using our LLM model.
        2. **Classify Text**: Use this option to analyze the sentiment of the text (positive or negative).
        
        Make sure to properly configure the `.env` file with your Groq API key to use the agent.
        """)

if __name__ == "__main__":
    main() 