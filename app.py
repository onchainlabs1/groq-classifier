import streamlit as st
from agents import answer
from ml_logic import classify_text, get_category_description, get_classifier_metrics
import time
import os
from data_utils import save_classification_results
import pandas as pd
import base64
import numpy as np
import matplotlib.pyplot as plt

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
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .positive-box {
        background-color: #43a047 !important;
        border: 2px solid #1b5e20;
        color: #fff !important;
    }
    .negative-box {
        background-color: #ff4d4f !important;
        border: 2px solid #b71c1c;
        color: #fff !important;
    }
    .question-box {
        background-color: #1976d2 !important;
        border: 2px solid #0d47a1;
        color: #fff !important;
    }
    .informational-box {
        background-color: #8e24aa !important;
        border: 2px solid #4a148c;
        color: #fff !important;
    }
    .neutral-box {
        background-color: #757575 !important;
        border: 2px solid #212121;
        color: #fff !important;
    }
    .uncertain-box {
        background-color: #ffc107 !important;
        border: 2px solid #ff9800;
        color: #212121 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_csv_download_link(df, filename="classification_results.csv", text="Download CSV"):
    """Generate a download link for a dataframe as CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-link">{text}</a>'
    return href

def create_metrics_charts(metrics):
    """Create charts for model metrics visualization"""
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    # Plot 1: Per-class F1 scores
    class_f1 = {}
    report = metrics['classification_report']
    
    for class_name, metrics_dict in report.items():
        if class_name not in ['accuracy', 'macro avg', 'weighted avg']:
            class_f1[class_name] = metrics_dict['f1-score']
    
    axes[0].bar(class_f1.keys(), class_f1.values(), color='skyblue')
    axes[0].set_title('F1 Score by Category')
    axes[0].set_ylim([0, 1])
    axes[0].set_ylabel('F1 Score')
    axes[0].set_xlabel('Category')
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Plot 2: Cross-validation scores
    cv_scores = metrics['cv_scores']
    axes[1].boxplot(cv_scores)
    axes[1].set_title('Cross-Validation Scores')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_ylim([0, 1])
    
    plt.tight_layout()
    return fig

def main():
    add_custom_css()
    
    # Initialize session state for storing classification history
    if 'classification_history' not in st.session_state:
        st.session_state.classification_history = []
    
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
        - 🔍 **Neutral** factual or ambiguous statements
        """)
        
        # API Key input
        st.markdown("### API Configuration")
        api_key = st.text_input("Enter your Groq API Key:", type="password", 
                               help="Required only for the 'Answer with Agent' feature")
        
        if api_key:
            # Store the API key in session state
            st.session_state.groq_api_key = api_key
            st.success("API Key set! You can now use the agent.")
        else:
            st.warning("No API Key provided. Agent feature will be limited.")
            
        # Classification History and Export
        if st.session_state.classification_history:
            st.markdown("### Classification History")
            st.write(f"You have classified {len(st.session_state.classification_history)} texts.")
            
            # Export to CSV button
            if st.button("Export All Classifications to CSV"):
                try:
                    # Create DataFrame from history
                    history_df = pd.DataFrame(st.session_state.classification_history)
                    
                    # Save to CSV file
                    file_path = save_classification_results(
                        history_df['text'].tolist(), 
                        history_df['category'].tolist()
                    )
                    
                    st.success(f"Classifications saved to {file_path}")
                    st.markdown(get_csv_download_link(history_df), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error exporting data: {str(e)}")
            
            # Clear history button
            if st.button("Clear History"):
                st.session_state.classification_history = []
                st.success("History cleared!")
    
    # Create tabs for main functionality
    tab1, tab2, tab3 = st.tabs(["Classify & Answer", "Model Metrics", "Batch Processing"])
    
    # Tab 1: Main classification and answering functionality
    with tab1:
        # Text input field
        user_text = st.text_area("Enter your text or question:", height=150)
        
        # Split into two columns for buttons
        col1, col2 = st.columns(2)
        
        # Button to answer with the agent
        if col1.button("Answer with Agent 🤖", use_container_width=True):
            if user_text:
                with st.spinner("Generating response..."):
                    # Set API key for this request if available in session state
                    if hasattr(st.session_state, 'groq_api_key') and st.session_state.groq_api_key:
                        # Temporarily set environment variable for this request
                        os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key
                    
                    # Check if API key is available
                    if "GROQ_API_KEY" in os.environ and os.environ["GROQ_API_KEY"]:
                        # Add a slight delay to show the spinner
                        time.sleep(0.5)
                        result = answer(user_text)
                        
                        st.markdown("### 🤖 Agent Response:")
                        st.write(result)
                    else:
                        st.error("⚠️ No Groq API key found. Please enter your API key in the sidebar.")
                        st.info("You can get an API key from [Groq Console](https://console.groq.com/).")
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
                    
                    # Add to classification history
                    st.session_state.classification_history.append({
                        'text': user_text,
                        'category': category,
                        'description': description,
                        'timestamp': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    st.markdown("### 🔍 Classification Result:")
                    
                    # Format the output based on the category
                    category_icon = {
                        "positive": "😊",
                        "negative": "😠",
                        "question": "❓",
                        "informational": "ℹ️",
                        "neutral": "🔍",
                        "uncertain": "🤔"
                    }.get(category, "🔍")
                    
                    category_class = {
                        "positive": "positive-box",
                        "negative": "negative-box",
                        "question": "question-box",
                        "informational": "informational-box",
                        "neutral": "neutral-box",
                        "uncertain": "uncertain-box"
                    }.get(category, "")
                    
                    st.markdown(f"""
                    <div class="category-box {category_class}">
                        <h3>{category_icon} {category.upper()}</h3>
                        <p>{description}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show example response based on category
                    if category == "question" and hasattr(st.session_state, 'groq_api_key') and st.session_state.groq_api_key:
                        st.markdown("### 🤖 Suggested Response:")
                        with st.spinner("Generating answer to question..."):
                            # Temporarily set environment variable for this request
                            os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key
                            response = answer(user_text)
                            st.write(response)
                    elif category == "question":
                        st.info("💡 This appears to be a question. Add your Groq API key in the sidebar to get an automatic answer.")
                    
                    # Download single result
                    result_df = pd.DataFrame([{
                        'text': user_text,
                        'category': category,
                        'description': description
                    }])
                    st.markdown(get_csv_download_link(result_df, "single_classification.csv", "💾 Download this result"), unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please enter a text first.")
        
        # Display classification history
        if st.session_state.classification_history:
            with st.expander("View Classification History"):
                history_df = pd.DataFrame(st.session_state.classification_history)
                st.dataframe(history_df, use_container_width=True)
    
    # Tab 2: Model Metrics
    with tab2:
        st.markdown("### Model Performance Metrics")
        st.markdown("""
        This section shows the performance metrics of the text classification model.
        The metrics are calculated using cross-validation on the training data.
        """)
        
        if st.button("Calculate Model Metrics"):
            with st.spinner("Calculating metrics..."):
                try:
                    # Get model metrics
                    metrics = get_classifier_metrics()
                    
                    # Display overall accuracy
                    st.markdown(f"### Overall Performance")
                    st.metric("Mean Cross-Validation Accuracy", f"{metrics['mean_cv_score']:.4f}")
                    
                    # Create and display charts
                    fig = create_metrics_charts(metrics)
                    st.pyplot(fig)
                    
                    # Detailed metrics table
                    st.markdown("### Detailed Metrics by Category")
                    
                    # Create a DataFrame for the classification report
                    report = metrics['classification_report']
                    categories = [cat for cat in report.keys() if cat not in ['accuracy', 'macro avg', 'weighted avg']]
                    
                    report_data = []
                    for cat in categories:
                        report_data.append({
                            'Category': cat,
                            'Precision': f"{report[cat]['precision']:.3f}",
                            'Recall': f"{report[cat]['recall']:.3f}",
                            'F1-Score': f"{report[cat]['f1-score']:.3f}",
                            'Support': report[cat]['support']
                        })
                    
                    report_df = pd.DataFrame(report_data)
                    st.dataframe(report_df, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error calculating metrics: {str(e)}")
    
    # Tab 3: Batch Processing
    with tab3:
        st.markdown("### Batch Text Classification")
        st.markdown("""
        Classify multiple texts at once by uploading a CSV file or entering texts manually.
        """)
        
        batch_method = st.radio(
            "Choose input method:",
            ["Manual Entry", "CSV Upload"]
        )
        
        if batch_method == "Manual Entry":
            batch_texts = st.text_area(
                "Enter multiple texts (one per line):",
                height=200,
                help="Enter each text on a new line. Each line will be classified separately."
            )
            
            if st.button("Classify Batch"):
                if batch_texts:
                    texts = [text.strip() for text in batch_texts.split('\n') if text.strip()]
                    
                    if texts:
                        with st.spinner(f"Classifying {len(texts)} texts..."):
                            results = []
                            for text in texts:
                                category = classify_text(text)
                                description = get_category_description(category)
                                results.append({
                                    'text': text,
                                    'category': category,
                                    'description': description
                                })
                            
                            results_df = pd.DataFrame(results)
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Add download link
                            st.markdown(get_csv_download_link(results_df, "batch_classifications.csv", "💾 Download batch results"), unsafe_allow_html=True)
                            
                            # Show category distribution
                            st.markdown("### Category Distribution")
                            category_counts = results_df['category'].value_counts()
                            st.bar_chart(category_counts)
                    else:
                        st.warning("No valid texts found. Please enter at least one text.")
                else:
                    st.warning("Please enter at least one text to classify.")
        
        else:  # CSV Upload
            uploaded_file = st.file_uploader("Upload CSV file with texts to classify", type=["csv"])
            
            if uploaded_file is not None:
                try:
                    # Load the CSV file
                    df = pd.read_csv(uploaded_file)
                    
                    # Check if the CSV has a text column
                    if 'text' in df.columns:
                        text_column = 'text'
                    else:
                        # Let the user select which column contains the texts
                        text_column = st.selectbox(
                            "Select the column containing texts to classify:",
                            df.columns
                        )
                    
                    # Show preview of the data
                    st.markdown("### Data Preview")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    if st.button("Classify CSV Data"):
                        texts = df[text_column].tolist()
                        
                        with st.spinner(f"Classifying {len(texts)} texts..."):
                            results = []
                            for text in texts:
                                if pd.notna(text):  # Check for NaN values
                                    category = classify_text(str(text))
                                    description = get_category_description(category)
                                    results.append({
                                        'text': text,
                                        'category': category,
                                        'description': description
                                    })
                            
                            results_df = pd.DataFrame(results)
                            
                            # Display results
                            st.markdown("### Classification Results")
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Add download link
                            st.markdown(get_csv_download_link(results_df, "csv_classifications.csv", "💾 Download results"), unsafe_allow_html=True)
                            
                            # Show category distribution
                            st.markdown("### Category Distribution")
                            category_counts = results_df['category'].value_counts()
                            st.bar_chart(category_counts)
                            
                except Exception as e:
                    st.error(f"Error processing CSV file: {str(e)}")
    
    # Instructions
    with st.expander("How to use this application"):
        st.markdown("""
        ### Instructions:
        1. **Enter your Groq API Key** in the sidebar (required for the Agent feature)
        2. **Answer with Agent**: Get detailed answers to your questions using a powerful language model
        3. **Classify Text**: Analyze what type of content your text represents
        4. **Model Metrics**: View performance metrics of the classification model
        5. **Batch Processing**: Classify multiple texts at once
        
        ### Tips:
        - For best results with the agent, ask clear and specific questions
        - For classification, provide complete sentences or paragraphs
        - The classifier works best on English text
        - You can download classification results as CSV files
        
        ### Categories:
        - **Positive**: Express satisfaction, happiness, or approval
        - **Negative**: Express dissatisfaction, unhappiness, or disapproval
        - **Question**: Ask for information or assistance
        - **Informational**: Provide factual information
        - **Neutral**: State facts without sentiment or express ambiguity
        
        ### Getting a Groq API Key:
        1. Visit [console.groq.com](https://console.groq.com/)
        2. Create an account or sign in
        3. Generate an API key from your account settings
        """)

if __name__ == "__main__":
    main() 