# AI Assistant and Text Classifier

![GitHub last commit](https://img.shields.io/github/last-commit/onchainlabs1/groq-classifier)
![License](https://img.shields.io/badge/license-MIT-blue)

A powerful tool that combines an LLM agent using the Groq API with a scikit-learn-based text classifier.

![App Screenshot](https://via.placeholder.com/800x400?text=Groq+Classifier+Screenshot)
<!-- Replace the placeholder above with an actual screenshot of your application when available -->

## Features

- **LLM Agent**: Answers general questions using the llama3-70b-8192 model via Groq API
- **Text Classification**: Analyzes and categorizes text into multiple categories:
  - 😊 **Positive**: Identifies positive sentiment in text
  - 😠 **Negative**: Identifies negative sentiment in text
  - ❓ **Question**: Identifies questions seeking information
  - ℹ️ **Informational**: Identifies text providing factual information
- **Streamlit Interface**: User-friendly interface with responsive design and visual feedback
- **Confidence Scoring**: Provides uncertainty detection when classification confidence is low

## Screenshots

<div align="center">
  <p><i>Screenshots will be added soon</i></p>
  
  <!-- Add your screenshots here when available -->
  <!--
  <img src="screenshots/main-interface.png" alt="Main Interface" width="80%"/>
  <p>Main Interface</p>
  
  <img src="screenshots/classification-example.png" alt="Classification Example" width="80%"/>
  <p>Classification Example</p>
  
  <img src="screenshots/agent-response.png" alt="Agent Response" width="80%"/>
  <p>Agent Response</p>
  -->
</div>

## Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (from [Groq](https://console.groq.com/))

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/onchainlabs1/groq-classifier.git
   cd groq-classifier
   ```

2. Set up the environment:
   ```bash
   # Option 1: Using setup script (recommended)
   chmod +x setup.sh
   ./setup.sh
   
   # Option 2: Manual setup
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Examples

### Using the LLM Agent

1. Enter your question in the text field
2. Click "Answer with Agent 🤖"
3. Wait for the response to be generated

Example questions:
- "What is machine learning?"
- "How does the Groq API work?"
- "Explain the difference between classification and regression"

### Using the Text Classifier

1. Enter the text you want to classify in the text field
2. Click "Classify Text 🔍"
3. View the classification result

Example texts to classify:
- "I love this product, it's amazing!" (Positive)
- "This is terrible quality, don't buy it" (Negative)
- "When will my order arrive?" (Question)
- "The store opens at 9am and closes at 6pm" (Informational)

## Development

### Project Structure

```
groq-classifier/
├── agents.py        # LLM agent implementation
├── app.py           # Streamlit interface
├── ml_logic.py      # Text classification model
├── tests.py         # Automated tests
├── .env             # Environment variables (create this)
├── .gitignore       # Git ignore file
├── requirements.txt # Dependencies
├── setup.sh         # Setup script
└── README.md        # Documentation
```

### Running Tests

```bash
python -m unittest tests.py
```

## Roadmap

- [ ] Add more sophisticated classification models
- [ ] Support for multiple languages
- [ ] Save and load classification examples
- [ ] Implement user feedback for improving the classifier
- [ ] Add visualization of classification confidence
- [ ] Create a Docker container for easy deployment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Groq](https://groq.com/) for their powerful LLM API
- [LangChain](https://langchain.com/) for the LLM framework
- [scikit-learn](https://scikit-learn.org/) for the ML tools
- [Streamlit](https://streamlit.io/) for the web application framework 