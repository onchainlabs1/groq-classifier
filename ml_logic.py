import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def classify_text(text: str) -> str:
    """
    Classifies a text into multiple categories using a MultinomialNB classifier.
    
    Args:
        text (str): The text to be classified
        
    Returns:
        str: The predicted category for the text
    """
    # Training examples (texts and categories)
    examples = [
        # Positive sentiment
        "This product is great, I loved it!", 
        "Amazing experience, I recommend it to everyone",
        "Very satisfied with the service provided",
        "The product arrived as expected and working perfectly",
        
        # Negative sentiment
        "Horrible, I don't recommend it to anyone",
        "Terrible experience, don't buy",
        "Low quality product, broke on first use",
        "Poor customer service and defective product",
        
        # Questions
        "How does this work?",
        "What is the return policy?",
        "Can you help me with this issue?",
        "When will my order arrive?",
        
        # Informational
        "The store opens at 9am and closes at 6pm",
        "This product contains 500mg of vitamin C",
        "The company was founded in 2010",
        "The product weighs 2.5 kg and measures 30x40 cm"
    ]
    
    categories = [
        # Positive sentiment
        "positive",
        "positive", 
        "positive",
        "positive",
        
        # Negative sentiment
        "negative",
        "negative",
        "negative",
        "negative",
        
        # Questions
        "question",
        "question",
        "question", 
        "question",
        
        # Informational
        "informational",
        "informational",
        "informational",
        "informational"
    ]
    
    try:
        # Create pipeline for vectorization and classification
        model = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        # Train the model
        model.fit(examples, categories)
        
        # Make prediction
        predicted_category = model.predict([text])[0]
        
        # Get probability distribution
        probabilities = model.predict_proba([text])[0]
        category_probabilities = dict(zip(model.classes_, probabilities))
        
        # Find the highest probability category
        top_category = max(category_probabilities, key=category_probabilities.get)
        confidence = category_probabilities[top_category]
        
        if confidence < 0.5:
            return "uncertain"
        
        return predicted_category
    except Exception as e:
        return f"Error classifying the text: {str(e)}"

def get_category_description(category: str) -> str:
    """
    Returns a description for each category.
    
    Args:
        category (str): The predicted category
        
    Returns:
        str: A human-readable description of the category
    """
    descriptions = {
        "positive": "This text expresses positive sentiment or satisfaction",
        "negative": "This text expresses negative sentiment or dissatisfaction",
        "question": "This text is asking for information or assistance",
        "informational": "This text is providing factual information",
        "uncertain": "The classifier is not confident about the category"
    }
    
    return descriptions.get(category, "Unknown category") 