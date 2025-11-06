import os
from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from typing import Any, Dict, List, Optional
from pydantic import Field, ConfigDict
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiLLM(LLM):
    """Implementation of Google's Gemini 2.0 Flash API."""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set default values if not provided
        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY", "")
        
        # Initialize the Gemini API
        genai.configure(api_key=self.api_key)
        # Store model as a regular attribute instead of field
        object.__setattr__(self, '_model', genai.GenerativeModel(model_name=self.model_name))
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Execute the LLM call."""
        try:
            model = object.__getattribute__(self, '_model')
            response = model.generate_content(
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
