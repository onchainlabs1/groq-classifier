"""
Data Utilities for Groq Classifier

Utilities for saving classification results and exporting model data.
"""

import csv
import os
import json
import datetime
from typing import List, Dict, Any, Tuple

def save_classification_results(texts: List[str], categories: List[str], filename: str = None) -> str:
    """
    Save classification results to a CSV file.
    
    Args:
        texts: List of texts that were classified
        categories: List of categories assigned to each text
        filename: Optional filename to save results to, defaults to timestamp
        
    Returns:
        The path to the saved file
    """
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate filename with timestamp if not provided
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"classification_results_{timestamp}.csv"
    
    filepath = os.path.join("data", filename)
    
    # Write results to CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Text', 'Category'])
        
        for text, category in zip(texts, categories):
            writer.writerow([text, category])
    
    return filepath


def export_classifier_examples() -> str:
    """
    Export the examples used for training the classifier to a JSON file.
    
    Returns:
        The path to the saved file
    """
    from ml_logic import classify_text
    import inspect
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Get the source code of the classify_text function
    source = inspect.getsource(classify_text)
    
    # Extract examples and categories - this is a simple extraction method
    # A more robust method would be to use the AST module
    examples_start = source.find("examples = [")
    examples_end = source.find("]", examples_start)
    categories_start = source.find("categories = [")
    categories_end = source.find("]", categories_start)
    
    # Extract the example lists as strings
    examples_str = source[examples_start:examples_end+1]
    categories_str = source[categories_start:categories_end+1]
    
    # Create a dictionary with the data
    data = {
        "examples": examples_str,
        "categories": categories_str,
        "exported_at": datetime.datetime.now().isoformat()
    }
    
    # Save to JSON file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join("data", f"classifier_examples_{timestamp}.json")
    
    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)
    
    return filepath


def batch_classify(texts: List[str]) -> List[Tuple[str, str, str]]:
    """
    Classify a batch of texts and return results with descriptions.
    
    Args:
        texts: List of texts to classify
        
    Returns:
        List of tuples (text, category, description)
    """
    from ml_logic import classify_text, get_category_description
    
    results = []
    
    for text in texts:
        category = classify_text(text)
        description = get_category_description(category)
        results.append((text, category, description))
    
    return results


def export_classification_stats() -> Dict[str, Any]:
    """
    Generate statistics about the classifier training data.
    
    Returns:
        Dictionary with statistics
    """
    from ml_logic import classify_text
    import inspect
    
    # Get the source code of the classify_text function
    source = inspect.getsource(classify_text)
    
    # Extract examples and categories - this is a simple extraction method
    examples_start = source.find("examples = [")
    examples_end = source.find("]", examples_start)
    categories_start = source.find("categories = [")
    categories_end = source.find("]", categories_start)
    
    # Extract the example lists as strings and convert to actual lists
    examples_str = source[examples_start+11:examples_end].strip()
    categories_str = source[categories_start+13:categories_end].strip()
    
    # Split by commas followed by newlines to get items
    examples = [item.strip().strip('"\'').strip() for item in examples_str.split('",\n')]
    categories = [item.strip().strip('"\'').strip() for item in categories_str.split('",\n')]
    
    # Calculate stats
    category_counts = {}
    for category in categories:
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    
    stats = {
        "total_examples": len(examples),
        "category_distribution": category_counts,
        "average_example_length": sum(len(ex) for ex in examples) / len(examples) if examples else 0,
        "categories": list(set(categories))
    }
    
    return stats


if __name__ == "__main__":
    # Run a demo of the utilities
    print("Running data utilities demo...")
    
    # Demo batch classification
    sample_texts = [
        "This product exceeded my expectations!",
        "Awful service, never ordering again",
        "Can you tell me how to return this item?",
        "The package contains 12 units per box"
    ]
    
    results = batch_classify(sample_texts)
    print("\nBatch Classification Results:")
    for text, category, description in results:
        print(f"Text: '{text[:30]}...' → Category: {category} ({description})")
    
    # Save results to CSV
    filepath = save_classification_results([r[0] for r in results], [r[1] for r in results])
    print(f"\nSaved classification results to: {filepath}")
    
    # Export classifier examples
    examples_file = export_classifier_examples()
    print(f"Exported classifier examples to: {examples_file}")
    
    # Show classifier stats
    stats = export_classification_stats()
    print("\nClassifier Statistics:")
    print(f"Total examples: {stats['total_examples']}")
    print(f"Categories: {', '.join(stats['categories'])}")
    print("Category distribution:")
    for category, count in stats['category_distribution'].items():
        print(f"  - {category}: {count} examples")
    print(f"Average example length: {stats['average_example_length']:.1f} characters") 