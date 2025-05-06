import unittest
from unittest.mock import patch, MagicMock
from ml_logic import classify_text, get_category_description
import os

class TestClassifier(unittest.TestCase):
    """Tests for the text classifier"""
    
    def test_positive_classification(self):
        """Test that positive texts are correctly classified"""
        text = "This is an amazing product, I love it!"
        result = classify_text(text)
        self.assertEqual(result, "positive")
    
    def test_negative_classification(self):
        """Test that negative texts are correctly classified"""
        text = "This is terrible, I hate it and would not recommend it."
        result = classify_text(text)
        self.assertEqual(result, "negative")
    
    def test_question_classification(self):
        """Test that questions are correctly classified"""
        text = "How does this product work? Can you help me?"
        result = classify_text(text)
        self.assertEqual(result, "question")
    
    def test_informational_classification(self):
        """Test that informational texts are correctly classified"""
        text = "The product weighs 2kg and is available in blue and red colors."
        result = classify_text(text)
        self.assertEqual(result, "informational")
    
    def test_category_descriptions(self):
        """Test that category descriptions are returned correctly"""
        categories = ["positive", "negative", "question", "informational", "uncertain"]
        for category in categories:
            description = get_category_description(category)
            self.assertIsNotNone(description)
            self.assertNotEqual(description, "Unknown category")


class TestAgent(unittest.TestCase):
    """Tests for the LLM agent"""
    
    @patch('agents.get_model')
    def test_answer_function(self, mock_get_model):
        """Test the answer function with a mocked model"""
        # Import here to avoid importing at module level
        from agents import answer
        
        # Setup mock
        mock_model = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "This is a test response"
        
        mock_model.__or__ = MagicMock(return_value=mock_chain)
        mock_chain.invoke = MagicMock(return_value=mock_response)
        mock_get_model.return_value = mock_model
        
        # Call the function
        result = answer("Test question")
        
        # Assert the result
        self.assertEqual(result, "This is a test response")
        
        # Verify the mock was called
        mock_get_model.assert_called_once()
        mock_chain.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main() 