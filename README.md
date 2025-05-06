# AI Assistant and Text Classifier

![GitHub last commit](https://img.shields.io/github/last-commit/onchainlabs1/groq-classifier)
![License](https://img.shields.io/badge/license-MIT-blue)
![Made with Cursor](https://img.shields.io/badge/Made_with-Cursor_AI-blue?logo=cursor&logoColor=white)

A powerful tool that combines an LLM agent using the Groq API with a scikit-learn-based text classifier, built entirely using Cursor AI as a development challenge.

![App Screenshot](https://via.placeholder.com/800x400?text=Groq+Classifier+Screenshot)
<!-- Replace the placeholder above with an actual screenshot of your application when available -->

## The 1-Hour Cursor AI Challenge

This project was developed as a speed-coding challenge: **build a complete AI application in under 1 hour using only Cursor AI**. The entire application, including all features, was built in a single development session with AI assistance, demonstrating the power of AI-powered development tools for rapid prototyping.

This challenge highlights:

- Rapid prototype-to-production development with AI assistance
- Building a full-stack application in record time (under 1 hour!)
- Seamlessly combining modern LLMs with traditional ML techniques
- Creating production-ready code with comprehensive testing and documentation

## Live Demo

Try the application live on Streamlit Cloud:
[Groq Classifier App](https://groq-classifier.streamlit.app) <!-- Update with your actual Streamlit Cloud URL -->

Note: When using the live demo, you'll need to provide your own Groq API key to use the LLM agent functionality. The text classification works without an API key.

## Features

- **LLM Agent**: Answers general questions using the llama3-70b-8192 model via Groq API
- **Text Classification**: Analyzes and categorizes text into multiple categories:
  - 😊 **Positive**: Identifies positive sentiment in text
  - 😠 **Negative**: Identifies negative sentiment in text
  - ❓ **Question**: Identifies questions seeking information
  - ℹ️ **Informational**: Identifies text providing factual information
- **Streamlit Interface**: User-friendly interface with responsive design and visual feedback
- **Data Analysis Dashboard**: Complete analytics tools with visualizations and batch processing
- **Confidence Scoring**: Provides uncertainty detection when classification confidence is low
- **Direct API Key Input**: Enter your Groq API key directly in the interface (no configuration files needed)

## Tech Stack

- **[LangChain](https://langchain.com/)**: Framework for working with LLMs
- **[Groq API](https://groq.com/)**: Ultra-fast LLM inference API
- **[scikit-learn](https://scikit-learn.org/)**: Machine learning tools and algorithms
- **[Streamlit](https://streamlit.io/)**: Web application framework for data apps
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[Matplotlib](https://matplotlib.org/)**: Data visualization
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)**: Environment variable management

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

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Enter your Groq API key in the sidebar (if you want to use the LLM features)

## Additional Applications

Beyond the main classifier interface, this project includes:

### 1. Analytics Dashboard
```bash
streamlit run report.py
```
Provides detailed metrics, visualizations, and batch processing capabilities.

### 2. Programmatic API Examples
```bash
python api.py
```
Demonstrates how to use the classification system programmatically.

### 3. Data Utilities
```bash
python data_utils.py
```
Tools for exporting classification results and model statistics.

## Development Process

This project was built using Cursor AI to demonstrate how modern AI-assisted development can accelerate creation of complex applications. The entire development process took place in a single session lasting less than 1 hour, including:

1. Setting up the core architecture
2. Implementing the ML classification system
3. Building the LLM integration
4. Creating a responsive UI
5. Adding comprehensive testing
6. Implementing data analysis features
7. Writing detailed documentation

This approach showcases the potential of AI-assisted coding for rapid prototyping and development of production-ready applications.

## Deploy Your Own Version

You can easily deploy this project to Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Visit [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub
3. Deploy a new app, selecting your forked repository
4. Set the main file path to `app.py`
5. Optionally, add your Groq API key as a secret named `GROQ_API_KEY`
6. Deploy and share your app!

## Documentation

For comprehensive documentation of all features and components, see the [DOCUMENTATION.md](DOCUMENTATION.md) file.

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
- [Cursor](https://cursor.sh/) for the AI-powered development environment