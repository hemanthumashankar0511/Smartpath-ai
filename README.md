# SmartPath AI

SmartPath AI is a personalized learning path generator and assessment platform powered by AI. The application uses the Llama 3.2 language model to provide intelligent assessments, generate customized learning paths, and offer interactive AI assistance for various technical domains.

## Features

- **Domain-Specific Assessments**: Pre-built assessments for multiple domains including Python, Data Science, Web Development, Machine Learning, and more
- **AI-Powered Learning Paths**: Customized curriculum generation based on assessment results
- **Progress Tracking**: Monitor your learning journey with milestone completion tracking
- **Resource Integration**: Curated YouTube videos and PDF resources for each learning milestone
- **Interactive AI Agent**: Get explanations and answers using Llama 3.2
- **User Profiles**: Track multiple learning paths and progress across different domains

## Prerequisites

- Python 3.7 or higher
- [Ollama](https://ollama.ai/) installed and running
- Google Chrome or Firefox (recommended browsers)
- 8GB RAM minimum (16GB recommended for optimal performance)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smartpath-ai.git
   cd smartpath-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key
   YOUTUBE_API_KEY=your_youtube_api_key  # Optional, for enhanced video recommendations
   ```

5. Pull required AI model:
   ```bash
   # Install the language model
   ollama pull llama3.2:3b
   ```

## Running the Application

1. Ensure Ollama is running in the background:
   ```bash
   # On Windows, start Ollama from the installed application
   # On macOS/Linux:
   ollama serve
   ```

2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## Usage

1. Register/Login with your email
2. Select a domain and take the assessment
3. View your results and AI-generated explanations
4. Generate a personalized learning path
5. Track your progress through milestones
6. Use the AI agent for additional help and explanations

## Troubleshooting

### Common Issues

1. **MemoryError or Ollama Errors**:
   - Ensure you have enough RAM available
   - Try restarting Ollama service
   - Consider using a smaller language model if issues persist

2. **Model Not Found**:
   ```bash
   # Re-pull the model
   ollama pull llama3.2:3b
   ```

3. **API Key Issues**:
   - Verify your API keys in the `.env` file
   - Ensure the file is in the root directory
   - Check for any whitespace in the keys

## Documentation Links

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



