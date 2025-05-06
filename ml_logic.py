import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def classify_text(text: str) -> str:
    """
    Classifies a text into simple categories using a MultinomialNB classifier.
    
    Args:
        text (str): The text to be classified
        
    Returns:
        str: The predicted category for the text
    """
    # Training examples (texts and categories)
    examples = [
        "This product is great, I loved it!", 
        "Amazing experience, I recommend it to everyone",
        "Very satisfied with the service provided",
        "The product arrived as expected and working perfectly",
        "Horrible, I don't recommend it to anyone",
        "Terrible experience, don't buy",
        "Low quality product, broke on first use",
        "Poor customer service and defective product"
    ]
    
    categories = [
        "positive",
        "positive", 
        "positive",
        "positive",
        "negative",
        "negative",
        "negative",
        "negative"
    ]
    
    try:
        # Create pipeline for vectorization and classification
        model = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])
        
        # Train the model
        model.fit(examples, categories)
        
        # Make prediction
        predicted_category = model.predict([text])[0]
        
        return predicted_category
    except Exception as e:
        return f"Error classifying the text: {str(e)}" 