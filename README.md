# SHAKTI-AI: Reproductive & Legal Health AI Agents

SHAKTI-AI is a suite of AI-powered agents designed to support Indian women and families with reproductive health, legal rights, mental wellness, and more. Each agent is tailored for a specific domain, providing empathetic, evidence-based, and culturally relevant guidance.

## Features
- **Maaya**: Maternal health nurse for pregnancy, childbirth, and baby care.
- **Gynika**: Reproductive health advisor for periods, puberty, and contraception.
- **Meher**: Emotional support counselor for trauma, anxiety, and abuse.
- **Nyaya**: Legal-ethical guide for Indian laws on consent, abortion, and family rights.
- **Vaanya**: Feminist educator for menopause and hormonal health.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root (or update the existing one) with your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

You need to obtain a Google API key with access to the Gemini 2.0 Flash model.

### 3. Run the Application

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Usage

1. Enter your question or concern in the text area
2. Optionally select which expert agents you want to consult
3. Click "Get Guidance" to receive a response
4. Provide feedback on the response

## Project Structure

- `app.py`: Streamlit web application
- `llm.py`: LLM implementation using Google's Gemini 2.0 Flash
- `agents.py`: Agent definitions and configurations
- `crew.py`: CrewAI setup and orchestration
- `.env`: Environment variables and configuration
- `requirements.txt`: Project dependencies

## Disclaimer

SHAKTI-AI provides general information only and is not a substitute for professional medical, legal, or mental health advice. Always consult qualified professionals for specific concerns.
