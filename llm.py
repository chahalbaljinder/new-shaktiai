import os
from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from typing import Any, Dict, List, Optional
from pydantic import Field, PrivateAttr
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiLLM(LLM):
    """Implementation of Google's Gemini 2.0 Flash API."""
    
    model_name: str = Field(default="gemini-2.0-flash")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=4096)
    api_key: str = Field(default=os.getenv("GOOGLE_API_KEY"))
    
    # Define a private attribute for the model
    _model: Any = PrivateAttr(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the Gemini API
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(model_name=self.model_name)
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Execute the LLM call."""
        try:
            response = self._model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                    "top_p": 0.95,
                }
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return "I apologize, but I encountered an error processing your request."
    
    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "gemini"
        
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
