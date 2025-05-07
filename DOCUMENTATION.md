# Groq Classifier Documentation

This document provides detailed information on how to use and extend the Groq Classifier project.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Components](#components)
4. [Usage Examples](#usage-examples)
5. [API Reference](#api-reference)
6. [Extending the Project](#extending-the-project)
7. [Model Performance](#model-performance)
8. [Batch Processing](#batch-processing)
9. [Troubleshooting](#troubleshooting)

## Project Overview

Groq Classifier is a tool that combines an LLM agent using the Groq API with a scikit-learn-based text classifier. It provides a user-friendly interface for interacting with both components, as well as tools for analyzing classification results.

### Key Features

- **LLM Agent**: Uses Groq's llama3-70b-8192 model to answer questions and provide information
- **Text Classification**: Categorizes text into multiple categories (positive, negative, question, informational, neutral)
- **Interactive UI**: Streamlit interface with tabbed organization for easy interaction
- **Data Analysis**: Tools for analyzing and visualizing classification results
- **Batch Processing**: Ability to process multiple texts or CSV files at once
- **Model Persistence**: Save and load trained models for improved performance
- **Performance Metrics**: Evaluate model accuracy with cross-validation

## Installation

### Prerequisites

- Python 3.8+
- Groq API Key (from [Groq Console](https://console.groq.com/))

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/onchainlabs1/groq-classifier.git
   cd groq-classifier
   ```

2. Set up environment:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Create a `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Components

The project consists of several components:

### 1. LLM Agent (`agents.py`)

The LLM agent uses LangChain with the Groq API to provide responses to user questions. It uses the llama3-70b-8192 model, which is a state-of-the-art language model.

### 2. Text Classifier (`ml_logic.py`)

The text classifier uses scikit-learn to categorize text into multiple categories:
- Positive sentiment
- Negative sentiment
- Questions
- Informational content
- Neutral/Ambiguous statements

The classifier now includes model persistence for faster loading, advanced text preprocessing, and proper performance evaluation using cross-validation.

### 3. Main Application (`app.py`)

The main Streamlit application provides a user interface for interacting with both the LLM agent and the text classifier. The interface is now organized into tabs:
- **Classify & Answer**: Main classification and LLM interaction
- **Model Metrics**: Visualize and analyze model performance
- **Batch Processing**: Process multiple texts or CSV files at once

### 4. Data Utilities (`data_utils.py`)

Utilities for saving classification results, exporting model data, and performing batch classification.

### 5. Analytics Dashboard (`report.py`)

A Streamlit dashboard for analyzing and visualizing classification results.

### 6. API Examples (`api.py`)

Examples of how to use the components programmatically.

## Usage Examples

### Main Application

To start the main application:

```bash
streamlit run app.py
```

This will open a web interface where you can:
- Enter text to be classified or questions to be answered
- Choose between using the LLM agent or the text classifier
- View the results
- Analyze model performance
- Process batch texts

### Analytics Dashboard

To run the analytics dashboard:

```bash
streamlit run report.py
```

This dashboard provides:
- Statistics about the classifier
- Tools for batch classification
- Analysis of historical classification data

### API Usage

You can use the components programmatically:

```python
from agents import answer
from ml_logic import classify_text, get_category_description

# Using the LLM agent
response = answer("What is machine learning?")
print(response)

# Using the text classifier
category = classify_text("I love this product!")
description = get_category_description(category)
print(f"Category: {category}")
print(f"Description: {description}")
```

For more examples, see `api.py`.

## API Reference

### Agents Module

#### `answer(question: str) -> str`

Uses the LLM agent to answer a question.

**Parameters:**
- `question`: The question to answer

**Returns:**
- A string containing the agent's response

### ML Logic Module

#### `classify_text(text: str) -> str`

Classifies a text into one of several categories.

**Parameters:**
- `text`: The text to classify

**Returns:**
- A string representing the category ('positive', 'negative', 'question', 'informational', 'neutral', or 'uncertain')

#### `get_category_description(category: str) -> str`

Returns a human-readable description of a category.

**Parameters:**
- `category`: The category name

**Returns:**
- A string describing the category

#### `preprocess_text(text: str) -> str`

Preprocesses text for improved classification.

**Parameters:**
- `text`: The text to preprocess

**Returns:**
- The preprocessed text

#### `train_classifier(examples: List[str], categories: List[str]) -> Pipeline`

Trains a new classifier with the given examples and categories.

**Parameters:**
- `examples`: List of text examples
- `categories`: List of corresponding categories

**Returns:**
- A trained scikit-learn Pipeline

#### `save_model(model, filename: str = 'classifier_model.joblib') -> str`

Saves a trained model to disk.

**Parameters:**
- `model`: The model to save
- `filename`: The name for the saved model file

**Returns:**
- The path to the saved model

#### `load_model(filename: str = 'classifier_model.joblib') -> Pipeline`

Loads a trained model from disk.

**Parameters:**
- `filename`: The name of the model file to load

**Returns:**
- The loaded model

#### `get_classifier_metrics() -> Dict`

Gets performance metrics for the current classifier.

**Returns:**
- Dictionary containing metrics including cross-validation scores and classification report

### Data Utils Module

#### `save_classification_results(texts: List[str], categories: List[str], filename: str = None) -> str`

Saves classification results to a CSV file.

**Parameters:**
- `texts`: List of texts that were classified
- `categories`: List of categories assigned to each text
- `filename`: Optional filename to save results to (defaults to timestamp)

**Returns:**
- The path to the saved file

#### `batch_classify(texts: List[str]) -> List[Tuple[str, str, str]]`

Classifies a batch of texts.

**Parameters:**
- `texts`: List of texts to classify

**Returns:**
- List of tuples (text, category, description)

## Extending the Project

### Adding New Categories

To add new categories to the classifier, modify the `examples` and `categories` lists in `ml_logic.py`:

1. Add example texts for the new category
2. Add corresponding category labels
3. Update the `get_category_description` function to include descriptions for the new categories

### Using a Different Model

To use a different LLM model:

1. Modify the `get_model` function in `agents.py` to use a different model
2. Update the `requirements.txt` file if necessary
3. Update documentation to reflect the change

## Model Performance

The application now includes a dedicated "Model Metrics" tab to analyze the performance of the text classifier:

### Cross-Validation Scores

The model is evaluated using 5-fold cross-validation to provide a reliable estimate of its performance:

1. The data is split into 5 folds
2. The model is trained on 4 folds and tested on 1
3. This process is repeated for each fold
4. The average accuracy score is reported

### Per-Category Metrics

For each category, the following metrics are displayed:
- **Precision**: The ability of the model to avoid false positives
- **Recall**: The ability of the model to find all positive samples
- **F1-Score**: The harmonic mean of precision and recall
- **Support**: The number of samples in each category

### Visualizations

The Model Metrics tab includes:
- Bar chart of F1 scores by category
- Box plot of cross-validation scores
- Detailed metrics table

## Batch Processing

The application now includes a dedicated "Batch Processing" tab for processing multiple texts at once:

### Manual Entry

You can enter multiple texts, one per line, to classify them all at once.

### CSV Upload

You can upload a CSV file containing a column of texts to classify. The application will:
1. Allow you to select which column contains the texts
2. Process all texts in the CSV
3. Display results and category distribution
4. Provide a download link for the results

## Troubleshooting

### Common Issues

#### "GROQ_API_KEY not found" Error

Make sure you have created a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can also enter the API key directly in the sidebar of the main application.

#### Classifier Returning "uncertain"

The classifier returns "uncertain" when its confidence is below 0.5. To improve classification:

1. Add more examples to the `examples` list in `ml_logic.py`
2. Make sure the text is clear and matches one of the categories
3. Try rephrasing the text

#### Model Not Saving or Loading

If you encounter issues with model persistence:

1. Make sure the `models` directory exists and is writable
2. Check that `joblib` is installed (`pip install joblib`)
3. Try manually creating the `models` directory if it doesn't exist

#### Slow Responses from the LLM Agent

LLM responses may be slow due to:

1. Network latency
2. Queue times on the Groq API
3. Complexity of the question

For faster responses, consider using a smaller model or optimizing your queries.

### Getting Help

If you encounter issues not covered here, please:

1. Check the [GitHub repository](https://github.com/onchainlabs1/groq-classifier) for known issues
2. Open a new issue with details about your problem
3. Include relevant error messages and steps to reproduce 