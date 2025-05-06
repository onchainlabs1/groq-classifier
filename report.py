"""
Classification Report Dashboard

A Streamlit dashboard for analyzing classification results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import datetime
from data_utils import export_classification_stats, batch_classify, save_classification_results

# Set page config
st.set_page_config(
    page_title="Classification Report",
    page_icon="📊",
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
    .stat-box {
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 1rem;
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 1rem;
        color: #6C757D;
    }
    </style>
    """, unsafe_allow_html=True)


def load_saved_data():
    """Load all saved classification results"""
    data_dir = "data"
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Find all CSV files in the data directory
    csv_files = glob.glob(os.path.join(data_dir, "classification_results_*.csv"))
    
    if not csv_files:
        return None
    
    # Load and combine all CSV files
    dataframes = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            # Add a column for the file name (for tracking)
            df['source_file'] = os.path.basename(file)
            # Extract timestamp from filename
            timestamp_str = os.path.basename(file).replace("classification_results_", "").replace(".csv", "")
            try:
                timestamp = datetime.datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                df['timestamp'] = timestamp
            except:
                df['timestamp'] = None
                
            dataframes.append(df)
        except Exception as e:
            st.warning(f"Error loading file {file}: {str(e)}")
    
    if not dataframes:
        return None
        
    # Combine all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df


def display_classification_stats():
    """Display statistics about the classifier"""
    stats = export_classification_stats()
    
    st.markdown("### Classifier Statistics")
    
    # Display key stats in boxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{stats['total_examples']}</div>
            <div class="stat-label">Training Examples</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{len(stats['categories'])}</div>
            <div class="stat-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{stats['average_example_length']:.1f}</div>
            <div class="stat-label">Avg. Example Length</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display category distribution as a bar chart
    st.markdown("#### Category Distribution")
    
    category_data = stats['category_distribution']
    categories = list(category_data.keys())
    counts = list(category_data.values())
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(categories, counts, color=['#4B8BF5', '#F44336', '#2196F3', '#9C27B0'])
    
    # Add data labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height}', ha='center', va='bottom')
    
    ax.set_title('Number of Examples per Category')
    ax.set_ylabel('Count')
    ax.set_ylim(0, max(counts) * 1.2)  # Add some space for the labels
    
    st.pyplot(fig)


def batch_classification_tool():
    """Tool for batch classification of text samples"""
    st.markdown("### Batch Classification Tool")
    st.write("Classify multiple texts at once and analyze the results.")
    
    # Text input area for multiple samples
    sample_text = st.text_area(
        "Enter multiple texts to classify (one per line):",
        height=150,
        placeholder="Enter one text sample per line..."
    )
    
    if st.button("Classify Batch"):
        if sample_text:
            # Split the input by newlines and filter out empty lines
            texts = [text.strip() for text in sample_text.split('\n') if text.strip()]
            
            if not texts:
                st.warning("Please enter at least one text to classify.")
                return
                
            with st.spinner("Classifying texts..."):
                # Classify each text
                results = batch_classify(texts)
                
                # Create a dataframe with the results
                df = pd.DataFrame(results, columns=['Text', 'Category', 'Description'])
                
                # Save results to CSV
                texts_list = df['Text'].tolist()
                categories_list = df['Category'].tolist()
                filepath = save_classification_results(texts_list, categories_list)
                
                # Show the results
                st.markdown("#### Classification Results")
                st.dataframe(df, use_container_width=True)
                
                # Show a summary of the results
                st.markdown("#### Summary")
                category_counts = df['Category'].value_counts().reset_index()
                category_counts.columns = ['Category', 'Count']
                
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    st.dataframe(category_counts, use_container_width=True)
                
                with col2:
                    # Plot the category distribution
                    fig, ax = plt.subplots(figsize=(8, 4))
                    colors = {
                        'positive': '#4CAF50',
                        'negative': '#F44336',
                        'question': '#2196F3',
                        'informational': '#9C27B0',
                        'uncertain': '#FFC107'
                    }
                    
                    # Get colors for each category, defaulting to gray if not in the dictionary
                    bar_colors = [colors.get(cat, '#9E9E9E') for cat in category_counts['Category']]
                    
                    bars = ax.bar(category_counts['Category'], category_counts['Count'], color=bar_colors)
                    
                    # Add data labels
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                f'{height}', ha='center', va='bottom')
                    
                    ax.set_title('Category Distribution')
                    ax.set_ylabel('Count')
                    
                    st.pyplot(fig)
                
                st.success(f"Results saved to {filepath}")
        else:
            st.warning("Please enter some text to classify.")


def historical_data_analysis():
    """Analyze historical classification data"""
    st.markdown("### Historical Data Analysis")
    
    # Load saved data
    df = load_saved_data()
    
    if df is None or df.empty:
        st.info("No historical data found. Use the Batch Classification Tool to generate data.")
        return
    
    # Show summary statistics
    st.markdown("#### Overview")
    
    total_classifications = len(df)
    unique_texts = df['Text'].nunique()
    data_sources = df['source_file'].nunique()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{total_classifications}</div>
            <div class="stat-label">Total Classifications</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{unique_texts}</div>
            <div class="stat-label">Unique Texts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{data_sources}</div>
            <div class="stat-label">Data Sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Category distribution
    st.markdown("#### Category Distribution")
    category_counts = df['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(category_counts, use_container_width=True)
    
    with col2:
        # Create a pie chart of category distribution
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = {
            'positive': '#4CAF50',
            'negative': '#F44336',
            'question': '#2196F3',
            'informational': '#9C27B0',
            'uncertain': '#FFC107'
        }
        
        # Get colors for each category, defaulting to gray if not in the dictionary
        pie_colors = [colors.get(cat, '#9E9E9E') for cat in category_counts['Category']]
        
        ax.pie(category_counts['Count'], labels=category_counts['Category'], autopct='%1.1f%%',
               colors=pie_colors, startangle=90, wedgeprops={'width': 0.5, 'edgecolor': 'w'})
        ax.set_title('Category Distribution')
        
        st.pyplot(fig)
    
    # Show the raw data
    st.markdown("#### Raw Data")
    st.dataframe(df, use_container_width=True)


def main():
    add_custom_css()
    
    st.markdown('<h1 class="main-header">Classification Report Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze and visualize classification results</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", [
        "Classifier Statistics",
        "Batch Classification",
        "Historical Data Analysis"
    ])
    
    # Display the selected page
    if page == "Classifier Statistics":
        display_classification_stats()
    elif page == "Batch Classification":
        batch_classification_tool()
    elif page == "Historical Data Analysis":
        historical_data_analysis()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown(
        "This dashboard provides analytics and visualizations "
        "for the Groq Classifier project."
    )
    st.sidebar.markdown(
        "Use the Batch Classification tool to classify multiple texts "
        "at once and save the results for later analysis."
    )


if __name__ == "__main__":
    main() 