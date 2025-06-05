# SmartPath AI

SmartPath AI is a personalized, AI-powered learning path generator designed to help users assess their current knowledge, receive tailored curricula, and track their learning progress. The application leverages advanced language models to provide dynamic learning experiences based on user assessments.

## Features

- **Skill Assessment**: Users can take assessments to evaluate their knowledge in various domains.
- **Personalized Learning Paths**: Generate custom curricula based on assessment results and user preferences.
- **Progress Tracking**: Monitor learning progress and achievements.
- **AI Agent**: Interact with a GenAI-powered assistant for questions and multimodal Q&A.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.7 or higher
- Streamlit
- Required libraries (see `requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory and add your API keys:

   ```plaintext
   GEMINI_API_KEY=<your-gemini-api-key>
   ```

## Running the Project

To run the application, use the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server, and you can access the application in your web browser at `http://localhost:8501`.

## Pulling the Model

Make sure to pull the necessary models before using the application. You can do this by running the following command in your terminal:

```bash
# Example command to pull the model
# Replace <model-name> with the actual model you need
llama pull <model-name>
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

